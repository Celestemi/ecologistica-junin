"""Validaciones de arranque para entornos no demostrativos."""

from __future__ import annotations

from app.core.config import Settings

INSECURE_SECRET_KEYS = frozenset(
    {
        "cambia-esta-clave-en-produccion-local",
        "changeme",
        "secret",
        "dev",
    }
)


def validate_security_settings(settings: Settings) -> None:
    if settings.app_environment == "demo":
        return
    if settings.expose_api_docs:
        raise RuntimeError("EXPOSE_API_DOCS=true is not allowed outside the demo environment.")
    if settings.secret_key.strip().lower() in INSECURE_SECRET_KEYS:
        raise RuntimeError(
            "SECRET_KEY predeterminada no permitida fuera del entorno demo. "
            "Define una clave fuerte en el entorno."
        )
    if len(settings.secret_key) < 32:
        raise RuntimeError("SECRET_KEY demasiado corta para entornos no demo (mínimo 32 caracteres).")
    if settings.allow_demo_accounts:
        raise RuntimeError(
            "ALLOW_DEMO_ACCOUNTS=true no está permitido fuera del entorno demo."
        )
