"""EN-001 / RNF-001 — SLA ≤ 45 s para 150 pedidos × 15 vehículos."""

from __future__ import annotations

import json
import os
import platform
import statistics
import sys
from time import perf_counter

import pytest

from app.core.config import get_settings
from app.services.genetic_solver import solve_vrptw
from app.services.optimizer_benchmark import (
    overloaded_orders,
    synthetic_depot,
    synthetic_orders,
    synthetic_vehicles,
    tight_window_orders,
)
from app.services.optimizer_runtime import optimization_time_budget_seconds, resolve_ga_parameters
from app.services.route_constraints import precheck_fleet_capacity

SLA_SECONDS = 45.0
BENCHMARK_SEED = 901_001
REPEATS = int(os.environ.get("EN001_REPEATS", "3"))


def _assigned_count(solution) -> int:
    return sum(
        1
        for itinerary in solution.itineraries
        for stop in itinerary.stops
        if stop.order_id is not None
    )


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_precheck_infactible_overload() -> None:
    orders = overloaded_orders(150, seed=BENCHMARK_SEED)
    vehicles = synthetic_vehicles(15, seed=BENCHMARK_SEED)
    check = precheck_fleet_capacity(orders, vehicles)  # type: ignore[arg-type]
    assert check.feasible is False
    assert check.excess_kg > 0


def test_resolve_ga_parameters_scales_for_150() -> None:
    generations, population = resolve_ga_parameters(150, 15)
    assert generations <= get_settings().optimizer_max_generations
    assert population <= get_settings().optimizer_max_population
    assert generations <= 40
    assert population <= 30


@pytest.mark.slow
def test_solver_sla_150x15_reproducible() -> None:
    """Escenario RNF-001: solver (GA + baselines) dentro del presupuesto configurado."""
    orders = synthetic_orders(150, seed=BENCHMARK_SEED)
    vehicles = synthetic_vehicles(15, seed=BENCHMARK_SEED)
    depot = synthetic_depot()
    generations, population = resolve_ga_parameters(150, 15)
    budget = optimization_time_budget_seconds()
    solution = solve_vrptw(
        orders,
        vehicles,
        depot,
        generations=generations,
        population_size=population,
        seed=BENCHMARK_SEED,
        time_budget_seconds=budget,
    )
    assert solution.solver_elapsed_seconds <= budget + 0.05
    assert solution.generations_executed >= 1
    assert _assigned_count(solution) > 0


@pytest.mark.slow
def test_en001_benchmark_report_json(tmp_path_factory) -> None:
    """Genera métricas para REPORTE_RENDIMIENTO_EN_001.md (stdout si EN001_WRITE=1)."""
    scenarios = [
        ("feasible_150x15", 150, 15, synthetic_orders(150, seed=BENCHMARK_SEED)),
        ("medium_50x8", 50, 8, synthetic_orders(50, seed=BENCHMARK_SEED + 1)),
        ("small_5x2", 5, 2, synthetic_orders(5, seed=BENCHMARK_SEED + 2)),
        ("restricted_tight_windows", 30, 5, tight_window_orders(30, seed=BENCHMARK_SEED + 3)),
    ]
    depot = synthetic_depot()
    rows: list[dict[str, object]] = []
    for name, _n, vcount, orders in scenarios:
        vehicles = synthetic_vehicles(vcount, seed=BENCHMARK_SEED)
        generations, population = resolve_ga_parameters(len(orders), vcount)
        solver_times: list[float] = []
        feasible_flags: list[bool] = []
        last = None
        for repeat in range(REPEATS):
            started = perf_counter()
            last = solve_vrptw(
                orders,
                vehicles,
                depot,
                generations=generations,
                population_size=population,
                seed=BENCHMARK_SEED + repeat,
                time_budget_seconds=optimization_time_budget_seconds(),
            )
            solver_times.append(last.solver_elapsed_seconds)
            feasible_flags.append(last.feasible)
        assert last is not None
        rows.append(
            {
                "escenario": name,
                "pedidos": len(orders),
                "vehiculos": vcount,
                "generations_cap": generations,
                "population": population,
                "repeticiones": REPEATS,
                "solver_s_mean": statistics.mean(solver_times),
                "solver_s_median": statistics.median(solver_times),
                "solver_s_max": max(solver_times),
                "factible_ultima": last.feasible,
                "factible_ratio": sum(feasible_flags) / len(feasible_flags),
                "distancia_km": last.distance_km,
                "co2_kg": last.co2_kg,
                "asignados": _assigned_count(last),
                "no_asignados": len(last.unassigned_order_ids),
                "stop_reason": last.stop_reason,
                "cumple_sla_45s": max(solver_times) <= SLA_SECONDS,
            }
        )
    payload = {
        "python": sys.version,
        "platform": platform.platform(),
        "sla_seconds": SLA_SECONDS,
        "budget_config": optimization_time_budget_seconds(),
        "resultados": rows,
    }
    if os.environ.get("EN001_WRITE") == "1":
        path = os.path.join(os.getcwd(), "en001_benchmark_last.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
    assert payload["resultados"]
