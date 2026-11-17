"""Ingreso y consulta de la bitácora."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.models.enums import RolUsuario
from app.models.identity import Bitacora, Usuario
from app.schemas.auth import BitacoraRead, LoginRequest, LoginResponse, UsuarioRead
from app.services.access import authenticate, record
from app.services.tokens import create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["acceso"])


@router.post(
    "/ingresar",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    responses={401: {"description": "Credenciales inválidas o cuenta bloqueada."}},
)
async def login(body: LoginRequest, session: AsyncSession = Depends(get_db)) -> LoginResponse:
    user = await authenticate(session, body.correo, body.clave)
    return LoginResponse(access_token=create_access_token(user), usuario=UsuarioRead.model_validate(user))


@router.get("/yo", response_model=UsuarioRead, summary="Usuario de la sesión")
async def me(user: Usuario = Depends(get_current_user)) -> Usuario:
    return user


@router.post('/salir', status_code=204, summary='Revocar la sesión actual')
async def logout(session: AsyncSession = Depends(get_db), user: Usuario = Depends(get_current_user)) -> None:
    await session.scalar(select(Usuario).where(Usuario.id == user.id).with_for_update())
    payload = session.info['access_payload']
    await record(session, correo=user.correo, accion='sesion_revocada',
                 detalle=f"jti:{payload['jti']}", usuario=user)
    await session.commit()


@router.get(
    "/bitacora",
    response_model=list[BitacoraRead],
    summary="Leer la bitácora",
    responses={403: {"description": "El rol no puede leer la bitácora."}},
)
async def list_audit(
    limite: int = Query(50, ge=1, le=200),
    antes_de: int | None = Query(None, ge=1),
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(
        require_roles(
            RolUsuario.ADMIN,
            RolUsuario.AUDITOR,
            accion="bitacora_denegada",
            detail="Solo el auditor y el administrador pueden leer la bitácora.",
        )
    ),
) -> list[Bitacora]:
    filters = (Bitacora.id < antes_de,) if antes_de is not None else ()
    result = await session.scalars(
        select(Bitacora).where(*filters).order_by(Bitacora.id.desc()).limit(limite + 1)
    )
    return list(result.all())
