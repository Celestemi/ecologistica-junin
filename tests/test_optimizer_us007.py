"""US-007 / RF-007 / RN-008 — motor VRPTW + Green VRP (GA propio)."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.core.database import engine
from app.models.enums import TipoCombustible, TipoParada
from app.services.genetic_solver import (
    RN008_MIN_CO2_SAVINGS_PCT,
    RN008_MIN_DISTANCE_SAVINGS_PCT,
    haversine_km,
    leg_co2_grams,
    savings_percent,
    solve_vrptw,
)
from tests.helpers import login_headers

LIMA = ZoneInfo("America/Lima")
DAY = datetime(2026, 10, 6, tzinfo=LIMA)


def _point(lon: float, lat: float) -> dict[str, object]:
    return {"type": "Point", "coordinates": [lon, lat]}


def _depot() -> SimpleNamespace:
    return SimpleNamespace(
        nombre="Depósito",
        ubicacion=_point(-75.2120, -12.0520),
        altitud_msnm=3250.0,
    )


def _vehicle(**kwargs: object) -> SimpleNamespace:
    base = dict(
        id=1,
        placa="V-001",
        capacidad_kg=1500.0,
        capacidad_m3=9.0,
        tipo_combustible=TipoCombustible.DIESEL,
        emision_base_co2_g_km=220.0,
        factor_penalizacion_pendiente=0.045,
        activo=True,
    )
    base.update(kwargs)
    return SimpleNamespace(**base)


def _order(
    order_id: int,
    *,
    lon: float,
    lat: float,
    start_h: int,
    end_h: int,
    start_m: int = 0,
    end_m: int = 0,
    weight_kg: float = 10.0,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=order_id,
        codigo_pedido=f"P-{order_id:03d}",
        cliente_nombre=f"C{order_id}",
        ubicacion=_point(lon, lat),
        altitud_msnm=3270.0,
        peso_kg=weight_kg,
        volumen_m3=None,
        ventana_inicio=DAY.replace(hour=start_h, minute=start_m),
        ventana_fin=DAY.replace(hour=end_h, minute=end_m),
    )


def test_savings_percent_honest_no_forced_floor() -> None:
    assert savings_percent(100.0, 90.0) == pytest.approx(10.0)
    assert savings_percent(100.0, 100.0) == 0.0
    assert savings_percent(0.0, 50.0) == 0.0


def test_haversine_and_emission_units() -> None:
    km = haversine_km(-12.06513, -75.20486, -12.06940, -75.20749)
    assert km > 0.5
    grams = leg_co2_grams(km, 220.0, 0.045, 50.0)
    assert grams == pytest.approx(km * 220.0 * (1.0 + 0.045 * 0.5))


def test_one_order_one_vehicle_feasible() -> None:
    solution = solve_vrptw(
        [_order(1, lon=-75.20486, lat=-12.06513, start_h=8, end_h=12)],
        [_vehicle()],
        _depot(),
        generations=3,
        population_size=4,
        seed=1,
    )
    assert solution.feasible is True
    deliveries = [
        s
        for it in solution.itineraries
        for s in it.stops
        if s.stop_type == TipoParada.DELIVERY
    ]
    assert len(deliveries) == 1
    assert solution.sequential_baseline_distance_km >= solution.distance_km


def test_reproducible_with_same_seed() -> None:
    orders = [
        _order(1, lon=-75.20486, lat=-12.06513, start_h=8, end_h=12),
        _order(2, lon=-75.20550, lat=-12.06600, start_h=9, end_h=13),
    ]
    kwargs = dict(orders=orders, vehicles=[_vehicle()], depot=_depot(), generations=4, population_size=4)
    a = solve_vrptw(**kwargs, seed=99)
    b = solve_vrptw(**kwargs, seed=99)
    assert a.distance_km == pytest.approx(b.distance_km)
    assert a.co2_kg == pytest.approx(b.co2_kg)
    assert a.fitness == pytest.approx(b.fitness)


def test_sequential_baseline_reported_not_as_hard_gate() -> None:
    """RN-008: se informa el % real; no se rechaza la solución si la meta no se alcanza."""
    solution = solve_vrptw(
        [_order(1, lon=-75.20486, lat=-12.06513, start_h=8, end_h=18)],
        [_vehicle()],
        _depot(),
        generations=2,
        population_size=3,
        seed=5,
    )
    assert solution.sequential_baseline_distance_km >= 0.0
    assert 0.0 <= solution.savings_distance_pct_vs_sequential <= 100.0
    assert solution.rn008_distance_goal_met == (
        solution.savings_distance_pct_vs_sequential >= RN008_MIN_DISTANCE_SAVINGS_PCT
    )
    assert solution.rn008_co2_goal_met == (
        solution.savings_co2_pct_vs_sequential >= RN008_MIN_CO2_SAVINGS_PCT
    )


def test_infeasible_windows_not_marked_feasible() -> None:
    orders = [
        _order(1, lon=-75.20486, lat=-12.06513, start_h=8, end_h=8, start_m=0, end_m=1, weight_kg=10),
        _order(2, lon=-75.20550, lat=-12.06600, start_h=8, end_h=8, start_m=0, end_m=1, weight_kg=10),
    ]
    solution = solve_vrptw(
        orders,
        [_vehicle()],
        _depot(),
        generations=4,
        population_size=4,
        seed=1,
    )
    assert solution.feasible is False
    assert solution.late_minutes > 0


@pytest.mark.asyncio
async def test_optimize_seed_metadata_rn008(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert optimized.status_code == 201
    meta = optimized.json()["metadata"]
    assert meta["pedidos"] == 5
    assert meta["feasible"] is True
    assert meta["linea_base_secuencial_km"] is not None
    assert meta["ahorro_distancia_pct_vs_secuencial"] is not None
    assert meta["ahorro_co2_pct_vs_secuencial"] is not None
    assert isinstance(meta["rn008_meta_distancia_cumplida"], bool)
    assert isinstance(meta["rn008_meta_co2_cumplida"], bool)


@pytest.mark.asyncio
async def test_jornada_filter_excludes_other_days(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    other_day = "2026-11-01"
    csv_body = (
        "codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin,lat,lon,altitud\n"
        'OTRO-001,Otro,"Plaza Constitución Huancayo",10,09:00,12:00,'
        "-12.06513,-75.20486,3271\n"
    )
    imported = await client.post(
        f"/api/v1/jornadas/{other_day}/importar",
        headers=operador,
        json={"csv": csv_body},
    )
    assert imported.status_code == 200

    seed_day = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert seed_day.status_code == 201
    assert seed_day.json()["metadata"]["pedidos"] == 5

    async with engine.begin() as connection:
        row = await connection.execute(
            text("SELECT estado FROM pedidos WHERE codigo_pedido = 'OTRO-001'")
        )
        assert row.scalar_one() == "pending"

    other = await client.post(
        "/api/v1/optimizar-rutas",
        headers=operador,
        params={"fecha": other_day},
    )
    assert other.status_code == 201
    assert other.json()["metadata"]["pedidos"] == 1
