"""Re-enrutamiento en caliente y estado de las conexiones en tiempo real.

Una ruta en ejecución se recalcula desde el GPS del conductor, no desde el
depósito. Un deslizamiento o un bloqueo que cae encima de una parada la saca
de la secuencia. El tráfico pesado no la cancela: alarga el tramo que lo
atraviesa para que el genético busque otro orden. Un pedido nuevo se inserta
en esa misma corrida; uno cancelado sale antes de volver a optimizar.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from math import cos, radians, sqrt
from typing import Any

from starlette.websockets import WebSocket

from app.core.geo import geometry_to_geojson
from app.models.domain import Deposito, Pedido, Vehiculo
from app.services.genetic_solver import (
    RouteSolution,
    haversine_km,
    solve_vrptw,
    travel_minutes,
)

logger = logging.getLogger("ecologistica.realtime")

# Misma caja del valle que usa el alta de pedidos.
LAT_RANGE = (-12.30, -11.70)
LON_RANGE = (-75.50, -74.90)
ADMIN_CHANNEL = "despacho"
TRAFFIC_SLOWDOWN = 1.8
REALTIME_GENERATIONS = 40
REALTIME_POPULATION = 20

class IncidentKind(str, Enum):
    """Imprevisto que obliga a mirar de nuevo la secuencia."""

    TRAFFIC = "traffic"
    LANDSLIDE = "landslide"
    BLOCKADE = "blockade"


_BLOCKING = {IncidentKind.LANDSLIDE, IncidentKind.BLOCKADE}


@dataclass(frozen=True)
class RoadIncident:
    """Círculo sobre la vía. El radio va en kilómetros."""

    latitude: float
    longitude: float
    radius_km: float
    kind: IncidentKind
    note: str = ""


@dataclass(frozen=True)
class GpsFix:
    """Última posición conocida de un conductor."""

    latitude: float
    longitude: float
    altitude_m: float
    recorded_at: datetime


@dataclass(frozen=True)
class EtaUpdate:
    """Llegada estimada al siguiente pedido, ya con el rodeo si lo hay."""

    driver_id: str
    order_code: str | None
    eta: datetime | None
    distance_km: float
    minutes: float


@dataclass(frozen=True)
class LiveReroute:
    """Resultado de re-insertar o de recalcular una ruta que ya salió."""

    reason: str
    solution: RouteSolution | None
    sequence: tuple[str, ...]
    blocked_codes: tuple[str, ...]
    removed_codes: tuple[str, ...]


@dataclass
class LiveDriver:
    """Estado en memoria de una unidad que está repartiendo."""

    driver_id: str
    vehicle_id: int | None = None
    fix: GpsFix | None = None
    active_order_code: str | None = None
    remaining_codes: list[str] = field(default_factory=list)
    updated_at: datetime | None = None


class FleetState:
    """Posiciones, incidentes y candados por conductor."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self.drivers: dict[str, LiveDriver] = {}
        self.incidents: list[RoadIncident] = []

    async def driver(self, driver_id: str) -> LiveDriver:
        async with self._lock:
            current = self.drivers.get(driver_id)
            if current is None:
                current = LiveDriver(driver_id=driver_id)
                self.drivers[driver_id] = current
            return current

    async def remember_position(
        self,
        driver_id: str,
        fix: GpsFix,
        vehicle_id: int | None,
        order_code: str | None,
    ) -> LiveDriver:
        async with self._lock:
            current = self.drivers.get(driver_id)
            if current is None:
                current = LiveDriver(driver_id=driver_id)
                self.drivers[driver_id] = current
            current.fix = fix
            current.updated_at = fix.recorded_at
            if vehicle_id is not None:
                current.vehicle_id = vehicle_id
            if order_code:
                current.active_order_code = order_code
            return current

    async def drivers_snapshot(self) -> tuple[LiveDriver, ...]:
        async with self._lock:
            return tuple(self.drivers.values())

    async def replace_sequence(self, driver_id: str, codes: Sequence[str]) -> None:
        async with self._lock:
            current = self.drivers.get(driver_id)
            if current is None:
                current = LiveDriver(driver_id=driver_id)
                self.drivers[driver_id] = current
            current.remaining_codes = list(codes)

    async def add_incident(self, incident: RoadIncident) -> None:
        async with self._lock:
            self.incidents.append(incident)

    async def snapshot_incidents(self) -> tuple[RoadIncident, ...]:
        async with self._lock:
            return tuple(self.incidents)


