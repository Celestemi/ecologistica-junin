"""Crea la extensión PostGIS, las tablas y la semilla de Huancayo.

Uso:
    python -m app.db.init_db
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, time
from zoneinfo import ZoneInfo

from sqlalchemy import func, select, text

from app.core.database import async_session_factory, engine
from app.core.geo import point_wkt
from app.db.accounts import DEMO_ACCOUNTS, DEMO_PASSWORD_BY_ROLE
from app.models.domain import Base, Deposito, Pedido, Vehiculo
from app.models.enums import EstadoPedido, TipoCombustible
from app.models.identity import Usuario
from app.models.operations import HistorialVehiculo, Jornada
from app.services.passwords import hash_password

logger = logging.getLogger("ecologistica.init_db")

LIMA = ZoneInfo("America/Lima")
# Día operativo fijo para que las ventanas de la semilla no cambien entre ejecuciones.
OPERATION_DAY = datetime(2026, 10, 6, tzinfo=LIMA)


@dataclass(frozen=True)
class VehicleSeed:
    placa: str
    capacidad_kg: float
    capacidad_m3: float
    tipo_combustible: TipoCombustible
    emision_base_co2_g_km: float
    factor_penalizacion_pendiente: float


@dataclass(frozen=True)
class OrderSeed:
    codigo_pedido: str
    cliente_nombre: str
    direccion_referencia: str
    lat: float
    lon: float
    altitud_msnm: float
    peso_kg: float
    ventana_inicio: time
    ventana_fin: time


# Av. Ferrocarril / El Tambo, punto de acopio del MVP.
DEPOT_NAME = "Depósito Principal El Tambo"
DEPOT_ADDRESS = "Av. Ferrocarril, El Tambo, Huancayo"
DEPOT_LAT = -12.0520
DEPOT_LON = -75.2120
DEPOT_ALTITUDE_M = 3250.0

VEHICLES: tuple[VehicleSeed, ...] = (
    VehicleSeed(
        placa="W4U-158",
        capacidad_kg=1500.0,
        capacidad_m3=9.0,
        tipo_combustible=TipoCombustible.DIESEL,
        emision_base_co2_g_km=220.0,
        factor_penalizacion_pendiente=0.045,
    ),
    VehicleSeed(
        placa="E7M-304",
        capacidad_kg=300.0,
        capacidad_m3=1.4,
        tipo_combustible=TipoCombustible.ELECTRIC,
        emision_base_co2_g_km=38.0,
        factor_penalizacion_pendiente=0.012,
    ),
)

# Coordenadas de hitos reales. Los clientes y los pesos son ficticios.
ORDERS: tuple[OrderSeed, ...] = (
    OrderSeed(
        codigo_pedido="PED-001",
        cliente_nombre="Bodega La Colmena",
        direccion_referencia="Plaza Constitución, Cercado de Huancayo",
        lat=-12.06513,
        lon=-75.20486,
        altitud_msnm=3271.0,
        peso_kg=120.0,
        ventana_inicio=time(8, 0),
        ventana_fin=time(11, 0),
    ),
    OrderSeed(
        codigo_pedido="PED-002",
        cliente_nombre="Distribuidora Andina",
        direccion_referencia="Jr. Calixto cdra. 7, zona mayorista, Huancayo",
        lat=-12.06940,
        lon=-75.20749,
        altitud_msnm=3268.0,
        peso_kg=480.0,
        ventana_inicio=time(6, 0),
        ventana_fin=time(9, 0),
    ),
    OrderSeed(
        codigo_pedido="PED-003",
        cliente_nombre="Librería Universitaria",
        direccion_referencia="Universidad Nacional del Centro del Perú, Av. Mariscal Castilla 3909, El Tambo",
        lat=-12.03305,
        lon=-75.23733,
        altitud_msnm=3290.0,
        peso_kg=85.0,
        ventana_inicio=time(9, 0),
        ventana_fin=time(13, 0),
    ),
    OrderSeed(
        codigo_pedido="PED-004",
        cliente_nombre="Botica Santa Rosa",
        direccion_referencia="Chilca Alta, ladera este del distrito de Chilca",
        lat=-12.09820,
        lon=-75.18680,
        altitud_msnm=3410.0,
        peso_kg=40.0,
        ventana_inicio=time(10, 0),
        ventana_fin=time(14, 0),
    ),
    OrderSeed(
        codigo_pedido="PED-005",
        cliente_nombre="Agropecuaria Tunán",
        direccion_referencia="Plaza de Armas, San Jerónimo de Tunán",
        lat=-11.94903,
        lon=-75.28268,
        altitud_msnm=3274.0,
        peso_kg=260.0,
        ventana_inicio=time(8, 30),
        ventana_fin=time(12, 30),
    ),
)


def _window(moment: time) -> datetime:
    return OPERATION_DAY.replace(
        hour=moment.hour,
        minute=moment.minute,
        second=0,
        microsecond=0,
    )


async def ensure_users(session) -> None:
    """Crea las cuentas de demostración que todavía no existen. No pisa claves ya guardadas."""
    existing = set(await session.scalars(select(Usuario.correo)))
    created = 0
    for nombre, correo, rol in DEMO_ACCOUNTS:
        if correo in existing:
            continue
        session.add(
            Usuario(
                nombre=nombre,
                correo=correo,
                rol=rol,
                clave_hash=hash_password(DEMO_PASSWORD_BY_ROLE[rol]),
            )
        )
        created += 1
    if created:
        logger.info("Cuentas de acceso creadas: %s.", created)


async def init_database() -> None:
    """Habilita PostGIS, crea el esquema y carga la semilla si aún no hay depósito."""
    async with engine.begin() as connection:
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(
            text("ALTER TABLE pedidos ADD COLUMN IF NOT EXISTS jornada_id INTEGER REFERENCES jornadas(id)")
        )
    logger.info("Esquema PostGIS listo.")

    async with async_session_factory() as session:
        await ensure_users(session)
        existing = await session.scalar(select(func.count()).select_from(Deposito))
        if existing:
            await session.commit()
            logger.info("La semilla ya existe (%s depósitos). Usuarios de acceso verificados.", existing)
            return

        depot = Deposito(
            nombre=DEPOT_NAME,
            direccion=DEPOT_ADDRESS,
            ubicacion=point_wkt(DEPOT_LON, DEPOT_LAT),
            altitud_msnm=DEPOT_ALTITUDE_M,
        )
        session.add(depot)
        await session.flush()

        for vehicle in VEHICLES:
            session.add(
                Vehiculo(
                    deposito_id=depot.id,
                    placa=vehicle.placa,
                    capacidad_kg=vehicle.capacidad_kg,
                    capacidad_m3=vehicle.capacidad_m3,
                    tipo_combustible=vehicle.tipo_combustible,
                    emision_base_co2_g_km=vehicle.emision_base_co2_g_km,
                    factor_penalizacion_pendiente=vehicle.factor_penalizacion_pendiente,
                )
            )

        for order in ORDERS:
            session.add(
                Pedido(
                    codigo_pedido=order.codigo_pedido,
                    cliente_nombre=order.cliente_nombre,
                    direccion_referencia=order.direccion_referencia,
                    ubicacion=point_wkt(order.lon, order.lat),
                    altitud_msnm=order.altitud_msnm,
                    peso_kg=order.peso_kg,
                    ventana_inicio=_window(order.ventana_inicio),
                    ventana_fin=_window(order.ventana_fin),
                    estado=EstadoPedido.PENDING,
                )
            )

        await session.commit()
        logger.info(
            "Semilla cargada: 1 depósito, %s vehículos, %s pedidos.",
            len(VEHICLES),
            len(ORDERS),
        )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    asyncio.run(init_database())


if __name__ == "__main__":
    main()
