"""Entidades ORM. Importar este paquete registra las tablas en Base.metadata."""

from app.models.domain import Deposito, Pedido, RutaDetalle, SolucionRuta, Vehiculo
from app.models.enums import (
    EstadoPedido,
    EstadoSolucion,
    TipoCombustible,
    TipoParada,
)

__all__ = [
    "Deposito",
    "EstadoPedido",
    "EstadoSolucion",
    "Pedido",
    "RutaDetalle",
    "SolucionRuta",
    "TipoCombustible",
    "TipoParada",
    "Vehiculo",
]
