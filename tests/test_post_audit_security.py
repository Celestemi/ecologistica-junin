"""Regresiones AF-01/02/03; casos de BD solo sobre fixture descartable."""

from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import select

from app.api.v1 import websockets
from app.core.database import async_session_factory
from app.models.domain import Pedido, RutaDetalle, SolucionRuta, Vehiculo
from app.models.enums import EstadoPedido, EstadoSolucion, TipoParada
from app.models.identity import Usuario
from app.models.operations import AsignacionConductor
from app.services.realtime_router import ConnectionManager, LiveReroute
from tests.helpers import login_headers
from tests.test_realtime import FakeSocket
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from app.main import app


@pytest.fixture
async def reassigned_case(client):
    """Dos snapshots completos: A histórico, B vigente; conductor aún en A."""
    headers = await login_headers(client, 'conductor@distrirapido.pe', 'Conductor.2026')
    async with async_session_factory() as session:
        order = await session.scalar(select(Pedido).order_by(Pedido.id))
        vehicles = list(await session.scalars(select(Vehiculo).order_by(Vehiculo.id)))
        user = await session.scalar(select(Usuario).where(Usuario.correo == 'conductor@distrirapido.pe'))
        assignment = await session.scalar(select(AsignacionConductor).where(AsignacionConductor.usuario_id == user.id))
        assignment.vehiculo_id = vehicles[0].id
        day = order.ventana_inicio.astimezone(ZoneInfo('America/Lima')).date()
        for index, vehicle in enumerate(vehicles[:2]):
            plan = SolucionRuta(codigo=f'AF-PLAN-{index}', deposito_id=vehicle.deposito_id,
                fecha_operacion=day, distancia_total_km=1, duracion_total_min=5,
                co2_estimado_kg=.2, co2_referencia_kg=.3, co2_evitado_kg=.1,
                arboles_quinual_eq=0, fitness=1, estado=EstadoSolucion.COMPUTED)
            plan.detalles.append(RutaDetalle(vehiculo_id=vehicle.id, pedido_id=order.id,
                secuencia=1, tipo_parada=TipoParada.DELIVERY, ubicacion=order.ubicacion,
                altitud_msnm=order.altitud_msnm))
            session.add(plan)
            await session.flush()
        order.estado = EstadoPedido.ASSIGNED
        await session.commit()
        return SimpleNamespace(client=client, headers=headers, code=order.codigo_pedido,
            order_id=order.id, old_vehicle=vehicles[0].id, new_vehicle=vehicles[1].id,
            assignment_id=assignment.id, actor_id=user.id)


@pytest.mark.asyncio
async def test_reassigned_old_driver_cannot_deliver_but_current_driver_can(reassigned_case):
    case = reassigned_case
    payload = {'operation_id': '00000000-0000-4000-8000-000000000001', 'delivered_at': datetime.now(ZoneInfo('America/Lima')).isoformat()}
    denied = await case.client.post(f'/api/v1/pedidos/{case.code}/entrega', headers=case.headers, json=payload)
    assert denied.status_code == 403
    async with async_session_factory() as session:
        assert (await session.get(Pedido, case.order_id)).estado == EstadoPedido.ASSIGNED
        assignment = await session.get(AsignacionConductor, case.assignment_id)
        assignment.vehiculo_id = case.new_vehicle
        await session.commit()
    accepted = await case.client.post(f'/api/v1/pedidos/{case.code}/entrega', headers=case.headers, json=payload)
    assert accepted.status_code == 200, accepted.text
    repeated = await case.client.post(f'/api/v1/pedidos/{case.code}/entrega', headers=case.headers, json=payload)
    assert repeated.status_code == 200


@pytest.mark.asyncio
async def test_old_vehicle_cannot_cancel_reassigned_order(reassigned_case):
    case = reassigned_case
    async with async_session_factory() as session:
        order = await session.get(Pedido, case.order_id)
        with pytest.raises(ValueError, match='no pertenece'):
            await websockets._require_order_on_vehicle_route(session, order, case.old_vehicle)
        await websockets._require_order_on_vehicle_route(session, order, case.new_vehicle)


