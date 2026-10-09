"""Parámetros de entorno y constantes topográficas de Huancayo."""

from functools import lru_cache
from urllib.parse import quote

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración del MVP. Los valores locales alimentan el cálculo de CO2."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_host: str = "localhost"
    db_port: int = 5433
    db_user: str = "ecologistica"
    db_password: str = "ecologistica"
    db_name: str = "ecologistica"
    database_url: str = ""
    secret_key: str = "cambia-esta-clave-en-produccion-local"
    auth_bcrypt_rounds: int = 12
    auth_token_hours: int = 12
    auth_max_attempts: int = 3
    auth_lock_minutes: int = 15
    cors_origins: str = (
        "http://localhost,http://127.0.0.1,"
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:8080,http://127.0.0.1:8080"
    )
    app_name: str = "EcoLogística Huancayo"
    app_debug: bool = False

    @model_validator(mode="after")
    def fill_database_url(self) -> "Settings":
        """Arma la URL async si el entorno solo trae las piezas DB_*."""
        if not self.database_url:
            password = quote(self.db_password, safe="")
            self.database_url = (
                f"postgresql+asyncpg://{quote(self.db_user, safe='')}:"
                f"{password}@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        return self

    def allowed_origins(self) -> list[str]:
        """Orígenes CORS separados por coma en CORS_ORIGINS."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

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
