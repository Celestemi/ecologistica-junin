"""Aplicación de RN-002 solo cuando la regla está validada y activa."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.domain import Vehiculo
from app.models.restrictions import (
    AMBITO_PROYECTO,
    ETIQUETA_PENDIENTE,
    HistorialRestriccionPlaca,
    RestriccionPlacaConfig,
    RestriccionPlacaRegla,
)

MENSAJE_ACTIVAR_SIN_VALIDAR = (
    "La restricción vehicular por placa requiere validación normativa previa "
    f"({ETIQUETA_PENDIENTE}). No se puede activar hasta confirmación legal para "
    f"{AMBITO_PROYECTO}."
)

_DIA_NOMBRE = {
    1: "lunes",
    2: "martes",
    3: "miércoles",
    4: "jueves",
    5: "viernes",
    6: "sábado",
    7: "domingo",
}


@dataclass(frozen=True)
class ExclusionPlaca:
    placa: str
    ultimo_digito: int | None
    motivo: str


def ultimo_digito_placa(placa: str) -> int | None:
    digits = [char for char in placa if char.isdigit()]
    if not digits:
        return None
    return int(digits[-1])


def regla_aplicable(config: RestriccionPlacaConfig) -> bool:
    return bool(config.validada_normativamente and config.activa)


async def load_config(session: AsyncSession) -> RestriccionPlacaConfig:
    row = await session.scalar(
        select(RestriccionPlacaConfig)
        .options(selectinload(RestriccionPlacaConfig.reglas))
        .order_by(RestriccionPlacaConfig.id)
        .limit(1)
    )
    if row is not None:
        return row
    config = RestriccionPlacaConfig(
        ambito=AMBITO_PROYECTO,
        etiqueta_validacion=ETIQUETA_PENDIENTE,
        validada_normativamente=False,
        activa=False,
    )
    session.add(config)
    await session.flush()
    return config


def assert_can_activate(config: RestriccionPlacaConfig, activa: bool) -> None:
    if activa and not config.validada_normativamente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=MENSAJE_ACTIVAR_SIN_VALIDAR,
        )


def vehicle_excluded(
    placa: str,
    planning_day: date,
    rules: list[RestriccionPlacaRegla],
) -> ExclusionPlaca | None:
    digit = ultimo_digito_placa(placa)
    if digit is None:
        return None
    weekday = planning_day.isoweekday()
    for rule in rules:
        if rule.ultimo_digito != digit:
            continue
        if weekday not in rule.dias_semana:
            continue
        day_label = _DIA_NOMBRE.get(weekday, str(weekday))
        return ExclusionPlaca(
            placa=placa,
            ultimo_digito=digit,
            motivo=(
                "Restricción de circulación por placa (RN-002): "
                f"último dígito {digit} sin circulación los {day_label} "
                f"({planning_day.isoformat()})."
            ),
        )
    return None


def filter_vehicles_for_planning(
    vehicles: list[Vehiculo],
    planning_day: date,
    config: RestriccionPlacaConfig,
) -> tuple[list[Vehiculo], list[ExclusionPlaca]]:
    if not regla_aplicable(config):
        return vehicles, []
    allowed: list[Vehiculo] = []
    excluded: list[ExclusionPlaca] = []
    for vehicle in vehicles:
        hit = vehicle_excluded(vehicle.placa, planning_day, config.reglas)
        if hit is None:
            allowed.append(vehicle)
        else:
            excluded.append(hit)
    return allowed, excluded


async def append_history(session: AsyncSession, *, correo: str, detalle: str) -> None:
    session.add(HistorialRestriccionPlaca(correo=correo, detalle=detalle))
