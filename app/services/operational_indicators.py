"""Consolidado único de indicadores Sprint 3 a partir de soluciones persistidas."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import isfinite
from typing import Iterable

from app.core.config import get_settings
from app.core.emissions import quinual_equivalent
from app.models.domain import SolucionRuta
from app.models.enums import TipoParada
from app.services.active_plan import latest_snapshots
from app.services.energy_accounting import estimate_energy, vehicle_factors


@dataclass(frozen=True)
class IndicatorSummary:
    fecha_inicio: date
    fecha_fin: date
    rutas: int
    distancia_total_km: float
    duracion_total_min: float
    consumo_estimado_gal: float | None
    co2_estimado_kg: float
    co2_evitado_kg: float
    arboles_quinual_eq: float | None
    quinual_kg_co2_por_ano: float | None
    linea_base_secuencial_km: float | None
    linea_base_secuencial_co2_kg: float | None
    ahorro_distancia_pct_vs_secuencial: float | None
    ahorro_co2_pct_vs_secuencial: float | None
    consumo_estimado_kwh: float | None = None
    costo_estimado_pen: float | None = None
    base_metricas: str = 'plan_vigente_estimado'
    referencia_comparable: bool = True


def _valid(value: object) -> float | None:
    if isinstance(value, (int, float)) and isfinite(value) and value >= 0:
        return float(value)
    return None


def _saving(baseline: float | None, optimized: float) -> float | None:
    if baseline is None or baseline <= 0:
        return None
    return (baseline - optimized) / baseline * 100.0


def summarize_indicators(solutions: Iterable[SolucionRuta], start: date, end: date) -> IndicatorSummary:
    items = latest_snapshots(solutions)
    distance = sum(item.distancia_total_km for item in items)
    duration = sum(item.duracion_total_min for item in items)
    emitted = sum(item.co2_estimado_kg for item in items)
    avoided = sum(item.co2_evitado_kg for item in items)
    gallons = 0.0
    has_consumption = False
    kwh, has_electricity, cost = 0.0, False, 0.0
    sequential_km = 0.0
    sequential_co2 = 0.0
    comparable = bool(items)
    for solution in items:
        metadata = solution.metadatos_ga or {}
        if metadata.get('referencia_comparable') is False:
            comparable = False
        baseline_km = _valid(metadata.get("linea_base_secuencial_km"))
        baseline_co2 = _valid(metadata.get("linea_base_secuencial_co2_kg"))
        if baseline_km is None or baseline_co2 is None or baseline_km <= 0 or baseline_co2 <= 0:
            comparable = False
        else:
            sequential_km += baseline_km
            sequential_co2 += baseline_co2
        for stop in solution.detalles:
            if stop.tipo_parada == TipoParada.DEPOT_START or stop.vehiculo is None:
                continue
            fuel, efficiency = vehicle_factors(solution, stop.vehiculo)
            energy = estimate_energy(fuel, stop.distancia_tramo_km, getattr(stop,'co2_tramo_g',0.), efficiency)
            if energy.gallons is not None:
                gallons += energy.gallons
                has_consumption = True
            if energy.kwh is not None:
                kwh += energy.kwh
                has_electricity = True
            cost += energy.energy_pen + energy.maintenance_pen
    factor = get_settings().quinual_kg_co2_per_year
    valid_factor = factor if factor > 0 else None
    return IndicatorSummary(
        fecha_inicio=start, fecha_fin=end, rutas=len(items), distancia_total_km=distance,
        duracion_total_min=duration, consumo_estimado_gal=gallons if has_consumption else None,
        co2_estimado_kg=emitted, co2_evitado_kg=avoided,
        arboles_quinual_eq=quinual_equivalent(avoided) if valid_factor is not None else None,
        quinual_kg_co2_por_ano=valid_factor,
        linea_base_secuencial_km=sequential_km if comparable else None,
        linea_base_secuencial_co2_kg=sequential_co2 if comparable else None,
        ahorro_distancia_pct_vs_secuencial=_saving(sequential_km if comparable else None, distance),
        ahorro_co2_pct_vs_secuencial=_saving(sequential_co2 if comparable else None, emitted),
        consumo_estimado_kwh=kwh if has_electricity else None,
        costo_estimado_pen=cost if items else None,
        referencia_comparable=all((item.metadatos_ga or {}).get('referencia_comparable',True) for item in items),
    )
