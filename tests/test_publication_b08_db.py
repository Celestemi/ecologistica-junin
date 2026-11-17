"""B-08: API, transacción real y mapa, exclusivamente en ecologistica_test."""

import os
import socket
from dataclasses import replace
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from urllib.parse import urlsplit

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.api.v1 import routes, websockets
from app.core.database import async_session_factory, engine
from app.models.domain import Deposito, Pedido, RutaDetalle, SolucionRuta, Vehiculo
from app.models.enums import EstadoOperativoVehiculo, EstadoPedido, TipoParada
from app.services.genetic_solver import solve_vrptw
from app.services.realtime_router import FleetState, GpsFix, LiveReroute
from tests.helpers import login_headers


def _database_unavailable():
    address = urlsplit(os.environ["DATABASE_URL"])
    if address.path != "/ecologistica_test":
        raise RuntimeError("B-08 solo admite la base ecologistica_test.")
    try:
        with socket.create_connection((address.hostname, address.port or 5432), timeout=0.3):
            return False
    except OSError:
        return True


pytestmark = pytest.mark.skipif(
    _database_unavailable(), reason="PostgreSQL de pruebas no escucha en el host/puerto configurado; sin motor Docker disponible.",
)


@pytest.fixture
async def db_case(client, monkeypatch):
    """Fixture sintética sobre la semilla descartable, nunca registros operativos."""
    async with async_session_factory() as session:
        orders = list(await session.scalars(select(Pedido).order_by(Pedido.id)))
        vehicles = list(await session.scalars(select(Vehiculo).order_by(Vehiculo.id)))
        depot = await session.scalar(select(Deposito).order_by(Deposito.id))
        selected = orders[:2]
        for order in orders:
            order.estado = EstadoPedido.PENDING if order in selected else EstadoPedido.DELIVERED
            if order in selected:
                order.peso_kg = 20.0
                order.volumen_m3 = 1.0
                order.ventana_inicio = selected[0].ventana_inicio.replace(hour=8)
                order.ventana_fin = order.ventana_inicio.replace(hour=18)
        for vehicle in vehicles:
            vehicle.estado_operativo = (EstadoOperativoVehiculo.ACTIVO if vehicle is vehicles[0]
                                       else EstadoOperativoVehiculo.INACTIVO)
            vehicle.activo = vehicle is vehicles[0]
        await session.commit()
        vehicle = vehicles[0]
        solution = solve_vrptw(selected, [vehicle], depot, generations=3, population_size=3, seed=8)
        assert solution.feasible
    monkeypatch.setattr(routes, "run_optimizer_in_worker", AsyncMock(return_value=solution))
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    return SimpleNamespace(client=client, headers=headers, solution=solution, orders=selected, vehicle=vehicle)


async def snapshot():
    async with async_session_factory() as session:
        return (
            await session.scalar(select(func.count()).select_from(SolucionRuta)),
            await session.scalar(select(func.count()).select_from(RutaDetalle)),
            list((await session.execute(select(Pedido.id, Pedido.estado).order_by(Pedido.id))).all()),
        )


def invalid_solution(case, kind):
    solution = case.solution
    itinerary = solution.itineraries[0]
    if kind == "weight":
        itinerary = replace(itinerary, capacity_excess_kg=1.0)
    elif kind == "volume":
        itinerary = replace(itinerary, capacity_excess_m3=1.0)
    elif kind == "missing":
        itinerary = replace(itinerary, stops=tuple(stop for stop in itinerary.stops
                                                 if stop.order_id != case.orders[0].id))
    else:
        stops = tuple(
            replace(stop, eta=case.orders[0].ventana_fin + timedelta(hours=1), late_minutes=0.0)
            if kind == "window" and stop.order_id == case.orders[0].id else
            replace(stop, travel_minutes=481.0)
            if kind == "shift" and stop.order_id == case.orders[0].id else stop
            for stop in itinerary.stops
        )
        itinerary = replace(itinerary, stops=stops)
    return replace(solution, itineraries=(itinerary,))


@pytest.mark.asyncio
async def test_api_database_and_map_agree_after_valid_publication(db_case):
    case = db_case
    response = await case.client.post("/api/v1/optimizar-rutas", headers=case.headers)
    assert response.status_code == 201, response.text
    map_response = await case.client.get("/api/v1/rutas/mapa", headers=case.headers)
    assert map_response.status_code == 200
    assert response.json()["metadata"]["feasible"] is True
    assert map_response.json()["metadata"]["feasible"] is True
    assert response.json()["metadata"]["id"] == map_response.json()["metadata"]["id"]
    plans, details, states = await snapshot()
    assert plans == 1 and details == len(case.solution.itineraries[0].stops)
    assert {state for oid, state in states if oid in {order.id for order in case.orders}} == {EstadoPedido.ASSIGNED}


