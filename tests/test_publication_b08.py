"""B-08: política de publicación y orden transaccional (sin BD ni red)."""

from dataclasses import replace
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from zoneinfo import ZoneInfo

import pytest

from app.api.v1 import routes, websockets
from app.core.geo import point_wkt
from app.models.domain import Deposito, Pedido, Vehiculo
from app.models.enums import EstadoOperativoVehiculo, EstadoPedido, RolUsuario, TipoCombustible, TipoParada
from app.services.genetic_solver import SERVICE_MINUTES, solve_vrptw
from app.services.realtime_router import FleetState, GpsFix, LiveReroute
from app.services.route_constraints import PUBLICATION_VEHICLE_IDS, PublicationValidation, validate_for_publication


@pytest.fixture
def publication_case():
    day = datetime(2026, 10, 6, 8, tzinfo=ZoneInfo("America/Lima"))
    order = SimpleNamespace(
        id=1, codigo_pedido="B08-001", cliente_nombre="Prueba B08",
        ubicacion={"type": "Point", "coordinates": [-75.200, -12.050]},
        altitud_msnm=3250.0, peso_kg=20.0, volumen_m3=1.0,
        ventana_inicio=day, ventana_fin=day.replace(hour=18), estado=EstadoPedido.ASSIGNED,
    )
    vehicle = SimpleNamespace(
        id=1, placa="B08-001", capacidad_kg=100.0, capacidad_m3=5.0,
        tipo_combustible=TipoCombustible.DIESEL, emision_base_co2_g_km=220.0,
        factor_penalizacion_pendiente=0.045, activo=True,
        estado_operativo=EstadoOperativoVehiculo.ACTIVO,
    )
    depot = SimpleNamespace(
        id=1, nombre="Depósito B08", altitud_msnm=3250.0,
        ubicacion={"type": "Point", "coordinates": [-75.210, -12.060]},
    )
    solution = solve_vrptw([order], [vehicle], depot, generations=2, population_size=2, seed=8)
    assert solution.feasible
    return order, vehicle, depot, solution


def validate(case, solution=None):
    order, vehicle, _, original = case
    return validate_for_publication(
        original if solution is None else solution, [order], [vehicle], service_minutes=SERVICE_MINUTES,
    )


def change_delivery(solution, **changes):
    itinerary = solution.itineraries[0]
    stops = tuple(replace(stop, **changes) if stop.stop_type == TipoParada.DELIVERY else stop
                  for stop in itinerary.stops)
    return replace(solution, itineraries=(replace(itinerary, stops=stops),))


def test_valid_solution_can_be_published(publication_case):
    assert validate(publication_case).ok


@pytest.mark.parametrize("field,value,code", [
    ("peso_kg", 101.0, "CAPACIDAD_PESO"),
    ("volumen_m3", 6.0, "CAPACIDAD_VOLUMEN"),
])
def test_capacity_uses_orders_and_current_vehicle_not_solver_flags(publication_case, field, value, code):
    setattr(publication_case[0], field, value)
    result = validate(publication_case)
    assert not result.ok
    assert code in {item.code for item in result.violations}


def test_late_eta_cannot_be_hidden_by_zero_penalty(publication_case):
    order, _, _, solution = publication_case
    invalid = change_delivery(solution, eta=order.ventana_fin.replace(hour=19), late_minutes=0.0)
    result = validate(publication_case, invalid)
    assert not result.ok
    assert "VENTANA_ENTREGA" in {item.code for item in result.violations}


@pytest.mark.parametrize("changes", [{"eta": None}, {"matrix_trusted": False}])
def test_window_cannot_be_approved_without_reliable_eta(publication_case, changes):
    assert not validate(publication_case, change_delivery(publication_case[3], **changes)).ok


def test_shift_is_recomputed_from_stops(publication_case, monkeypatch):
    from app.core.config import get_settings
    monkeypatch.setenv("MAX_SHIFT_MINUTES", "30")
    get_settings.cache_clear()
    try:
        invalid = change_delivery(publication_case[3], travel_minutes=31.0)
        result = validate(publication_case, invalid)
        assert not result.ok
        assert "JORNADA_MAXIMA" in {item.code for item in result.violations}
    finally:
        get_settings.cache_clear()


def test_required_order_missing_even_if_unassigned_list_is_empty(publication_case):
    invalid = replace(publication_case[3], itineraries=(), unassigned_order_ids=())
    result = validate(publication_case, invalid)
    assert not result.ok
    assert result.unassigned_order_codes == [publication_case[0].codigo_pedido]


def test_order_cannot_be_assigned_twice(publication_case):
    solution = publication_case[3]
    assert not validate(publication_case, replace(solution, itineraries=solution.itineraries * 2)).ok


