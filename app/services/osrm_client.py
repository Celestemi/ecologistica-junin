"""Cliente mínimo OSRM (red vial OpenStreetMap, perfil driving).

No implica tráfico en tiempo real: solo distancia, duración y geometría sobre la red.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any
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
