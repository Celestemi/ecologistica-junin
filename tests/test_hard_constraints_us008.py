"""US-008 / RF-008 — restricciones duras de capacidad y jornada operativa."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select, text

from app.core.database import engine

from app.models.domain import SolucionRuta
from app.models.enums import TipoCombustible, TipoParada
from app.services.genetic_solver import (
    SERVICE_MINUTES,
    RouteSolution,
    StopItinerary,
    VehicleItinerary,
    solve_vrptw,
)
from app.services.route_constraints import (
    compute_shift_minutes,
    precheck_fleet_capacity,
    validate_for_publication,
)
from tests.helpers import login_headers

LIMA = ZoneInfo("America/Lima")
DAY = datetime(2026, 10, 6, tzinfo=LIMA)


def _point(lon: float, lat: float) -> dict[str, object]:
    return {"type": "Point", "coordinates": [lon, lat]}


def _depot() -> SimpleNamespace:
    return SimpleNamespace(
        nombre="Depósito Principal El Tambo",
        ubicacion=_point(-75.2120, -12.0520),
        altitud_msnm=3250.0,
    )


def _vehicle(
    vehicle_id: int = 1,
    *,
    capacity_kg: float = 1500.0,
    capacity_m3: float = 9.0,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=vehicle_id,
        placa="W4U-158",
        capacidad_kg=capacity_kg,
        capacidad_m3=capacity_m3,
        tipo_combustible=TipoCombustible.DIESEL,
        emision_base_co2_g_km=220.0,
        factor_penalizacion_pendiente=0.045,
        activo=True,
    )


def _order(
    order_id: int,
    *,
    lon: float = -75.20486,
    lat: float = -12.06513,
    altitude_m: float = 3271.0,
    start_hour: int = 8,
    end_hour: int = 18,
    weight_kg: float = 20.0,
    volume_m3: float | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=order_id,
        codigo_pedido=f"PED-{order_id:03d}",
        cliente_nombre=f"Cliente {order_id}",
        ubicacion=_point(lon, lat),
        altitud_msnm=altitude_m,
        peso_kg=weight_kg,
        volumen_m3=volume_m3,
        ventana_inicio=DAY.replace(hour=start_hour, minute=0),
        ventana_fin=DAY.replace(hour=end_hour, minute=0),
    )


def _pedido(order_id: int, code: str, kg: float, m3: float | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        id=order_id,
        codigo_pedido=code,
        peso_kg=kg,
        volumen_m3=m3,
    )


def _veh_entity(vid: int, plate: str, kg: float, m3: float) -> SimpleNamespace:
    return SimpleNamespace(id=vid, placa=plate, capacidad_kg=kg, capacidad_m3=m3)


def _delivery_stop(*, travel_minutes: float = 10.0, late: float = 0.0) -> StopItinerary:
    return StopItinerary(
        sequence=2,
        stop_type=TipoParada.DELIVERY,
        order_id=1,
        order_code="PED-001",
        customer_name="Cliente",
        latitude=-12.06513,
        longitude=-75.20486,
        altitude_m=3271.0,
        eta=DAY.replace(hour=9),
        distance_km=4.0,
        elevation_delta_m=0.0,
        travel_minutes=travel_minutes,
        co2_grams=100.0,
        late_minutes=late,
        enters_historic_center=False,
    )


def _itinerary(**overrides: object) -> VehicleItinerary:
    base = dict(
        vehicle_id=1,
        plate="W4U-158",
        fuel=TipoCombustible.DIESEL,
        capacity_kg=100.0,
        capacity_m3=10.0,
        load_kg=80.0,
        load_m3=4.0,
        stops=(_delivery_stop(),),
        distance_km=8.0,
        co2_grams=200.0,
        duration_minutes=30.0,
        capacity_excess_kg=0.0,
        capacity_excess_m3=0.0,
        shift_minutes=20.0,
        shift_excess_minutes=0.0,
        historic_entries=0,
    )
    base.update(overrides)
    return VehicleItinerary(**base)  # type: ignore[arg-type]


def _route_solution(*itineraries: VehicleItinerary, unassigned: tuple[int, ...] = ()) -> RouteSolution:
    return RouteSolution(
        itineraries=itineraries,
        distance_km=sum(item.distance_km for item in itineraries),
        duration_minutes=sum(item.duration_minutes for item in itineraries),
        co2_grams=sum(item.co2_grams for item in itineraries),
        co2_kg=0.0,
        fifo_co2_kg=0.0,
        fifo_distance_km=0.0,
        sequential_baseline_co2_kg=0.0,
        sequential_baseline_distance_km=0.0,
        savings_co2_pct_vs_sequential=0.0,
        savings_distance_pct_vs_sequential=0.0,
        rn008_distance_goal_met=False,
        rn008_co2_goal_met=False,
        co2_saved_kg=0.0,
        arboles_quinual_eq=0.0,
        fitness=0.0,
        feasible=False,
        late_minutes=0.0,
        capacity_excess_kg=sum(item.capacity_excess_kg for item in itineraries),
        capacity_excess_m3=sum(item.capacity_excess_m3 for item in itineraries),
        shift_excess_minutes=sum(item.shift_excess_minutes for item in itineraries),
        unassigned_order_ids=unassigned,
        historic_entries=0,
        generations=1,
        population_size=1,
        seed=0,
        best_fitness_per_generation=(0.0,),
        generations_executed=1,
        ga_elapsed_seconds=0.0,
        solver_elapsed_seconds=0.0,
        stop_reason="test",
    )


def test_precheck_exact_weight_at_fleet_limit_is_feasible() -> None:
    orders = [_pedido(1, "A", 100.0), _pedido(2, "B", 50.0)]
    vehicles = [_veh_entity(1, "V1", 100.0, 5.0), _veh_entity(2, "V2", 50.0, 5.0)]
    result = precheck_fleet_capacity(orders, vehicles)  # type: ignore[arg-type]
    assert result.feasible is True
    assert result.excess_kg == 0.0


def test_precheck_weight_over_fleet() -> None:
    orders = [_pedido(1, "A", 200.0)]
    vehicles = [_veh_entity(1, "V1", 150.0, 10.0)]
    result = precheck_fleet_capacity(orders, vehicles)  # type: ignore[arg-type]
    assert result.feasible is False
    assert result.excess_kg == pytest.approx(50.0)


def test_precheck_volume_exact_and_over() -> None:
    orders = [_pedido(1, "A", 1.0, 5.0), _pedido(2, "B", 1.0, 5.0)]
    vehicles = [_veh_entity(1, "V1", 100.0, 10.0)]
    ok = precheck_fleet_capacity(orders, vehicles)  # type: ignore[arg-type]
    assert ok.feasible is True
    assert ok.excess_m3 == 0.0

    heavy = [_pedido(1, "A", 1.0, 11.0)]
    bad = precheck_fleet_capacity(heavy, vehicles)  # type: ignore[arg-type]
    assert bad.feasible is False
    assert bad.excess_m3 == pytest.approx(1.0)


def test_validate_weight_at_100_percent_ok() -> None:
    itinerary = _itinerary(load_kg=100.0, capacity_kg=100.0, capacity_excess_kg=0.0)
    solution = _route_solution(itinerary)
    orders = [_pedido(1, "PED-001", 100.0)]
    vehicles = [_veh_entity(1, "W4U-158", 100.0, 10.0)]
    pub = validate_for_publication(
        solution,
        orders,  # type: ignore[arg-type]
        vehicles,  # type: ignore[arg-type]
        service_minutes=SERVICE_MINUTES,
    )
    assert pub.ok is True


def test_validate_rejects_weight_and_volume_excess() -> None:
    orders = [_pedido(1, "PED-001", 120.0, 12.0)]
    vehicles = [_veh_entity(1, "W4U-158", 100.0, 10.0)]
    by_weight = _route_solution(
        _itinerary(load_kg=120.0, capacity_excess_kg=20.0, load_m3=4.0),
    )
    pub_w = validate_for_publication(
        by_weight,
        orders,  # type: ignore[arg-type]
        vehicles,  # type: ignore[arg-type]
        service_minutes=SERVICE_MINUTES,
    )
    assert pub_w.ok is False
    assert any(v.code == "CAPACIDAD_PESO" for v in pub_w.violations)

    by_volume = _route_solution(
        _itinerary(load_m3=12.0, capacity_excess_m3=2.0, load_kg=80.0),
    )
    pub_v = validate_for_publication(
        by_volume,
        orders,  # type: ignore[arg-type]
        vehicles,  # type: ignore[arg-type]
        service_minutes=SERVICE_MINUTES,
    )
    assert pub_v.ok is False
    assert any(v.code == "CAPACIDAD_VOLUMEN" for v in pub_v.violations)


def test_compute_shift_within_and_over_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MAX_SHIFT_MINUTES", "30")
    monkeypatch.setenv("ENFORCE_SHIFT_LIMIT", "true")
    from app.core.config import get_settings

    get_settings.cache_clear()
    short = _itinerary(stops=(_delivery_stop(travel_minutes=10.0),))
    assert compute_shift_minutes(short, SERVICE_MINUTES) == pytest.approx(10.0 + SERVICE_MINUTES)

    long = _itinerary(stops=(_delivery_stop(travel_minutes=500.0),))
    solution = _route_solution(long)
    pub = validate_for_publication(
        solution,
        [_pedido(1, "PED-001", 10.0)],
        [_veh_entity(1, "W4U-158", 500.0, 50.0)],
        service_minutes=SERVICE_MINUTES,
    )
    assert pub.ok is False
    assert any(v.code == "JORNADA_MAXIMA" for v in pub.violations)
    get_settings.cache_clear()


def test_solver_weight_exact_max_and_over() -> None:
    at_max = solve_vrptw(
        [_order(1, weight_kg=1500.0)],
        [_vehicle(capacity_kg=1500.0)],
        _depot(),
        generations=3,
        population_size=3,
        seed=7,
    )
    assert at_max.capacity_excess_kg == 0.0
    assert at_max.feasible is True

    over = solve_vrptw(
        [_order(1, weight_kg=1600.0)],
        [_vehicle(capacity_kg=1500.0)],
        _depot(),
        generations=3,
        population_size=3,
        seed=7,
    )
    assert over.capacity_excess_kg > 0.0
    assert over.feasible is False


def test_solver_accumulated_volume_on_one_vehicle() -> None:
    orders = [
        _order(1, weight_kg=10.0, volume_m3=4.0, start_hour=8, end_hour=12),
        _order(2, weight_kg=10.0, volume_m3=4.0, start_hour=9, end_hour=13),
    ]
    solution = solve_vrptw(
        orders,
        [_vehicle(capacity_kg=100.0, capacity_m3=8.0)],
        _depot(),
        generations=5,
        population_size=4,
        seed=3,
    )
    assert solution.capacity_excess_m3 == 0.0
    assert solution.feasible is True
    deliveries = [
        stop
        for it in solution.itineraries
        for stop in it.stops
        if stop.stop_type == TipoParada.DELIVERY
    ]
    assert len(deliveries) == 2


def test_solver_volume_over_capacity_infeasible() -> None:
    solution = solve_vrptw(
        [_order(1, weight_kg=1.0, volume_m3=10.0)],
        [_vehicle(capacity_kg=100.0, capacity_m3=9.0)],
        _depot(),
        generations=3,
        population_size=3,
        seed=1,
    )
    assert solution.capacity_excess_m3 > 0.0
    assert solution.feasible is False


@pytest.mark.asyncio
async def test_seed_optimize_regression_sprint1(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert optimized.status_code == 201
    meta = optimized.json()["metadata"]
    assert meta["feasible"] is True
    assert meta["pedidos"] == 5
    assert meta.get("jornada_normativa_validada") is False
    assert "ahorro_distancia_pct_vs_secuencial" in meta


@pytest.mark.asyncio
async def test_fleet_insufficient_409_without_persisting(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    async with engine.begin() as connection:
        await connection.execute(
            text("UPDATE pedidos SET peso_kg = 2500 WHERE codigo_pedido = 'PED-002'")
        )
    before = await client.get("/api/v1/pedidos", headers=operador)
    pending_before = sum(1 for row in before.json() if row["estado"] == "pendiente")

    denied = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert denied.status_code == 409
    detail = denied.json()["detail"]
    assert detail["codigo"] == "CAPACIDAD_FLOTA_INSUFICIENTE"
    assert detail["exceso_kg"] > 0

    async with engine.begin() as connection:
        count = await connection.scalar(select(func.count()).select_from(SolucionRuta))
    assert count == 0

    after = await client.get("/api/v1/pedidos", headers=operador)
    pending_after = sum(1 for row in after.json() if row["estado"] == "pendiente")
    assert pending_after == pending_before


@pytest.mark.asyncio
async def test_import_optional_volume_persisted(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    day = "2026-10-07"
    csv_body = (
        "codigo,cliente,direccion,peso_kg,volumen_m3,hora_inicio,hora_fin,lat,lon,altitud\n"
        'VOL-001,Cliente Vol,"Jr. Calixto cdra. 7 Huancayo",50,2.5,08:00,12:00,'
        "-12.06940,-75.20749,3268\n"
    )
    imported = await client.post(
        f"/api/v1/jornadas/{day}/importar",
        headers=operador,
        json={"csv": csv_body},
    )
    assert imported.status_code == 200
    async with engine.begin() as connection:
        row = await connection.execute(
            text(
                "SELECT volumen_m3 FROM pedidos WHERE codigo_pedido = 'VOL-001'"
            )
        )
        volume = row.scalar_one()
    assert volume == pytest.approx(2.5)