def test_unknown_vehicle_or_order_is_rejected(publication_case):
    solution = publication_case[3]
    itinerary = replace(solution.itineraries[0], vehicle_id=999)
    assert not validate(publication_case, replace(solution, itineraries=(itinerary,))).ok
    assert not validate(publication_case, change_delivery(solution, order_id=999)).ok


def test_inactive_vehicle_is_rejected(publication_case):
    publication_case[1].estado_operativo = EstadoOperativoVehiculo.MANTENIMIENTO
    assert not validate(publication_case).ok


def test_solver_infeasibility_cannot_be_reported_as_success(publication_case):
    assert not validate(publication_case, replace(publication_case[3], feasible=False)).ok


class TransactionDouble:
    """Doble de orquestación, no sustituto de las pruebas PostGIS."""

    def __init__(self, order, timeline, fail_commit=False):
        self.order = order
        self.before = order.estado
        self.timeline = timeline
        self.fail_commit = fail_commit
        self.flush = AsyncMock()
        # El lock PostgreSQL se comprueba con concurrencia real en la nueva suite.
        self.execute = AsyncMock()
        self.add = Mock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        if exc_type is not None:
            self.order.estado = self.before

    async def commit(self):
        if self.fail_commit:
            raise RuntimeError("fallo de commit simulado")
        self.timeline.append("commit")


@pytest.fixture
async def live_case(publication_case, monkeypatch):
    order, vehicle, depot, solution = publication_case
    timeline = []
    session = TransactionDouble(order, timeline)
    state = FleetState()
    await state.remember_position(vehicle.placa, GpsFix(-12.06, -75.21, 3250, order.ventana_inicio), vehicle.id, None)
    await state.replace_sequence(vehicle.placa, [order.codigo_pedido])
    monkeypatch.setattr(websockets, "fleet_state", state)
    monkeypatch.setattr(websockets, "async_session_factory", lambda: session)
    monkeypatch.setattr(websockets, "_load_route", AsyncMock(return_value=(depot, vehicle, [order])))
    monkeypatch.setattr(websockets, "_require_order", AsyncMock(return_value=order))
    monkeypatch.setattr(websockets, "_require_order_on_vehicle_route", AsyncMock())
    monkeypatch.setattr(websockets, "_eta_for_code", AsyncMock(return_value=None))
    config = SimpleNamespace(validada_normativamente=False, activa=False, reglas=[])
    monkeypatch.setattr(websockets, "load_config", AsyncMock(return_value=config), raising=False)
    result = LiveReroute("test", solution, (order.codigo_pedido,), (), ())
    worker = AsyncMock(return_value=result)
    monkeypatch.setattr(websockets, "run_optimizer_in_worker", worker)
    manager = SimpleNamespace(publish=AsyncMock(side_effect=lambda *args, **kw: timeline.append("publish")))
    monkeypatch.setattr(websockets, "manager", manager)

    def persist(*args, **kwargs):
        timeline.append("persist")
        order.estado = EstadoPedido.ASSIGNED
        return SimpleNamespace(id=1)

    persistence = Mock(side_effect=persist)
    monkeypatch.setattr(routes, "_persist_solution", persistence)
    monkeypatch.setattr(routes, "retain_other_vehicles", AsyncMock())
    from app.services import active_plan
    monkeypatch.setattr(active_plan, 'activate_snapshot', AsyncMock())
    return SimpleNamespace(order=order, vehicle=vehicle, solution=solution, worker=worker,
                           session=session, state=state, manager=manager, persistence=persistence,
                           timeline=timeline, result=result)


@pytest.mark.asyncio
async def test_invalid_live_solution_changes_neither_orders_nor_sequence(live_case):
    case = live_case
    case.worker.return_value = replace(case.result, solution=replace(case.solution, itineraries=()))
    with pytest.raises(ValueError):
        await websockets._reroute(case.vehicle.placa, reason="test")
    case.persistence.assert_not_called()
    case.manager.publish.assert_not_awaited()
    assert case.order.estado == EstadoPedido.ASSIGNED
    assert (await case.state.driver(case.vehicle.placa)).remaining_codes == [case.order.codigo_pedido]
    assert case.timeline == []


@pytest.mark.asyncio
async def test_live_notifications_follow_successful_commit(live_case):
    case = live_case
    await websockets._reroute(case.vehicle.placa, reason="test")
    assert case.timeline[:3] == ["persist", "commit", "publish"]
    assert case.manager.publish.call_args_list[0].args[0]["feasible"] is True


