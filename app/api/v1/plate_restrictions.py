"""Administración de restricciones vehiculares por placa (US-002 / RF-002)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles
from app.core.database import get_db
from app.models.enums import RolUsuario
from app.models.identity import Usuario
from app.models.restrictions import HistorialRestriccionPlaca, RestriccionPlacaRegla
from app.schemas.restrictions import (
    HistorialRestriccionPlacaRead,
    RestriccionPlacaConfigRead,
    RestriccionPlacaConfigUpdate,
    RestriccionPlacaReglaWrite,
    advertencia_config,
)
from app.services.access import record
from app.services.plate_restriction import (
    MENSAJE_ACTIVAR_SIN_VALIDAR,
    append_history,
    load_config,
)

router = APIRouter(prefix="/api/v1/restricciones-placa", tags=["restricciones-placa"])

DESK = (RolUsuario.ADMIN, RolUsuario.OPERADOR, RolUsuario.GERENTE, RolUsuario.AUDITOR)
WRITERS = (RolUsuario.ADMIN, RolUsuario.OPERADOR)
DENY_READ = "Tu rol no consulta la configuración de restricciones por placa."
DENY_WRITE = "Tu rol no puede modificar restricciones por placa."
DENY_VALIDATE = "Solo el administrador puede registrar validación normativa."

RESTRICCION_ACTUALIZADA = "restriccion_placa_actualizada"


def _to_read(config) -> RestriccionPlacaConfigRead:
    return RestriccionPlacaConfigRead(
        id=config.id,
        ambito=config.ambito,
        etiqueta_validacion=config.etiqueta_validacion,
        validada_normativamente=config.validada_normativamente,
        activa=config.activa,
        referencia_normativa=config.referencia_normativa,
        reglas=config.reglas,
        advertencia=advertencia_config(config.validada_normativamente, config.activa),
    )


@router.get(
    "",
    response_model=RestriccionPlacaConfigRead,
    summary="Configuración de restricción por placa",
)
async def read_plate_restrictions(
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_roles(*DESK, accion="restriccion_placa_denegada", detail=DENY_READ)),
) -> RestriccionPlacaConfigRead:
    config = await load_config(session)
    return _to_read(config)


@router.get(
    "/historial",
    response_model=list[HistorialRestriccionPlacaRead],
    summary="Historial de cambios en restricciones por placa",
)
async def plate_restriction_history(
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_roles(*DESK, accion="restriccion_placa_denegada", detail=DENY_READ)),
) -> list[HistorialRestriccionPlaca]:
    result = await session.scalars(
        select(HistorialRestriccionPlaca).order_by(HistorialRestriccionPlaca.id.desc()).limit(30)
    )
    return list(result.all())


@router.patch(
    "",
    response_model=RestriccionPlacaConfigRead,
    summary="Actualizar restricción por placa",
)
async def update_plate_restrictions(
    payload: RestriccionPlacaConfigUpdate,
    session: AsyncSession = Depends(get_db),
    actor: Usuario = Depends(require_roles(*WRITERS, accion="restriccion_placa_denegada", detail=DENY_WRITE)),
) -> RestriccionPlacaConfigRead:
    config = await load_config(session)
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay cambios para guardar.")

    reglas_payload = changes.pop("reglas", None)
    if "validada_normativamente" in changes and actor.rol != RolUsuario.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=DENY_VALIDATE)

    next_validada = changes.get("validada_normativamente", config.validada_normativamente)
    next_activa = changes.get("activa", config.activa)
    if next_activa and not next_validada:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MENSAJE_ACTIVAR_SIN_VALIDAR)

    if changes.get("validada_normativamente") is False and config.activa:
        changes["activa"] = False
        next_activa = False

    notes: list[str] = []
    for field, value in changes.items():
        if field == "validada_normativamente" and value != config.validada_normativamente:
            notes.append(f"validación normativa → {'confirmada' if value else 'pendiente'}")
        elif field == "activa" and value != config.activa:
            notes.append(f"regla → {'activa' if value else 'inactiva'}")
        elif field == "ambito" and value != config.ambito:
            notes.append(f"ámbito → {value}")
        elif field == "referencia_normativa":
            notes.append("referencia normativa actualizada")
        setattr(config, field, value)

    if reglas_payload is not None:
        _replace_rules(config, reglas_payload)
        notes.append(f"{len(reglas_payload)} regla(s) por dígito")

    if not notes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay cambios para guardar.")

    detail = "; ".join(notes)
    await append_history(session, correo=actor.correo, detalle=detail)
    await record(
        session,
        correo=actor.correo,
        accion=RESTRICCION_ACTUALIZADA,
        detalle=detail,
        usuario=actor,
    )
    await session.commit()
    await session.refresh(config)
    return _to_read(config)


def _replace_rules(config, reglas: list[dict] | list[RestriccionPlacaReglaWrite]) -> None:
    digits = [item["ultimo_digito"] if isinstance(item, dict) else item.ultimo_digito for item in reglas]
    if len(set(digits)) != len(digits):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cada último dígito solo puede tener una regla.",
        )
    config.reglas.clear()
    for item in reglas:
        if isinstance(item, dict):
            config.reglas.append(
                RestriccionPlacaRegla(
                    ultimo_digito=item["ultimo_digito"],
                    dias_semana=item["dias_semana"],
                )
            )
        else:
            config.reglas.append(
                RestriccionPlacaRegla(
                    ultimo_digito=item.ultimo_digito,
                    dias_semana=item.dias_semana,
                )
            )
