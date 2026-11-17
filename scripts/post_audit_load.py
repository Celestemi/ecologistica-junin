"""AF-23: smoke de densidad/carga y restore SINTETICOS, no SLI productivo."""

import asyncio
from datetime import datetime, timedelta
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
from time import perf_counter
from zoneinfo import ZoneInfo

import httpx


async def main():
    importlib.import_module('scripts.post-audit-e2e').assert_disposable()
    from tests.conftest import _reset_seed
    from app.core.database import async_session_factory, engine
    from app.core.geo import point_wkt
    from app.models.domain import Deposito, Pedido, Vehiculo
    from app.models.enums import EstadoPedido, EstadoUbicacion, TipoCombustible
    from sqlalchemy import select
    await _reset_seed()
    day=datetime.now(ZoneInfo('America/Lima')).replace(hour=7,minute=0,second=0,microsecond=0)
    async with async_session_factory() as session:
        depot=await session.scalar(select(Deposito).order_by(Deposito.id))
        for old in await session.scalars(select(Vehiculo)): old.activo=False
        for old in await session.scalars(select(Pedido)): old.estado=EstadoPedido.DELIVERED
        session.add_all([Vehiculo(deposito_id=depot.id,placa=f'QL-{i:03}',modelo='Synthetic load',
            capacidad_kg=1200,capacidad_m3=8,tipo_combustible=TipoCombustible.DIESEL,
            rendimiento_km_gal=15,emision_base_co2_g_km=200,factor_penalizacion_pendiente=.04,activo=True) for i in range(50)])
        session.add_all([Pedido(codigo_pedido=f'QL-{i:04}',cliente_nombre='Synthetic load',
            direccion_referencia='Synthetic test point',ubicacion=point_wkt(-75.212+(i%20)*.00001,-12.052+(i//20)*.00001),
            altitud_msnm=3250,volumen_m3=.1,peso_kg=8,ventana_inicio=day,ventana_fin=day+timedelta(hours=12),
            estado_ubicacion=EstadoUbicacion.GEOCODIFICADO,estado=EstadoPedido.PENDING) for i in range(1000)])
        await session.commit()
    async with httpx.AsyncClient(base_url='http://127.0.0.1:18000',timeout=30) as client:
        login=await client.post('/api/v1/auth/ingresar',json={'correo':'operador@distrirapido.pe','clave':'Operador.2026'})
        assert login.status_code==200
        headers={'Authorization':'Bearer '+login.json()['access_token']}
        assert sum(bool(item['activo']) for item in (await client.get('/api/v1/vehiculos',headers=headers)).json())==50
        assert len((await client.get('/api/v1/pedidos',headers=headers)).json())==1000
        semaphore=asyncio.Semaphore(8)
        async def read(index):
            async with semaphore:
                start=perf_counter()
                response=await client.get('/api/v1/vehiculos' if index%2 else '/api/v1/pedidos',headers=headers)
                return perf_counter()-start,response.status_code
        start=perf_counter(); results=await asyncio.gather(*(read(i) for i in range(80))); elapsed=perf_counter()-start
        assert all(status==200 for _,status in results)
    target=Path('AUDITORIA/CORRECCIONES_EVIDENCIAS/fase3-load')
    target.mkdir(parents=True,exist_ok=True)
    runtime=Path('AUDITORIA/CORRECCIONES_EVIDENCIAS/runtime/backup'); runtime.mkdir(parents=True,exist_ok=True)
    container='ecologistica-post-audit-20261117'
    backup_start=perf_counter()
    dump=subprocess.check_output(['docker','exec',container,'pg_dump','-U','ecologistica','--no-owner','--no-privileges','ecologistica_test'])
    (runtime/'synthetic-backup.sql').write_bytes(dump)
    backup_seconds=perf_counter()-backup_start
    database='ecologistica_restore_'+datetime.now().strftime('%Y%m%d_%H%M%S')
    subprocess.run(['docker','exec',container,'psql','-U','ecologistica','-d','postgres','-v','ON_ERROR_STOP=1','-c',f'CREATE DATABASE {database}'],check=True,stdout=subprocess.PIPE)
    restore_start=perf_counter()
    subprocess.run(['docker','exec','-i',container,'psql','-U','ecologistica','-d',database,'-v','ON_ERROR_STOP=1'],input=dump,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    restore_seconds=perf_counter()-restore_start
    query='SELECT (SELECT count(*) FROM pedidos), (SELECT count(*) FROM vehiculos), (SELECT count(*) FROM bitacora);'
    def counts(name):
        return subprocess.check_output(['docker','exec',container,'psql','-U','ecologistica','-d',name,'-At','-c',query]).decode().strip()
    source,restored=counts('ecologistica_test'),counts(database)
    assert source==restored
    times=sorted(value for value,_ in results)
    report={'synthetic':True,'date':datetime.now().astimezone().isoformat(),'records':1000,'active_vehicles':50,
        'requests':80,'concurrency':8,'errors':0,'window_seconds':elapsed,
        'p50_seconds':statistics.median(times),'p95_seconds':times[int(len(times)*.95)-1],
        'backup_seconds':backup_seconds,'restore_seconds':restore_seconds,'backup_bytes':len(dump),
        'backup_sha256':hashlib.sha256(dump).hexdigest(),'restore_database':database,
        'source_and_restored_counts':source,'python':platform.python_version(),'cpu_count':os.cpu_count(),
        'limits':'Read-density smoke and synthetic restore only. Not full business load, DB restart durability, real 1000/day service, multiworker or 99.5% availability in an agreed window.'}
    (target/'result.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report)); await engine.dispose()


if __name__=='__main__':
    asyncio.run(main())
