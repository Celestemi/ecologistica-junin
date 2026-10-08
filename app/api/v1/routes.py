"""Endpoints de pedidos, flota y optimización de rutas.

`POST /optimizar-rutas` lee los pedidos pendientes y la flota activa, corre el
algoritmo genético y persiste `soluciones_ruta` junto con `rutas_detalle`.
La respuesta es un FeatureCollection listo para Leaflet. Los Quinuales salen
de `CO2 evitado (kg) / 12`.
"""

from __future__ import annotations

import io
import logging
from datetime import date, datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from geoalchemy2.elements import WKTElement
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.requests import Request

from app.core.config import get_settings
from app.core.database import get_db
from app.core.emissions import quinual_equivalent
from app.core.geo import geometry_to_geojson, point_wkt
from app.models.domain import Deposito, Pedido, RutaDetalle, SolucionRuta, Vehiculo
from app.models.enums import EstadoPedido, EstadoSolucion, TipoParada, TipoParada
from app.schemas.logistics import (
    OptimizedRouteResponse,
    DepositoRead,
    ActiveRouteRead,
    DriverStopRead,
    TrackingRead,
    PedidoCreateRequest,
    PedidoRead,
    RouteOptimizationGeoJSON,
    RouteOptimizationMetadata,
    VehiculoRead,
    _feature_collection,
)
from app.services.genetic_solver import RouteSolution, StopItinerary, solve_vrptw
from app.services.pdf_generator import build_sustainability_pdf, load_sustainability_report

logger = logging.getLogger("ecologistica.api")
LIMA = ZoneInfo("America/Lima")

API_DESCRIPTION = """
API del MVP de EcoLogística Huancayo.

Optimiza el reparto de última milla en el valle del Mantaro con un algoritmo
genético VRPTW. El mapa recibe un GeoJSON y estos indicadores:

- distancia total (km)
- CO2 de la ruta optimizada y de un FIFO de referencia
- CO2 evitado
- árboles Quinual equivalentes, con la relación **1 Quinual = 12 kg CO2/año**

Las coordenadas se guardan en WGS84 (EPSG:4326). El centro de la operación es
la Plaza Constitución.
""".strip()

OPENAPI_TAGS = [
    {
        "name": "pedidos",
        "description": "Pedidos pendientes de última milla y alta de nuevas entregas.",
    },
    {
        "name": "vehiculos",
        "description": "Flota activa disponible para el reparto.",
    },
    {
        "name": "depositos",
        "description": "Puntos de acopio que originan las rutas.",
    },
    {
        "name": "optimizacion",
        "description": "Corrida del algoritmo genético y capa GeoJSON para el mapa.",
    },
    {
        "name": "reportes",
        "description": "Informes descargables de sostenibilidad y costo de la flota.",
    },
    {
        "name": "sistema",
        "description": "Salud del proceso y de PostGIS.",
    },
]

router = APIRouter(prefix="/api/v1")


@router.get(
    "/pedidos",
    response_model=list[PedidoRead],
    tags=["pedidos"],
    summary="Listar pedidos pendientes",
)
async def list_pending_orders(session: AsyncSession = Depends(get_db)) -> list[Pedido]:
    """Devuelve los pedidos en estado pendiente, del más urgente al más tardío."""
    result = await session.scalars(
        select(Pedido)
        .where(Pedido.estado == EstadoPedido.PENDING)
        .order_by(Pedido.ventana_inicio, Pedido.id)
    )
    return list(result.all())


