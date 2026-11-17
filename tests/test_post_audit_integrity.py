"""AF-07/08/09/15: oráculos y persistencia reales, datos de prueba sintéticos."""

from datetime import date, datetime, timedelta
from types import SimpleNamespace

import pytest
from sqlalchemy import select

from app.core.database import async_session_factory
from app.models.domain import Pedido, SolucionRuta
from app.models.enums import EstadoSolucion, TipoCombustible
from app.models.operations import AsignacionConductor
from app.services.operational_indicators import summarize_indicators
from app.services.pdf_generator import _completion_day, load_sustainability_report
from tests.test_operational_indicators import _solution
from tests.test_post_audit_security import reassigned_case
from tests.helpers import login_headers


def test_only_latest_snapshot_per_day_is_counted():
    plans = [_solution() for _ in range(3)]
    for index, plan in enumerate(plans):
        plan.id, plan.fecha_operacion, plan.estado = index+1, date(2026,10,1), EstadoSolucion.COMPUTED
    result = summarize_indicators(plans, date(2026,10,1), date(2026,10,1))
    assert result.rutas == 1
    assert result.distancia_total_km == 10


def test_electricity_never_becomes_gallons_and_cost_has_explicit_units():
    plan = _solution()
    for stop in plan.detalles:
        stop.vehiculo.tipo_combustible = TipoCombustible.ELECTRIC
        stop.co2_tramo_g = 1500 if stop.distancia_tramo_km else 0
    result = summarize_indicators([plan], date(2026,10,1), date(2026,10,1))
    assert result.consumo_estimado_gal is None
    assert result.consumo_estimado_kwh == pytest.approx(10)
    # Supuestos ya existentes del PDF: 0,150 kg/kWh; S/0,70/kWh y S/0,15/km.
    assert result.costo_estimado_pen == pytest.approx(10*.70 + 10*.15)


def test_eta_is_not_an_actual_delivery_timestamp():
    detail = SimpleNamespace(eta=datetime(2026,10,1))
    order = SimpleNamespace(ventana_fin=datetime(2026,10,1))
    assert _completion_day(detail, order) is None


def test_live_reoptimization_never_departed_before_the_actual_fix():
    from tests.test_realtime import _solve, ORIGIN, DAY
    from dataclasses import replace
    late_fix = replace(ORIGIN, recorded_at=DAY.replace(hour=13))
    result = _solve(origin=late_fix, reason='late-position')
    assert result.solution is not None
    assert all(stop.eta >= late_fix.recorded_at for itinerary in result.solution.itineraries for stop in itinerary.stops)


