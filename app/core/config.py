"""Parámetros de entorno y constantes topográficas de Huancayo."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración del MVP. Los valores locales alimentan el cálculo de CO2."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = (
        "postgresql+asyncpg://ecologistica:ecologistica@localhost:5433/ecologistica"
    )
    app_name: str = "EcoLogística Huancayo"
    app_debug: bool = False

    # Plaza Constitución, centro de Huancayo (WGS84).
    huancayo_base_lat: float = -12.06513
    huancayo_base_lon: float = -75.20486

    # Banda operativa del valle y laderas inmediatas, en metros sobre el nivel del mar.
    altitude_min_m: float = 3200.0
    altitude_max_m: float = 3450.0
    # Incremento de emisión por combustión incompleta entre el piso y el techo de la banda.
    altitude_emission_uplift: float = 0.08
    # Fracción del recargo de altitud que se aplica a vehículos eléctricos.
    electric_altitude_share: float = 0.25

    # Un Quinual abonado en la zona andina fija unos 12 kg de CO2 al año.
    quinual_kg_co2_per_year: float = 12.0

    # SRID de almacenamiento. Las distancias métricas del optimizador usarán UTM 18S (EPSG:32718).
    storage_srid: int = 4326


@lru_cache
def get_settings() -> Settings:
    return Settings()