@router.post(
    "/pedidos",
    response_model=PedidoRead,
    status_code=status.HTTP_201_CREATED,
    tags=["pedidos"],
    summary="Crear un pedido",
    responses={400: {"description": "Datos inválidos o código de pedido duplicado."}},
)
async def create_order(
    payload: PedidoCreateRequest,
    session: AsyncSession = Depends(get_db),
) -> Pedido:
    """Crea un pedido. `lat`/`lon` se convierten a un Point PostGIS (SRID 4326)."""
    duplicate = await session.scalar(
        select(Pedido.id).where(Pedido.codigo_pedido == payload.codigo_pedido)
    )
    if duplicate is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un pedido con el código {payload.codigo_pedido}.",
        )
    order = Pedido(
        codigo_pedido=payload.codigo_pedido,
        cliente_nombre=payload.cliente_nombre,
        direccion_referencia=payload.direccion_referencia,
        ubicacion=point_wkt(payload.lon, payload.lat),
        altitud_msnm=payload.altitud_msnm,
        peso_kg=payload.peso_kg,
        ventana_inicio=_as_lima(payload.ventana_inicio),
        ventana_fin=_as_lima(payload.ventana_fin),
        estado=EstadoPedido.PENDING,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@router.get(
    "/vehiculos",
    response_model=list[VehiculoRead],
    tags=["vehiculos"],
    summary="Listar la flota disponible",
)
async def list_vehicles(session: AsyncSession = Depends(get_db)) -> list[Vehiculo]:
    """Devuelve los vehículos activos, ordenados por placa."""
    result = await session.scalars(
        select(Vehiculo).where(Vehiculo.activo.is_(True)).order_by(Vehiculo.placa, Vehiculo.id)
    )
    return list(result.all())


@router.get(
    "/depositos",
    response_model=list[DepositoRead],
    tags=["depositos"],
    summary="Listar depósitos",
)
async def list_depots(session: AsyncSession = Depends(get_db)) -> list[Deposito]:
    """Devuelve los depósitos con su punto PostGIS, para el marcador del mapa."""
    result = await session.scalars(select(Deposito).order_by(Deposito.id))
    return list(result.all())


@router.get(
    "/reportes/sostenibilidad/pdf",
    tags=["reportes"],
    summary="Descargar el informe de sostenibilidad en PDF",
    responses={
        200: {"content": {"application/pdf": {}}, "description": "PDF del periodo."},
        400: {"description": "El rango de fechas está invertido."},
    },
)
async def sustainability_pdf(
    fecha_inicio: date | None = None,
    fecha_fin: date | None = None,
    session: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Emite el informe ISO 14083 del periodo como archivo PDF."""
    try:
        report = await load_sustainability_report(session, fecha_inicio, fecha_fin)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    pdf = build_sustainability_pdf(report)
    filename = f"sostenibilidad-{report.period_start:%Y%m%d}-{report.period_end:%Y%m%d}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(pdf)),
        },
    )


@router.get(
    "/rutas/activas",
    response_model=ActiveRouteRead,
    tags=["optimizacion"],
    summary="Leer la ruta activa para el conductor",
    responses={404: {"description": "Todavía no hay una solución calculada."}},
)
async def active_route(
    placa: str | None = None,
    session: AsyncSession = Depends(get_db),
) -> ActiveRouteRead:
    """Devuelve las paradas vigentes de cada vehículo, aunque un recálculo sea más nuevo."""
    grouped = await _fleet_groups(session)
    if placa is not None:
        grouped = [details for details in grouped if details and details[0].vehiculo.placa == placa]
    if not grouped:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay una ruta activa." if placa is None else f"La placa {placa} no tiene paradas en la ruta activa.",
        )
    details = sorted(
        (detail for group in grouped for detail in group),
        key=lambda detail: (detail.vehiculo.placa, detail.secuencia),
    )
    newest = max(grouped, key=lambda group: group[0].solucion_id)
    return ActiveRouteRead(
        codigo=newest[0].solucion.codigo,
        fecha_operacion=newest[0].solucion.fecha_operacion,
        paradas=[_driver_stop(detail) for detail in details],
    )


@router.get(
    "/rutas/mapa",
    response_model=RouteOptimizationGeoJSON,
    tags=["optimizacion"],
    summary="Mapa vigente de toda la flota",
    responses={404: {"description": "Todavía no hay una solución calculada."}},
)
async def fleet_map(session: AsyncSession = Depends(get_db)) -> RouteOptimizationGeoJSON:
    """GeoJSON de la última ruta de cada vehículo. Un recálculo no borra al resto."""
    grouped = await _fleet_groups(session)
    if not grouped:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay una ruta activa.")
    details = [detail for group in grouped for detail in group]
    anchor = max((group[0].solucion for group in grouped), key=lambda item: item.id)
    deliveries = [detail for detail in details if detail.tipo_parada == TipoParada.DELIVERY]
    plates = {detail.vehiculo.placa for detail in details}
    metadata = RouteOptimizationMetadata(
        id=anchor.id,
        codigo=anchor.codigo,
        fecha_operacion=anchor.fecha_operacion,
        distancia_total_km=sum(detail.distancia_tramo_km for detail in details),
        duracion_total_min=sum(detail.tiempo_viaje_min for detail in details),
        co2_estimado_kg=anchor.co2_estimado_kg,
        co2_referencia_kg=anchor.co2_referencia_kg,
        co2_evitado_kg=anchor.co2_evitado_kg,
        arboles_quinual_eq=anchor.arboles_quinual_eq,
        quinual_kg_co2_por_ano=get_settings().quinual_kg_co2_per_year,
        fitness=anchor.fitness,
        estado=anchor.estado,
        feasible=True,
        pedidos=len(deliveries),
        vehiculos_usados=len(plates),
    )
    return RouteOptimizationGeoJSON(features=_feature_collection(details).features, metadata=metadata)


@router.get(
    "/seguimiento/{codigo_pedido}",
    response_model=TrackingRead,
    tags=["pedidos"],
    summary="Seguimiento público de un pedido",
    responses={404: {"description": "No existe ese código de pedido."}},
)
async def track_order(codigo_pedido: str, session: AsyncSession = Depends(get_db)) -> TrackingRead:
    """Devuelve destino, ETA planificada, paradas previas y el CO2 evitado de ese envío."""
    order = await session.scalar(select(Pedido).where(Pedido.codigo_pedido == codigo_pedido))
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el pedido {codigo_pedido}.",
        )
    solution = await session.scalar(
        select(SolucionRuta)
        .where(SolucionRuta.detalles.any(RutaDetalle.pedido_id == order.id))
        .options(
            selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.vehiculo),
            selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.pedido),
        )
        .order_by(SolucionRuta.id.desc())
        .limit(1)
    )
    return _tracking_read(order, solution)


@router.post(
    "/optimizar-rutas",
    response_model=RouteOptimizationGeoJSON,
    status_code=status.HTTP_201_CREATED,
    tags=["optimizacion"],
    summary="Optimizar las rutas del día",
    responses={
        400: {"description": "La corrida no pudo interpretarse."},
        404: {"description": "Falta depósito, flota activa o pedidos pendientes."},
    },
)
async def optimize_routes(
    session: AsyncSession = Depends(get_db),
) -> RouteOptimizationGeoJSON:
    """Corre el GA, guarda la solución y responde con el mapa y los KPIs."""
    depot = await _require_depot(session)
    vehicles = await _require_vehicles(session, depot.id)
    orders = await _require_pending_orders(session)
    try:
        solved = solve_vrptw(orders, vehicles, depot)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    solution = _persist_solution(session, depot, orders, vehicles, solved)
    await session.commit()
    geojson = OptimizedRouteResponse.from_solution(solution).geojson
    return RouteOptimizationGeoJSON(
        features=geojson.features,
        metadata=_metadata(solution, solved, len(orders)),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Traduce validaciones a HTTP 400 y oculta los errores no previstos."""

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "La solicitud no es válida.",
                "errors": [_public_error(error) for error in exc.errors()],
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_conflict(request: Request, exc: IntegrityError) -> JSONResponse:
        logger.info("Conflicto de integridad en %s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "El registro entra en conflicto con datos ya guardados."},
        )

    @app.exception_handler(Exception)
    async def unexpected(request: Request, exc: Exception) -> JSONResponse:
        if isinstance(exc, HTTPException):
            raise exc
        logger.exception("Error no controlado en %s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error interno al procesar la solicitud."},
        )


async def _require_depot(session: AsyncSession) -> Deposito:
    depot = await session.scalar(select(Deposito).order_by(Deposito.id).limit(1))
    if depot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay un depósito configurado.",
        )
    return depot


