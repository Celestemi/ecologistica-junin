"""Matriz de distancias intercambiable (geodésica por defecto; OSRM opcional).

Las distancias geodésicas (Haversine) no representan recorridos viales. OSRM solo
se usa cuando `OSRM_BASE_URL` está configurado y responde; si falla, la celda queda
sin matriz de confianza (RF-009 infeliz) sin inventar tiempos.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from app.core.config import get_settings

logger = logging.getLogger("ecologistica.routing_matrix")

DistanceAdjuster = Callable[[float, float, float, float, float], float | None]


def geodesic_adjuster(
    _origin_lat: float,
    _origin_lon: float,
    _dest_lat: float,
    _dest_lon: float,
    haversine_km: float,
) -> float:
    """Devuelve la distancia geodésica ya calculada (cuerda en el mapa)."""
    return max(0.0, haversine_km)


def optional_osrm_adjuster() -> DistanceAdjuster | None:
    """Adaptador OSRM si hay URL; None = solo geodésica en el solver."""
    base = (get_settings().osrm_base_url or "").strip().rstrip("/")
    if not base:
        return None

    def adjust(
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
        haversine_km: float,
    ) -> float | None:
        del haversine_km
        try:
            params = urlencode(
                {
                    "overview": "false",
                    "steps": "false",
                }
            )
            url = (
                f"{base}/route/v1/driving/"
                f"{origin_lon},{origin_lat};{dest_lon},{dest_lat}?{params}"
            )
            with urlopen(url, timeout=3.0) as response:
                payload: dict[str, Any] = __import__("json").load(response)
            if payload.get("code") != "Ok":
                logger.warning("OSRM respondió sin ruta: %s", payload.get("code"))
                return None
            routes = payload.get("routes") or []
            if not routes:
                return None
            meters = float(routes[0].get("distance", 0.0))
            if meters <= 0:
                return None
            return meters / 1000.0
        except (URLError, TimeoutError, ValueError, KeyError, OSError) as exc:
            logger.warning("OSRM no disponible para el tramo: %s", exc)
            return None

    return adjust


def active_distance_adjuster() -> DistanceAdjuster | None:
    """OSRM si está configurado; en otro caso el solver usa solo Haversine."""
    return optional_osrm_adjuster()
