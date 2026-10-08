"""Canales WebSocket del conductor y del seguimiento de un pedido.

`/ws/driver/{driver_id}` recibe el GPS y los imprevistos, y devuelve la ETA.
`/ws/tracking/{order_code}` escucha esa misma ETA. El código `despacho` une
al administrador con todos los eventos de la flota.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import async_session_factory
from app.models.domain import Deposito, Pedido, RutaDetalle, SolucionRuta, Vehiculo
from app.models.enums import EstadoPedido
from app.services.realtime_router import (
    ADMIN_CHANNEL,
    GpsFix,
    IncidentKind,
    LiveReroute,
    RoadIncident,
    coordinates_in_valley,
    estimate_eta,
    eta_payload,
    fleet_state,
    manager,
    reoptimize_live_route,
    route_payload,
)

logger = logging.getLogger("ecologistica.realtime")
router = APIRouter(tags=["tiempo-real"])
LIMA = ZoneInfo("America/Lima")
MAX_MESSAGE_CHARS = 8_000


@router.websocket("/ws/driver/{driver_id}")
async def driver_socket(websocket: WebSocket, driver_id: str) -> None:
    """Recibe coordenadas e imprevistos y empuja la ETA recalculada."""
    if not _valid_driver_id(driver_id):
        await websocket.close(code=1008)
        return
    await manager.connect_driver(driver_id, websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            if len(raw) > MAX_MESSAGE_CHARS:
                await manager.publish(
                    {"type": "error", "detail": "Mensaje demasiado largo."},
                    driver_id=driver_id,
                )
                continue
            await _on_driver_message(driver_id, raw)
    except WebSocketDisconnect:
        logger.info("El conductor %s cerró el canal.", driver_id)
    finally:
        await manager.disconnect_driver(driver_id, websocket)


@router.websocket("/ws/tracking/{order_code}")
async def tracking_socket(websocket: WebSocket, order_code: str) -> None:
    """Entrega al cliente, o al despacho, la posición y la ETA del pedido."""
    if not _valid_order_code(order_code):
        await websocket.close(code=1008)
        return
    await manager.connect_tracker(order_code, websocket)
    try:
        snapshot = await _tracking_snapshot(order_code)
        if snapshot is not None:
            await websocket.send_json(snapshot)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info("Seguimiento cerrado para %s.", order_code)
    finally:
        await manager.disconnect_tracker(order_code, websocket)


async def _on_driver_message(driver_id: str, raw: str) -> None:
    try:
        message = json.loads(raw)
    except json.JSONDecodeError:
        await manager.publish({"type": "error", "detail": "JSON inválido."}, driver_id=driver_id)
        return
    if not isinstance(message, dict) or not isinstance(message.get("type"), str):
        await manager.publish(
            {"type": "error", "detail": "El mensaje necesita un type."},
            driver_id=driver_id,
        )
        return

    kind = message["type"]
    try:
        if kind == "position":
            await _on_position(driver_id, message)
        elif kind == "incident":
            await _on_incident(driver_id, message)
        elif kind == "cancel_order":
            await _on_cancel(driver_id, message)
        elif kind == "add_order":
            await _on_add(driver_id, message)
        else:
            await manager.publish(
                {"type": "error", "detail": f"Tipo de mensaje no reconocido: {kind}."},
                driver_id=driver_id,
            )
    except ValueError as exc:
        await manager.publish({"type": "error", "detail": str(exc)}, driver_id=driver_id)
    except Exception:
        logger.exception("Fallo al procesar %s del conductor %s.", kind, driver_id)
        await manager.publish(
            {"type": "error", "detail": "No se pudo procesar el evento."},
            driver_id=driver_id,
        )


async def _on_position(driver_id: str, message: dict[str, Any]) -> None:
    fix = _fix_from_message(message)
    vehicle_id = _optional_int(message.get("vehicle_id"))
    order_code = _optional_code(message.get("order_code"))
    live = await fleet_state.remember_position(driver_id, fix, vehicle_id, order_code)
    now = fix.recorded_at
    async with async_session_factory() as session:
        order = await _order_by_code(session, order_code) if order_code else None
        if order is not None and order.estado in {EstadoPedido.ASSIGNED, EstadoPedido.PENDING}:
            order.estado = EstadoPedido.IN_TRANSIT
            await session.commit()
            await _publish_status(order_code, EstadoPedido.IN_TRANSIT.value, driver_id)
        incidents = await fleet_state.snapshot_incidents()
        update = estimate_eta(driver_id, fix, order, incidents, now)
    payload = {
        "type": "position",
        "driver_id": driver_id,
        "vehicle_id": live.vehicle_id,
        "lat": fix.latitude,
        "lon": fix.longitude,
        "altitud_msnm": fix.altitude_m,
        "order_code": order_code,
        "recorded_at": now.isoformat(),
    }
    await manager.publish(payload, driver_id=driver_id, order_codes=_codes(order_code, live.remaining_codes))
    await manager.publish(
        eta_payload(update),
        driver_id=driver_id,
        order_codes=_codes(update.order_code),
    )


async def _on_incident(driver_id: str, message: dict[str, Any]) -> None:
    incident = _incident_from_message(message)
    await fleet_state.add_incident(incident)
    alert = {
        "type": "incident",
        "driver_id": driver_id,
        "kind": incident.kind.value,
        "lat": incident.latitude,
        "lon": incident.longitude,
        "radius_km": incident.radius_km,
        "note": incident.note,
    }
    await manager.publish(alert, driver_id=driver_id)
    await _reroute(driver_id, reason=incident.kind.value)


async def _on_cancel(driver_id: str, message: dict[str, Any]) -> None:
    code = _required_code(message.get("order_code"))
    async with async_session_factory() as session:
        order = await _require_order(session, code)
        order.estado = EstadoPedido.CANCELLED
        await session.commit()
    await _publish_status(code, EstadoPedido.CANCELLED.value, driver_id)
    await _reroute(driver_id, reason="cancel", cancel_codes=(code,))


async def _on_add(driver_id: str, message: dict[str, Any]) -> None:
    code = _required_code(message.get("order_code"))
    async with async_session_factory() as session:
        order = await _require_order(session, code)
        if order.estado not in {EstadoPedido.PENDING, EstadoPedido.ASSIGNED}:
            raise ValueError(f"El pedido {code} no se puede insertar en la ruta.")
    await _reroute(driver_id, reason="priority", add_codes=(code,))


async def _reroute(
    driver_id: str,
    *,
    reason: str,
    cancel_codes: tuple[str, ...] = (),
    add_codes: tuple[str, ...] = (),
) -> None:
    live = await fleet_state.driver(driver_id)
    if live.fix is None:
        raise ValueError("Hace falta una posición GPS antes de recalcular la ruta.")
    incidents = await fleet_state.snapshot_incidents()
    async with async_session_factory() as session:
        depot, vehicle, remaining = await _load_route(session, live)
        by_code = {order.codigo_pedido: order for order in remaining}
        for code in cancel_codes:
            order = by_code.get(code) or await _require_order(session, code)
            by_code[order.codigo_pedido] = order
        added = []
        for code in add_codes:
            order = await _require_order(session, code)
            added.append(order)
        cancel_ids = [order.id for order in by_code.values() if order.codigo_pedido in cancel_codes]
        reroute = reoptimize_live_route(
            vehicle=vehicle,
            depot=depot,
            origin=live.fix,
            remaining_orders=list(by_code.values()),
            incidents=incidents,
            cancel_ids=cancel_ids,
            added_orders=added,
            reason=reason,
        )
        await _apply_reroute(session, reroute, by_code, added)
        if reroute.solution is not None and reroute.solution.itineraries:
            from app.api.v1.routes import _persist_solution, retain_other_vehicles

            persisted = _persist_solution(
                session,
                depot,
                _orders_in_solution(reroute, by_code, added),
                [vehicle],
                reroute.solution,
            )
            await retain_other_vehicles(session, persisted, vehicle.id)
        await session.commit()
    await fleet_state.replace_sequence(driver_id, reroute.sequence)
    codes = list(reroute.sequence) + list(reroute.blocked_codes) + list(reroute.removed_codes)
    await manager.publish(route_payload(driver_id, reroute), driver_id=driver_id, order_codes=codes)
    for code in reroute.blocked_codes:
        await _publish_status(code, EstadoPedido.INCIDENT.value, driver_id)
    for code in add_codes:
        if code in reroute.sequence:
            await _publish_status(code, EstadoPedido.ASSIGNED.value, driver_id)
    if reroute.sequence:
        nxt = await _eta_for_code(driver_id, live.fix, reroute.sequence[0], incidents)
        if nxt is not None:
            await manager.publish(
                eta_payload(nxt),
                driver_id=driver_id,
                order_codes=[nxt.order_code] if nxt.order_code else [],
            )


async def _apply_reroute(
    session: AsyncSession,
    reroute: LiveReroute,
    by_code: dict[str, Pedido],
    added: list[Pedido],
) -> None:
    for code in reroute.blocked_codes:
        order = by_code.get(code)
        if order is not None:
            order.estado = EstadoPedido.INCIDENT
    for order in added:
        if order.codigo_pedido not in reroute.blocked_codes:
            order.estado = EstadoPedido.ASSIGNED
    await session.flush()


def _orders_in_solution(reroute: LiveReroute, by_code: dict[str, Pedido], added: list[Pedido]) -> list[Pedido]:
    catalog = dict(by_code)
    for order in added:
        catalog[order.codigo_pedido] = order
    return [catalog[code] for code in reroute.sequence if code in catalog]


async def _load_route(session: AsyncSession, live: Any) -> tuple[Deposito, Vehiculo, list[Pedido]]:
    depot = await session.scalar(select(Deposito).order_by(Deposito.id).limit(1))
    if depot is None:
        raise ValueError("No hay un depósito configurado.")
    vehicle = await _vehicle_for_driver(session, live.driver_id, live.vehicle_id)
    remaining = await _remaining_for_vehicle(session, vehicle, live.remaining_codes)
    return depot, vehicle, remaining


async def _remaining_for_vehicle(
    session: AsyncSession,
    vehicle: Vehiculo,
    codes: list[str],
) -> list[Pedido]:
    """Usa la secuencia en memoria o, si aún no hay, la última solución de ese vehículo."""
    closed = {EstadoPedido.DELIVERED, EstadoPedido.CANCELLED, EstadoPedido.INCIDENT}
    if codes:
        result = await session.scalars(select(Pedido).where(Pedido.codigo_pedido.in_(codes)))
        by_code = {order.codigo_pedido: order for order in result.all()}
        return [by_code[code] for code in codes if code in by_code and by_code[code].estado not in closed]
    solution = await session.scalar(
        select(SolucionRuta)
        .options(selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.pedido))
        .order_by(SolucionRuta.id.desc())
        .limit(1)
    )
    if solution is None:
        return []
    remaining: list[Pedido] = []
    for detail in solution.detalles:
        order = detail.pedido
        if detail.vehiculo_id != vehicle.id or order is None or order.estado in closed:
            continue
        remaining.append(order)
    return remaining


async def _vehicle_for_driver(session: AsyncSession, driver_id: str, vehicle_id: int | None) -> Vehiculo:
    if vehicle_id is not None:
        vehicle = await session.get(Vehiculo, vehicle_id)
        if vehicle is None or not vehicle.activo:
            raise ValueError("El vehículo indicado no está activo.")
        return vehicle
    if driver_id.isdigit():
        vehicle = await session.get(Vehiculo, int(driver_id))
        if vehicle is not None and vehicle.activo:
            return vehicle
    vehicle = await session.scalar(select(Vehiculo).where(Vehiculo.placa == driver_id, Vehiculo.activo.is_(True)))
    if vehicle is None:
        raise ValueError("No hay un vehículo activo para ese conductor.")
    return vehicle


async def _order_by_code(session: AsyncSession, code: str | None) -> Pedido | None:
    if not code:
        return None
    return await session.scalar(select(Pedido).where(Pedido.codigo_pedido == code))


async def _require_order(session: AsyncSession, code: str) -> Pedido:
    order = await _order_by_code(session, code)
    if order is None:
        raise ValueError(f"No existe el pedido {code}.")
    return order


async def _eta_for_code(driver_id: str, origin: GpsFix, code: str, incidents: tuple[RoadIncident, ...]) -> Any:
    async with async_session_factory() as session:
        order = await _order_by_code(session, code)
    if order is None:
        return None
    return estimate_eta(driver_id, origin, order, incidents, origin.recorded_at)


async def _tracking_snapshot(order_code: str) -> dict[str, Any] | None:
    if order_code == ADMIN_CHANNEL:
        return {"type": "hello", "channel": ADMIN_CHANNEL}
    drivers = await fleet_state.drivers_snapshot()
    for live in drivers:
        if live.fix is None:
            continue
        if order_code not in live.remaining_codes and live.active_order_code != order_code:
            continue
        async with async_session_factory() as session:
            order = await _order_by_code(session, order_code)
        incidents = await fleet_state.snapshot_incidents()
        update = estimate_eta(live.driver_id, live.fix, order, incidents, live.fix.recorded_at)
        return {
            "type": "position",
            "driver_id": live.driver_id,
            "vehicle_id": live.vehicle_id,
            "lat": live.fix.latitude,
            "lon": live.fix.longitude,
            "altitud_msnm": live.fix.altitude_m,
            "order_code": order_code,
            "recorded_at": live.fix.recorded_at.isoformat(),
            **{key: value for key, value in eta_payload(update).items() if key != "type"},
            "eta_type": "eta",
        }
    return None


async def _publish_status(order_code: str, estado: str, driver_id: str) -> None:
    await manager.publish(
        {"type": "order_status", "order_code": order_code, "estado": estado, "driver_id": driver_id},
        driver_id=driver_id,
        order_codes=[order_code],
    )


def _fix_from_message(message: dict[str, Any]) -> GpsFix:
    try:
        latitude = float(message["lat"])
        longitude = float(message["lon"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("La posición necesita lat y lon numéricos.") from exc
    if not coordinates_in_valley(latitude, longitude):
        raise ValueError("La coordenada queda fuera del valle del Mantaro.")
    altitude = message.get("altitud_msnm", 3270)
    try:
        altitude_m = float(altitude)
    except (TypeError, ValueError) as exc:
        raise ValueError("La altitud debe ser numérica.") from exc
    if not 2500 <= altitude_m <= 5000:
        raise ValueError("La altitud queda fuera de la banda operativa.")
    return GpsFix(latitude, longitude, altitude_m, datetime.now(LIMA))


def _incident_from_message(message: dict[str, Any]) -> RoadIncident:
    try:
        kind = IncidentKind(str(message.get("kind", "")))
    except ValueError as exc:
        raise ValueError("El incidente debe ser traffic, landslide o blockade.") from exc
    try:
        latitude = float(message["lat"])
        longitude = float(message["lon"])
        radius_km = float(message.get("radius_km", 0.3))
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("El incidente necesita lat, lon y radius_km.") from exc
    if not coordinates_in_valley(latitude, longitude):
        raise ValueError("El incidente queda fuera del valle del Mantaro.")
    if not 0.05 <= radius_km <= 5:
        raise ValueError("El radio del incidente debe estar entre 0.05 km y 5 km.")
    note = str(message.get("note", ""))[:240]
    return RoadIncident(latitude, longitude, radius_km, kind, note)


def _codes(*groups: str | None | list[str]) -> list[str]:
    found: list[str] = []
    for group in groups:
        if group is None:
            continue
        if isinstance(group, str):
            if group and group not in found:
                found.append(group)
            continue
        for code in group:
            if code and code not in found:
                found.append(code)
    return found


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("vehicle_id debe ser entero.") from exc


def _optional_code(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return _required_code(value)


def _required_code(value: Any) -> str:
    if not isinstance(value, str) or not _valid_order_code(value) or value == ADMIN_CHANNEL:
        raise ValueError("Código de pedido inválido.")
    return value


def _valid_driver_id(value: str) -> bool:
    return 1 <= len(value) <= 32 and all(char.isalnum() or char in "-_" for char in value)


def _valid_order_code(value: str) -> bool:
    return 1 <= len(value) <= 32 and all(char.isalnum() or char in "-_" for char in value)