class ConnectionManager:
    """Reparte GPS, alertas y cambios de estado sin pisar el diccionario de sockets."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._drivers: dict[str, WebSocket] = {}
        self._trackers: dict[str, set[WebSocket]] = {}
        self._admins: set[WebSocket] = set()

    async def connect_driver(self, driver_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            previous = self._drivers.get(driver_id)
            self._drivers[driver_id] = websocket
        if previous is not None and previous is not websocket:
            await _close_quietly(previous)

    async def disconnect_driver(self, driver_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            if self._drivers.get(driver_id) is websocket:
                self._drivers.pop(driver_id, None)

    async def connect_tracker(self, order_code: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            if order_code == ADMIN_CHANNEL:
                self._admins.add(websocket)
                return
            self._trackers.setdefault(order_code, set()).add(websocket)

    async def disconnect_tracker(self, order_code: str, websocket: WebSocket) -> None:
        async with self._lock:
            self._admins.discard(websocket)
            room = self._trackers.get(order_code)
            if room is None:
                return
            room.discard(websocket)
            if not room:
                self._trackers.pop(order_code, None)

    async def publish(
        self,
        payload: dict[str, Any],
        *,
        driver_id: str | None = None,
        order_codes: Iterable[str] = (),
    ) -> None:
        """Envía fuera del candado. Un socket muerto se retira al terminar."""
        async with self._lock:
            targets: list[WebSocket] = list(self._admins)
            if driver_id is not None:
                driver_socket = self._drivers.get(driver_id)
                if driver_socket is not None:
                    targets.append(driver_socket)
            for code in order_codes:
                targets.extend(self._trackers.get(code, ()))
        seen: set[int] = set()
        dead: list[WebSocket] = []
        for socket in targets:
            identity = id(socket)
            if identity in seen:
                continue
            seen.add(identity)
            try:
                await socket.send_json(payload)
            except Exception:
                logger.info("Socket cerrado durante un envío de %s.", payload.get("type"))
                dead.append(socket)
        if dead:
            async with self._lock:
                for socket in dead:
                    self._drop(socket)

    def _drop(self, websocket: WebSocket) -> None:
        stale = [key for key, socket in self._drivers.items() if socket is websocket]
        for key in stale:
            self._drivers.pop(key, None)
        self._admins.discard(websocket)
        empty: list[str] = []
        for code, room in self._trackers.items():
            room.discard(websocket)
            if not room:
                empty.append(code)
        for code in empty:
            self._trackers.pop(code, None)


def coordinates_in_valley(latitude: float, longitude: float) -> bool:
    """True si el punto cae en la caja operativa del Mantaro."""
    return LAT_RANGE[0] <= latitude <= LAT_RANGE[1] and LON_RANGE[0] <= longitude <= LON_RANGE[1]


def point_to_segment_km(
    latitude: float,
    longitude: float,
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Distancia en kilómetros de un punto al segmento, en proyección local."""
    px, py = _local_xy(latitude, longitude, lat1, lon1)
    bx, by = _local_xy(lat2, lon2, lat1, lon1)
    length_sq = bx * bx + by * by
    if length_sq == 0:
        return sqrt(px * px + py * py)
    projection = max(0.0, min(1.0, (px * bx + py * by) / length_sq))
    dx = px - projection * bx
    dy = py - projection * by
    return sqrt(dx * dx + dy * dy)


def leg_hits_incident(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    incident: RoadIncident,
) -> bool:
    """True si el tramo recto entra en el círculo del imprevisto."""
    return point_to_segment_km(incident.latitude, incident.longitude, lat1, lon1, lat2, lon2) <= incident.radius_km


def adjusted_leg_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    distance_km: float,
    incidents: Sequence[RoadIncident],
) -> float:
    """Kilómetros del tramo después de tráfico y de rodeos."""
    distance = distance_km
    slowdown = 1.0
    detour = 0.0
    for incident in incidents:
        if not leg_hits_incident(lat1, lon1, lat2, lon2, incident):
            continue
        if incident.kind is IncidentKind.TRAFFIC:
            slowdown = max(slowdown, TRAFFIC_SLOWDOWN)
        else:
            detour += incident.radius_km * 2.0
    return distance * slowdown + detour


def order_coordinates(order: Pedido) -> tuple[float, float]:
    """Latitud y longitud de un pedido, venga de PostGIS o de un GeoJSON."""
    geojson = geometry_to_geojson(order.ubicacion)
    longitude, latitude = geojson["coordinates"][:2]
    return float(latitude), float(longitude)


def orders_blocked_by(orders: Sequence[Pedido], incidents: Sequence[RoadIncident]) -> list[Pedido]:
    """Paradas que quedaron dentro de un deslizamiento o un cierre de vía."""
    blocked: list[Pedido] = []
    for order in orders:
        latitude, longitude = order_coordinates(order)
        for incident in incidents:
            if incident.kind not in _BLOCKING:
                continue
            if haversine_km(latitude, longitude, incident.latitude, incident.longitude) <= incident.radius_km:
                blocked.append(order)
                break
    return blocked


def estimate_eta(
    driver_id: str,
    origin: GpsFix,
    order: Pedido | None,
    incidents: Sequence[RoadIncident],
    now: datetime,
) -> EtaUpdate:
    """Minutos hasta el siguiente pedido, con la penalización del tramo si aplica."""
    if order is None:
        return EtaUpdate(driver_id, None, None, 0.0, 0.0)
    latitude, longitude = order_coordinates(order)
    direct = haversine_km(origin.latitude, origin.longitude, latitude, longitude)
    distance = adjusted_leg_km(origin.latitude, origin.longitude, latitude, longitude, direct, incidents)
    minutes = travel_minutes(distance)
    return EtaUpdate(
        driver_id=driver_id,
        order_code=str(order.codigo_pedido),
        eta=now + timedelta(minutes=minutes),
        distance_km=distance,
        minutes=minutes,
    )


