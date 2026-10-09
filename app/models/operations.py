"""Jornada del día e historial de la flota."""

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


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


class HistorialVehiculo(Base):
    """Cambio de estado o de capacidad. No se borra al inactivar la unidad."""

    __tablename__ = "historial_vehiculo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    detalle: Mapped[str] = mapped_column(String(240), nullable=False)
    correo: Mapped[str] = mapped_column(String(160), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
