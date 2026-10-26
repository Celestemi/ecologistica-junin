"""Conexión asíncrona a PostgreSQL 15 con PostGIS.

El motor usa el dialecto `postgresql+asyncpg`. Las columnas espaciales se
declaran con GeoAlchemy2 y se persisten en SRID 4326 para Leaflet. El cálculo
métrico (distancia y pendiente) debe proyectar a UTM zona 18S, EPSG:32718.
"""

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import get_settings

settings = get_settings()

# pytest y TestClient (WebSocket) no comparten el mismo event loop.
# Un pool reutiliza conexiones asyncpg ligadas al loop de pytest y deja
# tareas pendientes o MissingGreenlet en el portal de Starlette.
_engine_kwargs: dict[str, object] = {
    "echo": settings.app_debug,
    "pool_pre_ping": True,
}
if os.environ.get("ECOLOGISTICA_PYTEST") == "1":
    _engine_kwargs["poolclass"] = NullPool

engine = create_async_engine(settings.database_url, **_engine_kwargs)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base declarativa de los modelos GeoAlchemy2."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia de FastAPI. El llamador confirma la transacción."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
