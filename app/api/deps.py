"""Dependencias de sesión y de rol."""

import logging
from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.enums import RolUsuario
from app.models.identity import Usuario
from app.services.access import record
from app.services.rbac import DENY_ANON
from app.services.tokens import read_access_token

bearer_scheme = HTTPBearer(auto_error=False)
logger = logging.getLogger("ecologistica.security")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db),
) -> Usuario:
    if credentials is None or credentials.scheme.lower() != "bearer":
        logger.warning("security_event=authentication_rejected reason=missing_or_wrong_scheme")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=DENY_ANON,
        )
    payload = read_access_token(credentials.credentials)
    if payload is None:
        logger.warning("security_event=authentication_rejected reason=invalid_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión no es válida. Vuelve a ingresar.",
        )
    try:
        user_id = int(str(payload["sub"]))
    except (TypeError, ValueError):
        logger.warning("security_event=authentication_rejected reason=invalid_subject")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión no es válida. Vuelve a ingresar.",
        ) from None
    user = await session.scalar(select(Usuario).where(Usuario.id == user_id))
    if user is None or not user.activo:
        logger.warning("security_event=authentication_rejected reason=inactive_or_unknown_user")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión no es válida. Vuelve a ingresar.",
        )
    return user


def require_roles(*roles: RolUsuario, accion: str, detail: str) -> Callable[..., object]:
    """Deja pasar los roles indicados y anota en la bitácora el rechazo."""

    async def dependency(
        session: AsyncSession = Depends(get_db),
        user: Usuario = Depends(get_current_user),
    ) -> Usuario:
        if user.rol in roles:
            return user
        logger.warning("security_event=authorization_denied action=%s user_id=%s", accion, user.id)
        await record(
            session,
            correo=user.correo,
            accion=accion,
            detalle=detail,
            usuario=user,
        )
        await session.commit()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

    return dependency
