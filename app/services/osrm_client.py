"""Cliente mínimo OSRM (red vial OpenStreetMap, perfil driving).

No implica tráfico en tiempo real: solo distancia, duración y geometría sobre la red.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
from time import monotonic
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from app.core.config import get_settings

logger = logging.getLogger("ecologistica.osrm")


@dataclass(frozen=True)
class OsrmRouteLeg:
    distance_km: float
    duration_minutes: float
    coordinates: tuple[tuple[float, float], ...]


def _coord_key(
    origin_lat: float,
    origin_lon: float,
    dest_lat: float,
    dest_lon: float,
) -> tuple[float, float, float, float]:
    return (
        round(origin_lat, 6),
        round(origin_lon, 6),
        round(dest_lat, 6),
        round(dest_lon, 6),
    )


class OsrmLegCache:
    """Cache de tramos OSRM para matriz del GA y geometría de mapa."""

    def __init__(self, base_url: str, *, timeout_seconds: float) -> None:
        self._base = base_url.rstrip("/")
        self._timeout = max(0.5, timeout_seconds)
        self._legs: dict[tuple[float, float, float, float], OsrmRouteLeg | None] = {}
        self._matrix: dict[tuple[float, float, float, float], tuple[float, float] | None] = {}
        self._matrix_prepared = False

    @property
    def matrix_prepared(self) -> bool:
        return self._matrix_prepared

    def prepare_distance_matrix(
        self,
        points: Sequence[tuple[float, float]],
        *,
        chunk_size: int = 50,
        deadline: float | None = None,
    ) -> None:
        """Carga distancias y duraciones en bloques compatibles con el límite OSRM de 100 puntos."""
        keys = list(dict.fromkeys(_coord_key(lat, lon, lat, lon)[:2] for lat, lon in points))
        size = max(1, min(50, chunk_size))
        self._matrix_prepared = True
        for row_start in range(0, len(keys), size):
            origins = keys[row_start : row_start + size]
            for column_start in range(0, len(keys), size):
                destinations = keys[column_start : column_start + size]
                locations = list(dict.fromkeys([*origins, *destinations]))
                indexes = {point: index for index, point in enumerate(locations)}
                coordinates = ";".join(f"{lon:.6f},{lat:.6f}" for lat, lon in locations)
                params = urlencode({
                    "sources": ";".join(str(indexes[point]) for point in origins),
                    "destinations": ";".join(str(indexes[point]) for point in destinations),
                    "annotations": "distance,duration",
                    "skip_waypoints": "true",
                }, safe=";")
                url = f"{self._base}/table/v1/driving/{coordinates}?{params}"
                try:
                    if deadline is not None:
                        remaining = deadline - monotonic()
                        if remaining <= 0:
                            raise TimeoutError("El presupuesto de optimización venció al preparar la matriz OSRM.")
                        timeout = min(self._timeout, remaining)
                    else:
                        timeout = self._timeout
                    with urlopen(url, timeout=timeout) as response:
                        payload: dict[str, Any] = json.load(response)
                    distances = payload.get("distances")
                    durations = payload.get("durations")
                    if payload.get("code") != "Ok" or not isinstance(distances, list) or not isinstance(durations, list):
                        logger.warning("OSRM no devolvió una matriz válida: %s", payload.get("code"))
                        continue
                    if len(distances) != len(origins) or len(durations) != len(origins):
                        logger.warning("OSRM devolvió dimensiones de matriz inesperadas.")
                        continue
                    for row, origin in enumerate(origins):
                        distance_row = distances[row]
                        duration_row = durations[row]
                        if not isinstance(distance_row, list) or not isinstance(duration_row, list):
                            continue
                        for column, destination in enumerate(destinations):
                            meters = distance_row[column] if column < len(distance_row) else None
                            seconds = duration_row[column] if column < len(duration_row) else None
                            if meters is None or seconds is None:
                                self._matrix[(*origin, *destination)] = None
                            else:
                                self._matrix[(*origin, *destination)] = (
                                    max(0.0, float(meters) / 1000.0),
                                    max(0.0, float(seconds) / 60.0),
                                )
                except TimeoutError:
                    raise
                except (URLError, ValueError, OSError) as exc:
                    logger.warning("No se pudo cargar un bloque de la matriz OSRM: %s", exc)
        if deadline is not None and monotonic() >= deadline:
            raise TimeoutError("El presupuesto de optimización venció al preparar la matriz OSRM.")

    def get_matrix_leg(
        self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float,
    ) -> tuple[float, float] | None:
        """Devuelve (km, minutos) de la matriz precargada, también si el tramo no tiene ruta."""
        return self._matrix.get(_coord_key(origin_lat, origin_lon, dest_lat, dest_lon))

    def get_leg(
        self,
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
    ) -> OsrmRouteLeg | None:
        key = _coord_key(origin_lat, origin_lon, dest_lat, dest_lon)
        if key not in self._legs:
            self._legs[key] = fetch_driving_leg(
                self._base,
                origin_lat,
                origin_lon,
                dest_lat,
                dest_lon,
                timeout_seconds=self._timeout,
            )
        return self._legs[key]

    @property
    def configured(self) -> bool:
        return bool(self._base)


def fetch_driving_leg(
    base_url: str,
    origin_lat: float,
    origin_lon: float,
    dest_lat: float,
    dest_lon: float,
    *,
    timeout_seconds: float = 5.0,
) -> OsrmRouteLeg | None:
    """Consulta /route/v1/driving con geometría GeoJSON (overview=full)."""
    params = urlencode(
        {
            "overview": "full",
            "geometries": "geojson",
            "steps": "false",
        }
    )
    url = (
        f"{base_url.rstrip('/')}/route/v1/driving/"
        f"{origin_lon},{origin_lat};{dest_lon},{dest_lat}?{params}"
    )
    try:
        with urlopen(url, timeout=timeout_seconds) as response:
            payload: dict[str, Any] = json.load(response)
    except (URLError, TimeoutError, ValueError, OSError) as exc:
        logger.warning("OSRM no disponible para el tramo: %s", exc)
        return None

    if payload.get("code") != "Ok":
        logger.warning("OSRM respondió sin ruta: %s", payload.get("code"))
        return None
    routes = payload.get("routes") or []
    if not routes:
        return None
    route = routes[0]
    meters = float(route.get("distance", 0.0))
    seconds = float(route.get("duration", 0.0))
    if meters <= 0 or seconds <= 0:
        return None
    geometry = route.get("geometry") or {}
    raw = geometry.get("coordinates") or []
    coordinates: list[tuple[float, float]] = []
    for pair in raw:
        if not isinstance(pair, (list, tuple)) or len(pair) < 2:
            continue
        coordinates.append((float(pair[0]), float(pair[1])))
    if len(coordinates) < 2:
        return None
    return OsrmRouteLeg(
        distance_km=meters / 1000.0,
        duration_minutes=seconds / 60.0,
        coordinates=tuple(coordinates),
    )


def create_osrm_cache() -> OsrmLegCache | None:
    base = (get_settings().osrm_base_url or "").strip()
    if not base:
        return None
    timeout = max(0.5, float(get_settings().osrm_request_timeout_seconds))
    return OsrmLegCache(base, timeout_seconds=timeout)
