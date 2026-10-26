"""Jornada del día e historial de la flota."""

from datetime import date, datetime

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import get_settings
from app.core.database import Base

_SRID = get_settings().storage_srid


class Jornada(Base):
    """Un día de reparto en America/Lima."""

    __tablename__ = "jornadas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[date] = mapped_column(Date, unique=True, nullable=False)
    creada_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class AsignacionConductor(Base):
    """Un conductor autenticado solo puede operar el vehículo activo asignado."""

    __tablename__ = "asignaciones_conductor"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id", ondelete="CASCADE"), nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    asignado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class AreaOperacion(Base):
    """Contorno de trabajo para RF-005. No sustituye límites distritales oficiales."""

    __tablename__ = "area_operacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    etiqueta: Mapped[str] = mapped_column(String(240), nullable=False)
    geom: Mapped[object] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=_SRID, spatial_index=True),
        nullable=False,
    )


class HistorialVehiculo(Base):
    """Cambio de estado o de capacidad. No se borra al inactivar la unidad."""

    __tablename__ = "historial_vehiculo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    estado_anterior: Mapped[str | None] = mapped_column(String(32), nullable=True)
    estado_nuevo: Mapped[str | None] = mapped_column(String(32), nullable=True)
    motivo: Mapped[str | None] = mapped_column(String(240), nullable=True)
    detalle: Mapped[str] = mapped_column(String(240), nullable=False)
    correo: Mapped[str] = mapped_column(String(160), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
