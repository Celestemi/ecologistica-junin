"""Usuarios y bitácora de acceso. El cliente final no tiene fila aquí."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import RolUsuario


def _rol_column() -> Enum:
    return Enum(
        RolUsuario,
        name="rol_usuario",
        native_enum=False,
        length=32,
        values_callable=lambda members: [member.value for member in members],
    )


class Usuario(Base):
    """Cuenta interna de DistriRápido. La contraseña solo se guarda como hash."""

    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint("intentos_fallidos >= 0", name="ck_usuarios_intentos"),
        Index("ix_usuarios_rol", "rol"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    correo: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(_rol_column(), nullable=False)
    clave_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    intentos_fallidos: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    bloqueado_hasta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    eventos: Mapped[list["Bitacora"]] = relationship(back_populates="usuario")


class Bitacora(Base):
    """Hecho de acceso u operación que el auditor puede leer y no puede borrar."""

    __tablename__ = "bitacora"
    __table_args__ = (Index("ix_bitacora_creado_en", "creado_en"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
    )
    correo: Mapped[str] = mapped_column(String(160), nullable=False)
    accion: Mapped[str] = mapped_column(String(40), nullable=False)
    detalle: Mapped[str | None] = mapped_column(String(400), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    usuario: Mapped[Usuario | None] = relationship(back_populates="eventos")