@pytest.mark.asyncio
async def test_delivery_event_survives_retry_and_uses_actual_period(reassigned_case):
    from app.services.delivery_events import delivery_events
    case = reassigned_case
    async with async_session_factory() as session:
        assignment = await session.get(AsignacionConductor, case.assignment_id)
        assignment.vehiculo_id = case.new_vehicle
        order = await session.get(Pedido, case.order_id)
        actual = order.ventana_fin + timedelta(days=1)
        await session.commit()
    payload = {'operation_id':'delivery-regression-00001','delivered_at':actual.isoformat()}
    for _ in range(2):
        response = await case.client.post(f'/api/v1/pedidos/{case.code}/entrega', headers=case.headers, json=payload)
        assert response.status_code == 200, response.text
    async with async_session_factory() as session:
        events = await delivery_events(session)
        assert len(events) == 1
        assert events[case.order_id]['moment'] == actual
        assert events[case.order_id]['actor_id'] == case.actor_id
        assert events[case.order_id]['plan'] is not None
        report = await load_sustainability_report(session, actual.date(), actual.date())
        assert len(report.deliveries) == 1
        assert report.deliveries[0].completed_on == actual.date()
        before = await load_sustainability_report(session, actual.date()-timedelta(days=1), actual.date()-timedelta(days=1))
        assert before.deliveries == ()
    manager = await login_headers(case.client, 'gerente@distrirapido.pe', 'Gerente.2026')
    csv = await case.client.get('/api/v1/reportes/sostenibilidad/csv', headers=manager,
        params={'fecha_inicio':actual.date().isoformat(),'fecha_fin':actual.date().isoformat()})
    assert csv.status_code == 200
    assert 'version_plan' in csv.text and case.code in csv.text
    denied = await case.client.get('/api/v1/reportes/sostenibilidad/csv', headers=case.headers)
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_empty_snapshot_does_not_resurrect_a_historical_assignment(reassigned_case, monkeypatch):
    from unittest.mock import AsyncMock
    from app.api.v1 import websockets
    from app.services.realtime_router import FleetState, GpsFix, LiveReroute
    from app.models.domain import Vehiculo
    from app.models.enums import EstadoPedido
    case = reassigned_case
    async with async_session_factory() as session:
        order = await session.get(Pedido, case.order_id)
        vehicle = await session.get(Vehiculo, case.new_vehicle)
        state = FleetState()
        await state.remember_position(vehicle.placa, GpsFix(-12.06,-75.21,3250,order.ventana_inicio), vehicle.id, case.code)
        await state.replace_sequence(vehicle.placa, [case.code])
    monkeypatch.setattr(websockets, 'fleet_state', state)
    monkeypatch.setattr(websockets, 'run_optimizer_in_worker', AsyncMock(return_value=LiveReroute('cancel',None,(),(),(case.code,))))
    await websockets._on_cancel(vehicle.placa, {'order_code':case.code})
    async with async_session_factory() as session:
        assert (await session.get(Pedido,case.order_id)).estado == EstadoPedido.CANCELLED
        newest = await session.scalar(select(SolucionRuta).order_by(SolucionRuta.id.desc()))
        assert newest.metadatos_ga['snapshot_vacio'] is True
        old = await session.scalar(select(SolucionRuta).where(SolucionRuta.codigo=='AF-PLAN-1'))
        assert old.estado == EstadoSolucion.ARCHIVED
        from app.services.active_plan import current_order_detail
        assert await current_order_detail(session, await session.get(Pedido,case.order_id)) is None


@pytest.mark.asyncio
async def test_initial_optimization_cannot_orphan_an_active_assignment(reassigned_case):
    case = reassigned_case
    operator = await login_headers(case.client,'operador@distrirapido.pe','Operador.2026')
    async with async_session_factory() as session:
        order = await session.get(Pedido,case.order_id)
        day = order.ventana_inicio.date()
        before = list(await session.scalars(select(SolucionRuta.id)))
    response = await case.client.post('/api/v1/optimizar-rutas',headers=operator,params={'fecha':day.isoformat()})
    assert response.status_code == 409
    async with async_session_factory() as session:
        assert list(await session.scalars(select(SolucionRuta.id))) == before
        assert (await session.get(Pedido,case.order_id)).estado.value == 'assigned'


@pytest.mark.asyncio
@pytest.mark.parametrize('invalid_time', ['naive', 'future'])
async def test_invalid_delivery_clock_rolls_back_state_and_event(reassigned_case, invalid_time):
    from app.services.delivery_events import delivery_events
    case = reassigned_case
    async with async_session_factory() as session:
        assignment = await session.get(AsignacionConductor,case.assignment_id)
        assignment.vehiculo_id = case.new_vehicle
        await session.commit()
    now = datetime.now().isoformat() if invalid_time == 'naive' else (datetime.now().astimezone()+timedelta(days=1)).isoformat()
    response = await case.client.post(f'/api/v1/pedidos/{case.code}/entrega',headers=case.headers,
        json={'operation_id':'invalid-clock-regression-001','delivered_at':now})
    assert response.status_code == 400
    async with async_session_factory() as session:
        assert (await session.get(Pedido,case.order_id)).estado.value == 'assigned'
        assert await delivery_events(session) == {}