async def _require_vehicles(session: AsyncSession, depot_id: int) -> list[Vehiculo]:
    result = await session.scalars(
        select(Vehiculo)
        .where(Vehiculo.activo.is_(True), Vehiculo.deposito_id == depot_id)
        .order_by(Vehiculo.id)
    )
    vehicles = list(result.all())
    if not vehicles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay vehículos activos en el depósito.",
        )
    return vehicles


_CLOSED_ORDERS = {EstadoPedido.DELIVERED, EstadoPedido.CANCELLED, EstadoPedido.INCIDENT}


def _open_stop(detail: RutaDetalle) -> bool:
    """Una parada de depósito sigue. Un pedido cerrado ya no se dibuja ni se reparte."""
    if detail.pedido is None:
        return True
    return detail.pedido.estado not in _CLOSED_ORDERS


async def _fleet_groups(session: AsyncSession) -> list[list[RutaDetalle]]:
    """Última secuencia útil de cada vehículo, de la solución más reciente que aún la tenga."""
    solutions = list(
        (
            await session.scalars(
                select(SolucionRuta)
                .options(
                    selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.vehiculo),
                    selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.pedido),
                )
                .order_by(SolucionRuta.id.desc())
            )
        ).all()
    )
    chosen: dict[int, list[RutaDetalle]] = {}
    for solution in solutions:
        grouped: dict[int, list[RutaDetalle]] = {}
        for detail in solution.detalles:
            detail.solucion = solution
            grouped.setdefault(detail.vehiculo_id, []).append(detail)
        for vehicle_id, details in grouped.items():
            if vehicle_id in chosen:
                continue
            usable = [detail for detail in details if _open_stop(detail)]
            if any(detail.tipo_parada == TipoParada.DELIVERY for detail in usable):
                chosen[vehicle_id] = sorted(usable, key=lambda item: item.secuencia)
    return list(chosen.values())


