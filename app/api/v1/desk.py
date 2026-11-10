"""Jornada, carga CSV y mantenimiento de la flota."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles
from app.core.database import get_db
from app.models.enums import EstadoOperativoVehiculo, RolUsuario
from app.models.identity import Usuario
from app.models.operations import HistorialVehiculo
from app.schemas.logistics import PedidoRead, VehiculoCreate, VehiculoRead, VehiculoUpdate
from app.services.access import FLOTA_ACTUALIZADA, IMPORTAR_PEDIDOS, record
from app.models.domain import Deposito, Pedido, Vehiculo
from app.services.order_import import ImportReport, import_orders
from app.services.vehicle_state import apply_operational_state, sync_activo_flag

router = APIRouter(prefix="/api/v1", tags=["jornada"])
LIMA = ZoneInfo("America/Lima")

DESK = (RolUsuario.ADMIN, RolUsuario.OPERADOR, RolUsuario.GERENTE, RolUsuario.AUDITOR)
WRITERS = (RolUsuario.ADMIN, RolUsuario.OPERADOR)
DENY_WRITE = "Solo el operador o el administrador pueden cargar pedidos."
DENY_READ = "Tu rol no consulta la jornada."
DENY_FLEET = "Tu rol no puede modificar la flota."
DENY_CREATE = "Solo el administrador registra vehículos nuevos."


class DayImport(BaseModel):
    csv: str | None = None
    xlsx_base64: str | None = None


class HistorialRead(BaseModel):
    id: int
    activo: bool
    estado_anterior: str | None
    estado_nuevo: str | None
    motivo: str | None
    detalle: str
    correo: str
    creado_en: datetime


class JornadaRead(BaseModel):
    fecha: date
    pedidos: list[PedidoRead]
    total_pedidos: int
    offset: int
    limite: int
    hay_mas: bool


def _day_bounds(fecha: date) -> tuple[datetime, datetime]:
    start = datetime.combine(fecha, datetime.min.time(), tzinfo=LIMA)
    return start, start + timedelta(days=1)


@router.get(
    "/jornadas/{fecha}",
    response_model=JornadaRead,
    summary="Pedidos de una jornada",
)
async def read_day(
    fecha: date,
    offset: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=250),
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_roles(*DESK, accion="jornada_denegada", detail=DENY_READ)),
) -> JornadaRead:
    start, end = _day_bounds(fecha)
    filters = (Pedido.ventana_inicio >= start, Pedido.ventana_inicio < end)
    total = await session.scalar(select(func.count(Pedido.id)).where(*filters)) or 0
    result = await session.scalars(
        select(Pedido)
        .where(*filters)
        .order_by(Pedido.ventana_inicio, Pedido.id)
        .offset(offset)
        .limit(limite + 1)
    )
    rows = list(result.all())
    hay_mas = len(rows) > limite
    return JornadaRead(
        fecha=fecha,
        pedidos=rows[:limite],
        total_pedidos=total,
        offset=offset,
        limite=limite,
        hay_mas=hay_mas,
    )


@router.post(
    "/jornadas/{fecha}/importar",
    response_model=ImportReport,
    summary="Importar pedidos CSV o Excel (.xlsx) de la jornada",
    responses={400: {"description": "El archivo no se puede leer."}},
)
async def import_day(
    fecha: date,
    body: DayImport,
    session: AsyncSession = Depends(get_db),
    actor: Usuario = Depends(require_roles(*WRITERS, accion="importar_denegado", detail=DENY_WRITE)),
) -> ImportReport:
    from app.services.order_import import decode_xlsx_payload

    if body.csv and body.xlsx_base64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Envía solo CSV o solo Excel, no ambos.",
        )
    if not body.csv and not body.xlsx_base64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Indica el contenido CSV o un archivo Excel codificado en base64.",
        )
    try:
        xlsx_bytes = decode_xlsx_payload(body.xlsx_base64) if body.xlsx_base64 else None
        report = await import_orders(session, fecha, csv=body.csv, xlsx_bytes=xlsx_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    await record(
        session,
        correo=actor.correo,
        accion=IMPORTAR_PEDIDOS,
        detalle=f"Jornada {fecha.isoformat()}: {report.resumen}",
        usuario=actor,
    )
    await session.commit()
    return report


@router.get("/flota", response_model=list[VehiculoRead], summary="Flota, incluidas las unidades inactivas")
async def list_fleet(
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_roles(*DESK, accion="flota_denegada", detail=DENY_READ)),
) -> list[Vehiculo]:
    result = await session.scalars(
        select(Vehiculo).order_by(Vehiculo.estado_operativo.asc(), Vehiculo.placa)
    )
    return list(result.all())


@router.post(
    "/flota",
    response_model=VehiculoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un vehículo",
)
async def create_vehicle(
    payload: VehiculoCreate,
    session: AsyncSession = Depends(get_db),
    actor: Usuario = Depends(require_roles(RolUsuario.ADMIN, accion="flota_denegada", detail=DENY_CREATE)),
) -> Vehiculo:
    depot = await session.get(Deposito, payload.deposito_id)
    if depot is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El depósito no existe.")
    duplicate = await session.scalar(select(Vehiculo.id).where(Vehiculo.placa == payload.placa))
    if duplicate is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un vehículo con la placa {payload.placa}.",
        )
    vehicle = Vehiculo(
        **payload.model_dump(),
        estado_operativo=EstadoOperativoVehiculo.ACTIVO,
    )
    sync_activo_flag(vehicle)
    session.add(vehicle)
    await session.flush()
    session.add(
        HistorialVehiculo(
            vehiculo_id=vehicle.id,
            activo=True,
            estado_anterior=None,
            estado_nuevo=EstadoOperativoVehiculo.ACTIVO.value,
            detalle="Alta en la flota.",
            correo=actor.correo,
        )
    )
    await record(
        session,
        correo=actor.correo,
        accion=FLOTA_ACTUALIZADA,
        detalle=f"Alta de {vehicle.placa}.",
        usuario=actor,
    )
    await session.commit()
    await session.refresh(vehicle)
    return vehicle


@router.patch(
    "/flota/{vehiculo_id}",
    response_model=VehiculoRead,
    summary="Editar datos operativos o disponibilidad",
)
async def update_vehicle(
    vehiculo_id: int,
    payload: VehiculoUpdate,
    session: AsyncSession = Depends(get_db),
    actor: Usuario = Depends(require_roles(*WRITERS, accion="flota_denegada", detail=DENY_FLEET)),
) -> Vehiculo:
    vehicle = await session.get(Vehiculo, vehiculo_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe ese vehículo.")
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay cambios para guardar.")
    motivo = changes.pop("motivo", None)
    target_state = changes.pop("estado_operativo", None)
    if target_state is not None:
        session.add(
            apply_operational_state(
                vehicle,
                target_state,
                correo=actor.correo,
                motivo=motivo,
            )
        )
    for field, value in changes.items():
        setattr(vehicle, field, value)
    if changes:
        session.add(
            HistorialVehiculo(
                vehiculo_id=vehicle.id,
                activo=vehicle.activo,
                detalle=_change_text(vehicle.placa, changes),
                correo=actor.correo,
            )
        )
    if target_state is None and not changes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay cambios para guardar.")
    detail_parts: list[str] = []
    if target_state is not None:
        detail_parts.append(f"{vehicle.placa}: estado operativo → {target_state.value}")
    if changes:
        detail_parts.append(_change_text(vehicle.placa, changes))
    detail = " ".join(detail_parts)
    await record(session, correo=actor.correo, accion=FLOTA_ACTUALIZADA, detalle=detail, usuario=actor)
    await session.commit()
    await session.refresh(vehicle)
    return vehicle


@router.get(
    "/flota/{vehiculo_id}/historial",
    response_model=list[HistorialRead],
    summary="Historial de un vehículo",
)
async def vehicle_history(
    vehiculo_id: int,
    limite: int | None = Query(None, ge=1, le=100),
    antes_de: int | None = Query(None, ge=1),
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_roles(*DESK, accion="flota_denegada", detail=DENY_READ)),
) -> list[HistorialVehiculo]:
    page_size = limite if limite is not None else 20
    result = await session.scalars(
        select(HistorialVehiculo)
        .where(
            HistorialVehiculo.vehiculo_id == vehiculo_id,
            *([HistorialVehiculo.id < antes_de] if antes_de is not None else []),
        )
        .order_by(HistorialVehiculo.id.desc())
        .limit(page_size)
    )
    return list(result.all())


def _change_text(placa: str, changes: dict[str, object]) -> str:
    if "activo" in changes and len(changes) == 1:
        return f"{placa} queda {'activa' if changes['activo'] else 'inactiva'}."
    fields = ", ".join(changes)
    return f"{placa}: se actualizó {fields}."
