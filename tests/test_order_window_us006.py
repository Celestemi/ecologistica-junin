"""US-006 / RF-006 / RN-005 — ventanas horarias de pedidos."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.core.database import engine
from tests.helpers import login_headers
from tests.test_api import _order_payload

LIMA = ZoneInfo("America/Lima")


def _window_payload(**overrides: object) -> dict[str, object]:
    base = {
        "ventana_inicio": datetime(2026, 10, 9, 9, 0, tzinfo=LIMA).isoformat(),
        "ventana_fin": datetime(2026, 10, 9, 12, 0, tzinfo=LIMA).isoformat(),
    }
    base.update(overrides)
    return base


@pytest.mark.asyncio
async def test_valid_window_update_persists(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    created = await client.post(
        "/api/v1/pedidos",
        json=_order_payload(
            codigo_pedido="WIN-001",
            ventana_inicio=datetime(2026, 10, 9, 8, 0, tzinfo=LIMA).isoformat(),
            ventana_fin=datetime(2026, 10, 9, 10, 0, tzinfo=LIMA).isoformat(),
        ),
        headers=headers,
    )
    order_id = created.json()["id"]
    updated = await client.patch(
        f"/api/v1/pedidos/{order_id}",
        json=_window_payload(),
        headers=headers,
    )
    assert updated.status_code == 200
    body = updated.json()
    assert body["id"] == order_id
    assert body["codigo_pedido"] == "WIN-001"
    assert body["ventana_inicio"].startswith("2026-10-09T09:00:00")
    assert body["ventana_fin"].startswith("2026-10-09T12:00:00")


@pytest.mark.asyncio
async def test_rejects_inverted_and_equal_windows(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    created = await client.post(
        "/api/v1/pedidos",
        json=_order_payload(codigo_pedido="WIN-002"),
        headers=headers,
    )
    order_id = created.json()["id"]
    inverted = await client.patch(
        f"/api/v1/pedidos/{order_id}",
        json=_window_payload(
            ventana_inicio=datetime(2026, 10, 9, 14, 0, tzinfo=LIMA).isoformat(),
            ventana_fin=datetime(2026, 10, 9, 11, 0, tzinfo=LIMA).isoformat(),
        ),
        headers=headers,
    )
    assert inverted.status_code == 400
    assert "posterior" in inverted.json()["detail"].casefold()

    equal = await client.patch(
        f"/api/v1/pedidos/{order_id}",
        json=_window_payload(
            ventana_inicio=datetime(2026, 10, 9, 11, 0, tzinfo=LIMA).isoformat(),
            ventana_fin=datetime(2026, 10, 9, 11, 0, tzinfo=LIMA).isoformat(),
        ),
        headers=headers,
    )
    assert equal.status_code == 400


@pytest.mark.asyncio
async def test_auditor_cannot_edit_window(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    created = await client.post(
        "/api/v1/pedidos",
        json=_order_payload(codigo_pedido="WIN-003"),
        headers=operador,
    )
    order_id = created.json()["id"]
    auditor = await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026")
    denied = await client.patch(
        f"/api/v1/pedidos/{order_id}",
        json=_window_payload(),
        headers=auditor,
    )
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_missing_order_returns_404(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    missing = await client.patch("/api/v1/pedidos/999999", json=_window_payload(), headers=headers)
    assert missing.status_code == 404


@pytest.mark.asyncio
async def test_assigned_order_blocks_window_change(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    pending = await client.get("/api/v1/pedidos", headers=headers)
    order_id = pending.json()[0]["id"]
    optimized = await client.post("/api/v1/optimizar-rutas", headers=headers)
    assert optimized.status_code == 201
    blocked = await client.patch(
        f"/api/v1/pedidos/{order_id}",
        json=_window_payload(),
        headers=headers,
    )
    assert blocked.status_code == 409
    assert "ruta" in blocked.json()["detail"].casefold()


@pytest.mark.asyncio
async def test_delivered_order_blocks_window_change(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    pending = await client.get("/api/v1/pedidos", headers=headers)
    code = pending.json()[0]["codigo_pedido"]
    order_id = pending.json()[0]["id"]
    async with engine.begin() as connection:
        await connection.execute(
            text("UPDATE pedidos SET estado = 'delivered' WHERE codigo_pedido = :code"),
            {"code": code},
        )
    blocked = await client.patch(
        f"/api/v1/pedidos/{order_id}",
        json=_window_payload(),
        headers=headers,
    )
    assert blocked.status_code == 409
    assert "cerrado" in blocked.json()["detail"].casefold()


@pytest.mark.asyncio
async def test_updated_window_used_by_optimizer(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    created = await client.post(
        "/api/v1/pedidos",
        json=_order_payload(
            codigo_pedido="WIN-SOL",
            ventana_inicio=datetime(2026, 10, 7, 6, 0, tzinfo=LIMA).isoformat(),
            ventana_fin=datetime(2026, 10, 7, 7, 0, tzinfo=LIMA).isoformat(),
        ),
        headers=headers,
    )
    order_id = created.json()["id"]
    await client.patch(
        f"/api/v1/pedidos/{order_id}",
        json={
            "ventana_inicio": datetime(2026, 10, 7, 9, 0, tzinfo=LIMA).isoformat(),
            "ventana_fin": datetime(2026, 10, 7, 12, 0, tzinfo=LIMA).isoformat(),
        },
        headers=headers,
    )
    optimized = await client.post("/api/v1/optimizar-rutas", headers=headers)
    assert optimized.status_code == 201
