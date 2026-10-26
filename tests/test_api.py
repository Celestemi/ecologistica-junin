"""Integración HTTP de pedidos, flota y optimización VRPTW."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from httpx import AsyncClient

from tests.helpers import login_headers

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
    anonymous_orders = await client.get("/api/v1/pedidos")
    assert anonymous_orders.status_code == 401

    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    vehicles = await client.get("/api/v1/vehiculos", headers=headers)
    orders = await client.get("/api/v1/pedidos", headers=headers)
    assert vehicles.status_code == 200
    assert orders.status_code == 200
    plates = {item["placa"] for item in vehicles.json()}
    codes = {item["codigo_pedido"] for item in orders.json()}
    assert plates == {"W4U-158", "E7M-304"}
    assert {"PED-001", "PED-002", "PED-003", "PED-004", "PED-005"} <= codes
    assert all(item["estado"] == "pending" for item in orders.json())


@pytest.mark.asyncio
async def test_create_order_and_reject_invalid_payloads(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    created = await client.post("/api/v1/pedidos", json=_order_payload(), headers=headers)
    assert created.status_code == 201
    body = created.json()
    assert body["codigo_pedido"] == "PED-900"
    assert body["ubicacion"]["type"] == "Point"
    assert body["ubicacion"]["coordinates"] == [-75.21, -12.06806]
    assert body["estado"] == "pending"

    duplicate = await client.post("/api/v1/pedidos", json=_order_payload(), headers=headers)
    assert duplicate.status_code == 400

    outside = await client.post("/api/v1/pedidos", json=_order_payload(codigo_pedido="PED-901", lat=-10.0), headers=headers)
    assert outside.status_code == 400

    inverted = await client.post(
        "/api/v1/pedidos",
        json=_order_payload(
            codigo_pedido="PED-902",
            ventana_inicio="2026-10-07T12:00:00-05:00",
            ventana_fin="2026-10-07T09:00:00-05:00",
        ),
        headers=headers,
    )
    assert inverted.status_code == 400


@pytest.mark.asyncio
async def test_optimize_routes_returns_geojson_and_then_404(client: AsyncClient) -> None:
    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    first = await client.post("/api/v1/optimizar-rutas", headers=headers)
    assert first.status_code == 201
    payload = first.json()
    assert payload["type"] == "FeatureCollection"
    kinds = {feature["geometry"]["type"] for feature in payload["features"]}
    assert "Point" in kinds
    metadata = payload["metadata"]
    if metadata.get("geometria_vial_disponible"):
        assert "LineString" in kinds
    assert metadata["pedidos"] == 5
    assert 1 <= metadata["vehiculos_usados"] <= 2
    assert metadata["distancia_total_km"] > 0
    assert metadata["co2_evitado_kg"] >= 0
    assert metadata["arboles_quinual_eq"] == pytest.approx(metadata["co2_evitado_kg"] / 12.0)
    assert metadata["quinual_kg_co2_por_ano"] == 12.0

    operation_day = metadata["fecha_operacion"]
    indicators = await client.get(
        f"/api/v1/indicadores?fecha_inicio={operation_day}&fecha_fin={operation_day}",
        headers=headers,
    )
    assert indicators.status_code == 200
    consolidated = indicators.json()
    assert consolidated["rutas"] == 1
    assert consolidated["distancia_total_km"] == pytest.approx(metadata["distancia_total_km"])
    assert consolidated["consumo_estimado_gal"] is not None
    assert consolidated["arboles_quinual_eq"] == pytest.approx(consolidated["co2_evitado_kg"] / 12.0)

    pending = await client.get("/api/v1/pedidos", headers=headers)
    assert pending.status_code == 200
    assert pending.json() == []

    published = await client.get("/api/v1/rutas/mapa", headers=headers)
    assert published.status_code == 200
    map_plates = {
        feature["properties"].get("plate")
        for feature in published.json()["features"]
        if feature["geometry"]["type"] == "Point" and feature["properties"].get("stop_type") == "delivery"
    }
    assert map_plates <= {"W4U-158", "E7M-304"}
    assert len(map_plates) == metadata["vehiculos_usados"]
    # US-011: el mismo GeoJSON autorizado que pinta el mapa entrega el detalle
    # necesario para la parada, sin construir datos de ejemplo en el cliente.
    map_deliveries = [
        feature["properties"]
        for feature in published.json()["features"]
        if feature["geometry"]["type"] == "Point" and feature["properties"].get("stop_type") == "delivery"
    ]
    assert map_deliveries
    assert all(item["customer"] and item["address"] and item["weight_kg"] > 0 for item in map_deliveries)

    route_plates = {
        feature["properties"].get("plate")
        for feature in payload["features"]
        if feature["geometry"]["type"] == "LineString"
    }
    if not route_plates:
        route_plates = map_plates
    active_plate = next(iter(route_plates))
    active = await client.get("/api/v1/rutas/activas", params={"placa": active_plate}, headers=headers)
    assert active.status_code == 200
    route = active.json()
    assert route["codigo"].startswith("SOL-")
    deliveries = [stop for stop in route["paradas"] if stop["tipo_parada"] == "delivery"]
    assert deliveries
    assert deliveries[0]["cliente_nombre"]
    assert deliveries[0]["direccion_referencia"]
    assert deliveries[0]["peso_kg"] > 0
    assert isinstance(deliveries[0]["lat"], float)

    code = deliveries[0]["codigo_pedido"]
    denied_public = await client.get(f"/api/v1/seguimiento/{code}")
    assert denied_public.status_code == 401

    tracked = await client.get(f"/api/v1/seguimiento/{code}", headers=headers)
    assert tracked.status_code == 200
    card = tracked.json()
    assert card["codigo_pedido"] == code
    token = card["token_seguimiento"]
    assert token

    public = await client.get(f"/api/v1/seguimiento/publico/{token}")
    assert public.status_code == 200
    public_card = public.json()
    assert "cliente_nombre" not in public_card
    assert public_card["zona_entrega"]
    assert public_card["paradas_previas"] >= 0

    missing = await client.get("/api/v1/seguimiento/publico/00000000-0000-4000-8000-000000000000")
    assert missing.status_code == 404

    second = await client.post("/api/v1/optimizar-rutas", headers=headers)
    assert second.status_code == 404