async def retain_other_vehicles(session: AsyncSession, new_solution: SolucionRuta, vehicle_id: int) -> None:
    """Copia al resto de la flota dentro del recálculo para que el mapa no pierda sus pedidos."""
    await session.flush()
    previous = await session.scalar(
        select(SolucionRuta)
        .where(SolucionRuta.id != new_solution.id)
        .options(selectinload(SolucionRuta.detalles).selectinload(RutaDetalle.pedido))
        .order_by(SolucionRuta.id.desc())
        .limit(1)
    )
    if previous is None:
        return
    extra_km = 0.0
    extra_min = 0.0
    for detail in previous.detalles:
        if detail.vehiculo_id == vehicle_id or not _open_stop(detail):
            continue
        longitude, latitude = geometry_to_geojson(detail.ubicacion)["coordinates"][:2]
        session.add(
            RutaDetalle(
                solucion_id=new_solution.id,
                vehiculo_id=detail.vehiculo_id,
                pedido_id=detail.pedido_id,
                secuencia=detail.secuencia,
                tipo_parada=detail.tipo_parada,
                ubicacion=point_wkt(float(longitude), float(latitude)),
                altitud_msnm=detail.altitud_msnm,
                distancia_tramo_km=detail.distancia_tramo_km,
                desnivel_m=detail.desnivel_m,
                pendiente_pct=detail.pendiente_pct,
                tiempo_viaje_min=detail.tiempo_viaje_min,
                eta=detail.eta,
                co2_tramo_g=detail.co2_tramo_g,
            )
        )
        extra_km += detail.distancia_tramo_km
        extra_min += detail.tiempo_viaje_min
    new_solution.distancia_total_km += extra_km
    new_solution.duracion_total_min += extra_min
    new_solution.co2_referencia_kg = max(new_solution.co2_referencia_kg, previous.co2_referencia_kg)
    new_solution.co2_evitado_kg = max(new_solution.co2_evitado_kg, previous.co2_evitado_kg)
    new_solution.arboles_quinual_eq = max(new_solution.arboles_quinual_eq, previous.arboles_quinual_eq)


