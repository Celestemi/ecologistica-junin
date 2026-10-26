"""Configuración de restricción vehicular por placa (RF-002 / RN-002)."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, SmallInteger, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

AMBITO_PROYECTO = "Huancayo, El Tambo y Chilca"
ETIQUETA_PENDIENTE = "[PENDIENTE DE VALIDACIÓN NORMATIVA]"


class RestriccionPlacaConfig(Base):
    """Parámetros globales de la regla RN-002 (desactivada hasta validación normativa)."""

    __tablename__ = "restriccion_placa_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ambito: Mapped[str] = mapped_column(String(120), nullable=False)
    etiqueta_validacion: Mapped[str] = mapped_column(String(64), nullable=False)
    validada_normativamente: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )
    activa: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )
    referencia_normativa: Mapped[str | None] = mapped_column(String(240), nullable=True)
    actualizada_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    reglas: Mapped[list["RestriccionPlacaRegla"]] = relationship(
        back_populates="config",
        cascade="all, delete-orphan",
    )


class RestriccionPlacaRegla(Base):
    """Días de la semana (ISO 1=lunes … 7=domingo) en que aplica restricción por dígito."""

    __tablename__ = "restriccion_placa_reglas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    config_id: Mapped[int] = mapped_column(
        ForeignKey("restriccion_placa_config.id", ondelete="CASCADE"),
        nullable=False,
    )
    ultimo_digito: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    dias_semana: Mapped[list[int]] = mapped_column(ARRAY(SmallInteger), nullable=False)

    config: Mapped[RestriccionPlacaConfig] = relationship(back_populates="reglas")


class HistorialRestriccionPlaca(Base):
    """Auditoría de cambios en la configuración."""

    __tablename__ = "historial_restriccion_placa"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    correo: Mapped[str] = mapped_column(String(120), nullable=False)
    detalle: Mapped[str] = mapped_column(Text, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
