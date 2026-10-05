"""Integración HTTP de pedidos, flota y optimización VRPTW."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from httpx import AsyncClient

LIMA = ZoneInfo("America/Lima")


def _order_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "codigo_pedido": "PED-900",
        "cliente_nombre": "Bodega Los Andes",
        "direccion_referencia": "Jr. Puno 450, Cercado de Huancayo",
        "lat": -12.06806,
        "lon": -75.21000,
        "altitud_msnm": 3271,
        "peso_kg": 25,
        "ventana_inicio": datetime(2026, 10, 7, 9, 0, tzinfo=LIMA).isoformat(),
        "ventana_fin": datetime(2026, 10, 7, 12, 0, tzinfo=LIMA).isoformat(),
    }
    payload.update(overrides)
    return payload


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_list_vehicles_and_pending_orders(client: AsyncClient) -> None:
    vehicles = await client.get("/api/v1/vehiculos")
    orders = await client.get("/api/v1/pedidos")
    assert vehicles.status_code == 200
    assert orders.status_code == 200
    plates = {item["placa"] for item in vehicles.json()}
    codes = {item["codigo_pedido"] for item in orders.json()}
    assert plates == {"W4U-158", "E7M-304"}
    assert {"PED-001", "PED-002", "PED-003", "PED-004", "PED-005"} <= codes
    assert all(item["estado"] == "pending" for item in orders.json())


@pytest.mark.asyncio
async def test_create_order_and_reject_invalid_payloads(client: AsyncClient) -> None:
    created = await client.post("/api/v1/pedidos", json=_order_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["codigo_pedido"] == "PED-900"
    assert body["ubicacion"]["type"] == "Point"
    assert body["ubicacion"]["coordinates"] == [-75.21, -12.06806]
    assert body["estado"] == "pending"

    duplicate = await client.post("/api/v1/pedidos", json=_order_payload())
    assert duplicate.status_code == 400

    outside = await client.post("/api/v1/pedidos", json=_order_payload(codigo_pedido="PED-901", lat=-10.0))
    assert outside.status_code == 400

    inverted = await client.post(
        "/api/v1/pedidos",
        json=_order_payload(
            codigo_pedido="PED-902",
            ventana_inicio="2026-10-07T12:00:00-05:00",
            ventana_fin="2026-10-07T09:00:00-05:00",
        ),
    )
    assert inverted.status_code == 400


@pytest.mark.asyncio
async def test_optimize_routes_returns_geojson_and_then_404(client: AsyncClient) -> None:
    first = await client.post("/api/v1/optimizar-rutas")
    assert first.status_code == 201
    payload = first.json()
    assert payload["type"] == "FeatureCollection"
    kinds = {feature["geometry"]["type"] for feature in payload["features"]}
    assert "Point" in kinds
    assert "LineString" in kinds
    metadata = payload["metadata"]
    assert metadata["pedidos"] == 5
    assert metadata["vehiculos_usados"] == 2
    assert metadata["distancia_total_km"] > 0
    assert metadata["co2_evitado_kg"] >= 0
    assert metadata["arboles_quinual_eq"] == pytest.approx(metadata["co2_evitado_kg"] / 12.0)
    assert metadata["quinual_kg_co2_por_ano"] == 12.0

    pending = await client.get("/api/v1/pedidos")
    assert pending.status_code == 200
    assert pending.json() == []

    active = await client.get("/api/v1/rutas/activas", params={"placa": "W4U-158"})
    assert active.status_code == 200
    route = active.json()
    assert route["codigo"].startswith("SOL-")
    deliveries = [stop for stop in route["paradas"] if stop["tipo_parada"] == "delivery"]
    assert deliveries
    assert deliveries[0]["cliente_nombre"]
    assert deliveries[0]["direccion_referencia"]
    assert deliveries[0]["peso_kg"] > 0
    assert isinstance(deliveries[0]["lat"], float)

    tracked = await client.get(f"/api/v1/seguimiento/{deliveries[0]['codigo_pedido']}")
    assert tracked.status_code == 200
    card = tracked.json()
    assert card["codigo_pedido"] == deliveries[0]["codigo_pedido"]
    assert card["paradas_previas"] >= 0
    assert card["co2_evitado_kg"] >= 0
    assert card["lat"]

    missing = await client.get("/api/v1/seguimiento/NO-EXISTE")
    assert missing.status_code == 404

    second = await client.post("/api/v1/optimizar-rutas")
    assert second.status_code == 404
