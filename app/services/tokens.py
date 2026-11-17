"""JWT de sesión. El cliente lo manda en Authorization: Bearer."""

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
from uuid import uuid4

import jwt
from jwt.exceptions import PyJWTError

from app.core.config import get_settings
from app.models.identity import Bitacora, Usuario
from sqlalchemy import select


def session_fingerprint(user: Usuario) -> str:
    source = f'{user.clave_hash}:{user.rol.value}:{user.activo}'.encode()
    return hmac.new(get_settings().secret_key.encode(), source, hashlib.sha256).hexdigest()


def create_access_token(user: Usuario) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "rol": user.rol.value,
        "correo": user.correo,
        "iat": now,
        "exp": now + timedelta(seconds=settings.token_lifetime_seconds()),
        "jti": uuid4().hex,
        "sv": session_fingerprint(user),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def read_access_token(token: str) -> dict[str, object] | None:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"],
                             options={'require': ['sub', 'iat', 'exp', 'jti', 'sv']})
    except PyJWTError:
        return None
    if not isinstance(payload, dict) or "sub" not in payload:
        return None
    return payload


async def session_is_current(session, payload, user: Usuario) -> bool:
    if not user.activo or payload.get('rol') != user.rol.value:
        return False
    if not hmac.compare_digest(str(payload.get('sv', '')), session_fingerprint(user)):
        return False
    if user.bloqueado_hasta is not None and user.bloqueado_hasta > datetime.now(timezone.utc):
        return False
    revoked = await session.scalar(select(Bitacora.id).where(
        Bitacora.usuario_id == user.id, Bitacora.accion == 'sesion_revocada',
        Bitacora.detalle == f"jti:{payload.get('jti')}",
    ).limit(1))
    return revoked is None
