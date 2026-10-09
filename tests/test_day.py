"""Carga de la jornada y edición de flota."""

import pytest
from httpx import AsyncClient

from tests.helpers import login_headers

DAY = "2026-10-08"
CSV = """codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin,lat,lon,altitud
PED-210,Bodega Los Andes,"Jr. Puno 450, Huancayo",25,09:00,12:00,-12.06806,-75.21000,3271
PED-211,Bodega Centro,"Plaza Constitución, Huancayo",40,08:00,11:00,,,
PED-212,Puesto Sin Mapa,"Callejón sin nombre, El Tambo",15,10:00,13:00,,,
PED-213,Fuera del Valle,"Lima centro",10,09:00,11:00,-12.046,-77.043,150
"""


@pytest.mark.asyncio
async def test_csv_accepts_known_places_and_leaves_the_pin_for_the_rest(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    denied = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": CSV},
        headers=await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026"),
    )
    assert denied.status_code == 403

    imported = await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": CSV}, headers=headers)
    assert imported.status_code == 200
    rows = {row["codigo_pedido"]: row for row in imported.json()["filas"]}
    assert imported.json()["aceptados"] == 2
    assert rows["PED-210"]["resultado"] == "aceptado"
    assert rows["PED-211"]["resultado"] == "aceptado"
    assert rows["PED-211"]["lat"] == pytest.approx(-12.06513)
    assert rows["PED-212"]["resultado"] == "pendiente_punto"
    assert rows["PED-213"]["resultado"] == "rechazado"

    saved = await client.post(
        "/api/v1/pedidos",
        headers=headers,
        json={
            "codigo_pedido": "PED-212",
            "cliente_nombre": "Puesto Sin Mapa",
            "direccion_referencia": "Callejón sin nombre, El Tambo",
            "lat": -12.07,
            "lon": -75.21,
            "altitud_msnm": 3270,
            "peso_kg": 15,
            "ventana_inicio": "2026-10-08T10:00:00-05:00",
            "ventana_fin": "2026-10-08T13:00:00-05:00",
            "fecha": DAY,
        },
    )
    assert saved.status_code == 201

    day = await client.get(f"/api/v1/jornadas/{DAY}", headers=headers)
    assert day.status_code == 200
    codes = {order["codigo_pedido"] for order in day.json()["pedidos"]}
    assert codes == {"PED-210", "PED-211", "PED-212"}


@pytest.mark.asyncio
async def test_admin_registers_a_vehicle_and_operator_can_inactivate_it(client: AsyncClient) -> None:
    admin = await login_headers(client, "admin@distrirapido.pe", "Admin.2026")
    operador = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    depot = await client.get("/api/v1/depositos")
    depot_id = depot.json()[0]["id"]

    blocked = await client.post(
        "/api/v1/flota",
        headers=operador,
        json={
            "deposito_id": depot_id,
            "placa": "X1Y-200",
            "capacidad_kg": 800,
            "capacidad_m3": 4,
            "tipo_combustible": "diesel",
            "emision_base_co2_g_km": 200,
            "factor_penalizacion_pendiente": 0.04,
        },
    )
    assert blocked.status_code == 403

    created = await client.post(
        "/api/v1/flota",
        headers=admin,
        json={
            "deposito_id": depot_id,
            "placa": "X1Y-200",
            "capacidad_kg": 800,
            "capacidad_m3": 4,
            "tipo_combustible": "diesel",
            "emision_base_co2_g_km": 200,
            "factor_penalizacion_pendiente": 0.04,
        },
    )
    assert created.status_code == 201
    vehicle_id = created.json()["id"]

    updated = await client.patch(
        f"/api/v1/flota/{vehicle_id}",
        headers=operador,
        json={"activo": False, "capacidad_kg": 700},
    )
    assert updated.status_code == 200
    assert updated.json()["activo"] is False
    assert updated.json()["capacidad_kg"] == 700

    active = await client.get("/api/v1/vehiculos")
    assert "X1Y-200" not in {item["placa"] for item in active.json()}

    history = await client.get(f"/api/v1/flota/{vehicle_id}/historial", headers=operador)
    assert history.status_code == 200
    assert any("inactiva" in row["detalle"] or "capacidad_kg" in row["detalle"] for row in history.json())
