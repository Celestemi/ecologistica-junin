"""Reglas de edición y alta de ubicaciones de pedidos (RF-005)."""

from __future__ import annotations

from fastapi import HTTPException, status

from app.models.domain import Pedido
from app.models.enums import EstadoPedido, EstadoUbicacion
from app.services.order_window import assert_window_editable

_LAT = (-12.30, -11.70)
_LON = (-75.50, -74.90)


def assert_location_editable(order: Pedido) -> None:
    assert_window_editable(order)
    if order.estado not in {EstadoPedido.PENDING}:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El pedido {order.codigo_pedido} no admite cambios de ubicación.",
        )


def assert_valley_bounds(lat: float, lon: float) -> None:
    if not _LAT[0] <= lat <= _LAT[1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La latitud queda fuera del valle del Mantaro.",
        )
    if not _LON[0] <= lon <= _LON[1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La longitud queda fuera del valle del Mantaro.",
        )


def apply_geocoded_point(
    order: Pedido,
    *,
    lon: float,
    lat: float,
    altitud_msnm: float,
    ubicacion_wkt,
) -> None:
    order.ubicacion = ubicacion_wkt
    order.altitud_msnm = altitud_msnm
    order.estado_ubicacion = EstadoUbicacion.GEOCODIFICADO


def mark_pending_validation(order: Pedido) -> None:
    order.ubicacion = None
    order.altitud_msnm = None
    order.estado_ubicacion = EstadoUbicacion.PENDIENTE_VALIDACION


def is_routable(order: Pedido) -> bool:
    return (
        order.estado == EstadoPedido.PENDING
        and order.estado_ubicacion == EstadoUbicacion.GEOCODIFICADO
        and order.ubicacion is not None
    )
