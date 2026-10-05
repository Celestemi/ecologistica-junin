"""Emisiones de CO2 ajustadas por altitud y pendiente en el valle del Mantaro.

La fórmula del tramo es:

    gramos = km * emisión_base_g_km
             * factor_altitud
             * (1 + factor_penalizacion_pendiente * max(pendiente_%, 0))

`factor_altitud` vale 1.0 a 3 200 m s.n.m. y llega a 1.08 a 3 450 m para
motores de combustión. El eléctrico solo asume una fracción de ese recargo.
El coeficiente es conservador y debe calibrarse con consumo local.
"""

from app.core.config import get_settings
from app.models.enums import TipoCombustible

_COMBUSTION = {
    TipoCombustible.DIESEL,
    TipoCombustible.GASOLINE,
    TipoCombustible.GLP,
}


def altitude_emission_factor(altitude_m: float, fuel: TipoCombustible) -> float:
    """Devuelve el multiplicador de emisión según la altitud del tramo."""
    settings = get_settings()
    span = settings.altitude_max_m - settings.altitude_min_m
    if span <= 0:
        return 1.0
    clamped = min(max(altitude_m, settings.altitude_min_m), settings.altitude_max_m)
    position = (clamped - settings.altitude_min_m) / span
    uplift = settings.altitude_emission_uplift * position
    if fuel not in _COMBUSTION:
        uplift *= settings.electric_altitude_share
    return 1.0 + uplift


def leg_co2_grams(
    *,
    distance_km: float,
    base_g_per_km: float,
    slope_penalty: float,
    slope_pct: float,
    altitude_m: float,
    fuel: TipoCombustible,
) -> float:
    """Calcula los gramos de CO2 de un tramo. La pendiente negativa no bonifica."""
    if distance_km < 0 or base_g_per_km < 0 or slope_penalty < 0:
        raise ValueError("Distancia, emisión base y penalización deben ser no negativas.")
    grade = max(slope_pct, 0.0)
    return (
        distance_km
        * base_g_per_km
        * altitude_emission_factor(altitude_m, fuel)
        * (1.0 + slope_penalty * grade)
    )


def quinual_equivalent(co2_avoided_kg: float) -> float:
    """Convierte CO2 evitado (kg) a árboles Quinual equivalentes por año."""
    if co2_avoided_kg < 0:
        raise ValueError("El CO2 evitado no puede ser negativo.")
    per_tree = get_settings().quinual_kg_co2_per_year
    if per_tree <= 0:
        raise ValueError("El factor Quinual debe ser positivo.")
    return co2_avoided_kg / per_tree
