"""Flujo HTTP/WS TCP real sobre PostGIS NUEVO verificado. Sin navegador/mocks.

Usar solamente con servidor local de esta sesión y credencial de firma sintética.
"""

import asyncio
from datetime import datetime, time
import json
import os
from pathlib import Path
import subprocess
import sys
from time import perf_counter
from zoneinfo import ZoneInfo

import httpx
import websockets


def assert_disposable():
    info = json.loads(subprocess.check_output(['docker','inspect','ecologistica-post-audit-20261117']))[0]
    assert info['Config']['Labels'].get('ecologistica.purpose') == 'post-audit-disposable'
    assert not info['Mounts'] and info['HostConfig']['Tmpfs'].get('/var/lib/postgresql/data') == 'rw'
    assert info['NetworkSettings']['Ports']['5432/tcp'] == [{'HostIp':'127.0.0.1','HostPort':'25436'}]
    assert os.environ.get('DATABASE_URL') == 'postgresql+asyncpg://ecologistica:post-audit-disposable@127.0.0.1:25436/ecologistica_test'
    assert os.environ.get('ECOLOGISTICA_TEST_DISPOSABLE') == '1'
    assert os.environ.get('SECRET_KEY') == 'post-audit-only-disposable-signing-key-not-for-production'


async def main():
    assert_disposable()
    from tests.conftest import _reset_seed
    from app.core.database import async_session_factory, engine
    from app.models.domain import Pedido, Vehiculo
    from app.models.enums import EstadoPedido
    from sqlalchemy import select
    await _reset_seed()
    async with async_session_factory() as session:
        vehicles = list(await session.scalars(select(Vehiculo).order_by(Vehiculo.id)))
        for vehicle in vehicles: vehicle.activo = vehicle is vehicles[0]
        for order in await session.scalars(select(Pedido)): order.estado = EstadoPedido.DELIVERED
        await session.commit()
        plate = vehicles[0].placa
    phase = sys.argv[1] if len(sys.argv) > 1 else 'fase3-e2e'
    if not phase or any(char not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for char in phase):
        raise ValueError('Identificador de evidencia inválido.')
    destination=Path('AUDITORIA/CORRECCIONES_EVIDENCIAS') / phase
    destination.mkdir(parents=True,exist_ok=True)
    steps=[]
    started=perf_counter()
    def passed(step, **details): steps.append({'step':step,'result':'PASO',**details})
    async with httpx.AsyncClient(base_url='http://127.0.0.1:18000',timeout=45) as api, httpx.AsyncClient(base_url='http://127.0.0.1:15173',timeout=15) as frontend:
        assert (await api.get('/health')).status_code == 200
        assert (await api.get('/health/db')).status_code == 200
        passed('backend and real PostGIS health')
        page=await frontend.get('/')
        assert page.status_code == 200 and 'id="root"' in page.text
        assert (await frontend.get('/src/main.tsx')).status_code == 200
        assert (await frontend.get('/api/v1/vehiculos')).status_code == 401
        passed('frontend HTTP accessible; transformed JS and API proxy; not browser execution')
        async def login(email,password,client=api):
            response=await client.post('/api/v1/auth/ingresar',json={'correo':email,'clave':password})
            assert response.status_code==200
            return {'Authorization':'Bearer '+response.json()['access_token']}
        operator=await login('operador@distrirapido.pe','Operador.2026',frontend)
        driver=await login('conductor@distrirapido.pe','Conductor.2026')
        manager=await login('gerente@distrirapido.pe','Gerente.2026')
        passed('login through frontend proxy and backend; synthetic roles')
        now=datetime.now(ZoneInfo('America/Lima'))
        begin=datetime.combine(now.date(),time(0,0),tzinfo=now.tzinfo)
        end=begin.replace(hour=23,minute=59)
        created=await api.post('/api/v1/pedidos',headers=operator,json={
            'codigo_pedido':'QA-LIVE-001','cliente_nombre':'Synthetic QA',
            'direccion_referencia':'Synthetic El Tambo test point','lat':-12.0521,'lon':-75.2119,
            'altitud_msnm':3250,'peso_kg':20,'ventana_inicio':begin.isoformat(),'ventana_fin':end.isoformat()})
        assert created.status_code==201,created.text
        tracking_token=created.json()['token_seguimiento']
        passed('new order through real HTTP; persisted synthetic data')
        route=await api.post('/api/v1/optimizar-rutas',headers=operator,params={'fecha':now.date().isoformat()})
        assert route.status_code==201,route.text
        assert route.json()['metadata']['feasible'] is True
        map_response=await api.get('/api/v1/rutas/mapa',headers=operator)
        assert map_response.status_code==200
        assert map_response.json()['metadata']['id']==route.json()['metadata']['id']
        active=await api.get('/api/v1/rutas/activas',headers=driver)
        assert active.status_code==200
        assert any(stop.get('codigo_pedido')=='QA-LIVE-001' for stop in active.json()['paradas'])
        passed('optimization -> persistence -> GeoJSON map -> assigned driver',plan_id=route.json()['metadata']['id'],road_geometry=False)
        async with websockets.connect(f'ws://127.0.0.1:18000/ws/tracking/{tracking_token}',proxy=None) as public:
            initial=json.loads(await asyncio.wait_for(public.recv(),3))
            assert set(initial)=={'type','estado','eta'}
            token=driver['Authorization'].removeprefix('Bearer ')
            async with websockets.connect(f'ws://127.0.0.1:18000/ws/driver/{plate}',subprotocols=[f'bearer.{token}'],proxy=None) as live:
                await live.send(json.dumps({'type':'position','lat':-12.052,'lon':-75.212,'order_code':'QA-LIVE-001'}))
                safe=json.loads(await asyncio.wait_for(public.recv(),3))
                assert safe=={'type':'order_status','estado':'in_transit'}
                operation={'operation_id':'live-regression-delivery-00001','delivered_at':datetime.now(now.tzinfo).isoformat()}
                delivered=await api.post('/api/v1/pedidos/QA-LIVE-001/entrega',headers=driver,json=operation)
                assert delivered.status_code==200,delivered.text
                assert delivered.json()['estado']=='delivered'
                duplicate=await api.post('/api/v1/pedidos/QA-LIVE-001/entrega',headers=driver,json=operation)
                assert duplicate.status_code==200
                passed('live TCP WebSockets: safe public snapshot/status; driver position; durable delivery and retry')
        params={'fecha_inicio':now.date().isoformat(),'fecha_fin':now.date().isoformat()}
        indicators=await api.get('/api/v1/indicadores',headers=operator,params=params)
        assert indicators.status_code==200 and indicators.json()['rutas']==1
        passed('dashboard API uses current snapshot once',distance_km=indicators.json()['distancia_total_km'])
        for format in ('pdf','csv'):
            response=await api.get(f'/api/v1/reportes/sostenibilidad/{format}',headers=manager,params=params)
            assert response.status_code==200
            if format=='pdf': assert response.content.startswith(b'%PDF')
            else: assert 'QA-LIVE-001' in response.text and 'version_plan' in response.text
            (destination/f'synthetic-report.{format}').write_bytes(response.content)
            passed(f'authorized real {format.upper()} download',bytes=len(response.content))
        denied=await api.get('/api/v1/reportes/sostenibilidad/csv',headers=driver,params=params)
        assert denied.status_code==403
        assert (await api.post('/api/v1/auth/salir',headers=driver)).status_code==204
        assert (await api.get('/api/v1/auth/yo',headers=driver)).status_code==401
        passed('report role restriction and durable logout revocation')
    report={'synthetic':True,'date':datetime.now(now.tzinfo).isoformat(),'elapsed_seconds':perf_counter()-started,
        'scope':'real localhost HTTP/TCP WS + PostGIS; frontend HTTP/proxy only, NO browser/OSRM/TLS or timed 10-minute demo',
        'head':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'working_tree':'uncommitted corrections',
        'steps':steps}
    (destination/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True))
    await engine.dispose()


if __name__=='__main__':
    asyncio.run(main())
