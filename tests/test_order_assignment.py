"""Asignación persistente y restricciones del optimizador, con datos sintéticos."""

import pytest

from app.core.database import async_session_factory
from app.models.domain import Pedido, Vehiculo
from app.models.enums import EstadoPedido, EstadoOperativoVehiculo, TipoParada
from app.services.genetic_solver import solve_vrptw
from app.services.route_constraints import validate_for_publication
from tests.helpers import login_headers
from tests.test_optimizer_us007 import _depot, _order, _vehicle


def test_solver_keeps_manual_vehicle_assignments_through_generations():
    orders = [_order(i, lon=-75.20, lat=-12.04, start_h=8, end_h=18) for i in range(1, 5)]
    for order in orders:
        order.vehiculo_asignado_id = 2 if order.id % 2 == 0 else 1
    vehicles = [_vehicle(id=1), _vehicle(id=2, placa="V-002", emision_base_co2_g_km=0)]
    result = solve_vrptw(orders, vehicles, _depot(), generations=12, population_size=10, seed=17)
    assert result.feasible
    allocations = {stop.order_id: itinerary.vehicle_id for itinerary in result.itineraries
                   for stop in itinerary.stops if stop.stop_type == TipoParada.DELIVERY}
    assert allocations == {1: 1, 2: 2, 3: 1, 4: 2}


def test_unavailable_assignment_is_not_silently_ignored():
    order = _order(1, lon=-75.20, lat=-12.04, start_h=8, end_h=18)
    order.vehiculo_asignado_id = 99
    with pytest.raises(ValueError, match="no está disponible"):
        solve_vrptw([order], [_vehicle()], _depot(), generations=1, population_size=3)


def test_publication_rejects_a_solver_that_ignores_the_assignment():
    order = _order(1, lon=-75.20, lat=-12.04, start_h=8, end_h=18)
    vehicle = _vehicle()
    vehicle.estado_operativo = EstadoOperativoVehiculo.ACTIVO
    result = solve_vrptw([order], [vehicle], _depot(), generations=1, population_size=3)
    order.vehiculo_asignado_id = 2
    report = validate_for_publication(result, [order], [vehicle], service_minutes=5)
    assert not report.ok
    assert any(item.code == "ASIGNACION_VEHICULO" for item in report.violations)


@pytest.mark.asyncio
async def test_assignment_persists_and_optimization_uses_selected_vehicle(client):
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    orders = (await client.get("/api/v1/pedidos", headers=headers)).json()
    target = orders[0]
    response = await client.patch(f"/api/v1/pedidos/{target['id']}/vehiculo",
                                  json={"vehiculo_asignado_id": 2}, headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["vehiculo_asignado_id"] == 2
    fetched = (await client.get("/api/v1/pedidos?fecha=2026-10-06", headers=headers)).json()
    assert next(order for order in fetched if order["id"] == target["id"])["vehiculo_asignado_id"] == 2
    assert (await client.get("/api/v1/pedidos?fecha=2026-11-17", headers=headers)).json() == []
    optimized = await client.post("/api/v1/optimizar-rutas?fecha=2026-10-06", headers=headers)
    assert optimized.status_code == 201, optimized.text
    features = optimized.json()["features"]
    assert all(feature["properties"]["plate"] == "E7M-304" for feature in features
               if feature["properties"].get("order_code") == target["codigo_pedido"])
    assert (await client.get("/api/v1/rutas/mapa?fecha=2026-11-17", headers=headers)).status_code == 404


@pytest.mark.asyncio
async def test_assignment_can_be_cleared_and_invalid_assignments_are_rejected(client):
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    orders = (await client.get("/api/v1/pedidos", headers=headers)).json()
    order_id = orders[0]["id"]
    path = f"/api/v1/pedidos/{order_id}/vehiculo"
    assert (await client.patch(path, json={"vehiculo_asignado_id": 999}, headers=headers)).status_code == 404
    async with async_session_factory() as session:
        vehicle = await session.get(Vehiculo, 1)
        vehicle.estado_operativo = EstadoOperativoVehiculo.MANTENIMIENTO
        vehicle.activo = False
        await session.commit()
    assert (await client.patch(path, json={"vehiculo_asignado_id": 1}, headers=headers)).status_code == 409
    assert len((await client.get("/api/v1/vehiculos", headers=headers)).json()) == 1
    assert len((await client.get("/api/v1/vehiculos?todos=true", headers=headers)).json()) == 2
    assert (await client.patch(path, json={"vehiculo_asignado_id": 2}, headers=headers)).status_code == 200
    cleared = await client.patch(path, json={"vehiculo_asignado_id": None}, headers=headers)
    assert cleared.json()["vehiculo_asignado_id"] is None
    async with async_session_factory() as session:
        order = await session.get(Pedido, order_id)
        order.estado = EstadoPedido.DELIVERED
        await session.commit()
    assert (await client.patch(path, json={"vehiculo_asignado_id": 2}, headers=headers)).status_code == 409
    auditor = await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026")
    assert (await client.patch(path, json={"vehiculo_asignado_id": 2}, headers=auditor)).status_code == 403
