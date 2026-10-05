"""Conversión entre GeoJSON (lon, lat) y elementos GeoAlchemy2."""

from typing import Any

from geoalchemy2.elements import WKBElement, WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import LineString, mapping
from shapely.geometry.base import BaseGeometry

from app.core.config import get_settings


def point_wkt(lon: float, lat: float) -> WKTElement:
    """Crea un punto WGS84. El orden es longitud, latitud, como en GeoJSON."""
    srid = get_settings().storage_srid
    return WKTElement(f"POINT({lon} {lat})", srid=srid)


def geometry_to_geojson(value: Any) -> dict[str, Any]:
    """Normaliza WKB, WKT, Shapely o un dict GeoJSON a un dict GeoJSON."""
    if isinstance(value, dict) and "type" in value and "coordinates" in value:
        return value
    if isinstance(value, BaseGeometry):
        return mapping(value)
    if isinstance(value, (WKBElement, WKTElement)) or hasattr(value, "desc"):
        return mapping(to_shape(value))
    raise TypeError("No se pudo convertir la geometría a GeoJSON.")


def linestring_geojson(coordinates: list[list[float]]) -> dict[str, Any]:
    """Arma un LineString GeoJSON a partir de pares [lon, lat]."""
    if len(coordinates) < 2:
        raise ValueError("Un LineString necesita al menos dos puntos.")
    return mapping(LineString(coordinates))
