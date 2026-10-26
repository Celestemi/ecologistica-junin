"""Dataset sintético reproducible para EN-001 / RNF-001 (150×15)."""

from __future__ import annotations

import random
from datetime import datetime, time, timedelta
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from app.models.enums import TipoCombustible

LIMA = ZoneInfo("America/Lima")
# Caja del valle (semilla y US-005).
LAT_MIN, LAT_MAX = -12.12, -12.03
LON_MIN, LON_MAX = -75.24, -75.18
ALT_MIN, ALT_MAX = 3250.0, 3400.0


def benchmark_operation_day(seed: int = 901001) -> datetime:
    rng = random.Random(seed)
    base = datetime(2026, 10, 15, tzinfo=LIMA)
    return base.replace(day=15 + (seed % 5))


def synthetic_depot() -> SimpleNamespace:
    return SimpleNamespace(
        nombre="Depósito benchmark EN-001",
        ubicacion={"type": "Point", "coordinates": [-75.2120, -12.0520]},
        altitud_msnm=3250.0,
    )


def synthetic_vehicles(count: int, *, seed: int = 901001) -> list[SimpleNamespace]:
    rng = random.Random(seed + 1)
    vehicles: list[SimpleNamespace] = []
    for index in range(count):
        vehicles.append(
            SimpleNamespace(
                id=index + 1,
                placa=f"BM-{index + 1:03d}",
                capacidad_kg=800.0 + rng.randint(0, 400),
                capacidad_m3=4.0 + rng.random() * 4.0,
                tipo_combustible=TipoCombustible.DIESEL,
                emision_base_co2_g_km=210.0 + rng.random() * 20.0,
                factor_penalizacion_pendiente=0.04,
                activo=True,
            )
        )
    return vehicles


def synthetic_orders(
    count: int,
    *,
    seed: int = 901001,
    weight_kg: float = 8.0,
    spread_windows: bool = True,
) -> list[SimpleNamespace]:
    """Pedidos geocodificados dentro del valle; ventanas amplias para factibilidad."""
    rng = random.Random(seed + 2)
    day = benchmark_operation_day(seed)
    orders: list[SimpleNamespace] = []
    for index in range(count):
        lat = LAT_MIN + rng.random() * (LAT_MAX - LAT_MIN)
        lon = LON_MIN + rng.random() * (LON_MAX - LON_MIN)
        if spread_windows:
            start_h = 7 + (index % 8)
            end_h = min(18, start_h + 4)
        else:
            start_h = 8
            end_h = 17
        orders.append(
            SimpleNamespace(
                id=index + 1,
                codigo_pedido=f"BM-{index + 1:03d}",
                cliente_nombre=f"Cliente benchmark {index + 1}",
                ubicacion={"type": "Point", "coordinates": [lon, lat]},
                altitud_msnm=ALT_MIN + rng.random() * (ALT_MAX - ALT_MIN),
                peso_kg=weight_kg,
                volumen_m3=None,
                ventana_inicio=day.replace(hour=start_h, minute=0, second=0, microsecond=0),
                ventana_fin=day.replace(hour=end_h, minute=0, second=0, microsecond=0),
            )
        )
    return orders


def overloaded_orders(count: int, *, seed: int = 901001) -> list[SimpleNamespace]:
    """Demanda alta para escenario infactible de precheck."""
    return synthetic_orders(count, seed=seed, weight_kg=200.0)


def tight_window_orders(count: int, *, seed: int = 901001) -> list[SimpleNamespace]:
    """Ventanas estrechas para escenario restringido."""
    rng = random.Random(seed + 3)
    day = benchmark_operation_day(seed)
    orders = synthetic_orders(count, seed=seed, spread_windows=False)
    for index, order in enumerate(orders):
        minute = (index * 3) % 60
        start = day.replace(hour=8, minute=minute, second=0, microsecond=0)
        order.ventana_inicio = start
        order.ventana_fin = start + timedelta(minutes=2)
        order.peso_kg = 5.0 + rng.random() * 5.0
    return orders
