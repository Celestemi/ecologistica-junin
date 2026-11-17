"""AF-09: oráculo compartido de estimaciones, NO tarifas ni gasto real/EVM.

Supuestos ya presentes en pdf_generator antes de la corrección; versión explícita.
La electricidad se infiere del CO2 estimado: no se afirma medición de energía.
"""

from dataclasses import dataclass
from app.models.enums import TipoCombustible

FACTOR_VERSION = 'supuestos-pdf-legacy-v1'
LITERS_PER_GALLON = 3.785411784
GRAMS_PER_LITER = {TipoCombustible.DIESEL:2680.0, TipoCombustible.GASOLINE:2310.0, TipoCombustible.GLP:1660.0}
PEN_PER_LITER = {TipoCombustible.DIESEL:4.90, TipoCombustible.GASOLINE:5.40, TipoCombustible.GLP:2.40}
GRID_KG_CO2_PER_KWH = .150
PEN_PER_KWH = .70


@dataclass(frozen=True)
class EnergyEstimate:
    gallons: float | None
    kwh: float | None
    energy_pen: float
    maintenance_pen: float


def estimate_energy(fuel, km: float, co2_g: float, efficiency_km_gal: float | None = None) -> EnergyEstimate:
    kind = TipoCombustible(fuel)
    distance, grams = max(0., km), max(0., co2_g)
    if kind == TipoCombustible.ELECTRIC:
        kwh = grams / 1000. / GRID_KG_CO2_PER_KWH
        return EnergyEstimate(None, kwh, kwh * PEN_PER_KWH, distance * .15)
    gallons = distance / efficiency_km_gal if efficiency_km_gal and efficiency_km_gal > 0 else grams / GRAMS_PER_LITER[kind] / LITERS_PER_GALLON
    return EnergyEstimate(gallons, None, gallons * LITERS_PER_GALLON * PEN_PER_LITER[kind], distance * .35)


def vehicle_factors(plan, vehicle):
    """Usa snapshot congelado si existe; legado sin snapshot queda identificable."""
    data = (plan.metadatos_ga or {}).get('factores_vehiculos', {}).get(str(vehicle.id), {}) if hasattr(vehicle, 'id') else {}
    return (data.get('tipo_combustible', getattr(vehicle,'tipo_combustible',TipoCombustible.DIESEL)),
            data.get('rendimiento_km_gal', getattr(vehicle,'rendimiento_km_gal',None)))
