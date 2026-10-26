"""US-009 / RF-009 — secuencia de paradas y ETA."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
from httpx import AsyncClient

from app.models.enums import EstadoEta, TipoCombustible, TipoParada
from app.services.eta_schedule import (
    classify_delivery_arrival,
    late_minutes_after_window,
    wait_minutes_before_window,
)
from app.services.genetic_solver import solve_vrptw
from tests.helpers import login_headers

LIMA = ZoneInfo("America/Lima")
DAY = datetime(2026, 10, 6, 12, 0, tzinfo=LIMA)


def test_wait_and_late_minutes() -> None:
    window_start = DAY.replace(hour=10)
    window_end = DAY.replace(hour=11)
    early = DAY.replace(hour=9, minute=30)
    assert wait_minutes_before_window(early, window_start) == pytest.approx(30.0)
    assert late_minutes_after_window(early, window_end) == 0.0
    late = DAY.replace(hour=11, minute=20)
    assert late_minutes_after_window(late, window_end) == pytest.approx(20.0)
    state, wait, mins_late = classify_delivery_arrival(
        early, window_start, window_end, matrix_available=True
    )
    assert state == EstadoEta.EN_ESPERA
    assert wait == pytest.approx(30.0)
    assert mins_late == 0.0


def test_matrix_missing_null_eta_state() -> None:
    state, _, _ = classify_delivery_arrival(
        DAY, DAY.replace(hour=9), DAY.replace(hour=12), matrix_available=False
    )
    assert state == EstadoEta.REVISION_MATRIZ


def _point(lon: float, lat: float) -> dict[str, object]:
    return {"type": "Point", "coordinates": [lon, lat]}


def _depot() -> SimpleNamespace:
    return SimpleNamespace(
        nombre="Depósito",
        ubicacion=_point(-75.2120, -12.0520),
        altitud_msnm=3250.0,
    )


def _vehicle() -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        placa="V1",
        capacidad_kg=1500.0,
        capacidad_m3=9.0,
        tipo_combustible=TipoCombustible.DIESEL,
        emision_base_co2_g_km=220.0,
        factor_penalizacion_pendiente=0.045,
        activo=True,
    )


def _order(oid: int, lat: float, lon: float, sh: int, eh: int) -> SimpleNamespace:
    return SimpleNamespace(
        id=oid,
        codigo_pedido=f"P-{oid}",
        cliente_nombre="Cliente",
        ubicacion=_point(lon, lat),
        altitud_msnm=3270.0,
        peso_kg=10.0,
        volumen_m3=None,
        ventana_inicio=DAY.replace(hour=sh, minute=0),
        ventana_fin=DAY.replace(hour=eh, minute=0),
    )


def test_delivery_sequence_and_eta_on_solver() -> None:
    solution = solve_vrptw(
        [
            _order(1, -12.06513, -75.20486, 8, 12),
            _order(2, -12.06600, -75.20550, 9, 13),
        ],
        [_vehicle()],
        _depot(),
        generations=4,
        population_size=4,
        seed=3,
    )
    deliveries = [
        (stop.delivery_index, stop.eta, stop.eta_estado)
        for it in solution.itineraries
        for stop in it.stops
        if stop.stop_type == TipoParada.DELIVERY
    ]
    assert len(deliveries) == 2
    assert {item[0] for item in deliveries} == {1, 2}
    assert all(item[1] is not None for item in deliveries)
    assert all(item[2] != EstadoEta.REVISION_MATRIZ for item in deliveries)


def test_untrusted_matrix_leaves_eta_null() -> None:
    target_lat = -12.06600

    def deny_leg(_olat: float, _olon: float, dlat: float, _dlon: float, haversine_km: float) -> float | None:
        if abs(dlat - target_lat) < 0.0001:
            return None
        return haversine_km

    solution = solve_vrptw(
        [
            _order(1, -12.06513, -75.20486, 8, 18),
            _order(2, target_lat, -75.20550, 9, 18),
        ],
        [_vehicle()],
        _depot(),
        generations=2,
        population_size=3,
        seed=1,
        distance_adjuster=deny_leg,
    )
    stops = [
        stop
        for it in solution.itineraries
        for stop in it.stops
        if stop.stop_type == TipoParada.DELIVERY and stop.order_id == 2
    ]
    assert len(stops) == 1
    assert stops[0].eta is None
    assert stops[0].eta_estado == EstadoEta.REVISION_MATRIZ


@pytest.mark.asyncio
async def test_optimize_geojson_eta_fields(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert optimized.status_code == 201
    points = [
        f
        for f in optimized.json()["features"]
        if f["geometry"]["type"] == "Point" and f["properties"].get("stop_type") == "delivery"
    ]
    assert len(points) >= 5
    sample = points[0]["properties"]
    assert sample.get("delivery_index") is not None
    assert sample.get("distance_note")
    assert "geodésica" in sample["distance_note"].lower() or "cuerda" in sample["distance_note"].lower()


@pytest.mark.asyncio
async def test_recalculate_etas_endpoint(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert optimized.status_code == 201
    solution_id = optimized.json()["metadata"]["id"]
    recalc = await client.post(
        f"/api/v1/soluciones/{solution_id}/recalcular-etas",
        headers=operador,
    )
    assert recalc.status_code == 200
    deliveries = [p for p in recalc.json()["paradas"] if p["tipo_parada"] == "delivery"]
    assert len(deliveries) >= 5
    assert all(p.get("secuencia_entrega") for p in deliveries)
