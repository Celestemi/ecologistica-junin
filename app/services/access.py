"""Ingreso, bloqueo por intentos y registro en la bitácora."""

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.identity import Bitacora, Usuario
from app.services.passwords import verify_password

LIMA = ZoneInfo("America/Lima")

INGRESO_CORRECTO = "ingreso_correcto"
INGRESO_FALLIDO = "ingreso_fallido"
INGRESO_BLOQUEADO = "ingreso_bloqueado"
OPTIMIZAR_RUTAS = "optimizar_rutas"
OPTIMIZAR_DENEGADO = "optimizar_denegado"
REPORTE_DENEGADO = "reporte_denegado"
IMPORTAR_PEDIDOS = "importar_pedidos"
FLOTA_ACTUALIZADA = "flota_actualizada"

WRONG_CREDENTIALS = "Correo o contraseña incorrectos."


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _clock(moment: datetime) -> str:
    return moment.astimezone(LIMA).strftime("%H:%M")


async def record(
    session: AsyncSession,
    *,
    correo: str,
    accion: str,
    detalle: str | None = None,
    usuario: Usuario | None = None,
) -> None:
    session.add(
        Bitacora(
            usuario_id=usuario.id if usuario is not None else None,
            correo=correo,
            accion=accion,
            detalle=detalle,
        )
    )


async def authenticate(session: AsyncSession, correo: str, clave: str) -> Usuario:
    """Valida la clave. Al tercer fallo bloquea la cuenta 15 minutos (RN-001)."""
    settings = get_settings()
    user = await session.scalar(select(Usuario).where(Usuario.correo == correo))
    now = _now()

    if user is None or not user.activo:
        verify_password(clave, _placeholder_hash())
        await record(
            session,
            correo=correo,
            accion=INGRESO_FALLIDO,
            detalle="Cuenta inexistente o inactiva." if user is None else "Cuenta inactiva.",
            usuario=user,
        )
        await session.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=WRONG_CREDENTIALS)

    if user.bloqueado_hasta is not None and user.bloqueado_hasta > now:
        await record(
            session,
            correo=correo,
            accion=INGRESO_BLOQUEADO,
            detalle=f"Intento durante el bloqueo vigente hasta las {_clock(user.bloqueado_hasta)}.",
            usuario=user,
        )
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"La cuenta está bloqueada hasta las {_clock(user.bloqueado_hasta)}.",
        )

    if user.bloqueado_hasta is not None and user.bloqueado_hasta <= now:
        user.bloqueado_hasta = None
        user.intentos_fallidos = 0

    if not verify_password(clave, user.clave_hash):
        user.intentos_fallidos += 1
        if user.intentos_fallidos >= settings.auth_max_attempts:
            user.bloqueado_hasta = now + timedelta(minutes=settings.auth_lock_minutes)
            user.intentos_fallidos = 0
            await record(
                session,
                correo=correo,
                accion=INGRESO_BLOQUEADO,
                detalle=f"Tercer intento fallido. Bloqueo hasta las {_clock(user.bloqueado_hasta)}.",
                usuario=user,
            )
            await session.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Demasiados intentos. La cuenta queda bloqueada 15 minutos.",
            )
        attempt = user.intentos_fallidos
        await record(
            session,
            correo=correo,
            accion=INGRESO_FALLIDO,
            detalle=f"Intento {attempt} de {settings.auth_max_attempts}.",
            usuario=user,
        )
        await session.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=WRONG_CREDENTIALS)

    user.intentos_fallidos = 0
    user.bloqueado_hasta = None
    await record(session, correo=correo, accion=INGRESO_CORRECTO, detalle="Ingreso aceptado.", usuario=user)
    await session.commit()
    return user


_placeholder: str | None = None


def _placeholder_hash() -> str:
    """Hash real para que un correo inexistente tarde lo mismo que uno válido."""
    global _placeholder
    if _placeholder is None:
        from app.services.passwords import hash_password

        _placeholder = hash_password("cuenta-inexistente")
    return _placeholder
