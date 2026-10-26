"""Esquemas API para restricciones por placa (US-002)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.restrictions import AMBITO_PROYECTO, ETIQUETA_PENDIENTE


class RestriccionPlacaReglaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ultimo_digito: int
    dias_semana: list[int]


class RestriccionPlacaReglaWrite(BaseModel):
    ultimo_digito: int = Field(ge=0, le=9)
    dias_semana: list[int] = Field(min_length=1)

    @field_validator("dias_semana")
    @classmethod
    def weekdays_in_range(cls, value: list[int]) -> list[int]:
        cleaned = sorted(set(value))
        if any(day < 1 or day > 7 for day in cleaned):
            raise ValueError("Los días deben estar entre 1 (lunes) y 7 (domingo).")
        return cleaned


class RestriccionPlacaConfigRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ambito: str
    etiqueta_validacion: str
    validada_normativamente: bool
    activa: bool
    referencia_normativa: str | None
    reglas: list[RestriccionPlacaReglaRead]
    advertencia: str


class RestriccionPlacaConfigUpdate(BaseModel):
    ambito: str | None = Field(default=None, min_length=3, max_length=120)
    activa: bool | None = None
    referencia_normativa: str | None = Field(default=None, max_length=240)
    validada_normativamente: bool | None = None
    reglas: list[RestriccionPlacaReglaWrite] | None = None


class HistorialRestriccionPlacaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    correo: str
    detalle: str
    creado_en: datetime


class ExclusionPlacaRead(BaseModel):
    placa: str
    ultimo_digito: int | None
    motivo: str


def advertencia_config(config_validada: bool, config_activa: bool) -> str:
    if not config_validada:
        return (
            f"{ETIQUETA_PENDIENTE} La regla RN-002 permanece desactivada hasta "
            f"confirmación normativa para {AMBITO_PROYECTO}. "
            "La parametrización técnica está disponible; su aplicación en rutas "
            "requiere validación legal."
        )
    if not config_activa:
        return (
            "Regla validada normativamente pero desactivada. "
            "La planificación considera todos los vehículos activos."
        )
    return (
        "Regla validada y activa: la planificación excluye vehículos según "
        "último dígito de placa y días configurados."
    )