async def _require_pending_orders(session: AsyncSession) -> list[Pedido]:
    result = await session.scalars(
        select(Pedido)
        .where(Pedido.estado == EstadoPedido.PENDING)
        .order_by(Pedido.ventana_inicio, Pedido.id)
    )
    orders = list(result.all())
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay pedidos pendientes para optimizar.",
        )
    return orders


def _persist_solution(
    session: AsyncSession,
    depot: Deposito,
    orders: list[Pedido],
    vehicles: list[Vehiculo],
    solved: RouteSolution,
) -> SolucionRuta:
    avoided_kg = max(0.0, solved.co2_saved_kg)
    factor = get_settings().quinual_kg_co2_per_year
    operation_day = min(_as_lima(order.ventana_inicio) for order in orders).date()
    solution = SolucionRuta(
        codigo=_solution_code(operation_day),
        deposito_id=depot.id,
        fecha_operacion=operation_day,
        distancia_total_km=solved.distance_km,
        duracion_total_min=solved.duration_minutes,
        co2_estimado_kg=solved.co2_kg,
        co2_referencia_kg=solved.fifo_co2_kg,
        co2_evitado_kg=avoided_kg,
        arboles_quinual_eq=quinual_equivalent(avoided_kg),
        fitness=solved.fitness,
        estado=EstadoSolucion.COMPUTED,
        metadatos_ga={
            **solved.metadata(),
            "quinual_kg_co2_por_ano": factor,
        },
    )
    session.add(solution)
    vehicles_by_id = {vehicle.id: vehicle for vehicle in vehicles}
    orders_by_id = {order.id: order for order in orders}
    for itinerary in solved.itineraries:
        previous: tuple[float, float] | None = None
        for stop in itinerary.stops:
            detail = _detail_from_stop(itinerary.vehicle_id, stop, previous)
            detail.vehiculo = vehicles_by_id[itinerary.vehicle_id]
            if stop.order_id is not None:
                order = orders_by_id[stop.order_id]
                detail.pedido = order
                order.estado = EstadoPedido.ASSIGNED
            solution.detalles.append(detail)
            previous = (stop.longitude, stop.latitude)
    return solution


def _tracking_read(order: Pedido, solution: SolucionRuta | None) -> TrackingRead:
    longitude, latitude = geometry_to_geojson(order.ubicacion)["coordinates"][:2]
    detail = None
    if solution is not None:
        detail = next(
            (
                item
                for item in solution.detalles
                if item.pedido_id == order.id and item.tipo_parada == TipoParada.DELIVERY
            ),
            None,
        )
    previous = 0
    avoided_kg = 0.0
    distance_km = 0.0
    co2_g = 0.0
    plate = None
    eta = None
    route_code = None
    if detail is not None and solution is not None:
        route_code = solution.codigo
        plate = detail.vehiculo.placa
        eta = detail.eta
        distance_km = detail.distancia_tramo_km
        co2_g = detail.co2_tramo_g
        previous = sum(
            1
            for item in solution.detalles
            if item.vehiculo_id == detail.vehiculo_id
            and item.tipo_parada == TipoParada.DELIVERY
            and item.secuencia < detail.secuencia
            and item.pedido is not None
            and item.pedido.estado not in {EstadoPedido.DELIVERED, EstadoPedido.CANCELLED}
        )
        delivery_km = sum(
            item.distancia_tramo_km
            for item in solution.detalles
            if item.tipo_parada == TipoParada.DELIVERY and item.distancia_tramo_km > 0
        )
        if delivery_km > 0:
            avoided_kg = solution.co2_evitado_kg * (distance_km / delivery_km)
    return TrackingRead(
        codigo_pedido=order.codigo_pedido,
        cliente_nombre=order.cliente_nombre,
        direccion_referencia=order.direccion_referencia,
        estado=order.estado,
        lat=float(latitude),
        lon=float(longitude),
        ventana_inicio=order.ventana_inicio,
        ventana_fin=order.ventana_fin,
        eta=eta,
        paradas_previas=previous,
        distancia_km=distance_km,
        co2_tramo_g=co2_g,
        co2_evitado_kg=avoided_kg,
        placa=plate,
        codigo_ruta=route_code,
    )


