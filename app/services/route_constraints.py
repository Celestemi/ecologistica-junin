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
from app.services.genetic_solver import RouteSolution, VehicleItinerary


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
    solution: RouteSolution,
    orders: list[Pedido],
    vehicles: list[Vehiculo],
    *,
    service_minutes: float,
) -> PublicationValidation:
    orders_by_id = {order.id: order for order in orders}
    vehicles_by_id = {vehicle.id: vehicle for vehicle in vehicles}
    codes_by_id = {order.id: order.codigo_pedido for order in orders}
    violations: list[ConstraintViolation] = []
    max_shift = shift_limit_minutes()

    for itinerary in solution.itineraries:
        vehicle = vehicles_by_id.get(itinerary.vehicle_id)
        plate = itinerary.plate
        capacity_m3 = float(vehicle.capacidad_m3) if vehicle else itinerary.capacity_m3
        if itinerary.capacity_excess_kg > 0:
            violations.append(
                ConstraintViolation(
                    code="CAPACIDAD_PESO",
                    message=(
                        f"El vehículo {plate} supera el 100 % de capacidad de peso "
                        f"({itinerary.load_kg:.1f} kg / {itinerary.capacity_kg:.1f} kg)."
                    ),
                    vehicle_plate=plate,
                    excess_kg=itinerary.capacity_excess_kg,
                )
            )
        if itinerary.capacity_excess_m3 > 0:
            violations.append(
                ConstraintViolation(
                    code="CAPACIDAD_VOLUMEN",
                    message=(
                        f"El vehículo {plate} supera el 100 % de capacidad volumétrica "
                        f"({itinerary.load_m3:.2f} m³ / {capacity_m3:.2f} m³)."
                    ),
                    vehicle_plate=plate,
                    excess_m3=itinerary.capacity_excess_m3,
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
        for stop in itinerary.stops:
            if stop.late_minutes > 0 and stop.order_id is not None:
                order = orders_by_id.get(stop.order_id)
                code = order.codigo_pedido if order else stop.order_code
                violations.append(
                    ConstraintViolation(
                        code="VENTANA_ENTREGA",
                        message=(
                            f"El pedido {code} llegaría {stop.late_minutes:.1f} min "
                            f"después de su ventana."
                        ),
                        vehicle_plate=plate,
                        order_code=code,
                    )
                )

    unassigned = [codes_by_id[oid] for oid in solution.unassigned_order_ids if oid in codes_by_id]
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
