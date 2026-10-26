"""Validación del ámbito Huancayo, El Tambo y Chilca con PostGIS (RF-005)."""

from __future__ import annotations

import json
import logging
from functools import lru_cache
from pathlib import Path

from geoalchemy2.elements import WKTElement
from shapely.geometry import mapping, shape
from shapely.geometry.base import BaseGeometry
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.core.config import get_settings
from app.models.operations import AreaOperacion

logger = logging.getLogger("ecologistica.operating_area")

_BUNDLED = Path(__file__).resolve().parent.parent / "data" / "operating_area_dev.geojson"
_DEFAULT_LABEL = (
    "Sobre operativo provisional (desarrollo). "
    "Reemplace por límites distritales validados (OPERATING_AREA_GEOJSON_PATH)."
)


def operating_area_geojson_path() -> Path:
    configured = (get_settings().operating_area_geojson_path or "").strip()
    if configured:
        return Path(configured)
    return _BUNDLED


@lru_cache
def _load_multipolygon_wkt() -> tuple[str, str]:
    path = operating_area_geojson_path()
    payload = json.loads(path.read_text(encoding="utf-8"))
    geometries: list[BaseGeometry] = []
    if payload.get("type") == "FeatureCollection":
        for feature in payload.get("features", []):
            geometries.append(shape(feature["geometry"]))
    elif payload.get("type") == "Feature":
        geometries.append(shape(payload["geometry"]))
    else:
        geometries.append(shape(payload))
    if not geometries:
        raise ValueError(f"El GeoJSON de ámbito operativo está vacío: {path}")
    merged = geometries[0]
    for item in geometries[1:]:
        merged = merged.union(item)
    if merged.geom_type == "Polygon":
        merged = shape({"type": "MultiPolygon", "coordinates": [mapping(merged)["coordinates"]]})
    wkt = merged.wkt
    label = _DEFAULT_LABEL
    if path != _BUNDLED:
        label = f"Ámbito cargado desde {path.name}."
    return wkt, label


def operating_area_wkt_element() -> WKTElement:
    wkt, _ = _load_multipolygon_wkt()
    return WKTElement(wkt, srid=get_settings().storage_srid)


async def ensure_operating_area(session: AsyncSession) -> None:
    """Inserta el polígono de trabajo si la tabla está vacía."""
    exists = await session.scalar(select(func.count()).select_from(AreaOperacion))
    if exists:
        return
    wkt, label = _load_multipolygon_wkt()
    session.add(
        AreaOperacion(
            id=1,
            etiqueta=label,
            geom=WKTElement(wkt, srid=get_settings().storage_srid),
        )
    )
    await session.flush()
    if operating_area_geojson_path() == _BUNDLED:
        logger.warning(
            "RF-005: usando sobre geográfico provisional (%s). "
            "Configure OPERATING_AREA_GEOJSON_PATH con límites validados.",
            _BUNDLED.name,
        )


async def point_in_operating_area(session: AsyncSession, lon: float, lat: float) -> bool:
    """True si el punto WGS84 cae dentro del ámbito configurado (ST_Contains)."""
    await ensure_operating_area(session)
    contained = await session.scalar(
        select(
            func.ST_Contains(
                AreaOperacion.geom,
                func.ST_SetSRID(func.ST_MakePoint(lon, lat), get_settings().storage_srid),
            )
        ).limit(1)
    )
    return bool(contained)


async def ensure_operating_area_on_connection(connection: AsyncConnection) -> None:
    count = (
        await connection.execute(text("SELECT COUNT(*) FROM area_operacion"))
    ).scalar_one()
    if count:
        return
    wkt, label = _load_multipolygon_wkt()
    srid = get_settings().storage_srid
    await connection.execute(
        text(
            "INSERT INTO area_operacion (id, etiqueta, geom) "
            "VALUES (1, :label, ST_SetSRID(ST_GeomFromText(:wkt), :srid))"
        ),
        {"label": label, "wkt": wkt, "srid": srid},
    )