def _driver_stop(detail: RutaDetalle) -> DriverStopRead:
    order = detail.pedido
    longitude, latitude = geometry_to_geojson(detail.ubicacion)["coordinates"][:2]
    return DriverStopRead(
        secuencia=detail.secuencia,
        tipo_parada=detail.tipo_parada,
        vehiculo_id=detail.vehiculo_id,
        placa=detail.vehiculo.placa,
        codigo_pedido=order.codigo_pedido if order is not None else None,
        cliente_nombre=order.cliente_nombre if order is not None else None,
        direccion_referencia=order.direccion_referencia if order is not None else None,
        peso_kg=order.peso_kg if order is not None else None,
        ventana_inicio=order.ventana_inicio if order is not None else None,
        ventana_fin=order.ventana_fin if order is not None else None,
        lat=float(latitude),
        lon=float(longitude),
        eta=detail.eta,
        co2_tramo_g=detail.co2_tramo_g,
    )


def _detail_from_stop(
    vehicle_id: int,
    stop: StopItinerary,
    previous: tuple[float, float] | None,
) -> RutaDetalle:
    line = None
    if previous is not None and stop.distance_km > 0:
        line = WKTElement(
            (
                f"LINESTRING({previous[0]} {previous[1]}, "
                f"{stop.longitude} {stop.latitude})"
            ),
            srid=get_settings().storage_srid,
        )
    distance_m = stop.distance_km * 1000.0
    slope = (stop.elevation_delta_m / distance_m) * 100.0 if distance_m > 0 else 0.0
    return RutaDetalle(
        vehiculo_id=vehicle_id,
        pedido_id=stop.order_id,
        secuencia=stop.sequence,
        tipo_parada=stop.stop_type,
        ubicacion=point_wkt(stop.longitude, stop.latitude),
        altitud_msnm=stop.altitude_m,
        distancia_tramo_km=stop.distance_km,
        desnivel_m=stop.elevation_delta_m,
        pendiente_pct=slope,
        tiempo_viaje_min=stop.travel_minutes,
        eta=stop.eta,
        co2_tramo_g=stop.co2_grams,
        geometria_tramo=line,
    )


def _metadata(
    solution: SolucionRuta,
    solved: RouteSolution,
    order_count: int,
) -> RouteOptimizationMetadata:
    used = sum(1 for itinerary in solved.itineraries if itinerary.stops)
    return RouteOptimizationMetadata(
        id=solution.id,
        codigo=solution.codigo,
        fecha_operacion=solution.fecha_operacion,
        distancia_total_km=solution.distancia_total_km,
        duracion_total_min=solution.duracion_total_min,
        co2_estimado_kg=solution.co2_estimado_kg,
        co2_referencia_kg=solution.co2_referencia_kg,
        co2_evitado_kg=solution.co2_evitado_kg,
        arboles_quinual_eq=solution.arboles_quinual_eq,
        quinual_kg_co2_por_ano=get_settings().quinual_kg_co2_per_year,
        fitness=solution.fitness,
        estado=solution.estado,
        feasible=solved.feasible,
        pedidos=order_count,
        vehiculos_usados=used,
    )


def _solution_code(operation_day: date) -> str:
    return f"SOL-{operation_day:%Y%m%d}-{uuid4().hex[:6].upper()}"


def _as_lima(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=LIMA)
    return value.astimezone(LIMA)


def _public_error(error: dict) -> dict[str, object]:
    return {
        "loc": [str(part) for part in error.get("loc", [])],
        "msg": str(error.get("msg", "")),
        "type": str(error.get("type", "")),
    }
