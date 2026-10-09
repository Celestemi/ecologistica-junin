"""Contratos de ingreso y de la bitácora."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import RolUsuario


class LoginRequest(BaseModel):
    correo: str = Field(min_length=5, max_length=160)
    clave: str = Field(min_length=8, max_length=128)

    @field_validator("correo")
    @classmethod
    def normalize_correo(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if "@" not in cleaned or " " in cleaned or cleaned.startswith("@") or cleaned.endswith("@"):
            raise ValueError("El correo no es válido.")
        return cleaned


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: str
    rol: RolUsuario


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioRead


class BitacoraRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    correo: str
    accion: str
    detalle: str | None
    creado_en: datetime
