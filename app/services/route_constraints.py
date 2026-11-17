"""Restricciones duras de planificación (RF-008 / RN-003 / RN-004).

Las penalizaciones del algoritmo genético guían la búsqueda; este módulo decide
si una solución puede publicarse. RN-003 opera como límite operativo configurable
mientras la validación normativa siga pendiente (no se afirma obligación legal).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.core.config import get_settings
from app.models.domain import Pedido, Vehiculo
from app.models.enums import TipoParada
from app.services.eta_schedule import late_minutes_after_window
from app.services.genetic_solver import RouteSolution, VehicleItinerary
from app.services.vehicle_state import is_available_for_routing

PUBLICATION_VEHICLE_IDS = "vehiculos_validados_publicacion"


class PublicationRejected(ValueError):
    """Rechazo de dominio, transportable por HTTP o WebSocket."""

    def __init__(self, detail: dict[str, Any]) -> None:
        self.detail = detail
        super().__init__(detail["mensaje"])


@dataclass(frozen=True)
class ConstraintViolation:
    code: str
    message: str
    vehicle_plate: str | None = None
    order_code: str | None = None
    excess_kg: float | None = None
    excess_m3: float | None = None
    excess_minutes: float | None = None


@dataclass
class FleetPrecheckResult:
    feasible: bool
    total_kg: float
    total_m3: float
    fleet_kg: float
    fleet_m3: float
    excess_kg: float
    excess_m3: float
    orders_without_volume: int
    messages: list[str] = field(default_factory=list)

    def as_detail(self) -> dict[str, Any]:
        return {
            "codigo": "CAPACIDAD_FLOTA_INSUFICIENTE",
            "mensaje": (
                "La demanda del lote supera la capacidad agregada de la flota disponible."
            ),
            "total_kg": self.total_kg,
            "capacidad_flota_kg": self.fleet_kg,
            "exceso_kg": self.excess_kg,
            "total_m3": self.total_m3,
            "capacidad_flota_m3": self.fleet_m3,
            "exceso_m3": self.excess_m3,
            "pedidos_sin_volumen_m3": self.orders_without_volume,
            "detalle": self.messages,
        }


@dataclass
class PublicationValidation:
    ok: bool
    violations: list[ConstraintViolation] = field(default_factory=list)
    unassigned_order_codes: list[str] = field(default_factory=list)

    def as_detail(self) -> dict[str, Any]:
        return {
            "codigo": "RUTA_INFACTIBLE",
            "mensaje": "No se puede publicar la ruta porque incumple restricciones duras.",
            "pedidos_sin_asignar": self.unassigned_order_codes,
            "violaciones": [
                {
                    "codigo": item.code,
                    "mensaje": item.message,
                    "placa": item.vehicle_plate,
                    "pedido": item.order_code,
                    "exceso_kg": item.excess_kg,
                    "exceso_m3": item.excess_m3,
                    "exceso_minutos": item.excess_minutes,
                }
                for item in self.violations
            ],
        }


def shift_limit_minutes() -> float:
    settings = get_settings()
    if not settings.enforce_shift_limit:
        return float("inf")
    return max(1.0, settings.max_shift_minutes)


def shift_limit_label() -> str:
    settings = get_settings()
    hours = settings.max_shift_minutes / 60.0
    suffix = (
        " (límite operativo configurable; validación normativa RN-003 pendiente)"
        if not settings.shift_limit_normative_validated
        else ""
    )
    return f"{hours:g} h{suffix}"


def compute_shift_minutes(itinerary: VehicleItinerary, service_minutes: float) -> float:
    """Jornada = conducción + servicio en parada. No incluye espera por ventana."""
    deliveries = sum(1 for stop in itinerary.stops if stop.stop_type == TipoParada.DELIVERY)
    travel = sum(stop.travel_minutes for stop in itinerary.stops)
    return travel + deliveries * service_minutes


def precheck_fleet_capacity(orders: list[Pedido], vehicles: list[Vehiculo]) -> FleetPrecheckResult:
    total_kg = sum(float(order.peso_kg) for order in orders)
    fleet_kg = sum(float(vehicle.capacidad_kg) for vehicle in vehicles)
    volumes = [float(order.volumen_m3) for order in orders if order.volumen_m3 is not None]
    total_m3 = sum(volumes)
    fleet_m3 = sum(float(vehicle.capacidad_m3) for vehicle in vehicles)
    without_volume = sum(1 for order in orders if order.volumen_m3 is None)
    excess_kg = max(0.0, total_kg - fleet_kg)
    excess_m3 = 0.0
    if volumes:
        excess_m3 = max(0.0, total_m3 - fleet_m3)
    messages: list[str] = []
    if excess_kg > 0:
        messages.append(
            f"Peso total {total_kg:.1f} kg supera la flota ({fleet_kg:.1f} kg) "
            f"en {excess_kg:.1f} kg."
        )
    if excess_m3 > 0:
        messages.append(
            f"Volumen total {total_m3:.2f} m³ supera la flota ({fleet_m3:.2f} m³) "
            f"en {excess_m3:.2f} m³."
        )
    if without_volume:
        messages.append(
            f"{without_volume} pedido(s) no declaran volumen_m3; "
            "la comprobación volumétrica de flota solo suma pedidos con dato."
        )
    feasible = excess_kg <= 0 and excess_m3 <= 0
    return FleetPrecheckResult(
        feasible=feasible,
        total_kg=total_kg,
        total_m3=total_m3,
        fleet_kg=fleet_kg,
        fleet_m3=fleet_m3,
        excess_kg=excess_kg,
        excess_m3=excess_m3,
        orders_without_volume=without_volume,
        messages=messages,
    )


def validate_for_publication(
    solution: RouteSolution | None,
    orders: list[Pedido],
    vehicles: list[Vehiculo],
    *,
    service_minutes: float,
) -> PublicationValidation:
    """Valida el lote requerido, no solo las banderas producidas por el GA.

    Volumen desconocido conserva la política vigente: se suma solo el declarado.
    Una ruta vacía solo es válida si no queda ningún pedido obligatorio.
    """
    orders_by_id = {order.id: order for order in orders}
    vehicles_by_id = {vehicle.id: vehicle for vehicle in vehicles}
    codes_by_id = {order.id: order.codigo_pedido for order in orders}
    violations: list[ConstraintViolation] = []
    max_shift = shift_limit_minutes()
    assigned: set[int] = set()
    seen_vehicles: set[int] = set()

    if solution is not None and (not solution.feasible or not hard_feasible(solution)):
        violations.append(ConstraintViolation(
            code="SOLUCION_INFACTIBLE", message="El solver no acredita una solución factible completa.",
        ))

    for itinerary in solution.itineraries if solution is not None else ():
        vehicle = vehicles_by_id.get(itinerary.vehicle_id)
        plate = itinerary.plate
        if vehicle is None or not is_available_for_routing(vehicle) or not vehicle.activo:
            violations.append(ConstraintViolation(
                code="VEHICULO_NO_ELEGIBLE", message=f"El vehículo {plate} no pertenece a la flota apta.",
                vehicle_plate=plate,
            ))
        if itinerary.vehicle_id in seen_vehicles:
            violations.append(ConstraintViolation(
                code="VEHICULO_REPETIDO", message=f"El vehículo {plate} tiene más de un itinerario.",
                vehicle_plate=plate,
            ))
        seen_vehicles.add(itinerary.vehicle_id)
        deliveries = [stop for stop in itinerary.stops if stop.stop_type == TipoParada.DELIVERY]
        carried = [orders_by_id[stop.order_id] for stop in deliveries if stop.order_id in orders_by_id]
        load_kg = sum(float(order.peso_kg) for order in carried)
        load_m3 = sum(float(order.volumen_m3) for order in carried if order.volumen_m3 is not None)
        capacity_kg = float(vehicle.capacidad_kg) if vehicle else itinerary.capacity_kg
        capacity_m3 = float(vehicle.capacidad_m3) if vehicle else itinerary.capacity_m3
        excess_kg = max(itinerary.capacity_excess_kg, load_kg - capacity_kg)
        excess_m3 = max(itinerary.capacity_excess_m3, load_m3 - capacity_m3)
        if excess_kg > 0:
            violations.append(
                ConstraintViolation(
                    code="CAPACIDAD_PESO",
                    message=(
                        f"El vehículo {plate} supera el 100 % de capacidad de peso "
                        f"({load_kg:.1f} kg / {capacity_kg:.1f} kg)."
                    ),
                    vehicle_plate=plate,
                    excess_kg=excess_kg,
                )
            )
        if excess_m3 > 0:
            violations.append(
                ConstraintViolation(
                    code="CAPACIDAD_VOLUMEN",
                    message=(
                        f"El vehículo {plate} supera el 100 % de capacidad volumétrica "
                        f"({load_m3:.2f} m³ / {capacity_m3:.2f} m³)."
                    ),
                    vehicle_plate=plate,
                    excess_m3=excess_m3,
                )
            )
        shift_min = compute_shift_minutes(itinerary, service_minutes)
        if shift_min > max_shift:
            excess = shift_min - max_shift
            violations.append(
                ConstraintViolation(
                    code="JORNADA_MAXIMA",
                    message=(
                        f"El vehículo {plate} requiere {shift_min:.1f} min de conducción+servicio, "
                        f"por encima del límite operativo de {shift_limit_label()}."
                    ),
                    vehicle_plate=plate,
                    excess_minutes=excess,
                )
            )
        for stop in deliveries:
            order = orders_by_id.get(stop.order_id)
            if order is None:
                violations.append(ConstraintViolation(
                    code="PEDIDO_NO_REQUERIDO", message="La ruta contiene un pedido ajeno al lote requerido.",
                    vehicle_plate=plate, order_code=stop.order_code,
                ))
                continue
            code = order.codigo_pedido
            if order.id in assigned or code != stop.order_code:
                violations.append(ConstraintViolation(
                    code="ASIGNACION_INCONSISTENTE", message=f"Asignación repetida o código incorrecto de {code}.",
                    vehicle_plate=plate, order_code=code,
                ))
            assigned.add(order.id)
            requested_vehicle = getattr(order, "vehiculo_asignado_id", None)
            if requested_vehicle is not None and requested_vehicle != itinerary.vehicle_id:
                violations.append(ConstraintViolation(
                    code="ASIGNACION_VEHICULO", message=f"El pedido {code} debe viajar en su vehículo asignado.",
                    vehicle_plate=plate, order_code=code,
                ))
            if stop.eta is None or not stop.matrix_trusted:
                violations.append(ConstraintViolation(
                    code="VENTANA_NO_VERIFICABLE", message=f"El pedido {code} no tiene ETA confiable.",
                    vehicle_plate=plate, order_code=code,
                ))
                continue
            late = max(stop.late_minutes, late_minutes_after_window(stop.eta, order.ventana_fin))
            if late > 0:
                violations.append(
                    ConstraintViolation(
                        code="VENTANA_ENTREGA",
                        message=(
                            f"El pedido {code} llegaría {late:.1f} min "
                            f"después de su ventana."
                        ),
                        vehicle_plate=plate,
                        order_code=code,
                    )
                )

    missing = set(orders_by_id) - assigned
    if solution is not None:
        missing.update(oid for oid in solution.unassigned_order_ids if oid in codes_by_id)
    unassigned = [code for oid, code in codes_by_id.items() if oid in missing]
    if unassigned:
        violations.append(
            ConstraintViolation(
                code="PEDIDOS_SIN_ASIGNAR",
                message=f"{len(unassigned)} pedido(s) no pudieron asignarse sin violar restricciones.",
            )
        )

    ok = not violations and not unassigned
    return PublicationValidation(ok=ok, violations=violations, unassigned_order_codes=unassigned)


def hard_feasible(solution: RouteSolution) -> bool:
    return (
        solution.late_minutes == 0.0
        and solution.capacity_excess_kg == 0.0
        and solution.capacity_excess_m3 == 0.0
        and solution.shift_excess_minutes == 0.0
        and not solution.unassigned_order_ids
    )
