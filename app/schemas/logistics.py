"""Esquemas de alta y lectura para flota, pedidos y rutas optimizadas."""

from datetime import date, datetime
from typing import Any, Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.emissions import quinual_equivalent
from app.core.geo import geometry_to_geojson, linestring_geojson
from app.models.domain import RutaDetalle, SolucionRuta
from app.models.enums import EstadoPedido, EstadoSolucion, TipoCombustible, TipoParada

# Caja amplia del valle del Mantaro para rechazar coordenadas fuera de la operación.
_LAT_RANGE = (-12.30, -11.70)
_LON_RANGE = (-75.50, -74.90)


class GeoJSONPoint(BaseModel):
    """Punto GeoJSON. `coordinates` es [longitud, latitud]."""

    type: Literal["Point"] = "Point"
    coordinates: list[float] = Field(min_length=2, max_length=2)

    @field_validator("coordinates")
    @classmethod
    def within_mantaro(cls, value: list[float]) -> list[float]:
        lon, lat = value
        if not _LON_RANGE[0] <= lon <= _LON_RANGE[1]:
            raise ValueError("La longitud queda fuera del valle del Mantaro.")
        if not _LAT_RANGE[0] <= lat <= _LAT_RANGE[1]:
            raise ValueError("La latitud queda fuera del valle del Mantaro.")
        return [float(lon), float(lat)]


class GeoJSONLineString(BaseModel):
    type: Literal["LineString"] = "LineString"
    coordinates: list[list[float]] = Field(min_length=2)


class GeoJSONFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: GeoJSONPoint | GeoJSONLineString
    properties: dict[str, Any] = Field(default_factory=dict)


class GeoJSONFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[GeoJSONFeature]


class VehiculoCreate(BaseModel):
    deposito_id: int
    placa: str = Field(min_length=5, max_length=16)
    capacidad_kg: float = Field(gt=0)
    capacidad_m3: float = Field(gt=0)
    tipo_combustible: TipoCombustible
    emision_base_co2_g_km: float = Field(ge=0)
    factor_penalizacion_pendiente: float = Field(ge=0)


