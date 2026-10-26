"""US-003 / RF-003 — estados operativos de la flota."""

import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.core.database import engine
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


async def _create_vehicle(client: AsyncClient, placa: str) -> dict:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    depot_id = (await client.get("/api/v1/depositos", headers=operador)).json()[0]["id"]
    created = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={"deposito_id": depot_id, "placa": placa, **VEHICLE_BODY},
    )
    assert created.status_code == 201
    return created.json()


@pytest.mark.asyncio
async def test_active_to_maintenance_requires_motive_and_excludes_routing(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    vehicle = await _create_vehicle(client, "MNT-001")
    vehicle_id = vehicle["id"]

    denied = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"estado_operativo": "mantenimiento"},
    )
    assert denied.status_code == 400

    changed = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"estado_operativo": "mantenimiento", "motivo": "Revisión de frenos"},
    )
    assert changed.status_code == 200
    body = changed.json()
    assert body["estado_operativo"] == "mantenimiento"
    assert body["activo"] is False

    listed = await client.get("/api/v1/vehiculos", headers=operador)
    assert "MNT-001" not in {item["placa"] for item in listed.json()}

    history = await client.get(f"/api/v1/flota/{vehicle_id}/historial", headers=operador)
    row = history.json()[0]
    assert row["estado_anterior"] == "activo"
    assert row["estado_nuevo"] == "mantenimiento"
    assert row["motivo"] == "Revisión de frenos"
    assert row["correo"] == "operador@distrirapido.pe"


@pytest.mark.asyncio
async def test_maintenance_back_to_active(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    vehicle = await _create_vehicle(client, "ACT-002")
    vehicle_id = vehicle["id"]

    await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"estado_operativo": "mantenimiento", "motivo": "Aceite"},
    )
    restored = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"estado_operativo": "activo"},
    )
    assert restored.status_code == 200
    assert restored.json()["estado_operativo"] == "activo"
    assert restored.json()["activo"] is True

    listed = await client.get("/api/v1/vehiculos", headers=operador)
    assert "ACT-002" in {item["placa"] for item in listed.json()}


@pytest.mark.asyncio
async def test_active_to_inactive_and_invalid_transition(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    vehicle = await _create_vehicle(client, "INA-003")
    vehicle_id = vehicle["id"]

    inactive = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"estado_operativo": "inactivo"},
    )
    assert inactive.status_code == 200
    assert inactive.json()["estado_operativo"] == "inactivo"

    blocked = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"estado_operativo": "mantenimiento", "motivo": "Tarde"},
    )
    assert blocked.status_code == 400


@pytest.mark.asyncio
async def test_auditor_cannot_change_state(client: AsyncClient) -> None:
    vehicle = await _create_vehicle(client, "RB-004")
    auditor = await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026")
    denied = await client.patch(
        f"/api/v1/flota/{vehicle['id']}",
        headers=auditor,
        json={"estado_operativo": "inactivo"},
    )
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_legacy_activo_flag_maps_to_operational_state(client: AsyncClient) -> None:
    vehicle = await _create_vehicle(client, "LEG-005")
    async with engine.begin() as connection:
        await connection.execute(
            text(
                "UPDATE vehiculos SET activo = false, estado_operativo = 'inactivo' "
                "WHERE id = :id"
            ),
            {"id": vehicle["id"]},
        )
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    row = await client.get("/api/v1/flota", headers=operador)
    match = next(item for item in row.json() if item["id"] == vehicle["id"])
    assert match["activo"] is False
    assert match["estado_operativo"] == "inactivo"


@pytest.mark.asyncio
async def test_historical_routes_remain_after_inactivation(client: AsyncClient) -> None:
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    optimized = await client.post("/api/v1/optimizar-rutas", headers=operador)
    assert optimized.status_code == 201

    plate = next(
        feature["properties"]["plate"]
        for feature in optimized.json()["features"]
        if feature["geometry"]["type"] == "LineString"
    )
    fleet = await client.get("/api/v1/flota", headers=operador)
    vehicle = next(item for item in fleet.json() if item["placa"] == plate)

    inactive = await client.patch(
        f"/api/v1/flota/{vehicle['id']}",
        headers=operador,
        json={"estado_operativo": "inactivo"},
    )
    assert inactive.status_code == 200

    active_route = await client.get("/api/v1/rutas/activas", params={"placa": plate}, headers=operador)
    assert active_route.status_code == 200
    assert active_route.json()["paradas"]

    available = await client.get("/api/v1/vehiculos", headers=operador)
    assert plate not in {item["placa"] for item in available.json()}
