"""US-005 / RF-005 — geocodificación y validación espacial."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.helpers import login_headers

DAY = "2026-10-09"


@pytest.mark.asyncio
async def test_landmark_geocodes_and_persists_point(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    csv = """codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin
PED-901,Cliente Plaza,"Plaza Constitución, Huancayo",10,09:00,11:00
"""
    imported = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": csv},
        headers=headers,
    )
    assert imported.status_code == 200
    row = imported.json()["filas"][0]
    assert row["resultado"] == "aceptado"
    assert row["lat"] == pytest.approx(-12.06513)
    assert row["lon"] == pytest.approx(-75.20486)

    order = await client.get(f"/api/v1/jornadas/{DAY}", headers=headers)
    ped = next(item for item in order.json()["pedidos"] if item["codigo_pedido"] == "PED-901")
    assert ped["estado_ubicacion"] == "geocodificado"
    assert ped["ubicacion"]["coordinates"][0] == pytest.approx(-75.20486)


@pytest.mark.asyncio
async def test_unknown_address_persisted_pending_and_excluded_from_optimizer(
    client: AsyncClient,
) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    csv = """codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin
PED-902,Sin Mapa,"Calle inexistente 9999, Huancayo",12,10:00,12:00
"""
    imported = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": csv},
        headers=headers,
    )
    assert imported.status_code == 200
    row = imported.json()["filas"][0]
    assert row["resultado"] == "pendiente_punto"
    assert "ubicar" in (row["motivo"] or "").lower()
    assert row["pedido_id"] is not None

    pending = await client.get("/api/v1/pedidos", headers=headers)
    assert any(item["codigo_pedido"] == "PED-902" for item in pending.json())

    optimized = await client.post("/api/v1/optimizar-rutas", headers=headers)
    assert optimized.status_code == 201
    assert optimized.json()["metadata"]["pedidos"] == 5


@pytest.mark.asyncio
async def test_coordinates_outside_operating_area_become_pending(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    csv = (
        "codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin,lat,lon\n"
        "PED-903,Periferia,\"Sector norte\",8,09:00,10:00,-11.95,-75.28\n"
    )
    imported = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": csv},
        headers=headers,
    )
    assert imported.status_code == 200
    row = imported.json()["filas"][0]
    assert row["resultado"] == "pendiente_punto"
    assert "Huancayo" in (row["motivo"] or "")

    day = await client.get(f"/api/v1/jornadas/{DAY}", headers=headers)
    ped = next(item for item in day.json()["pedidos"] if item["codigo_pedido"] == "PED-903")
    assert ped["estado_ubicacion"] == "pendiente_validacion"


@pytest.mark.asyncio
async def test_manual_patch_geocodes_and_allows_routing(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    csv = """codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin
PED-904,Manual,"Sin geocodificar",5,08:00,09:00
"""
    await client.post(f"/api/v1/jornadas/{DAY}/importar", json={"csv": csv}, headers=headers)
    day = await client.get(f"/api/v1/jornadas/{DAY}", headers=headers)
    ped = next(item for item in day.json()["pedidos"] if item["codigo_pedido"] == "PED-904")

    denied = await client.patch(
        f"/api/v1/pedidos/{ped['id']}/ubicacion",
        json={"lat": -11.95, "lon": -75.28},
        headers=await login_headers(client, "auditor@distrirapido.pe", "Auditor.2026"),
    )
    assert denied.status_code == 403

    bad = await client.patch(
        f"/api/v1/pedidos/{ped['id']}/ubicacion",
        json={"lat": -11.95, "lon": -75.28},
        headers=headers,
    )
    assert bad.status_code == 400

    ok = await client.patch(
        f"/api/v1/pedidos/{ped['id']}/ubicacion",
        json={"lat": -12.06806, "lon": -75.21, "altitud_msnm": 3271},
        headers=headers,
    )
    assert ok.status_code == 200
    assert ok.json()["estado_ubicacion"] == "geocodificado"


@pytest.mark.asyncio
async def test_create_order_rejects_invalid_and_out_of_area(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    invalid = await client.post(
        "/api/v1/pedidos",
        headers=headers,
        json={
            "codigo_pedido": "PED-905",
            "cliente_nombre": "Cliente",
            "direccion_referencia": "Lima",
            "lat": -12.046,
            "lon": -77.043,
            "altitud_msnm": 150,
            "peso_kg": 1,
            "ventana_inicio": "2026-10-09T09:00:00-05:00",
            "ventana_fin": "2026-10-09T11:00:00-05:00",
        },
    )
    assert invalid.status_code == 400

    outside = await client.post(
        "/api/v1/pedidos",
        headers=headers,
        json={
            "codigo_pedido": "PED-906",
            "cliente_nombre": "Cliente",
            "direccion_referencia": "Fuera",
            "lat": -11.95,
            "lon": -75.28,
            "altitud_msnm": 3270,
            "peso_kg": 1,
            "ventana_inicio": "2026-10-09T09:00:00-05:00",
            "ventana_fin": "2026-10-09T11:00:00-05:00",
        },
    )
    assert outside.status_code == 400
    assert "Huancayo" in outside.json()["detail"]


@pytest.mark.asyncio
async def test_import_still_rejects_invalid_weight(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    csv = """codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin
PED-907,Cliente,"Plaza Constitución",0,09:00,11:00
"""
    imported = await client.post(
        f"/api/v1/jornadas/{DAY}/importar",
        json={"csv": csv},
        headers=headers,
    )
    assert imported.status_code == 200
    assert imported.json()["rechazados"] == 1
    assert imported.json()["aceptados"] == 0