class VehiculoRead(VehiculoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activo: bool


class PedidoCreate(BaseModel):
    codigo_pedido: str = Field(min_length=3, max_length=32)
    cliente_nombre: str = Field(min_length=2, max_length=160)
    direccion_referencia: str = Field(min_length=3, max_length=240)
    ubicacion: GeoJSONPoint
    altitud_msnm: float = Field(gt=0, le=6000)
    peso_kg: float = Field(gt=0)
    ventana_inicio: datetime
    ventana_fin: datetime

    @field_validator("ventana_fin")
    @classmethod
    def window_is_ordered(cls, value: datetime, info) -> datetime:
        start = info.data.get("ventana_inicio")
        if start is not None and value <= start:
            raise ValueError("La ventana de fin debe ser posterior a la de inicio.")
        return value


class PedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo_pedido: str
    cliente_nombre: str
    direccion_referencia: str
    ubicacion: GeoJSONPoint
    altitud_msnm: float
    peso_kg: float
    ventana_inicio: datetime
    ventana_fin: datetime
    estado: EstadoPedido

    @field_validator("ubicacion", mode="before")
    @classmethod
    def coerce_point(cls, value: Any) -> Any:
        if isinstance(value, GeoJSONPoint):
            return value
        geojson = geometry_to_geojson(value)
        return GeoJSONPoint.model_validate(geojson)


class DepositoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    direccion: str
    ubicacion: GeoJSONPoint
    altitud_msnm: float

    @field_validator("ubicacion", mode="before")
    @classmethod
    def coerce_point(cls, value: Any) -> Any:
        if isinstance(value, GeoJSONPoint):
            return value
        return GeoJSONPoint.model_validate(geometry_to_geojson(value))


class DriverStopRead(BaseModel):
    """Parada de la ruta activa, con lo que el conductor necesita en la calle."""

    secuencia: int
    tipo_parada: TipoParada
    vehiculo_id: int
    placa: str
    codigo_pedido: str | None = None
    cliente_nombre: str | None = None
    direccion_referencia: str | None = None
    peso_kg: float | None = None
    ventana_inicio: datetime | None = None
    ventana_fin: datetime | None = None
    lat: float
    lon: float
    eta: datetime | None = None
    co2_tramo_g: float


class ActiveRouteRead(BaseModel):
    """Última solución calculada, lista para el modo conductor."""

    codigo: str
    fecha_operacion: date
    paradas: list[DriverStopRead]


class TrackingRead(BaseModel):
    """Lo que el cliente final puede ver de su propio pedido."""

    codigo_pedido: str
    cliente_nombre: str
    direccion_referencia: str
    estado: EstadoPedido
    lat: float
    lon: float
    ventana_inicio: datetime
    ventana_fin: datetime
    eta: datetime | None = None
    paradas_previas: int
    distancia_km: float
    co2_tramo_g: float
    co2_evitado_kg: float
    placa: str | None = None
    codigo_ruta: str | None = None


class RouteStopRead(BaseModel):
    """Parada de una solución, lista para la lista del dispatcher o del conductor."""

    id: int
    secuencia: int
    tipo_parada: TipoParada
    vehiculo_id: int
    placa: str
    pedido_id: int | None
    codigo_pedido: str | None
    cliente_nombre: str | None
    ubicacion: GeoJSONPoint
    altitud_msnm: float
    distancia_tramo_km: float
    desnivel_m: float
    pendiente_pct: float
    tiempo_viaje_min: float
    eta: datetime | None
    co2_tramo_g: float


class OptimizedRouteResponse(BaseModel):
    """Solución VRPTW con métricas de sostenibilidad y capa GeoJSON para Leaflet."""

    id: int
    codigo: str
    fecha_operacion: date
    distancia_total_km: float
    duracion_total_min: float
    co2_estimado_kg: float
    co2_referencia_kg: float
    co2_evitado_kg: float
    arboles_quinual_eq: float
    fitness: float
    estado: EstadoSolucion
    paradas: list[RouteStopRead]
    geojson: GeoJSONFeatureCollection

    @classmethod
    def from_solution(cls, solution: SolucionRuta) -> "OptimizedRouteResponse":
        """Arma la respuesta. `detalles`, `vehiculo` y `pedido` deben estar cargados."""
        stops = [_stop_read(detail) for detail in solution.detalles]
        return cls(
            id=solution.id,
            codigo=solution.codigo,
            fecha_operacion=solution.fecha_operacion,
            distancia_total_km=solution.distancia_total_km,
            duracion_total_min=solution.duracion_total_min,
            co2_estimado_kg=solution.co2_estimado_kg,
            co2_referencia_kg=solution.co2_referencia_kg,
            co2_evitado_kg=solution.co2_evitado_kg,
            arboles_quinual_eq=solution.arboles_quinual_eq,
            fitness=solution.fitness,
            estado=solution.estado,
            paradas=stops,
            geojson=_feature_collection(solution.detalles),
        )


def _stop_read(detail: RutaDetalle) -> RouteStopRead:
    pedido = detail.pedido
    return RouteStopRead(
        id=detail.id,
        secuencia=detail.secuencia,
        tipo_parada=detail.tipo_parada,
        vehiculo_id=detail.vehiculo_id,
        placa=detail.vehiculo.placa,
        pedido_id=detail.pedido_id,
        codigo_pedido=pedido.codigo_pedido if pedido is not None else None,
        cliente_nombre=pedido.cliente_nombre if pedido is not None else None,
        ubicacion=GeoJSONPoint.model_validate(geometry_to_geojson(detail.ubicacion)),
        altitud_msnm=detail.altitud_msnm,
        distancia_tramo_km=detail.distancia_tramo_km,
        desnivel_m=detail.desnivel_m,
        pendiente_pct=detail.pendiente_pct,
        tiempo_viaje_min=detail.tiempo_viaje_min,
        eta=detail.eta,
        co2_tramo_g=detail.co2_tramo_g,
    )


def _feature_collection(details: list[RutaDetalle]) -> GeoJSONFeatureCollection:
    """Puntos de parada y una línea por vehículo, en el orden de la secuencia."""
    features: list[GeoJSONFeature] = []
    by_vehicle: dict[int, list[RutaDetalle]] = {}
    for detail in details:
        point = GeoJSONPoint.model_validate(geometry_to_geojson(detail.ubicacion))
        pedido = detail.pedido
        title = pedido.direccion_referencia if pedido is not None else "Depósito"
        features.append(
            GeoJSONFeature(
                geometry=point,
                properties={
                    "sequence": detail.secuencia,
                    "stop_type": detail.tipo_parada.value,
                    "plate": detail.vehiculo.placa,
                    "order_code": pedido.codigo_pedido if pedido is not None else None,
                    "customer": pedido.cliente_nombre if pedido is not None else None,
                    "window_start": pedido.ventana_inicio.isoformat() if pedido is not None else None,
                    "window_end": pedido.ventana_fin.isoformat() if pedido is not None else None,
                    "title": title,
                    "co2_g": detail.co2_tramo_g,
                    "eta": detail.eta.isoformat() if detail.eta is not None else None,
                },
            )
        )
        by_vehicle.setdefault(detail.vehiculo_id, []).append(detail)

    for vehicle_stops in by_vehicle.values():
        ordered = sorted(vehicle_stops, key=lambda item: item.secuencia)
        stop_coordinates = [
            [float(pair) for pair in geometry_to_geojson(stop.ubicacion)["coordinates"]]
            for stop in ordered
        ]
        line_coordinates = _road_or_chord(ordered, stop_coordinates)
        if len(line_coordinates) < 2:
            continue
        features.append(
            GeoJSONFeature(
                geometry=GeoJSONLineString.model_validate(
                    linestring_geojson(line_coordinates)
                ),
                properties={
                    "plate": ordered[0].vehiculo.placa,
                    "kind": "route",
                },
            )
        )
    return GeoJSONFeatureCollection(features=features)


def _road_or_chord(
    ordered: list[RutaDetalle],
    stop_coordinates: list[list[float]],
) -> list[list[float]]:
    """Usa la geometría de calle guardada o, si no existe, la cuerda entre paradas."""
    road: list[list[float]] = []
    for stop in ordered:
        if stop.geometria_tramo is None:
            continue
        segment = geometry_to_geojson(stop.geometria_tramo)
        if segment.get("type") != "LineString":
            continue
        for coordinate in segment["coordinates"]:
            pair = [float(coordinate[0]), float(coordinate[1])]
            if road and road[-1] == pair:
                continue
            road.append(pair)
    return road or stop_coordinates


def avoided_co2_to_quinual(co2_avoided_kg: float) -> float:
    """Atajo de lectura: kg de CO2 evitados a Quinuales equivalentes/año."""
    return quinual_equivalent(co2_avoided_kg)


class PedidoCreateRequest(BaseModel):
    """Alta de pedido. `lat` y `lon` se guardan como Point de PostGIS."""

    codigo_pedido: str = Field(min_length=3, max_length=32, examples=["PED-006"])
    cliente_nombre: str = Field(min_length=2, max_length=160, examples=["Bodega Los Andes"])
    direccion_referencia: str = Field(
        min_length=3,
        max_length=240,
        examples=["Jr. Puno 450, Cercado de Huancayo"],
    )
    lat: float = Field(examples=[-12.06806])
    lon: float = Field(examples=[-75.21000])
    altitud_msnm: float = Field(gt=0, le=6000, examples=[3271])
    peso_kg: float = Field(gt=0, examples=[25])
    ventana_inicio: datetime = Field(examples=["2026-10-07T09:00:00-05:00"])
    ventana_fin: datetime = Field(examples=["2026-10-07T12:00:00-05:00"])
    fecha: date | None = None

    @field_validator("lat")
    @classmethod
    def lat_in_valley(cls, value: float) -> float:
        if not _LAT_RANGE[0] <= value <= _LAT_RANGE[1]:
            raise ValueError("La latitud queda fuera del valle del Mantaro.")
        return float(value)

    @field_validator("lon")
    @classmethod
    def lon_in_valley(cls, value: float) -> float:
        if not _LON_RANGE[0] <= value <= _LON_RANGE[1]:
            raise ValueError("La longitud queda fuera del valle del Mantaro.")
        return float(value)

    @field_validator("ventana_fin")
    @classmethod
    def window_is_ordered(cls, value: datetime, info) -> datetime:
        start = info.data.get("ventana_inicio")
        if isinstance(start, datetime) and _as_lima(value) <= _as_lima(start):
            raise ValueError("La ventana de fin debe ser posterior a la de inicio.")
        return value


def _as_lima(value: datetime) -> datetime:
    lima = ZoneInfo("America/Lima")
    if value.tzinfo is None:
        return value.replace(tzinfo=lima)
    return value.astimezone(lima)


class RouteOptimizationMetadata(BaseModel):
    """KPIs de la corrida, pensados para el panel del mapa."""

    id: int
    codigo: str
    fecha_operacion: date
    distancia_total_km: float
    duracion_total_min: float
    co2_estimado_kg: float
    co2_referencia_kg: float
    co2_evitado_kg: float
    arboles_quinual_eq: float
    quinual_kg_co2_por_ano: float = 12.0
    fitness: float
    estado: EstadoSolucion
    feasible: bool
    pedidos: int
    vehiculos_usados: int


class RouteOptimizationGeoJSON(BaseModel):
    """FeatureCollection de Leaflet más la metadata de sostenibilidad."""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[GeoJSONFeature]
    metadata: RouteOptimizationMetadata
