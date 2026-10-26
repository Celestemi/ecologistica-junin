"""US-013 a US-015: consolidado puro, sin PostGIS."""
from datetime import date
from types import SimpleNamespace

from app.models.enums import TipoParada
from app.services.operational_indicators import summarize_indicators


def _solution(*, baseline_km: float | None = 15.0, baseline_co2: float | None = 4.0):
    metadata = {}
    if baseline_km is not None:
        metadata["linea_base_secuencial_km"] = baseline_km
    if baseline_co2 is not None:
        metadata["linea_base_secuencial_co2_kg"] = baseline_co2
    vehicle = SimpleNamespace(rendimiento_km_gal=10.0)
    return SimpleNamespace(
        distancia_total_km=10.0, duracion_total_min=42.0, co2_estimado_kg=2.0,
        co2_evitado_kg=1.0, metadatos_ga=metadata,
        detalles=[
            SimpleNamespace(tipo_parada=TipoParada.DEPOT_START, vehiculo=vehicle, distancia_tramo_km=0.0),
            SimpleNamespace(tipo_parada=TipoParada.DELIVERY, vehiculo=vehicle, distancia_tramo_km=10.0),
        ],
    )


def test_summary_uses_persisted_sequential_baseline_and_vehicle_efficiency() -> None:
    result = summarize_indicators([_solution()], date(2026, 10, 1), date(2026, 10, 1))
    assert result.consumo_estimado_gal == 1.0
    assert result.ahorro_distancia_pct_vs_secuencial == (15.0 - 10.0) / 15.0 * 100
    assert result.ahorro_co2_pct_vs_secuencial == 50.0
    assert result.arboles_quinual_eq == 1.0 / 12.0


def test_summary_does_not_invent_percentages_without_comparable_baseline() -> None:
    result = summarize_indicators([_solution(baseline_km=None)], date(2026, 10, 1), date(2026, 10, 1))
    assert result.linea_base_secuencial_km is None
    assert result.ahorro_distancia_pct_vs_secuencial is None
    assert result.ahorro_co2_pct_vs_secuencial is None