@pytest.mark.asyncio
@pytest.mark.parametrize("kind,code", [
    ("weight", "CAPACIDAD_PESO"), ("volume", "CAPACIDAD_VOLUMEN"),
    ("window", "VENTANA_ENTREGA"), ("shift", "JORNADA_MAXIMA"), ("missing", "PEDIDOS_SIN_ASIGNAR"),
])
async def test_api_rejection_rolls_back_and_does_not_create_map(db_case, monkeypatch, kind, code):
    case = db_case
    monkeypatch.setattr(routes, "run_optimizer_in_worker", AsyncMock(return_value=invalid_solution(case, kind)))
    before = await snapshot()
    response = await case.client.post("/api/v1/optimizar-rutas", headers=case.headers)
    assert response.status_code == 409, response.text
    assert code in {item["codigo"] for item in response.json()["detail"]["violaciones"]}
    assert await snapshot() == before
    map_response = await case.client.get("/api/v1/rutas/mapa", headers=case.headers)
    assert map_response.status_code == 404


async def prepare_live(case, monkeypatch):
    response = await case.client.post("/api/v1/optimizar-rutas", headers=case.headers)
    assert response.status_code == 201, response.text
    state = FleetState()
    await state.remember_position(
        case.vehicle.placa, GpsFix(-12.06, -75.21, 3250.0, case.orders[0].ventana_inicio), case.vehicle.id, None,
    )
    sequence = tuple(stop.order_code for stop in case.solution.itineraries[0].stops
                     if stop.stop_type == TipoParada.DELIVERY)
    await state.replace_sequence(case.vehicle.placa, sequence)
    monkeypatch.setattr(websockets, "fleet_state", state)
    monkeypatch.setattr(websockets, "_eta_for_code", AsyncMock(return_value=None))
    result = LiveReroute("test", case.solution, sequence, (), ())
    return state, result


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["weight", "volume", "window", "shift", "missing"])
async def test_invalid_live_result_preserves_database_and_sends_no_success(db_case, monkeypatch, kind):
    case = db_case
    state, result = await prepare_live(case, monkeypatch)
    monkeypatch.setattr(websockets, "run_optimizer_in_worker", AsyncMock(return_value=replace(result, solution=invalid_solution(case, kind))))
    notifications = AsyncMock()
    monkeypatch.setattr(websockets, "manager", SimpleNamespace(publish=notifications))
    before = await snapshot()
    with pytest.raises(ValueError):
        await websockets._reroute(case.vehicle.placa, reason="test")
    assert await snapshot() == before
    notifications.assert_not_awaited()
    assert (await state.driver(case.vehicle.placa)).remaining_codes == list(result.sequence)


@pytest.mark.asyncio
async def test_live_commit_failure_rolls_back_flushed_rows(db_case, monkeypatch):
    case = db_case
    state, result = await prepare_live(case, monkeypatch)
    monkeypatch.setattr(websockets, "run_optimizer_in_worker", AsyncMock(return_value=result))
    notifications = AsyncMock()
    monkeypatch.setattr(websockets, "manager", SimpleNamespace(publish=notifications))

    class FailingCommit(AsyncSession):
        async def commit(self):
            await self.flush()
            raise RuntimeError("commit B08 simulado después de flush")

    monkeypatch.setattr(websockets, "async_session_factory",
                        async_sessionmaker(engine, class_=FailingCommit, expire_on_commit=False))
    before = await snapshot()
    with pytest.raises(RuntimeError, match="commit B08"):
        await websockets._reroute(case.vehicle.placa, reason="test")
    assert await snapshot() == before
    notifications.assert_not_awaited()
    assert (await state.driver(case.vehicle.placa)).remaining_codes == list(result.sequence)


@pytest.mark.asyncio
async def test_rejected_cancellation_keeps_all_database_states(db_case, monkeypatch):
    case = db_case
    _, result = await prepare_live(case, monkeypatch)
    cancelled_code = case.orders[0].codigo_pedido
    invalid = LiveReroute("cancel", None, (), (), (cancelled_code,))
    monkeypatch.setattr(websockets, "run_optimizer_in_worker", AsyncMock(return_value=invalid))
    notifications = AsyncMock()
    monkeypatch.setattr(websockets, "manager", SimpleNamespace(publish=notifications))
    before = await snapshot()
    with pytest.raises(ValueError):
        await websockets._on_cancel(case.vehicle.placa, {"order_code": cancelled_code})
    assert await snapshot() == before
    notifications.assert_not_awaited()


@pytest.mark.asyncio
async def test_live_success_notifies_only_when_committed_plan_is_visible(db_case, monkeypatch):
    case = db_case
    _, result = await prepare_live(case, monkeypatch)
    monkeypatch.setattr(websockets, "run_optimizer_in_worker", AsyncMock(return_value=result))
    observations = []

    async def published(payload, **kwargs):
        if payload["type"] == "route_update":
            # Conexión independiente: un flush sin commit no hace visible el plan.
            plans, _, _ = await snapshot()
            map_response = await case.client.get("/api/v1/rutas/mapa", headers=case.headers)
            observations.append((plans, payload["feasible"], map_response.json()["metadata"]["feasible"]))

    monkeypatch.setattr(websockets, "manager", SimpleNamespace(publish=published))
    await websockets._reroute(case.vehicle.placa, reason="test")
    assert observations == [(2, True, True)]
