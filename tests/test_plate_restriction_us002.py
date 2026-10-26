"""US-002 / RF-002 / RN-002 — restricción vehicular por placa."""

import pytest
from httpx import AsyncClient

from tests.helpers import login_headers


@pytest.mark.asyncio
async def test_default_config_is_pending_and_inactive(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    config = await client.get("/api/v1/restricciones-placa", headers=operador)
    assert config.status_code == 200
    body = config.json()
    assert body["validada_normativamente"] is False
    assert body["activa"] is False
    assert "[PENDIENTE DE VALIDACIÓN NORMATIVA]" in body["etiqueta_validacion"]
    assert body["reglas"] == []


@pytest.mark.asyncio
async def test_cannot_activate_without_validation(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    denied = await client.patch(
        "/api/v1/restricciones-placa",
        headers=operador,
        json={"activa": True},
    )
    assert denied.status_code == 400
    assert "validación normativa" in denied.json()["detail"].casefold()


@pytest.mark.asyncio
async def test_operator_cannot_confirm_validation(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    denied = await client.patch(
        "/api/v1/restricciones-placa",
        headers=operador,
        json={"validada_normativamente": True},
    )
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_auditor_can_read_but_not_update(client: AsyncClient) -> None:
    auditor = await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026")
    read = await client.get("/api/v1/restricciones-placa", headers=auditor)
    assert read.status_code == 200
    denied = await client.patch(
        "/api/v1/restricciones-placa",
        headers=auditor,
        json={"ambito": "Otro"},
    )
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_optimizer_unchanged_without_active_validated_rule(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert optimized.status_code == 201
    meta = optimized.json()["metadata"]
    assert meta["restriccion_placa_aplicada"] is False
    assert meta["exclusiones_placa"] == []
    assert 1 <= meta["vehiculos_usados"] <= 2


@pytest.mark.asyncio
async def test_validated_inactive_rule_does_not_filter(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    await client.patch(
        "/api/v1/restricciones-placa",
        headers=admin,
        json={
            "validada_normativamente": True,
            "referencia_normativa": "Documento de prueba (solo entorno automatizado)",
            "activa": False,
            "reglas": [{"ultimo_digito": 8, "dias_semana": [2]}],
        },
    )
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert optimized.status_code == 201
    assert optimized.json()["metadata"]["restriccion_placa_aplicada"] is False
    assert 1 <= optimized.json()["metadata"]["vehiculos_usados"] <= 2


@pytest.mark.asyncio
async def test_active_validated_rule_excludes_vehicle_and_explains(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    await client.patch(
        "/api/v1/restricciones-placa",
        headers=admin,
        json={
            "validada_normativamente": True,
            "referencia_normativa": "Documento de prueba (solo entorno automatizado)",
            "activa": True,
            "reglas": [{"ultimo_digito": 8, "dias_semana": [2]}],
        },
    )
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert optimized.status_code == 201
    meta = optimized.json()["metadata"]
    assert meta["restriccion_placa_aplicada"] is True
    assert meta["vehiculos_usados"] == 1
    assert len(meta["exclusiones_placa"]) == 1
    assert meta["exclusiones_placa"][0]["placa"] == "W4U-158"
    assert meta["exclusiones_placa"][0]["ultimo_digito"] == 8
    assert "último dígito 8" in meta["exclusiones_placa"][0]["motivo"]


@pytest.mark.asyncio
async def test_allowed_vehicle_still_routes(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    await client.patch(
        "/api/v1/restricciones-placa",
        headers=admin,
        json={
            "validada_normativamente": True,
            "referencia_normativa": "Documento de prueba (solo entorno automatizado)",
            "activa": True,
            "reglas": [{"ultimo_digito": 8, "dias_semana": [2]}],
        },
    )
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    plates = {
        feature["properties"].get("plate")
        for feature in optimized.json()["features"]
        if feature["geometry"]["type"] == "LineString"
    }
    assert "E7M-304" in plates
    assert "W4U-158" not in plates


@pytest.mark.asyncio
async def test_configuration_changes_are_audited(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    patched = await client.patch(
        "/api/v1/restricciones-placa",
        headers=admin,
        json={"reglas": [{"ultimo_digito": 4, "dias_semana": [1, 3, 5]}]},
    )
    assert patched.status_code == 200
    history = await client.get("/api/v1/restricciones-placa/historial", headers=admin)
    assert history.status_code == 200
    assert any("regla" in row["detalle"] for row in history.json())

    persisted = await client.get("/api/v1/restricciones-placa", headers=admin)
    assert persisted.json()["reglas"][0]["ultimo_digito"] == 4
