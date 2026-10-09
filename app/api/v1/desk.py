"""Jornada, carga CSV y mantenimiento de la flota."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles
from app.core.database import get_db
from app.models.enums import RolUsuario
from app.models.identity import Usuario
from app.models.operations import HistorialVehiculo
from app.schemas.logistics import PedidoRead, VehiculoCreate, VehiculoRead
from app.services.access import FLOTA_ACTUALIZADA, IMPORTAR_PEDIDOS, record
from app.models.domain import Deposito, Pedido, Vehiculo
from app.services.order_import import ImportReport, import_orders

router = APIRouter(prefix="/api/v1", tags=["jornada"])
LIMA = ZoneInfo("America/Lima")

DESK = (RolUsuario.ADMIN, RolUsuario.OPERADOR, RolUsuario.GERENTE, RolUsuario.AUDITOR)
WRITERS = (RolUsuario.ADMIN, RolUsuario.OPERADOR)
DENY_WRITE = "Solo el operador o el administrador pueden cargar pedidos."
DENY_READ = "Tu rol no consulta la jornada."
DENY_FLEET = "Tu rol no puede modificar la flota."
DENY_CREATE = "Solo el administrador registra vehículos nuevos."


class CsvImport(BaseModel):
    csv: str = Field(min_length=1)


class VehiculoUpdate(BaseModel):
    capacidad_kg: float | None = Field(default=None, gt=0)
    capacidad_m3: float | None = Field(default=None, gt=0)
    emision_base_co2_g_km: float | None = Field(default=None, ge=0)
    factor_penalizacion_pendiente: float | None = Field(default=None, ge=0)
    activo: bool | None = None


class HistorialRead(BaseModel):
    activo: bool
    detalle: str
    correo: str
    creado_en: datetime


class JornadaRead(BaseModel):
    fecha: date
    pedidos: list[PedidoRead]


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
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_roles(*DESK, accion="jornada_denegada", detail=DENY_READ)),
) -> JornadaRead:
    start, end = _day_bounds(fecha)
    result = await session.scalars(
        select(Pedido)
        .where(Pedido.ventana_inicio >= start, Pedido.ventana_inicio < end)
        .order_by(Pedido.ventana_inicio, Pedido.id)
    )
    return JornadaRead(fecha=fecha, pedidos=list(result.all()))


@router.post(
    "/jornadas/{fecha}/importar",
    response_model=ImportReport,
    summary="Importar el CSV de la jornada",
    responses={400: {"description": "El archivo no se puede leer."}},
)
async def import_day(
    fecha: date,
    body: CsvImport,
    session: AsyncSession = Depends(get_db),
    actor: Usuario = Depends(require_roles(*WRITERS, accion="importar_denegado", detail=DENY_WRITE)),
) -> ImportReport:
    try:
        report = await import_orders(session, fecha, body.csv)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    await record(
        session,
        correo=actor.correo,
        accion=IMPORTAR_PEDIDOS,
        detalle=f"Jornada {fecha.isoformat()}: {report.aceptados} pedidos aceptados.",
        usuario=actor,
    )
    await session.commit()
    return report


@router.get("/flota", response_model=list[VehiculoRead], summary="Flota, incluidas las unidades inactivas")
async def list_fleet(
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_roles(*DESK, accion="flota_denegada", detail=DENY_READ)),
) -> list[Vehiculo]:
    result = await session.scalars(select(Vehiculo).order_by(Vehiculo.activo.desc(), Vehiculo.placa))
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
    vehicle = Vehiculo(**payload.model_dump())
    session.add(vehicle)
    await session.flush()
    session.add(
        HistorialVehiculo(
            vehiculo_id=vehicle.id,
            activo=True,
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


@router.patch("/flota/{vehiculo_id}", response_model=VehiculoRead, summary="Editar capacidad o disponibilidad")
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
    for field, value in changes.items():
        setattr(vehicle, field, value)
    detail = _change_text(vehicle.placa, changes)
    session.add(
        HistorialVehiculo(
            vehiculo_id=vehicle.id,
            activo=vehicle.activo,
            detalle=detail,
            correo=actor.correo,
        )
    )
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
    session: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_roles(*DESK, accion="flota_denegada", detail=DENY_READ)),
) -> list[HistorialVehiculo]:
    result = await session.scalars(
        select(HistorialVehiculo)
        .where(HistorialVehiculo.vehiculo_id == vehiculo_id)
        .order_by(HistorialVehiculo.id.desc())
        .limit(20)
    )
    return list(result.all())


def _change_text(placa: str, changes: dict[str, object]) -> str:
    if "activo" in changes and len(changes) == 1:
        return f"{placa} queda {'activa' if changes['activo'] else 'inactiva'}."
    fields = ", ".join(changes)
    return f"{placa}: se actualizó {fields}."
