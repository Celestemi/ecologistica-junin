"""JWT de sesión. El cliente lo manda en Authorization: Bearer."""

from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import PyJWTError

from app.core.config import get_settings
from app.models.identity import Usuario


def create_access_token(user: Usuario) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "rol": user.rol.value,
        "correo": user.correo,
        "iat": now,
        "exp": now + timedelta(hours=settings.auth_token_hours),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def read_access_token(token: str) -> dict[str, object] | None:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except PyJWTError:
        return None
    if not isinstance(payload, dict) or "sub" not in payload:
        return None
    return payload
