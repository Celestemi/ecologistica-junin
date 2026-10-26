"""Pruebas de EN-003 / RNF-003 (auth, RBAC, tokens, WS y configuración)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.core.config import Settings, get_settings
from app.core.database import async_session_factory
from app.core.security_boot import validate_security_settings
from app.main import app
from app.models.identity import Usuario
from tests.helpers import login_headers


@pytest.mark.asyncio
async def test_anonymous_cannot_read_operational_endpoints(client: AsyncClient) -> None:
    for path in ("/api/v1/pedidos", "/api/v1/vehiculos", "/api/v1/depositos", "/api/v1/rutas/mapa"):
        response = await client.get(path)
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_auditor_reads_but_cannot_optimize(client: AsyncClient) -> None:
    auditor = await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026")
    orders = await client.get("/api/v1/pedidos", headers=auditor)
    assert orders.status_code == 200
    denied = await client.post("/api/v1/optimizar-rutas", headers=auditor)
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_invalid_and_expired_tokens_are_rejected(client: AsyncClient) -> None:
    bad = await client.get("/api/v1/auth/yo", headers={"Authorization": "Bearer no-es-jwt"})
    assert bad.status_code == 401

    settings = get_settings()
    expired = jwt.encode(
        {
            "sub": "1",
            "rol": "operador",
            "correo": "operador@distrirapido.pe",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
        },
        settings.secret_key,
        algorithm="HS256",
    )
    stale = await client.get("/api/v1/auth/yo", headers={"Authorization": f"Bearer {expired}"})
    assert stale.status_code == 401


@pytest.mark.asyncio
async def test_inactive_user_cannot_use_the_api(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    async with async_session_factory() as session:
        user = await session.scalar(select(Usuario).where(Usuario.correo == "operador@distrirapido.pe"))
        assert user is not None
        user.activo = False
        await session.commit()
    blocked = await client.get("/api/v1/pedidos", headers=headers)
    assert blocked.status_code == 401


@pytest.mark.asyncio
async def test_conductor_cannot_open_driver_channel_for_foreign_plate(client: AsyncClient) -> None:
    conductor = await login_headers(client, "conductor@distrirapido.pe", "Conductor.2026")
    token = conductor["Authorization"].removeprefix("Bearer ")
    with TestClient(app) as sync:
        with pytest.raises(WebSocketDisconnect):
            with sync.websocket_connect(f"/ws/driver/E7M-304?token={token}") as socket:
                socket.receive_text()


@pytest.mark.asyncio
async def test_conductor_may_open_assigned_plate(client: AsyncClient) -> None:
    conductor = await login_headers(client, "conductor@distrirapido.pe", "Conductor.2026")
    token = conductor["Authorization"].removeprefix("Bearer ")
    with TestClient(app) as sync:
        with sync.websocket_connect(f"/ws/driver/W4U-158?token={token}") as socket:
            socket.send_json(
                {
                    "type": "position",
                    "lat": -12.06513,
                    "lon": -75.20486,
                    "altitud_msnm": 3270,
                }
            )
            body = socket.receive_json()
    assert body["type"] in {"position", "eta", "error"}


@pytest.mark.asyncio
async def test_public_tracking_hides_personal_data(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    orders = await client.get("/api/v1/pedidos", headers=operador)
    token = orders.json()[0]["token_seguimiento"]
    assert token
    public = await client.get(f"/api/v1/seguimiento/publico/{token}")
    assert public.status_code == 200
    body = public.json()
    assert "cliente_nombre" not in body
    assert "direccion_referencia" not in body
    assert "codigo_pedido" not in body


def test_production_rejects_default_secret() -> None:
    settings = Settings(
        app_environment="production",
        secret_key="cambia-esta-clave-en-produccion-local",
        allow_demo_accounts=False,
    )
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        validate_security_settings(settings)


def test_demo_accounts_disabled_outside_demo() -> None:
    settings = Settings(
        app_environment="staging",
        secret_key="x" * 40,
        allow_demo_accounts=True,
    )
    with pytest.raises(RuntimeError, match="ALLOW_DEMO_ACCOUNTS"):
        validate_security_settings(settings)
