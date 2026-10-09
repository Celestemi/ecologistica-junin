"""Valores persistidos del dominio. Las etiquetas de interfaz van en español."""

from enum import Enum


class TipoCombustible(str, Enum):
    """Combustible o fuente de energía del vehículo."""

    DIESEL = "diesel"
    ELECTRIC = "electric"
    GASOLINE = "gasoline"
    GLP = "glp"


class EstadoPedido(str, Enum):
    """Ciclo de vida de un pedido de última milla."""

    PENDING = "pending"  # pendiente
    ASSIGNED = "assigned"  # asignado
    IN_TRANSIT = "in_transit"  # en ruta
    DELIVERED = "delivered"  # entregado
    INCIDENT = "incident"  # incidencia
    CANCELLED = "cancelled"  # cancelado


class EstadoSolucion(str, Enum):
    """Estado de una corrida del algoritmo genético VRPTW."""

    DRAFT = "draft"  # borrador
    COMPUTED = "computed"  # calculada
    PUBLISHED = "published"  # publicada al dispatcher
    ARCHIVED = "archived"  # archivada


class RolUsuario(str, Enum):
    """Rol de acceso. El cliente final no tiene cuenta: entra con un enlace."""

    ADMIN = "admin"
    OPERADOR = "operador"
    CONDUCTOR = "conductor"
    GERENTE = "gerente"
    AUDITOR = "auditor"


class TipoParada(str, Enum):
    """Papel de una fila de detalle dentro de la ruta de un vehículo."""

    DEPOT_START = "depot_start"
    DELIVERY = "delivery"
    DEPOT_END = "depot_end"
