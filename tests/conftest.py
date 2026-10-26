"""Base de pruebas aparte de la semilla de desarrollo.

`DATABASE_URL` apunta a `ecologistica_test` antes de importar la aplicación,
tanto en el host (`localhost:5433`) como dentro del contenedor (`db:5432`).
"""

from __future__ import annotations

import os
from urllib.parse import urlsplit, urlunsplit

import asyncpg
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

_SOURCE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://ecologistica:ecologistica@localhost:5433/ecologistica",
)


def _with_database(url: str, database: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, f"/{database}", "", ""))


_TEST_DATABASE = "ecologistica_test"
os.environ["DATABASE_URL"] = _with_database(_SOURCE_URL, _TEST_DATABASE)
os.environ["ECOLOGISTICA_PYTEST"] = "1"


def _assert_test_database_isolated() -> None:
    """Evita TRUNCATE o semillas destructivas fuera de la BD de prueba."""
    url = os.environ.get("DATABASE_URL", "")
    parts = urlsplit(url)
    database = (parts.path or "").lstrip("/").split("?")[0]
    if database != _TEST_DATABASE:
        raise RuntimeError(
            "Abortando pruebas: DATABASE_URL debe apuntar exclusivamente a "
            f"'{_TEST_DATABASE}', no a '{database or '(vacío)'}'."
        )


_assert_test_database_isolated()
os.environ["AUTH_BCRYPT_ROUNDS"] = "4"
os.environ["APP_ENVIRONMENT"] = "demo"
os.environ["ALLOW_DEMO_ACCOUNTS"] = "true"

from app.core.database import engine  # noqa: E402
from app.db.init_db import init_database  # noqa: E402
from app.main import app  # noqa: E402


def _asyncpg_dsn(database: str) -> str:
    parts = urlsplit(_with_database(_SOURCE_URL, database))
    return urlunsplit(("postgresql", parts.netloc, parts.path, "", ""))


async def _ensure_test_database() -> None:
    connection = await asyncpg.connect(_asyncpg_dsn("postgres"))
    try:
        exists = await connection.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            "ecologistica_test",
        )
        if exists is None:
            await connection.execute("CREATE DATABASE ecologistica_test")
    finally:
        await connection.close()


async def _reset_seed() -> None:
    _assert_test_database_isolated()
    async with engine.begin() as connection:
        await connection.execute(
            text(
                "TRUNCATE TABLE bitacora, historial_restriccion_placa, restriccion_placa_reglas, "
                "restriccion_placa_config, asignaciones_conductor, historial_vehiculo, rutas_detalle, "
                "soluciones_ruta, pedidos, vehiculos, jornadas, depositos, area_operacion "
                "RESTART IDENTITY CASCADE"
            )
        )
        await connection.execute(
            text(
                "UPDATE usuarios SET intentos_fallidos = 0, "
                "bloqueado_hasta = NULL, activo = true"
            )
        )
    await init_database()


@pytest.fixture(scope="session")
async def database() -> None:
    """Crea PostGIS de prueba y cierra el pool al terminar la sesión."""
    await _ensure_test_database()
    await init_database()
    yield
    await engine.dispose()


@pytest.fixture
async def client(database: None):
    """Cliente HTTP sobre la app, con la semilla de Huancayo restaurada."""
    await _reset_seed()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http:
        yield http