def reoptimize_live_route(
    *,
    vehicle: Vehiculo,
    depot: Deposito,
    origin: GpsFix,
    remaining_orders: Sequence[Pedido],
    incidents: Sequence[RoadIncident] = (),
    cancel_ids: Iterable[int] = (),
    added_orders: Sequence[Pedido] = (),
    reason: str,
    generations: int = REALTIME_GENERATIONS,
    population_size: int = REALTIME_POPULATION,
    seed: int = 7,
) -> LiveReroute:
    """Recalcula la secuencia que todavía no se entregó.

    El origen es el GPS actual. Los pedidos cancelados salen. Los que están
    dentro de un bloqueo se informan aparte y no entran al genético. El pedido
    prioritario se suma a los que siguen pendientes y el algoritmo lo inserta
    donde menos alarga la ruta.
    """
    cancelled = {int(order_id) for order_id in cancel_ids}
    removed = [order for order in remaining_orders if int(order.id) in cancelled]
    pool = [order for order in remaining_orders if int(order.id) not in cancelled]
    known = {int(order.id) for order in pool}
    for order in added_orders:
        if int(order.id) not in known:
            pool.append(order)
            known.add(int(order.id))

    blocked = orders_blocked_by(pool, incidents)
    blocked_ids = {int(order.id) for order in blocked}
    active = [order for order in pool if int(order.id) not in blocked_ids]
    moving_depot = _depot_at(depot, origin)

    def adjust(lat1: float, lon1: float, lat2: float, lon2: float, distance_km: float) -> float:
        return adjusted_leg_km(lat1, lon1, lat2, lon2, distance_km, incidents)

    solution: RouteSolution | None
    if not active:
        solution = None
        sequence: tuple[str, ...] = ()
    else:
        solution = solve_vrptw(
            active,
            [vehicle],
            moving_depot,
            generations=generations,
            population_size=population_size,
            seed=seed,
            distance_adjuster=adjust if incidents else None,
        )
        sequence = _sequence_of(solution, int(vehicle.id))

    return LiveReroute(
        reason=reason,
        solution=solution,
        sequence=sequence,
        blocked_codes=tuple(str(order.codigo_pedido) for order in blocked),
        removed_codes=tuple(str(order.codigo_pedido) for order in removed),
    )


def eta_payload(update: EtaUpdate) -> dict[str, Any]:
    """Cuerpo JSON de una ETA para el conductor y para quien sigue el pedido."""
    return {
        "type": "eta",
        "driver_id": update.driver_id,
        "order_code": update.order_code,
        "eta": update.eta.isoformat() if update.eta is not None else None,
        "distance_km": round(update.distance_km, 3),
        "minutes": round(update.minutes, 2),
    }


def route_payload(driver_id: str, reroute: LiveReroute) -> dict[str, Any]:
    """Cuerpo JSON del itinerario recalculado."""
    solution = reroute.solution
    return {
        "type": "route_update",
        "driver_id": driver_id,
        "reason": reroute.reason,
        "sequence": list(reroute.sequence),
        "blocked": list(reroute.blocked_codes),
        "removed": list(reroute.removed_codes),
        "feasible": True if solution is None else solution.feasible,
        "distance_km": 0.0 if solution is None else round(solution.distance_km, 3),
        "co2_kg": 0.0 if solution is None else round(solution.co2_kg, 3),
        "late_minutes": 0.0 if solution is None else round(solution.late_minutes, 2),
    }


def _sequence_of(solution: RouteSolution, vehicle_id: int) -> tuple[str, ...]:
    for itinerary in solution.itineraries:
        if itinerary.vehicle_id != vehicle_id:
            continue
        return tuple(stop.order_code for stop in itinerary.stops if stop.order_code)
    return ()


def _depot_at(depot: Deposito, origin: GpsFix) -> _Origin:
    """Depósito virtual: la ruta sigue desde donde está el vehículo."""
    return _Origin(depot, origin)


class _Origin:
    """Objeto con la forma que `solve_vrptw` lee del depósito."""

    def __init__(self, depot: Deposito, origin: GpsFix) -> None:
        self.nombre = depot.nombre
        self.altitud_msnm = origin.altitude_m
        self.ubicacion = {
            "type": "Point",
            "coordinates": [origin.longitude, origin.latitude],
        }


def _local_xy(latitude: float, longitude: float, lat0: float, lon0: float) -> tuple[float, float]:
    mean_lat = radians((latitude + lat0) / 2.0)
    east_km = (longitude - lon0) * 111.32 * cos(mean_lat)
    north_km = (latitude - lat0) * 111.32
    return east_km, north_km


async def _close_quietly(websocket: WebSocket) -> None:
    try:
        await websocket.close()
    except Exception:
        logger.info("No se pudo cerrar un socket reemplazado.")


manager = ConnectionManager()
fleet_state = FleetState()
