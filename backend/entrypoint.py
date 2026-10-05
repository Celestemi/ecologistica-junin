"""Espera a PostGIS, crea el esquema y deja paso a Uvicorn."""

from __future__ import annotations

import asyncio
import os
import sys
import time
from urllib.parse import urlsplit, urlunsplit


def _asyncpg_dsn(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit(("postgresql", parts.netloc, parts.path or "/ecologistica", "", ""))


async def _ping(dsn: str) -> None:
    import asyncpg

    connection = await asyncpg.connect(dsn)
    await connection.close()


def wait_for_postgis() -> None:
    """Reintenta la conexión. Compose ya exige el healthcheck de PostgreSQL."""
    url = os.environ.get("DATABASE_URL")
    if not url:
        sys.exit("Falta DATABASE_URL.")
    dsn = _asyncpg_dsn(url)
    last_error: Exception | None = None
    for _attempt in range(30):
        try:
            asyncio.run(_ping(dsn))
            return
        except Exception as exc:  # noqa: BLE001 — el arranque debe tolerar el primer segundo de PostGIS
            last_error = exc
            time.sleep(1)
    sys.exit(f"PostGIS no aceptó conexiones: {last_error}")


def main() -> None:
    wait_for_postgis()
    import subprocess

    subprocess.check_call([sys.executable, "-m", "app.db.init_db"])
    os.execvp(sys.argv[1], sys.argv[1:])


if __name__ == "__main__":
    main()