@pytest.mark.asyncio
async def test_failed_commit_does_not_notify_or_replace_sequence(live_case):
    case = live_case
    case.session.fail_commit = True
    with pytest.raises(RuntimeError, match="commit"):
        await websockets._reroute(case.vehicle.placa, reason="test")
    case.manager.publish.assert_not_awaited()
    assert (await case.state.driver(case.vehicle.placa)).remaining_codes == [case.order.codigo_pedido]


@pytest.mark.asyncio
async def test_cancellation_is_not_committed_before_reroute_validation(live_case):
    case = live_case
    # Ningún pedido activo queda tras cancelar, pero el worker devuelve una ruta ajena al lote.
    with pytest.raises(ValueError):
        await websockets._on_cancel(case.vehicle.placa, {"order_code": case.order.codigo_pedido})
    assert case.order.estado == EstadoPedido.ASSIGNED
    case.manager.publish.assert_not_awaited()
    assert "commit" not in case.timeline


@pytest.mark.asyncio
async def test_empty_live_route_is_valid_only_when_no_required_orders_remain(live_case):
    case = live_case
    case.worker.return_value = LiveReroute("cancel", None, (), (), (case.order.codigo_pedido,))
    await websockets._on_cancel(case.vehicle.placa, {"order_code": case.order.codigo_pedido})
    assert case.order.estado == EstadoPedido.CANCELLED
    assert case.timeline[0] == "commit"
    case.persistence.assert_not_called()


@pytest.mark.asyncio
async def test_none_solution_cannot_hide_remaining_orders(live_case):
    case = live_case
    case.worker.return_value = LiveReroute("test", None, (), (), ())
    with pytest.raises(ValueError):
        await websockets._reroute(case.vehicle.placa, reason="test")
    case.manager.publish.assert_not_awaited()


@pytest.mark.asyncio
async def test_live_rejects_an_unjustified_exclusion(live_case):
    case = live_case
    case.worker.return_value = replace(case.result, blocked_codes=(case.order.codigo_pedido,))
    with pytest.raises(ValueError, match="exclusiones"):
        await websockets._reroute(case.vehicle.placa, reason="test")
    case.persistence.assert_not_called()
    case.manager.publish.assert_not_awaited()


@pytest.mark.asyncio
async def test_live_applies_the_same_fleet_precheck(live_case):
    case = live_case
    case.order.volumen_m3 = case.vehicle.capacidad_m3 + 1.0
    with pytest.raises(ValueError, match="capacidad agregada"):
        await websockets._reroute(case.vehicle.placa, reason="test")
    case.worker.assert_not_awaited()
    case.persistence.assert_not_called()


@pytest.mark.asyncio
async def test_live_rejects_a_plate_excluded_by_the_current_rule(live_case, monkeypatch):
    from app.services.plate_restriction import ExclusionPlaca
    case = live_case
    exclusion = ExclusionPlaca(case.vehicle.placa, 1, "Placa no apta en esta jornada.")
    monkeypatch.setattr(websockets, "filter_vehicles_for_planning", lambda *args: ([], [exclusion]))
    with pytest.raises(ValueError, match="Placa no apta"):
        await websockets._reroute(case.vehicle.placa, reason="test")
    case.worker.assert_not_awaited()
    case.manager.publish.assert_not_awaited()


@pytest.mark.asyncio
async def test_blocked_added_order_state_matches_the_event(live_case):
    case = live_case
    extra = SimpleNamespace(codigo_pedido="B08-002", estado=EstadoPedido.PENDING)
    result = LiveReroute("blockade", None, (), (extra.codigo_pedido,), ())
    await websockets._apply_reroute(case.session, result, {}, [extra])
    assert extra.estado == EstadoPedido.INCIDENT


@pytest.mark.asyncio
async def test_rejected_socket_operation_emits_error_without_route_success(live_case):
    case = live_case
    case.worker.return_value = replace(case.result, solution=replace(case.solution, itineraries=()))
    await websockets._on_driver_message(case.vehicle.placa, '{"type":"add_order","order_code":"B08-001"}')
    messages = [call.args[0] for call in case.manager.publish.call_args_list]
    assert len(messages) == 1
    assert messages[0]["type"] == "error"
    assert isinstance(messages[0]["detail"], str)
    assert messages[0]["validation"]["codigo"] == "RUTA_INFACTIBLE"


