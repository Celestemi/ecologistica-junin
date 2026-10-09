"""Entidades ORM. Importar este paquete registra las tablas en Base.metadata."""

from app.models.domain import Deposito, Pedido, RutaDetalle, SolucionRuta, Vehiculo
from app.models.enums import (
    EstadoPedido,
    EstadoSolucion,
    RolUsuario,
    TipoCombustible,
    TipoParada,
)
from app.models.identity import Bitacora, Usuario
from app.models.operations import HistorialVehiculo, Jornada

__all__ = [
    "Bitacora",
    "Deposito",
    "EstadoPedido",
    "EstadoSolucion",
    "HistorialVehiculo",
    "Jornada",
    "Pedido",
    "RolUsuario",
    "RutaDetalle",
    "SolucionRuta",
    "TipoCombustible",
    "TipoParada",
    "Usuario",
    "Vehiculo",
]
