"""Matriz de distancias intercambiable (geodésica por defecto; OSRM opcional).

Las distancias geodésicas (Haversine) no representan recorridos viales. OSRM solo
se usa cuando `OSRM_BASE_URL` está configurado y responde; si falla, la celda queda
sin matriz de confianza (RF-009 infeliz) sin inventar tiempos.
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from app.core.config import get_settings
from app.services.osrm_client import OsrmLegCache, create_osrm_cache

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


def prepare_osrm_routing() -> tuple[DistanceAdjuster | None, OsrmLegCache | None]:
    """Adaptador de distancia + cache de tramos (geometría y duración)."""
    cache = create_osrm_cache()
    if cache is None:
        return None, None

    def adjust(
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
        haversine_km: float,
    ) -> float | None:
        del haversine_km
        leg = cache.get_leg(origin_lat, origin_lon, dest_lat, dest_lon)
        if leg is None:
            return None
        return leg.distance_km

    return adjust, cache


def optional_osrm_adjuster() -> DistanceAdjuster | None:
    """Solo distancia (compatibilidad con llamadas que no necesitan cache)."""
    adjuster, _ = prepare_osrm_routing()
    return adjuster


def active_distance_adjuster() -> DistanceAdjuster | None:
    """OSRM si está configurado; en otro caso el solver usa solo Haversine."""
    return optional_osrm_adjuster()