def orm_case(case):
    """Entidades transitorias para inspeccionar persistencia/GeoJSON sin afirmar BD."""
    source, fleet, _, solved = case
    order = Pedido(
        id=source.id, codigo_pedido=source.codigo_pedido, cliente_nombre=source.cliente_nombre,
        direccion_referencia="Dirección sintética", peso_kg=source.peso_kg, volumen_m3=source.volumen_m3,
        ventana_inicio=source.ventana_inicio, ventana_fin=source.ventana_fin,
        ubicacion=point_wkt(-75.2, -12.05), altitud_msnm=3250, estado=source.estado,
    )
    vehicle = Vehiculo(
        id=fleet.id, placa=fleet.placa, capacidad_kg=fleet.capacidad_kg, capacidad_m3=fleet.capacidad_m3,
        estado_operativo=fleet.estado_operativo, activo=True,
    )
    depot = Deposito(id=1)
    return order, vehicle, depot, solved


def test_persistence_requires_successful_publication_validation(publication_case):
    order, vehicle, depot, solved = orm_case(publication_case)
    session = SimpleNamespace(add=Mock())
    with pytest.raises(ValueError):
        routes._persist_solution(session, depot, [order], [vehicle], solved,
                                 publication=PublicationValidation(ok=False))
    session.add.assert_not_called()
    assert order.estado == EstadoPedido.ASSIGNED


@pytest.mark.asyncio
async def test_map_uses_persisted_publication_evidence_including_legacy_case(publication_case, monkeypatch):
    order, vehicle, depot, solved = orm_case(publication_case)
    session = SimpleNamespace(add=Mock())
    proof = validate_for_publication(solved, [order], [vehicle], service_minutes=SERVICE_MINUTES)
    assert proof.ok
    solution = routes._persist_solution(session, depot, [order], [vehicle], solved, publication=proof)
    solution.id = 1
    monkeypatch.setattr(routes, "_enforce_vehicle_scope", AsyncMock(return_value=None))
    monkeypatch.setattr(routes, "_fleet_groups", AsyncMock(return_value=[solution.detalles]))
    response = await routes.fleet_map(session=session, actor=SimpleNamespace(rol=RolUsuario.OPERADOR))
    assert response.metadata.feasible is True
    assert solution.metadatos_ga[PUBLICATION_VEHICLE_IDS] == [vehicle.id]
    assert {feature.properties["order_code"] for feature in response.features
            if feature.properties.get("stop_type") == TipoParada.DELIVERY.value} == {order.codigo_pedido}
    # Una bandera histórica del solver no acredita que la ruta pasara por esta política.
    solution.metadatos_ga = {"feasible": True}
    legacy = await routes.fleet_map(session=session, actor=SimpleNamespace(rol=RolUsuario.OPERADOR))
    assert legacy.metadata.feasible is False


@pytest.mark.asyncio
@pytest.mark.parametrize("previous_validated", [True, False])
async def test_retaining_other_vehicle_preserves_but_does_not_invent_validation(publication_case, previous_validated):
    order, vehicle, depot, solved = orm_case(publication_case)
    proof = validate_for_publication(solved, [order], [vehicle], service_minutes=SERVICE_MINUTES)
    session = SimpleNamespace(add=Mock(), flush=AsyncMock())
    previous = routes._persist_solution(session, depot, [order], [vehicle], solved, publication=proof)
    previous.id = 1
    if not previous_validated:
        previous.metadatos_ga = {"feasible": True}
    # El vehículo 2 es el recién recalculado; el 1 viene del plan previo.
    new = SimpleNamespace(
        id=2, fecha_operacion=previous.fecha_operacion, co2_estimado_kg=0.0,
        metadatos_ga={PUBLICATION_VEHICLE_IDS: [2]}, distancia_total_km=1.0,
        duracion_total_min=1.0, co2_referencia_kg=0.0, co2_evitado_kg=0.0, arboles_quinual_eq=0.0,
    )
    session.scalar = AsyncMock(return_value=previous)
    await routes.retain_other_vehicles(session, new, 2)
    assert new.metadatos_ga[PUBLICATION_VEHICLE_IDS] == ([1, 2] if previous_validated else [2])


@pytest.mark.asyncio
async def test_eta_change_invalidates_the_previous_publication_evidence(publication_case, monkeypatch):
    order, vehicle, depot, solved = orm_case(publication_case)
    proof = validate_for_publication(solved, [order], [vehicle], service_minutes=SERVICE_MINUTES)
    session = SimpleNamespace(add=Mock(), commit=AsyncMock())
    solution = routes._persist_solution(session, depot, [order], [vehicle], solved, publication=proof)
    solution.id = 1
    for index, detail in enumerate(solution.detalles, start=1):
        detail.id = index
    session.scalar = AsyncMock(return_value=solution)
    monkeypatch.setattr(routes, "recalculate_solution_etas", AsyncMock(return_value=solution))
    await routes.recalculate_route_etas(solution.id, session=session, _=None)
    session.commit.assert_awaited_once()
    assert solution.metadatos_ga[PUBLICATION_VEHICLE_IDS] == []
