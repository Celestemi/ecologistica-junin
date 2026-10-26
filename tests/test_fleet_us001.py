"""US-001 / RF-001 — gestión de vehículos."""

import pytest
from httpx import AsyncClient

from tests.helpers import login_headers

VEHICLE_BODY = {
    "modelo": "Furgón Diésel",
    "capacidad_kg": 900,
    "capacidad_m3": 5,
    "tipo_combustible": "diesel",
    "rendimiento_km_gal": 11.5,
    "emision_base_co2_g_km": 210,
    "factor_penalizacion_pendiente": 0.04,
}


@pytest.mark.asyncio
async def test_valid_registration_is_active(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    depot_id = (await client.get("/api/v1/depositos", headers=operador)).json()[0]["id"]

    created = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={"deposito_id": depot_id, "placa": "abc-123", **VEHICLE_BODY},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["placa"] == "ABC-123"
    assert body["modelo"] == "Furgón Diésel"
    assert body["activo"] is True
    assert body["estado_operativo"] == "activo"
    assert body["id"] > 0

    listed = await client.get("/api/v1/flota", headers=operador)
    assert any(item["placa"] == "ABC-123" for item in listed.json())


@pytest.mark.asyncio
async def test_duplicate_plate_is_rejected(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    depot_id = (await client.get("/api/v1/depositos", headers=operador)).json()[0]["id"]

    first = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={"deposito_id": depot_id, "placa": "DUP-100", **VEHICLE_BODY},
    )
    assert first.status_code == 201
    second = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={"deposito_id": depot_id, "placa": "DUP-100", **VEHICLE_BODY, "modelo": "Otro"},
    )
    assert second.status_code == 400
    assert "placa" in second.json()["detail"].casefold()


@pytest.mark.asyncio
async def test_required_fields_and_invalid_numbers(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    depot_id = (await client.get("/api/v1/depositos", headers=operador)).json()[0]["id"]

    missing_model = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={"deposito_id": depot_id, "placa": "BAD-001", **VEHICLE_BODY, "modelo": ""},
    )
    assert missing_model.status_code == 400

    bad_rendimiento = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={
            "deposito_id": depot_id,
            "placa": "BAD-002",
            **VEHICLE_BODY,
            "rendimiento_km_gal": 0,
        },
    )
    assert bad_rendimiento.status_code == 400


@pytest.mark.asyncio
async def test_edit_keeps_id_and_inactivation_excludes_from_optimizer(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    depot_id = (await client.get("/api/v1/depositos", headers=operador)).json()[0]["id"]

    created = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={"deposito_id": depot_id, "placa": "EDT-300", **VEHICLE_BODY},
    )
    vehicle_id = created.json()["id"]

    patched = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"rendimiento_km_gal": 13.2, "capacidad_kg": 850},
    )
    assert patched.status_code == 200
    assert patched.json()["id"] == vehicle_id
    assert patched.json()["rendimiento_km_gal"] == pytest.approx(13.2)

    inactive = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"estado_operativo": "inactivo"},
    )
    assert inactive.status_code == 200
    assert inactive.json()["activo"] is False
    assert inactive.json()["estado_operativo"] == "inactivo"

    active_list = await client.get("/api/v1/vehiculos", headers=operador)
    assert "EDT-300" not in {item["placa"] for item in active_list.json()}

    history = await client.get(f"/api/v1/flota/{vehicle_id}/historial", headers=operador)
    assert history.status_code == 200
    assert len(history.json()) >= 2


@pytest.mark.asyncio
async def test_operator_cannot_create_but_can_update(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    depot_id = (await client.get("/api/v1/depositos", headers=operador)).json()[0]["id"]

    denied = await client.post(
        "/api/v1/flota",
        headers=operador,
        json={"deposito_id": depot_id, "placa": "RB-001", **VEHICLE_BODY},
    )
    assert denied.status_code == 403

    created = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={"deposito_id": depot_id, "placa": "RB-001", **VEHICLE_BODY},
    )
    vehicle_id = created.json()["id"]
    allowed = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"modelo": "Furgón actualizado"},
    )
    assert allowed.status_code == 200
