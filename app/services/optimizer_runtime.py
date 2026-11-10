"""Presupuesto de tiempo y parámetros del GA para RNF-001 / EN-001."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import BoundedSemaphore
from typing import Any, Callable

from app.core.config import get_settings
from app.services.genetic_solver import GENERATIONS, POPULATION_SIZE

_OPTIMIZER_EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="eco-optimizer")
_OPTIMIZER_SLOT = BoundedSemaphore(1)


class OptimizerBusyError(RuntimeError):
    """There is already one CPU-heavy route calculation in this worker."""


async def run_optimizer_in_worker(function: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Any:
    """Keep CPU and blocking routing calls off the ASGI event loop with one bounded slot."""
    if not _OPTIMIZER_SLOT.acquire(blocking=False):
        raise OptimizerBusyError("El optimizador está ocupado; vuelve a intentarlo en unos segundos.")
    loop = asyncio.get_running_loop()
    work = loop.run_in_executor(_OPTIMIZER_EXECUTOR, partial(function, *args, **kwargs))
    try:
        result = await asyncio.shield(work)
    except asyncio.CancelledError:
        work.add_done_callback(lambda _: _OPTIMIZER_SLOT.release())
        raise
    except BaseException:
        _OPTIMIZER_SLOT.release()
        raise
    _OPTIMIZER_SLOT.release()
    return result


def resolve_ga_parameters(order_count: int, vehicle_count: int) -> tuple[int, int]:
    """Escala generaciones/población según tamaño del lote (tope configurable)."""
    settings = get_settings()
    max_generations = max(1, settings.optimizer_max_generations)
    max_population = max(2, settings.optimizer_max_population)
    _ = vehicle_count
    if order_count <= 15:
        return min(GENERATIONS, max_generations), min(POPULATION_SIZE, max_population)
    if order_count <= 50:
        return min(60, max_generations), min(36, max_population)
    if order_count <= 100:
        return min(45, max_generations), min(30, max_population)
    return min(32, max_generations), min(24, max_population)


def optimization_time_budget_seconds() -> float:
    return max(1.0, get_settings().optimizer_time_budget_seconds)


def stagnation_generations_limit() -> int:
    return max(1, get_settings().optimizer_stagnation_generations)
