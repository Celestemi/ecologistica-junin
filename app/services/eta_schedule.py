"""Cálculo de ETA, espera en ventana y clasificación RF-009 / RN-005."""

from __future__ import annotations

from datetime import datetime, timedelta

from app.models.enums import EstadoEta, TipoParada

LATE_EPSILON_MIN = 0.05


def wait_minutes_before_window(arrival: datetime, window_start: datetime) -> float:
    if arrival >= window_start:
        return 0.0
    return max(0.0, (window_start - arrival).total_seconds() / 60.0)


def late_minutes_after_window(arrival: datetime, window_end: datetime) -> float:
    if arrival <= window_end:
        return 0.0
    late = (arrival - window_end).total_seconds() / 60.0
    return late if late >= LATE_EPSILON_MIN else 0.0


def classify_delivery_arrival(
    arrival: datetime,
    window_start: datetime,
    window_end: datetime,
    *,
    matrix_available: bool,
) -> tuple[EstadoEta, float, float]:
    if not matrix_available:
        return EstadoEta.REVISION_MATRIZ, 0.0, 0.0
    late = late_minutes_after_window(arrival, window_end)
    if late > 0:
        return EstadoEta.FUERA_VENTANA, 0.0, late
    wait = wait_minutes_before_window(arrival, window_start)
    if wait >= LATE_EPSILON_MIN:
        return EstadoEta.EN_ESPERA, wait, 0.0
    return EstadoEta.EN_VENTANA, 0.0, 0.0


def service_start_after_arrival(
    arrival: datetime,
    window_start: datetime,
    service_minutes: float,
) -> datetime:
    start = window_start if arrival < window_start else arrival
    return start + timedelta(minutes=service_minutes)


def delivery_sequence_index(stops: tuple[object, ...], current_sequence: int) -> int | None:
    """Número de visita de entrega 1…N (depósito excluido)."""
    count = 0
    for stop in stops:
        if getattr(stop, "sequence", -1) >= current_sequence:
            break
        if getattr(stop, "stop_type", None) == TipoParada.DELIVERY:
            count += 1
    if any(
        getattr(s, "sequence", None) == current_sequence
        and getattr(s, "stop_type", None) == TipoParada.DELIVERY
        for s in stops
    ):
        return count + 1
    return None
