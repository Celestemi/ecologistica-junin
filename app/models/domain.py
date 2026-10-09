"""Modelos ORM de depósito, flota, pedidos y solución de rutas.

Los nombres de clase y de columna siguen el esquema del MVP
(Deposito, Vehiculo, Pedido, SolucionRuta, RutaDetalle). Las funciones
de aplicación viven en módulos aparte y usan identificadores en inglés.
"""

from datetime import date, datetime

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import get_settings
from app.core.database import Base
from app.models.enums import EstadoPedido, EstadoSolucion, TipoCombustible, TipoParada


def _enum_values(enum_cls: type[EstadoPedido] | type[EstadoSolucion] | type[TipoCombustible] | type[TipoParada], name: str) -> Enum:
    """Persiste el valor del enum (`pending`), no el nombre (`PENDING`)."""
    return Enum(
        enum_cls,
        name=name,
        native_enum=False,
        length=32,
        values_callable=lambda members: [member.value for member in members],
    )

_SRID = get_settings().storage_srid


def _point_column() -> Geometry:
    return Geometry(geometry_type="POINT", srid=_SRID, spatial_index=True)


def _linestring_column() -> Geometry:
    return Geometry(geometry_type="LINESTRING", srid=_SRID, spatial_index=False)


class Deposito(Base):
    """Punto de partida y retorno de la flota."""

    __tablename__ = "depositos"
    __table_args__ = (
        CheckConstraint("altitud_msnm > 0", name="ck_depositos_altitud"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    direccion: Mapped[str] = mapped_column(String(240), nullable=False)
    ubicacion: Mapped[WKBElement] = mapped_column(_point_column(), nullable=False)
    altitud_msnm: Mapped[float] = mapped_column(Float, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    vehiculos: Mapped[list["Vehiculo"]] = relationship(back_populates="deposito")
    soluciones: Mapped[list["SolucionRuta"]] = relationship(back_populates="deposito")


class Vehiculo(Base):
    """Unidad de la flota con capacidad y factores de emisión."""

    __tablename__ = "vehiculos"
    __table_args__ = (
        CheckConstraint("capacidad_kg > 0", name="ck_vehiculos_capacidad_kg"),
        CheckConstraint("capacidad_m3 > 0", name="ck_vehiculos_capacidad_m3"),
        CheckConstraint("emision_base_co2_g_km >= 0", name="ck_vehiculos_emision"),
        CheckConstraint(
            "factor_penalizacion_pendiente >= 0",
            name="ck_vehiculos_penalizacion",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deposito_id: Mapped[int] = mapped_column(ForeignKey("depositos.id"), nullable=False)
    placa: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    capacidad_kg: Mapped[float] = mapped_column(Float, nullable=False)
    capacidad_m3: Mapped[float] = mapped_column(Float, nullable=False)
    tipo_combustible: Mapped[TipoCombustible] = mapped_column(
        _enum_values(TipoCombustible, "tipo_combustible"),
        nullable=False,
    )
    # Gramos de CO2 por kilómetro en llano, referidos a ~3 250 m s.n.m.
    emision_base_co2_g_km: Mapped[float] = mapped_column(Float, nullable=False)
    # Incremento relativo de emisión por cada 1% de pendiente positiva.
    factor_penalizacion_pendiente: Mapped[float] = mapped_column(Float, nullable=False)
    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    deposito: Mapped[Deposito] = relationship(back_populates="vehiculos")
    detalles: Mapped[list["RutaDetalle"]] = relationship(back_populates="vehiculo")


class Pedido(Base):
    """Entrega con ventana horaria y peso, anclada a un punto del valle."""

    __tablename__ = "pedidos"
    __table_args__ = (
        CheckConstraint("peso_kg > 0", name="ck_pedidos_peso"),
        CheckConstraint("altitud_msnm > 0", name="ck_pedidos_altitud"),
        CheckConstraint("ventana_fin > ventana_inicio", name="ck_pedidos_ventana"),
        Index("ix_pedidos_estado", "estado"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo_pedido: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    cliente_nombre: Mapped[str] = mapped_column(String(160), nullable=False)
    direccion_referencia: Mapped[str] = mapped_column(String(240), nullable=False)
    ubicacion: Mapped[WKBElement] = mapped_column(_point_column(), nullable=False)
    altitud_msnm: Mapped[float] = mapped_column(Float, nullable=False)
    peso_kg: Mapped[float] = mapped_column(Float, nullable=False)
    ventana_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ventana_fin: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado: Mapped[EstadoPedido] = mapped_column(
        _enum_values(EstadoPedido, "estado_pedido"),
        default=EstadoPedido.PENDING,
        server_default=text("'pending'"),
        nullable=False,
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    jornada_id: Mapped[int | None] = mapped_column(ForeignKey("jornadas.id"), nullable=True)

    detalles: Mapped[list["RutaDetalle"]] = relationship(back_populates="pedido")


class SolucionRuta(Base):
    """Resultado de una corrida del algoritmo genético VRPTW."""

    __tablename__ = "soluciones_ruta"
    __table_args__ = (
        CheckConstraint("distancia_total_km >= 0", name="ck_soluciones_distancia"),
        CheckConstraint("duracion_total_min >= 0", name="ck_soluciones_duracion"),
        CheckConstraint("co2_estimado_kg >= 0", name="ck_soluciones_co2"),
        CheckConstraint("co2_referencia_kg >= 0", name="ck_soluciones_co2_ref"),
        CheckConstraint("co2_evitado_kg >= 0", name="ck_soluciones_co2_evitado"),
        CheckConstraint("arboles_quinual_eq >= 0", name="ck_soluciones_quinual"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    deposito_id: Mapped[int] = mapped_column(ForeignKey("depositos.id"), nullable=False)
    fecha_operacion: Mapped[date] = mapped_column(Date, nullable=False)
    distancia_total_km: Mapped[float] = mapped_column(Float, nullable=False)
    duracion_total_min: Mapped[float] = mapped_column(Float, nullable=False)
    co2_estimado_kg: Mapped[float] = mapped_column(Float, nullable=False)
    # Emisión de una asignación de referencia, sin criterio ecológico.
    co2_referencia_kg: Mapped[float] = mapped_column(Float, nullable=False)
    co2_evitado_kg: Mapped[float] = mapped_column(Float, nullable=False)
    # Quinuales equivalentes/año. Se congela con el factor vigente al calcular.
    arboles_quinual_eq: Mapped[float] = mapped_column(Float, nullable=False)
    fitness: Mapped[float] = mapped_column(Float, nullable=False)
    estado: Mapped[EstadoSolucion] = mapped_column(
        _enum_values(EstadoSolucion, "estado_solucion"),
        default=EstadoSolucion.DRAFT,
        server_default=text("'draft'"),
        nullable=False,
    )
    # Generaciones, tamaño de población y mejor fitness por iteración.
    metadatos_ga: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    creada_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    deposito: Mapped[Deposito] = relationship(back_populates="soluciones")
    detalles: Mapped[list["RutaDetalle"]] = relationship(
        back_populates="solucion",
        cascade="all, delete-orphan",
        order_by="RutaDetalle.secuencia",
    )


class RutaDetalle(Base):
    """Parada ordenada de un vehículo dentro de una solución."""

    __tablename__ = "rutas_detalle"
    __table_args__ = (
        UniqueConstraint(
            "solucion_id",
            "vehiculo_id",
            "secuencia",
            name="uq_rutas_detalle_secuencia",
        ),
        UniqueConstraint("solucion_id", "pedido_id", name="uq_rutas_detalle_pedido"),
        CheckConstraint("secuencia >= 0", name="ck_rutas_detalle_secuencia"),
        CheckConstraint("distancia_tramo_km >= 0", name="ck_rutas_detalle_distancia"),
        CheckConstraint("co2_tramo_g >= 0", name="ck_rutas_detalle_co2"),
        CheckConstraint("altitud_msnm > 0", name="ck_rutas_detalle_altitud"),
        Index("ix_rutas_detalle_solucion_secuencia", "solucion_id", "secuencia"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    solucion_id: Mapped[int] = mapped_column(
        ForeignKey("soluciones_ruta.id", ondelete="CASCADE"),
        nullable=False,
    )
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), nullable=False)
    pedido_id: Mapped[int | None] = mapped_column(ForeignKey("pedidos.id"), nullable=True)
    secuencia: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_parada: Mapped[TipoParada] = mapped_column(
        _enum_values(TipoParada, "tipo_parada"),
        nullable=False,
    )
    ubicacion: Mapped[WKBElement] = mapped_column(_point_column(), nullable=False)
    altitud_msnm: Mapped[float] = mapped_column(Float, nullable=False)
    distancia_tramo_km: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    desnivel_m: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pendiente_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    tiempo_viaje_min: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    eta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    co2_tramo_g: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    # Geometría de calle cuando el ruteador la tenga. Vacía en la cuerda inicial.
    geometria_tramo: Mapped[WKBElement | None] = mapped_column(
        _linestring_column(),
        nullable=True,
    )

    solucion: Mapped[SolucionRuta] = relationship(back_populates="detalles")
    vehiculo: Mapped[Vehiculo] = relationship(back_populates="detalles")
    pedido: Mapped[Pedido | None] = relationship(back_populates="detalles")
