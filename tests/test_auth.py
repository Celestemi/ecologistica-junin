"""Ingreso, bloqueo de 15 minutos y permiso de optimización."""

from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core.database import async_session_factory
from app.models.identity import Usuario
from tests.helpers import login_headers


@pytest.mark.asyncio
async def test_login_and_me(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/ingresar",
        json={"correo": "operador@distrirapido.pe", "clave": "Operador.2026"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["usuario"]["rol"] == "operador"
    assert body["usuario"]["nombre"] == "Luis Huamán"
    me = await client.get("/api/v1/auth/yo", headers={"Authorization": f"Bearer {body['access_token']}"})
    assert me.status_code == 200
    assert me.json()["correo"] == "operador@distrirapido.pe"


@pytest.mark.asyncio
async def test_third_failure_locks_the_account_for_fifteen_minutes(client: AsyncClient) -> None:
    payload = {"correo": "gerente@distrirapido.pe", "clave": "clave-incorrecta"}
    first = await client.post("/api/v1/auth/ingresar", json=payload)
    second = await client.post("/api/v1/auth/ingresar", json=payload)
    third = await client.post("/api/v1/auth/ingresar", json=payload)
    assert first.status_code == 401
    assert second.status_code == 401
    assert first.json()["detail"] == "Correo o contraseña incorrectos."
    assert "bloqueada" in third.json()["detail"]

    still = await client.post(
        "/api/v1/auth/ingresar",
        json={"correo": "gerente@distrirapido.pe", "clave": "Gerente.2026"},
    )
    assert still.status_code == 401
    assert "bloqueada" in still.json()["detail"]

    async with async_session_factory() as session:
        user = await session.scalar(select(Usuario).where(Usuario.correo == "gerente@distrirapido.pe"))
        assert user is not None
        assert user.bloqueado_hasta is not None
        assert user.bloqueado_hasta > datetime.now(timezone.utc)
        user.bloqueado_hasta = datetime.now(timezone.utc) - timedelta(minutes=1)
        await session.commit()

    restored = await client.post(
        "/api/v1/auth/ingresar",
        json={"correo": "gerente@distrirapido.pe", "clave": "Gerente.2026"},
    )
    assert restored.status_code == 200


@pytest.mark.asyncio
async def test_auditor_cannot_optimize_and_operator_can(client: AsyncClient) -> None:
    anonymous = await client.post("/api/v1/optimizar-rutas")
    assert anonymous.status_code == 401

    auditor = await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026")
    denied = await client.post("/api/v1/optimizar-rutas", headers=auditor)
    assert denied.status_code == 403
    assert "operador" in denied.json()["detail"]

    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    allowed = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert allowed.status_code == 201

    journal = await client.get("/api/v1/auth/bitacora", headers=auditor)
    assert journal.status_code == 200
    actions = {row["accion"] for row in journal.json()}
    assert "optimizar_denegado" in actions
    assert "optimizar_rutas" in actions

    hidden = await client.get("/api/v1/auth/bitacora", headers=operador)
    assert hidden.status_code == 403
