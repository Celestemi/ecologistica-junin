"""Precisión de la penalización por pendiente y de las ventanas de tiempo."""

from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest

from app.models.enums import TipoCombustible
from app.services.genetic_solver import (
    leg_co2_grams,
    positive_elevation_gain_m,
    solve_vrptw,
    travel_minutes,
)

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


def _vehicle(vehicle_id: int = 1) -> SimpleNamespace:
    return SimpleNamespace(
        id=vehicle_id,
        placa="W4U-158",
        capacidad_kg=1500.0,
        capacidad_m3=9.0,
        tipo_combustible=TipoCombustible.DIESEL,
        emision_base_co2_g_km=220.0,
        factor_penalizacion_pendiente=0.045,
        activo=True,
    )


def _order(
    order_id: int,
    *,
    lon: float,
    lat: float,
    altitude_m: float,
    start_hour: int,
    start_minute: int,
    end_hour: int,
    end_minute: int,
    weight_kg: float = 20.0,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=order_id,
        codigo_pedido=f"PED-{order_id:03d}",
        cliente_nombre=f"Cliente {order_id}",
        ubicacion=_point(lon, lat),
        altitud_msnm=altitude_m,
        peso_kg=weight_kg,
        ventana_inicio=DAY.replace(hour=start_hour, minute=start_minute),
        ventana_fin=DAY.replace(hour=end_hour, minute=end_minute),
    )


def test_climb_increases_emission_and_descent_does_not() -> None:
    """E = km × base × (1 + penalización × max(0, Δh / 100))."""
    distance_km = 8.0
    base_g_per_km = 220.0
    slope_penalty = 0.045
    flat = leg_co2_grams(distance_km, base_g_per_km, slope_penalty, 0.0)
    climb = leg_co2_grams(distance_km, base_g_per_km, slope_penalty, 160.0)
    descent = leg_co2_grams(distance_km, base_g_per_km, slope_penalty, -90.0)

    assert positive_elevation_gain_m(3250.0, 3410.0) == 160.0
    assert positive_elevation_gain_m(3410.0, 3250.0) == 0.0
    assert flat == pytest.approx(distance_km * base_g_per_km)
    assert climb == pytest.approx(distance_km * base_g_per_km * (1.0 + slope_penalty * 1.6))
    assert descent == pytest.approx(flat)
    assert climb > flat


def test_negative_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        leg_co2_grams(-1.0, 220.0, 0.045, 10.0)
    with pytest.raises(ValueError):
        travel_minutes(1.0, speed_kmh=0.0)


def test_travel_time_uses_huancayo_speed() -> None:
    assert travel_minutes(12.5) == pytest.approx(30.0)


def test_overlapping_short_windows_are_late() -> None:
    """Con un solo vehículo, la segunda entrega no cabe en una ventana de un minuto."""
    orders = [
        _order(1, lon=-75.20486, lat=-12.06513, altitude_m=3271.0, start_hour=8, start_minute=0, end_hour=8, end_minute=1),
        _order(2, lon=-75.20550, lat=-12.06600, altitude_m=3270.0, start_hour=8, start_minute=0, end_hour=8, end_minute=1),
    ]
    solution = solve_vrptw(
        orders,
        [_vehicle()],
        _depot(),
        generations=5,
        population_size=4,
        seed=1,
    )
    assert solution.feasible is False
    assert solution.late_minutes >= 4.0


def test_early_arrival_waits_without_lateness() -> None:
    """Llegar antes de la ventana no penaliza: el vehículo espera a la apertura."""
    orders = [
        _order(1, lon=-75.20486, lat=-12.06513, altitude_m=3271.0, start_hour=8, start_minute=0, end_hour=10, end_minute=0),
        _order(2, lon=-75.20550, lat=-12.06600, altitude_m=3270.0, start_hour=11, start_minute=0, end_hour=13, end_minute=0),
    ]
    solution = solve_vrptw(
        orders,
        [_vehicle()],
        _depot(),
        generations=5,
        population_size=4,
        seed=2,
    )
    assert solution.feasible is True
    assert solution.late_minutes == 0.0
    deliveries = [
        stop
        for itinerary in solution.itineraries
        for stop in itinerary.stops
        if stop.order_id is not None
    ]
    assert [stop.order_id for stop in deliveries] == [1, 2]
