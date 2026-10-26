"""Estados operativos de la flota (US-003 / RF-003)."""

from __future__ import annotations

from fastapi import HTTPException, status

from app.models.enums import EstadoOperativoVehiculo
from app.models.operations import HistorialVehiculo
from app.models.domain import Vehiculo

_ALLOWED: dict[EstadoOperativoVehiculo, set[EstadoOperativoVehiculo]] = {
    EstadoOperativoVehiculo.ACTIVO: {
        EstadoOperativoVehiculo.MANTENIMIENTO,
        EstadoOperativoVehiculo.INACTIVO,
    },
    EstadoOperativoVehiculo.MANTENIMIENTO: {
        EstadoOperativoVehiculo.ACTIVO,
        EstadoOperativoVehiculo.INACTIVO,
    },
    EstadoOperativoVehiculo.INACTIVO: {EstadoOperativoVehiculo.ACTIVO},
}


def sync_activo_flag(vehicle: Vehiculo) -> None:
    vehicle.activo = vehicle.estado_operativo == EstadoOperativoVehiculo.ACTIVO


def assert_transition(
    current: EstadoOperativoVehiculo,
    target: EstadoOperativoVehiculo,
) -> None:
    if current == target:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El vehículo ya está en estado {target.value}.",
        )
    allowed = _ALLOWED.get(current, set())
    if target not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede pasar de {current.value} a {target.value}.",
        )


def apply_operational_state(
    vehicle: Vehiculo,
    target: EstadoOperativoVehiculo,
    *,
    correo: str,
    motivo: str | None = None,
) -> HistorialVehiculo:
    previous = vehicle.estado_operativo
    assert_transition(previous, target)
    if target == EstadoOperativoVehiculo.MANTENIMIENTO and not (motivo or "").strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Indica un motivo para enviar el vehículo a mantenimiento.",
        )
    vehicle.estado_operativo = target
    sync_activo_flag(vehicle)
    detail = _history_detail(previous, target, motivo)
    return HistorialVehiculo(
        vehiculo_id=vehicle.id,
        activo=vehicle.activo,
        estado_anterior=previous.value,
        estado_nuevo=target.value,
        motivo=(motivo or "").strip() or None,
        detalle=detail,
        correo=correo,
    )


def is_available_for_routing(vehicle: Vehiculo) -> bool:
    return vehicle.estado_operativo == EstadoOperativoVehiculo.ACTIVO


def _history_detail(
    previous: EstadoOperativoVehiculo,
    target: EstadoOperativoVehiculo,
    motivo: str | None,
) -> str:
    base = f"{previous.value} → {target.value}."
    if motivo and motivo.strip():
        return f"{base} Motivo: {motivo.strip()}"
    return base
