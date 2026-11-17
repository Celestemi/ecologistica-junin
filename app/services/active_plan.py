"""AF-01: snapshot vigente por jornada y exclusión transaccional.

La última solución computed/published de una jornada es su snapshot completo.
No se recupera una asignación antigua si un pedido desaparece del snapshot.
Todos los escritores de plan/estado usan el mismo advisory lock de PostgreSQL.
"""

from zoneinfo import ZoneInfo

from sqlalchemy import func, select, text, update

from app.models.domain import RutaDetalle, SolucionRuta
from app.models.enums import EstadoSolucion, TipoParada

ACTIVE_STATES = (EstadoSolucion.COMPUTED, EstadoSolucion.PUBLISHED)


async def lock_route_state(session) -> None:
    # Namespace propio, sin tabla/columna nueva. Liberación automática commit/rollback.
    await session.execute(text('SELECT pg_advisory_xact_lock(180324, 1)'))


async def current_order_detail(session, order, vehicle_id: int | None = None):
    day = order.ventana_inicio.astimezone(ZoneInfo('America/Lima')).date()
    latest = select(func.max(SolucionRuta.id)).where(
        SolucionRuta.fecha_operacion == day, SolucionRuta.estado.in_(ACTIVE_STATES)
    ).scalar_subquery()
    query = select(RutaDetalle).where(
        RutaDetalle.solucion_id == latest, RutaDetalle.pedido_id == order.id,
        RutaDetalle.tipo_parada == TipoParada.DELIVERY,
    )
    if vehicle_id is not None:
        query = query.where(RutaDetalle.vehiculo_id == vehicle_id)
    return await session.scalar(query)


async def require_current_order_vehicle(session, order, vehicle_id: int) -> None:
    if await current_order_detail(session, order, vehicle_id) is None:
        raise ValueError('El pedido no pertenece a la ruta asignada vigente.')


def latest_snapshots(solutions):
    """Una versión por jornada. No sumar planes sustituidos ni borradores."""
    days = {}
    unversioned = []
    for plan in solutions:
        if getattr(plan, 'estado', EstadoSolucion.COMPUTED) not in ACTIVE_STATES:
            continue
        day, identifier = getattr(plan, 'fecha_operacion', None), getattr(plan, 'id', None)
        if day is None or identifier is None:
            unversioned.append(plan)  # dobles de unidad sin identidad, no BD
            continue
        if day not in days or identifier > days[day].id:
            days[day] = plan
    return list(days.values()) + unversioned


async def activate_snapshot(session, plan) -> None:
    await session.flush()
    await session.execute(update(SolucionRuta).where(
        SolucionRuta.fecha_operacion == plan.fecha_operacion,
        SolucionRuta.id != plan.id, SolucionRuta.estado.in_(ACTIVE_STATES),
    ).values(estado=EstadoSolucion.ARCHIVED))