@pytest.mark.asyncio
@pytest.mark.parametrize('state', [EstadoPedido.DELIVERED, EstadoPedido.CANCELLED])
async def test_terminal_order_is_not_changed_by_reroute(state):
    order = SimpleNamespace(estado=state)
    from unittest.mock import AsyncMock
    session = SimpleNamespace(flush=AsyncMock())
    with pytest.raises(ValueError):
        await websockets._apply_reroute(session, LiveReroute('cancel', None, (), (), ('ONE',)), {'ONE': order}, [])
    assert order.estado == state
    session.flush.assert_not_awaited()


@pytest.mark.asyncio
async def test_public_channels_receive_only_their_safe_status_and_eta():
    manager = ConnectionManager()
    public_a, public_b, driver, desk = (FakeSocket() for _ in range(4))
    await manager.connect_tracker('ONE', public_a, public=True)
    await manager.connect_tracker('TWO', public_b, public=True)
    await manager.connect_driver('driver', driver)
    await manager.connect_tracker('despacho', desk)
    for payload in [
        {'type':'position','order_code':'ONE','lat':-12.061234,'lon':-75.215678,'driver_id':'secret'},
        {'type':'route_update','sequence':['ONE','TWO'],'removed_codes':['OTHER']},
        {'type':'incident','note':'private','lat':-12.06},
        {'type':'order_status','order_code':'ONE','estado':'delivered','driver_id':'secret'},
        {'type':'eta','order_code':'ONE','eta':'2026-11-17T12:00:00-05:00','distance_km':1.234,'vehicle_id':5},
    ]:
        await manager.publish(payload, driver_id='driver', order_codes=['ONE','TWO'])
    assert public_a.sent == [{'type':'order_status','estado':'delivered'}, {'type':'eta','eta':'2026-11-17T12:00:00-05:00'}]
    assert public_b.sent == []
    assert len(driver.sent) == len(desk.sent) == 5
    await manager.disconnect_tracker('ONE', public_a)
    await manager.publish({'type':'order_status','order_code':'ONE','estado':'delivered'}, order_codes=['ONE'])
    assert len(public_a.sent) == 2


@pytest.mark.asyncio
async def test_public_eta_rejects_nested_payload_that_could_smuggle_ids():
    manager = ConnectionManager()
    public = FakeSocket()
    await manager.connect_tracker('ONE',public,public=True)
    await manager.publish({'type':'eta','order_code':'ONE','eta':{'vehicle_id':99,'lat':-12.05}},order_codes=['ONE'])
    assert public.sent == []


@pytest.mark.asyncio
async def test_driver_socket_closes_after_message_burst(client):
    headers = await login_headers(client,'operador@distrirapido.pe','Operador.2026')
    token = headers['Authorization'].removeprefix('Bearer ')
    with TestClient(app) as sync:
        with sync.websocket_connect('/ws/driver/QA-LIMIT',subprotocols=[f'bearer.{token}']) as socket:
            for _ in range(30):
                socket.send_json({'type':'position','lat':0,'lon':0})
                assert socket.receive_json()['type'] == 'error'
            socket.send_json({'type':'position','lat':0,'lon':0})
            with pytest.raises(WebSocketDisconnect):
                socket.receive_json()


@pytest.mark.asyncio
async def test_public_snapshot_and_token_channel_cleanup(reassigned_case, caplog):
    import logging
    caplog.set_level(logging.INFO, logger='ecologistica.realtime')
    case = reassigned_case
    async with async_session_factory() as session:
        order = await session.get(Pedido, case.order_id)
        token = order.token_seguimiento
    with TestClient(app) as sync:
        with sync.websocket_connect(f'/ws/tracking/{token}') as socket:
            snapshot = socket.receive_json()
            assert set(snapshot) == {'type', 'estado', 'eta'}
            assert snapshot['estado'] == 'assigned'
    assert case.code not in websockets.manager._public_trackers
    class DisconnectingSocket(FakeSocket):
        async def receive_text(self):
            raise WebSocketDisconnect(code=1000)
    await websockets.tracking_socket(DisconnectingSocket(), token)
    assert token not in caplog.text


@pytest.mark.asyncio
async def test_delivered_order_cannot_cancel_or_be_inserted(reassigned_case):
    case = reassigned_case
    async with async_session_factory() as session:
        order = await session.get(Pedido, case.order_id)
        order.estado = EstadoPedido.DELIVERED
        await session.commit()
    for action in (websockets._on_cancel, websockets._on_add):
        with pytest.raises(ValueError):
            await action('synthetic-driver', {'order_code':case.code}, case.new_vehicle)
    async with async_session_factory() as session:
        assert (await session.get(Pedido, case.order_id)).estado == EstadoPedido.DELIVERED


