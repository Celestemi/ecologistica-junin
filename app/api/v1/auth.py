"""Ingreso y consulta de la bitácora."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.models.enums import RolUsuario
from app.models.identity import Bitacora, Usuario
from app.schemas.auth import BitacoraRead, LoginRequest, LoginResponse, UsuarioRead
from app.services.access import authenticate
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


@router.get(
    "/bitacora",
    response_model=list[BitacoraRead],
    summary="Leer la bitácora",
    responses={403: {"description": "El rol no puede leer la bitácora."}},
)
async def list_audit(
    limite: int = 50,
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
    capped = min(max(limite, 1), 200)
    result = await session.scalars(select(Bitacora).order_by(Bitacora.id.desc()).limit(capped))
    return list(result.all())
