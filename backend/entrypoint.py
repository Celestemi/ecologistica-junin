"""Espera a que PostGIS acepte conexiones antes de la semilla."""

from __future__ import annotations

import asyncio
import os
import sys
import time
from urllib.parse import quote, urlsplit, urlunsplit


def ensure_database_url() -> str:
    """Usa DATABASE_URL o la arma con DB_HOST, DB_PORT, DB_USER, DB_PASSWORD y DB_NAME."""
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    name = os.environ.get("DB_NAME")
    if not all((user, password, host, port, name)):
        sys.exit("Falta DATABASE_URL o el conjunto DB_HOST, DB_PORT, DB_USER, DB_PASSWORD y DB_NAME.")
    url = (
        f"postgresql+asyncpg://{quote(user or '', safe='')}:"
        f"{quote(password or '', safe='')}@{host}:{port}/{name}"
    )
    os.environ["DATABASE_URL"] = url
    return url


def _asyncpg_dsn(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit(("postgresql", parts.netloc, parts.path or "/ecologistica", "", ""))


async def _ping(dsn: str) -> None:
    import asyncpg

    connection = await asyncpg.connect(dsn)
    await connection.close()


def wait_for_postgis() -> None:
    """Reintenta la conexión. Compose ya exige el healthcheck de PostgreSQL."""
    dsn = _asyncpg_dsn(ensure_database_url())
    last_error: Exception | None = None
    for _attempt in range(30):
        try:
            asyncio.run(_ping(dsn))
            return
        except Exception as exc:  # noqa: BLE001 — el arranque debe tolerar el primer segundo de PostGIS
            last_error = exc
            time.sleep(1)
    sys.exit(f"PostGIS no aceptó conexiones: {last_error}")


if __name__ == "__main__":
    wait_for_postgis()
