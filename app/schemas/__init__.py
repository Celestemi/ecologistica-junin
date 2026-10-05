"""Esquemas Pydantic v2 del dominio logístico."""

from app.schemas.logistics import (
    DepositoRead,
    GeoJSONFeatureCollection,
    GeoJSONPoint,
    OptimizedRouteResponse,
    PedidoCreate,
    PedidoRead,
    VehiculoCreate,
    VehiculoRead,
)

__all__ = [
    "DepositoRead",
    "GeoJSONFeatureCollection",
    "GeoJSONPoint",
    "OptimizedRouteResponse",
    "PedidoCreate",
    "PedidoRead",
    "VehiculoCreate",
    "VehiculoRead",
]
