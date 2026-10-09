"""Hash de contraseñas con bcrypt. La clave en claro no se persiste."""

import bcrypt

from app.core.config import get_settings


def hash_password(plain: str) -> str:
    rounds = get_settings().auth_bcrypt_rounds
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=rounds))
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False
