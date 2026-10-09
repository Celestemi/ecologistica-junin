"""Re-optimización en ruta y reparto de eventos por WebSocket."""

from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.main import app
from app.models.enums import TipoCombustible
from app.services.realtime_router import (
    ConnectionManager,
    GpsFix,
    IncidentKind,
    RoadIncident,
    adjusted_leg_km,
    reoptimize_live_route,
)

LIMA = ZoneInfo("America/Lima")
DAY = datetime(2026, 10, 6, tzinfo=LIMA)
ORIGIN = GpsFix(-12.0600, -75.2100, 3270.0, DAY)


class FakeSocket:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.accepted = False
        self.sent: list[dict] = []

    async def accept(self) -> None:
        self.accepted = True

    async def send_json(self, payload: dict) -> None:
        if self.fail:
            raise RuntimeError("socket cerrado")
        self.sent.append(payload)

    async def close(self) -> None:
        return None


def _point(lon: float, lat: float) -> dict[str, object]:
    return {"type": "Point", "coordinates": [lon, lat]}


def _depot() -> SimpleNamespace:
    return SimpleNamespace(
        nombre="Depósito Principal El Tambo",
        ubicacion=_point(-75.2120, -12.0520),
        altitud_msnm=3250.0,
    )


def _vehicle() -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        placa="W4U-158",
        capacidad_kg=1500.0,
        capacidad_m3=9.0,
        tipo_combustible=TipoCombustible.DIESEL,
        emision_base_co2_g_km=220.0,
        factor_penalizacion_pendiente=0.045,
        activo=True,
    )


def _order(order_id: int, lat: float, start_hour: int, end_hour: int) -> SimpleNamespace:
    return SimpleNamespace(
        id=order_id,
        codigo_pedido=f"PED-{order_id:03d}",
        cliente_nombre=f"Cliente {order_id}",
        ubicacion=_point(-75.2100, lat),
        altitud_msnm=3270.0,
        peso_kg=20.0,
        ventana_inicio=DAY.replace(hour=start_hour),
        ventana_fin=DAY.replace(hour=end_hour),
    )


def _solve(**kwargs):
    base = {
        "vehicle": _vehicle(),
        "depot": _depot(),
        "origin": ORIGIN,
        "remaining_orders": [_order(1, -12.0700, 8, 12), _order(2, -12.0800, 9, 14)],
        "generations": 8,
        "population_size": 6,
        "seed": 3,
    }
    base.update(kwargs)
    return reoptimize_live_route(**base)


def test_traffic_slows_the_crossed_leg_and_a_blockade_adds_a_detour() -> None:
    direct = 2.0
    traffic = RoadIncident(-12.0650, -75.2100, 0.3, IncidentKind.TRAFFIC, "cola en Real")
    blockade = RoadIncident(-12.0650, -75.2100, 0.3, IncidentKind.BLOCKADE, "vía cerrada")
    slowed = adjusted_leg_km(-12.0600, -75.2100, -12.0700, -75.2100, direct, [traffic])
    detoured = adjusted_leg_km(-12.0600, -75.2100, -12.0700, -75.2100, direct, [blockade])
    untouched = adjusted_leg_km(-12.0900, -75.2100, -12.0950, -75.2100, direct, [traffic])
    assert slowed == pytest.approx(direct * 1.8)
    assert detoured == pytest.approx(direct + 0.6)
    assert untouched == pytest.approx(direct)


def test_live_reroute_drops_cancelled_and_blocked_stops_and_inserts_a_priority() -> None:
    plain = _solve(reason="baseline", incidents=())
    traffic = RoadIncident(-12.0650, -75.2100, 0.25, IncidentKind.TRAFFIC)
    slowed = _solve(reason="traffic", incidents=[traffic])
    assert plain.solution is not None and slowed.solution is not None
    assert slowed.solution.distance_km > plain.solution.distance_km

    landslide = RoadIncident(-12.0700, -75.2100, 0.05, IncidentKind.LANDSLIDE, "talud")
    blocked = _solve(reason="landslide", incidents=[landslide])
    assert blocked.blocked_codes == ("PED-001",)
    assert blocked.sequence == ("PED-002",)

    cancelled = _solve(reason="cancel", cancel_ids=[1])
    assert cancelled.removed_codes == ("PED-001",)
    assert cancelled.sequence == ("PED-002",)

    extra = _order(3, -12.0750, 10, 15)
    inserted = _solve(reason="priority", added_orders=[extra])
    assert "PED-003" in inserted.sequence


@pytest.mark.asyncio
async def test_connection_manager_fans_out_and_drops_dead_sockets() -> None:
    sockets = ConnectionManager()
    driver = FakeSocket()
    watcher = FakeSocket()
    desk = FakeSocket()
    dead = FakeSocket(fail=True)
    await sockets.connect_driver("W4U-158", driver)
    await sockets.connect_tracker("PED-001", watcher)
    await sockets.connect_tracker("despacho", desk)
    await sockets.connect_tracker("PED-001", dead)
    await sockets.publish(
        {"type": "eta", "order_code": "PED-001"},
        driver_id="W4U-158",
        order_codes=["PED-001"],
    )
    assert driver.sent == watcher.sent == desk.sent
    assert dead.sent == []
    await sockets.publish({"type": "position"}, driver_id="W4U-158", order_codes=["PED-001"])
    assert len(watcher.sent) == 2


@pytest.mark.asyncio
async def test_driver_socket_rejects_a_fix_outside_the_valley(client: AsyncClient) -> None:
    from tests.helpers import login_headers

    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    token = headers["Authorization"].removeprefix("Bearer ")
    with TestClient(app) as sync:
        with pytest.raises(WebSocketDisconnect):
            with sync.websocket_connect("/ws/driver/W4U-158") as socket:
                socket.receive_text()
        with sync.websocket_connect(f"/ws/driver/W4U-158?token={token}") as socket:
            socket.send_json({"type": "position", "lat": 0, "lon": 0})
            body = socket.receive_json()
    assert body["type"] == "error"
    assert "Mantaro" in body["detail"]


@pytest.mark.asyncio
async def test_tracking_desk_receives_the_hello_and_a_bad_driver_id_is_refused(client: AsyncClient) -> None:
    from tests.helpers import login_headers

    headers = await login_headers(client, "operador@distrirapido.pe", "Operador.2026")
    token = headers["Authorization"].removeprefix("Bearer ")
    with TestClient(app) as sync:
        with pytest.raises(WebSocketDisconnect):
            with sync.websocket_connect("/ws/tracking/despacho") as socket:
                socket.receive_text()
        with sync.websocket_connect(f"/ws/tracking/despacho?token={token}") as socket:
            hello = socket.receive_json()
        assert hello["channel"] == "despacho"
        with pytest.raises(WebSocketDisconnect):
            with sync.websocket_connect(f"/ws/driver/placa con espacios?token={token}") as socket:
                socket.receive_text()
