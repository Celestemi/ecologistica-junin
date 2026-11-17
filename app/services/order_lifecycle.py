"""AF-02: transiciones compartidas, sin alterar el historial."""

from app.models.enums import EstadoPedido

TERMINAL_STATES = frozenset({EstadoPedido.DELIVERED, EstadoPedido.CANCELLED})
_ALLOWED = {
    EstadoPedido.PENDING: {EstadoPedido.ASSIGNED, EstadoPedido.IN_TRANSIT, EstadoPedido.CANCELLED, EstadoPedido.INCIDENT},
    EstadoPedido.ASSIGNED: {EstadoPedido.PENDING, EstadoPedido.IN_TRANSIT, EstadoPedido.DELIVERED, EstadoPedido.CANCELLED, EstadoPedido.INCIDENT},
    EstadoPedido.IN_TRANSIT: {EstadoPedido.ASSIGNED, EstadoPedido.DELIVERED, EstadoPedido.CANCELLED, EstadoPedido.INCIDENT},
    EstadoPedido.INCIDENT: {EstadoPedido.PENDING, EstadoPedido.ASSIGNED, EstadoPedido.CANCELLED},
}


def require_transition(order, target: EstadoPedido, *, allow_same: bool = False) -> None:
    current = order.estado
    if allow_same and current == target:
        return
    if target not in _ALLOWED.get(current, set()):
        raise ValueError('El estado del pedido no permite esta transición.')


def transition_order(order, target: EstadoPedido, *, allow_same: bool = False) -> None:
    require_transition(order, target, allow_same=allow_same)
    order.estado = target
