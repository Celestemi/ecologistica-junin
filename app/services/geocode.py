"""Geocodificación ligera por hitos locales (RF-005 / US-005).

No sustituye direcciones desconocidas por el centro de Huancayo ni inventa
coordenadas. Si la dirección no coincide con un hito del catálogo, el pedido
queda pendiente de validación manual en el mapa.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Literal

# Hitos usados en la semilla y en la carga del día. Gana la frase más larga.
_PLACES: tuple[tuple[str, float, float, float], ...] = (
    ("universidad nacional del centro", -12.03305, -75.23733, 3290.0),
    ("plaza constitucion", -12.06513, -75.20486, 3271.0),
    ("calixto", -12.06940, -75.20749, 3268.0),
    ("chilca", -12.09820, -75.18680, 3410.0),
    ("uncp", -12.03305, -75.23733, 3290.0),
    ("ferrocarril", -12.0520, -75.2120, 3250.0),
)

MSG_NO_COORDS = "Sin coordenadas. Marque el punto en el mapa."
MSG_NOT_FOUND = (
    "No se pudo ubicar la dirección automáticamente. "
    "Revise el texto o marque el punto en el mapa."
)
MSG_OUT_OF_AREA = (
    "La ubicación queda fuera del ámbito de Huancayo, El Tambo y Chilca. "
    "Corrija el punto en el mapa."
)
MSG_OUT_OF_VALLEY = "El punto queda fuera del valle del Mantaro."
MSG_INVALID_COORDS = "La coordenada no es un número válido."


@dataclass(frozen=True)
class ResolvedPoint:
    lat: float
    lon: float
    altitude_m: float
    source: Literal["csv", "landmark"]


def _fold(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.casefold())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def locate_address(address: str) -> tuple[float, float, float] | None:
    """Devuelve lat, lon y altitud si la dirección nombra un hito del catálogo."""
    folded = _fold(address)
    best: tuple[str, float, float, float] | None = None
    for name, lat, lon, altitude in _PLACES:
        if name in folded and (best is None or len(name) > len(best[0])):
            best = (name, lat, lon, altitude)
    if best is None:
        return None
    return best[1], best[2], best[3]


def parse_coordinates(
    lat_text: str,
    lon_text: str,
    altitude_text: str = "",
) -> tuple[float | None, float | None, float | None, bool]:
    """Interpreta lat/lon del CSV. Devuelve `(lat, lon, alt, ok)`."""
    altitude = _optional_float(altitude_text)
    if not lat_text.strip() and not lon_text.strip():
        return None, None, altitude, False
    lat = _optional_float(lat_text)
    lon = _optional_float(lon_text)
    return lat, lon, altitude, lat is not None and lon is not None


def _optional_float(value: str) -> float | None:
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def resolve_from_address(address: str) -> ResolvedPoint | None:
    found = locate_address(address)
    if found is None:
        return None
    return ResolvedPoint(
        lat=found[0],
        lon=found[1],
        altitude_m=found[2],
        source="landmark",
    )


def default_altitude(altitude: float | None) -> float:
    return 3270.0 if altitude is None or altitude <= 0 else altitude
