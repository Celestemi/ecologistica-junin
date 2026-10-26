"""Recálculo de ETA sobre una secuencia ya persistida (RF-009 feliz)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.domain import Deposito, Pedido, RutaDetalle, SolucionRuta, Vehiculo
from app.models.enums import EstadoPedido, TipoParada
from app.services.genetic_solver import SERVICE_MINUTES, StopItinerary, _build_problem, _schedule_vehicle
from app.services.routing_matrix import active_distance_adjuster


async def recalculate_solution_etas(session: AsyncSession, solution_id: int) -> SolucionRuta:
    """Vuelve a simular tiempos sin cambiar el orden de paradas ni pedidos entregados."""
    solution = await session.scalar(
        select(SolucionRuta)
        .where(SolucionRuta.id == solution_id)
        .options(
            selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.pedido),
            selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.vehiculo),
        )
    )
    if solution is None:
        raise ValueError(f"No existe la solución {solution_id}.")

    depot = await session.scalar(select(Deposito).where(Deposito.id == solution.deposito_id))
    if depot is None:
        raise ValueError("Falta el depósito de la solución.")

    order_ids = {
        detail.pedido_id
        for detail in solution.detalles
        if detail.pedido_id is not None
    }
    if not order_ids:
        return solution

    orders = list(
        await session.scalars(select(Pedido).where(Pedido.id.in_(order_ids)))
    )
    vehicle_ids = {detail.vehiculo_id for detail in solution.detalles}
    vehicles = list(await session.scalars(select(Vehiculo).where(Vehiculo.id.in_(vehicle_ids))))

    problem = _build_problem(
        orders,
        vehicles,
        depot,
        distance_adjuster=active_distance_adjuster(),
    )
    vehicles_by_id = {vehicle.id: vehicle for vehicle in problem.vehicles}
    orders_by_id = {order.id: order for order in problem.orders}

    stops_by_vehicle: dict[int, list[RutaDetalle]] = {}
    for detail in sorted(solution.detalles, key=lambda item: (item.vehiculo_id, item.secuencia)):
        stops_by_vehicle.setdefault(detail.vehiculo_id, []).append(detail)

    for vehicle_id, details in stops_by_vehicle.items():
        vehicle = next(node for node in problem.vehicles if node.id == vehicle_id)
        route_orders = [
            detail.pedido_id
            for detail in details
            if detail.tipo_parada == TipoParada.DELIVERY
            and detail.pedido_id is not None
            and detail.pedido is not None
            and detail.pedido.estado not in {EstadoPedido.DELIVERED, EstadoPedido.CANCELLED}
        ]
        itinerary = _schedule_vehicle(
            problem,
            vehicle,
            [oid for oid in route_orders if oid in orders_by_id],
            orders_by_id,
            SERVICE_MINUTES,
        )
        stop_by_order = {
            stop.order_id: stop for stop in itinerary.stops if stop.order_id is not None
        }
        for detail in details:
            if detail.tipo_parada != TipoParada.DELIVERY or detail.pedido_id is None:
                continue
            if detail.pedido is not None and detail.pedido.estado in {
                EstadoPedido.DELIVERED,
                EstadoPedido.CANCELLED,
            }:
                continue
            stop: StopItinerary | None = stop_by_order.get(detail.pedido_id)
            if stop is None:
                detail.eta = None
                detail.estado_eta = "sin_datos"
                continue
            _apply_stop_to_detail(detail, stop)

    return solution


def _apply_stop_to_detail(detail: RutaDetalle, stop: StopItinerary) -> None:
    detail.eta = stop.eta
    detail.estado_eta = stop.eta_estado.value
    detail.minutos_espera_ventana = stop.wait_minutes
    detail.minutos_tarde_ventana = stop.late_minutes
    detail.secuencia_entrega = stop.delivery_index
    detail.modelo_distancia = stop.distance_model.value
    detail.tiempo_viaje_min = stop.travel_minutes
    detail.distancia_tramo_km = stop.distance_km
    detail.co2_tramo_g = stop.co2_grams
