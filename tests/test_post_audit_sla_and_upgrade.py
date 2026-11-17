"""AF-10/12: testigo factible independiente y upgrade sintético aislado."""

from datetime import datetime, timedelta
from pathlib import Path
from time import perf_counter
from zoneinfo import ZoneInfo
import json
import platform

import pytest
from sqlalchemy import select, text

from app.core.database import async_session_factory, engine
from app.core.geo import point_wkt
from app.models.domain import Deposito, Pedido, Vehiculo
from app.models.enums import EstadoPedido, EstadoUbicacion, TipoCombustible
from app.services.genetic_solver import SERVICE_MINUTES
from tests.helpers import login_headers


@pytest.mark.asyncio
async def test_synthetic_legacy_geometry_upgrade_is_idempotent_and_preserves_rows(client):
    script = Path('app/db/post_auditoria_001_geometria.sql').read_text(encoding='utf-8')
    async with engine.begin() as connection:
        await connection.execute(text('CREATE TEMP TABLE rutas_detalle (id integer PRIMARY KEY, marker text) ON COMMIT DROP'))
        await connection.execute(text("INSERT INTO rutas_detalle VALUES (7, 'synthetic-legacy')"))
        for _ in range(2):
            await connection.execute(text(script))
        await connection.execute(text("UPDATE rutas_detalle SET geometria_tramo=ST_GeomFromText('LINESTRING(-75.21 -12.05,-75.20 -12.06)',4326) WHERE id=7"))
        row = (await connection.execute(text('SELECT marker, ST_SRID(geometria_tramo), GeometryType(geometria_tramo) FROM rutas_detalle WHERE id=7'))).one()
        assert tuple(row) == ('synthetic-legacy',4326,'LINESTRING')


@pytest.mark.asyncio
@pytest.mark.slow
async def test_http_asgi_150x15_has_an_independent_feasible_witness(client, record_property):
    """No certifica OSRM/red externa: API ASGI + worker + PostGIS real aislado."""
    day = datetime(2026,11,17,8,tzinfo=ZoneInfo('America/Lima'))
    headers = await login_headers(client,'operador@distrirapido.pe','Operador.2026')
    async with async_session_factory() as session:
        depot = await session.scalar(select(Deposito).order_by(Deposito.id))
        # Testigo construido: 15 grupos de 10, cada uno 80 kg/1 m3.
        for old in await session.scalars(select(Pedido)):
            old.estado = EstadoPedido.DELIVERED
        for old in await session.scalars(select(Vehiculo)):
            old.activo = False
        vehicles = []
        orders = []
        for index in range(15):
            vehicle = Vehiculo(deposito_id=depot.id,placa=f'QA-{index:03}',modelo='Synthetic witness',
                capacidad_kg=80,capacidad_m3=1,tipo_combustible=TipoCombustible.DIESEL,
                rendimiento_km_gal=15,emision_base_co2_g_km=200,factor_penalizacion_pendiente=.04,activo=True)
            session.add(vehicle); vehicles.append(vehicle)
        for index in range(150):
            # Cuadrícula de ~45 m de diámetro cerca del depósito, fuera del centro.
            lon = -75.212 + (index%10)*.00002
            lat = -12.052 + (index//10)*.00002
            order = Pedido(codigo_pedido=f'QA-{index:03}',cliente_nombre='Synthetic benchmark',
                direccion_referencia='Synthetic benchmark',ubicacion=point_wkt(lon,lat),altitud_msnm=3250,
                volumen_m3=.1,peso_kg=8,ventana_inicio=day,ventana_fin=day+timedelta(hours=8),
                estado_ubicacion=EstadoUbicacion.GEOCODIFICADO,estado=EstadoPedido.PENDING)
            session.add(order); orders.append(order)
        await session.commit()
        ids = {order.id for order in orders}
    # Cota independiente del solver: <=200 km/grado, <=.001 grado por tramo,
    # 11 tramos/grupo a solo 10 km/h +10*5 min servicio = 63,2 min <480 min.
    witness_minutes = 11 * (.001*200) / 10 * 60 + 10 * SERVICE_MINUTES
    assert witness_minutes < 480 and 10*8 <= 80 and 10*.1 <= 1
    started = perf_counter()
    response = await client.post('/api/v1/optimizar-rutas',headers=headers,params={'fecha':day.date().isoformat()})
    elapsed = perf_counter()-started
    assert response.status_code == 201, response.text
    body = response.json()
    assert body['metadata']['feasible'] is True and body['metadata']['pedidos'] == 150
    # El contrato GeoJSON puede exponer solo el código; verificarlo sin depender del ID.
    codes = [feature['properties']['order_code'] for feature in body['features'] if feature['properties'].get('stop_type')=='delivery']
    assert len(codes) == len(set(codes)) == 150
    assert set(codes) == {f'QA-{index:03}' for index in range(150)}
    assert elapsed <= 45
    async with async_session_factory() as session:
        from app.models.domain import RutaDetalle, SolucionRuta
        plan = await session.get(SolucionRuta,body['metadata']['id'])
        stored = list(await session.scalars(select(RutaDetalle.pedido_id).where(RutaDetalle.solucion_id==plan.id,RutaDetalle.pedido_id.isnot(None))))
        assert set(stored) == ids and len(stored)==150
    from app.api.v1 import websockets
    from app.services.realtime_router import FleetState, GpsFix
    state = FleetState()
    vehicle = vehicles[0]
    await state.remember_position(vehicle.placa,GpsFix(-12.052,-75.212,3250,day),vehicle.id,None)
    previous_state = websockets.fleet_state
    websockets.fleet_state = state
    try:
        dynamic_started = perf_counter()
        await websockets._reroute(vehicle.placa,reason='synthetic-benchmark')
        dynamic_elapsed = perf_counter()-dynamic_started
        assert dynamic_elapsed < 30
    finally:
        websockets.fleet_state = previous_state
    record_property('benchmark',json.dumps({'synthetic':True,'scope':'HTTP ASGI + worker + real isolated PostGIS; OSRM disabled',
        'orders':150,'vehicles':15,'elapsed_seconds':elapsed,'feasible':True,'unique_assigned':150,
        'witness_minutes_upper_bound':witness_minutes,'dynamic_pipeline_seconds':dynamic_elapsed,
        'dynamic_scope':'function pipeline + worker + real PostGIS; not live websocket latency',
        'python':platform.python_version(),'platform':platform.platform()}))
