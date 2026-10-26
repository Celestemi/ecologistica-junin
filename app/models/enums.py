"""Valores persistidos del dominio. Las etiquetas de interfaz van en español."""

from enum import Enum


class TipoCombustible(str, Enum):
    """Combustible o fuente de energía del vehículo."""

    DIESEL = "diesel"
    ELECTRIC = "electric"
    GASOLINE = "gasoline"
    GLP = "glp"


class EstadoUbicacion(str, Enum):
    """Geocodificación espacial del punto de entrega (RF-005)."""

    GEOCODIFICADO = "geocodificado"
    PENDIENTE_VALIDACION = "pendiente_validacion"


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


class EstadoOperativoVehiculo(str, Enum):
    """Disponibilidad operativa de una unidad de la flota."""

    ACTIVO = "activo"
    MANTENIMIENTO = "mantenimiento"
    INACTIVO = "inactivo"


class TipoParada(str, Enum):
    """Papel de una fila de detalle dentro de la ruta de un vehículo."""

    DEPOT_START = "depot_start"
    DELIVERY = "delivery"
    DEPOT_END = "depot_end"


class EstadoEta(str, Enum):
    """Confianza del ETA respecto a la matriz de tiempos (RF-009)."""

    CALCULADO = "calculado"
    EN_VENTANA = "en_ventana"
    EN_ESPERA = "en_espera"
    FUERA_VENTANA = "fuera_ventana"
    REVISION_MATRIZ = "revision_matriz"
    SIN_DATOS = "sin_datos"


class ModeloDistancia(str, Enum):
    """Origen de la distancia usada para el tramo (no implica vía real salvo OSRM)."""

    GEODESICA = "geodesica"
    OSRM = "osrm"
