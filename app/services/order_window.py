"""Ventanas de entrega (RF-006 / RN-005)."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status

from app.models.domain import Pedido
from app.models.enums import EstadoPedido

LIMA = ZoneInfo("America/Lima")

_CLOSED = {EstadoPedido.DELIVERED, EstadoPedido.CANCELLED, EstadoPedido.INCIDENT}
_ACTIVE_ROUTE = {EstadoPedido.ASSIGNED, EstadoPedido.IN_TRANSIT}


def as_lima(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=LIMA)
    return value.astimezone(LIMA)


def normalize_delivery_window(start: datetime, end: datetime) -> tuple[datetime, datetime]:
    """Exige fin estrictamente posterior al inicio (America/Lima)."""
    start_lima = as_lima(start)
    end_lima = as_lima(end)
    if end_lima <= start_lima:
        raise ValueError("La ventana de fin debe ser posterior a la de inicio.")
    return start_lima, end_lima


def assert_window_editable(order: Pedido) -> None:
    if order.estado in _CLOSED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"No se puede modificar la ventana del pedido {order.codigo_pedido}: "
                "el pedido ya está cerrado."
            ),
        )
    if order.estado == EstadoPedido.IN_TRANSIT:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"El pedido {order.codigo_pedido} está en ruta. "
                "Cambiar la ventana no actualiza la ETA ya calculada; "
                "use el recálculo en vivo del conductor ante un imprevisto."
            ),
        )
    if order.estado == EstadoPedido.ASSIGNED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"El pedido {order.codigo_pedido} ya está en una ruta publicada. "
                "Ajuste la planificación antes de modificar la ventana horaria."
            ),
        )