@pytest.mark.asyncio
async def test_delivery_waits_for_reassignment_transaction_and_rechecks(reassigned_case):
    import asyncio
    from app.services.active_plan import lock_route_state
    case = reassigned_case
    payload = {'operation_id':'00000000-0000-4000-8000-000000000002',
               'delivered_at':datetime.now(ZoneInfo('America/Lima')).isoformat()}
    async with async_session_factory() as setup:
        new_plan = await setup.scalar(select(SolucionRuta).where(SolucionRuta.codigo == 'AF-PLAN-1'))
        new_plan.estado = EstadoSolucion.ARCHIVED
        await setup.commit()  # A es vigente antes de la carrera.
    async with async_session_factory() as writer:
        await lock_route_state(writer)
        new_plan = await writer.scalar(select(SolucionRuta).where(SolucionRuta.codigo == 'AF-PLAN-1'))
        new_plan.estado = EstadoSolucion.COMPUTED  # B pendiente de commit.
        await writer.flush()
        task = asyncio.create_task(case.client.post(f'/api/v1/pedidos/{case.code}/entrega', headers=case.headers, json=payload))
        await asyncio.sleep(.05)
        assert not task.done(), 'La mutación no debe cruzar una publicación en curso'
        await writer.commit()
    response = await task
    assert response.status_code == 403
    async with async_session_factory() as session:
        assert (await session.get(Pedido, case.order_id)).estado == EstadoPedido.ASSIGNED


@pytest.mark.asyncio
async def test_logout_revokes_existing_socket_and_rest(client):
    headers = await login_headers(client, 'operador@distrirapido.pe', 'Operador.2026')
    token = headers['Authorization'].removeprefix('Bearer ')
    with TestClient(app) as sync:
        with sync.websocket_connect('/ws/tracking/despacho', subprotocols=[f'bearer.{token}']) as socket:
            assert socket.receive_json()['type'] == 'hello'
            assert sync.post('/api/v1/auth/salir', headers=headers).status_code == 204
            with pytest.raises(WebSocketDisconnect):
                socket.receive_json()
    assert (await client.get('/api/v1/auth/yo', headers=headers)).status_code == 401


@pytest.mark.asyncio
async def test_idle_socket_expires(client):
    from datetime import timedelta, timezone
    import jwt
    from app.core.config import get_settings
    from app.services.tokens import read_access_token
    headers = await login_headers(client, 'operador@distrirapido.pe', 'Operador.2026')
    claims = read_access_token(headers['Authorization'].removeprefix('Bearer '))
    claims['exp'] = datetime.now(timezone.utc) + timedelta(seconds=2)
    token = jwt.encode(claims, get_settings().secret_key, algorithm='HS256')
    with TestClient(app) as sync:
        with sync.websocket_connect('/ws/tracking/despacho', subprotocols=[f'bearer.{token}']) as socket:
            assert socket.receive_json()['type'] == 'hello'
            with pytest.raises(WebSocketDisconnect):
                socket.receive_json()


@pytest.mark.asyncio
async def test_role_change_invalidates_rest_and_live_driver(client):
    from app.models.enums import RolUsuario
    headers = await login_headers(client, 'conductor@distrirapido.pe', 'Conductor.2026')
    token = headers['Authorization'].removeprefix('Bearer ')
    try:
        with TestClient(app) as sync:
            with sync.websocket_connect('/ws/driver/W4U-158', subprotocols=[f'bearer.{token}']) as socket:
                async with async_session_factory() as session:
                    user = await session.scalar(select(Usuario).where(Usuario.correo == 'conductor@distrirapido.pe'))
                    user.rol = RolUsuario.AUDITOR
                    await session.commit()
                with pytest.raises(WebSocketDisconnect):
                    socket.receive_json()
        assert (await client.get('/api/v1/auth/yo', headers=headers)).status_code == 401
    finally:
        async with async_session_factory() as session:
            user = await session.scalar(select(Usuario).where(Usuario.correo == 'conductor@distrirapido.pe'))
            user.rol = RolUsuario.CONDUCTOR
            await session.commit()
