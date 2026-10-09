"""Lectura del CSV de la jornada y alta de las filas que ya tienen punto."""

import csv
import io
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.geo import point_wkt
from app.models.domain import Pedido
from app.models.enums import EstadoPedido
from app.models.operations import Jornada
from app.services.geocode import locate_address

LIMA = ZoneInfo("America/Lima")
_LAT = (-12.30, -11.70)
_LON = (-75.50, -74.90)

_HEADER = {
    "codigo": "codigo",
    "codigo_pedido": "codigo",
    "cliente": "cliente",
    "cliente_nombre": "cliente",
    "direccion": "direccion",
    "direccion_referencia": "direccion",
    "peso_kg": "peso_kg",
    "peso": "peso_kg",
    "hora_inicio": "hora_inicio",
    "ventana_inicio": "hora_inicio",
    "hora_fin": "hora_fin",
    "ventana_fin": "hora_fin",
    "lat": "lat",
    "latitud": "lat",
    "lon": "lon",
    "longitud": "lon",
    "altitud": "altitud",
    "altitud_msnm": "altitud",
}
_REQUIRED = ("codigo", "cliente", "direccion", "peso_kg", "hora_inicio", "hora_fin")


class ImportRow(BaseModel):
    linea: int
    codigo_pedido: str = ""
    cliente_nombre: str = ""
    direccion_referencia: str = ""
    peso_kg: float | None = None
    hora_inicio: str = ""
    hora_fin: str = ""
    lat: float | None = None
    lon: float | None = None
    altitud_msnm: float | None = None
    resultado: str
    motivo: str | None = None


class ImportReport(BaseModel):
    fecha: date
    aceptados: int = 0
    filas: list[ImportRow] = Field(default_factory=list)


def parse_csv(raw: str, fecha: date) -> tuple[list[dict[str, str]], str | None]:
    """Normaliza el CSV. El segundo valor es un error de archivo, no de una fila."""
    text = raw.lstrip("\ufeff").strip()
    if not text:
        return [], "El archivo no tiene filas."
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        return [], "El archivo no tiene encabezado."
    columns = {_HEADER.get(_fold_header(name), ""): name for name in reader.fieldnames}
    missing = [name for name in _REQUIRED if not columns.get(name)]
    if missing:
        return [], f"Faltan columnas: {', '.join(missing)}."
    rows: list[dict[str, str]] = []
    for raw_row in reader:
        item = {key: (raw_row.get(source) or "").strip() for key, source in columns.items() if source}
        if not any(item.values()):
            continue
        rows.append(item)
    if not rows:
        return [], "El archivo no tiene filas."
    return rows, None


async def ensure_jornada(session: AsyncSession, fecha: date) -> Jornada:
    found = await session.scalar(select(Jornada).where(Jornada.fecha == fecha))
    if found is not None:
        return found
    created = Jornada(fecha=fecha)
    session.add(created)
    await session.flush()
    return created


async def import_orders(session: AsyncSession, fecha: date, raw: str) -> ImportReport:
    parsed, error = parse_csv(raw, fecha)
    if error is not None:
        raise ValueError(error)
    jornada = await ensure_jornada(session, fecha)
    existing = set(await session.scalars(select(Pedido.codigo_pedido)))
    seen: set[str] = set()
    report = ImportReport(fecha=fecha)
    for index, item in enumerate(parsed, start=2):
        row, order = _classify(fecha, index, item, existing, seen)
        report.filas.append(row)
        if order is None:
            continue
        order.jornada_id = jornada.id
        session.add(order)
        existing.add(order.codigo_pedido)
        seen.add(order.codigo_pedido)
        report.aceptados += 1
    return report


def _classify(
    fecha: date,
    linea: int,
    item: dict[str, str],
    existing: set[str],
    seen: set[str],
) -> tuple[ImportRow, Pedido | None]:
    row = ImportRow(
        linea=linea,
        codigo_pedido=item.get("codigo", ""),
        cliente_nombre=item.get("cliente", ""),
        direccion_referencia=item.get("direccion", ""),
        hora_inicio=item.get("hora_inicio", ""),
        hora_fin=item.get("hora_fin", ""),
        resultado="rechazado",
    )
    code = row.codigo_pedido
    if len(code) < 3:
        row.motivo = "El código es demasiado corto."
        return row, None
    if code in existing or code in seen:
        row.motivo = f"Ya existe un pedido con el código {code}."
        return row, None
    if len(row.cliente_nombre) < 2 or len(row.direccion_referencia) < 3:
        row.motivo = "Faltan el cliente o la dirección."
        return row, None
    try:
        weight = float(item.get("peso_kg", ""))
    except ValueError:
        row.motivo = "El peso no es un número."
        return row, None
    if weight <= 0:
        row.motivo = "El peso tiene que ser mayor que cero."
        return row, None
    row.peso_kg = weight
    start = _clock(item.get("hora_inicio", ""))
    end = _clock(item.get("hora_fin", ""))
    if start is None or end is None or end <= start:
        row.motivo = "La ventana horaria no es válida."
        return row, None
    lat, lon, altitude, located = _point(item, row.direccion_referencia)
    row.lat = lat
    row.lon = lon
    row.altitud_msnm = altitude
    wrote_coordinates = bool(item.get("lat") or item.get("lon"))
    if wrote_coordinates and not located:
        row.motivo = "La coordenada no es un número."
        return row, None
    if not located:
        row.resultado = "pendiente_punto"
        row.motivo = "Sin coordenadas. Márcalo en el mapa."
        seen.add(code)
        return row, None
    if lat is None or lon is None or not (_LAT[0] <= lat <= _LAT[1] and _LON[0] <= lon <= _LON[1]):
        row.motivo = "El punto queda fuera del valle del Mantaro."
        return row, None
    if altitude is None or altitude <= 0:
        altitude = 3270.0
        row.altitud_msnm = altitude
    order = Pedido(
        codigo_pedido=code,
        cliente_nombre=row.cliente_nombre,
        direccion_referencia=row.direccion_referencia,
        ubicacion=point_wkt(lon, lat),
        altitud_msnm=altitude,
        peso_kg=weight,
        ventana_inicio=datetime.combine(fecha, start, tzinfo=LIMA),
        ventana_fin=datetime.combine(fecha, end, tzinfo=LIMA),
        estado=EstadoPedido.PENDING,
    )
    row.resultado = "aceptado"
    row.motivo = "Ubicado por la dirección." if item.get("lat", "") == "" else None
    return row, order


def _point(
    item: dict[str, str],
    address: str,
) -> tuple[float | None, float | None, float | None, bool]:
    lat_text = item.get("lat", "")
    lon_text = item.get("lon", "")
    altitude = _optional_float(item.get("altitud", ""))
    if lat_text or lon_text:
        lat = _optional_float(lat_text)
        lon = _optional_float(lon_text)
        return lat, lon, altitude, lat is not None and lon is not None
    found = locate_address(address)
    if found is None:
        return None, None, altitude, False
    return found[0], found[1], altitude if altitude is not None else found[2], True


def _optional_float(value: str) -> float | None:
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _clock(value: str) -> time | None:
    try:
        hour, minute = value.split(":", maxsplit=1)
        parsed = time(int(hour), int(minute))
    except (ValueError, AttributeError):
        return None
    return parsed


def _fold_header(name: str | None) -> str:
    return (name or "").strip().casefold()
