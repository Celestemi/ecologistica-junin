"""Vincula conductores autenticados con un vehículo activo."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import Vehiculo
from app.models.operations import AsignacionConductor
from app.services.vehicle_state import is_available_for_routing


async def assigned_vehicle(
    session: AsyncSession,
    usuario_id: int,
    *, lock: bool = False,
) -> Vehiculo | None:
    query = (
        select(AsignacionConductor)
        .where(
            AsignacionConductor.usuario_id == usuario_id,
            AsignacionConductor.activa.is_(True),
        )
        .limit(1)
    )
    if lock:
        query = query.with_for_update()
    row = await session.scalar(query)
    if row is None:
        return None
    return await session.get(Vehiculo, row.vehiculo_id)


async def conductor_may_drive(session: AsyncSession, usuario_id: int, driver_id: str) -> bool:
    vehicle = await assigned_vehicle(session, usuario_id)
    if vehicle is None or not is_available_for_routing(vehicle):
        return False
    return vehicle.placa == driver_id
