"""Algoritmo genético para el VRPTW de última milla en Huancayo.

El individuo es una partición de pedidos: una secuencia de ids por vehículo.
El cruce es Order Crossover (OX) sobre esa permutación. La mutación intercambia
dos visitas y, con menor probabilidad, mueve una visita a otro vehículo.
La selección es por torneo. Se minimiza una suma penalizada de kilómetros y CO2.

Emisión de un tramo, con Δh en metros de subida:

    E = distancia_km × emision_base_g_km × (1 + penalizacion_pendiente × max(0, Δh / 100))

El tiempo de viaje usa 25 km/h sobre distancia geodésica (Haversine), salvo tramos
con OSRM configurado. No representa longitud vial real salvo esos tramos.
Llegar después de `ventana_fin` y exceder `capacidad_kg` reciben una penalización
alta. Un vehículo grande que entra al Centro Histórico también la recibe.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from time import perf_counter
from math import asin, cos, radians, sin, sqrt
from typing import Any
from zoneinfo import ZoneInfo

from app.core.config import get_settings
from app.core.emissions import quinual_equivalent
from app.core.geo import geometry_to_geojson
from app.models.domain import Deposito, Pedido, Vehiculo
from app.models.enums import EstadoEta, ModeloDistancia, TipoCombustible, TipoParada
from app.services.eta_schedule import (
    classify_delivery_arrival,
    service_start_after_arrival,
)

LIMA = ZoneInfo("America/Lima")
EARTH_RADIUS_KM = 6371.0

# Parámetros operativos y del algoritmo. Los valores por defecto son los del MVP.
SPEED_KMH = 25.0
SERVICE_MINUTES = 5.0
GENERATIONS = 100
POPULATION_SIZE = 50
TOURNAMENT_SIZE = 3
MUTATION_RATE = 0.35
TRANSFER_RATE = 0.25
# Un kg de CO2 equivale a 25 km en el fitness: la emisión manda y el kilometraje
# sigue castigando los rodeos.
CO2_KG_WEIGHT = 25.0
LATE_PENALTY_PER_MIN = 80.0
CAPACITY_PENALTY_PER_KG = 200.0
VOLUME_PENALTY_PER_M3 = 250.0
SHIFT_PENALTY_PER_MIN = 120.0
UNASSIGNED_PENALTY = 8_000.0
HISTORIC_PENALTY_PER_LEG = 4_000.0
# RN-008: metas empresariales (informe comparativo; no son restricción dura de publicación).
RN008_MIN_DISTANCE_SAVINGS_PCT = 15.0
RN008_MIN_CO2_SAVINGS_PCT = 10.0
# El furgón de 1 500 kg queda restringido. El motocarro de 300 kg puede entrar.
LARGE_VEHICLE_MIN_KG = 1_000.0
LARGE_VEHICLE_MIN_M3 = 6.0

# Damero entre Jr. Ayacucho, Av. Real, Jr. Ancash y Av. Huancavelica.
# El vértice noreste queda en La Merced (Ayacucho con Real). El sureste pasa
# la Plaza Constitución para que la plaza, apoyada sobre Real y Ancash, quede
# dentro. El lado oeste son unas cuatro cuadras, hasta Av. Huancavelica.
HISTORIC_CENTER: tuple[tuple[float, float], ...] = (
    (-12.06590, -75.21165),  # Jr. Ayacucho con Av. Real
    (-12.06890, -75.20865),  # Jr. Ancash con Av. Real
    (-12.07240, -75.21420),  # Jr. Ancash con Av. Huancavelica
    (-12.06950, -75.21640),  # Jr. Ayacucho con Av. Huancavelica
)


@dataclass(frozen=True)
class StopItinerary:
    """Una parada del itinerario, con llegada, tramo y emisión."""

    sequence: int
    stop_type: TipoParada
    order_id: int | None
    order_code: str | None
    customer_name: str | None
    latitude: float
    longitude: float
    altitude_m: float
    eta: datetime | None
    distance_km: float
    elevation_delta_m: float
    travel_minutes: float
    co2_grams: float
    late_minutes: float
    enters_historic_center: bool
    eta_estado: EstadoEta = EstadoEta.CALCULADO
    wait_minutes: float = 0.0
    delivery_index: int | None = None
    distance_model: ModeloDistancia = ModeloDistancia.GEODESICA
    matrix_trusted: bool = True


@dataclass(frozen=True)
class VehicleItinerary:
    """Ruta completa de un vehículo, ida al depósito incluida."""

    vehicle_id: int
    plate: str
    fuel: TipoCombustible
    capacity_kg: float
    capacity_m3: float
    load_kg: float
    load_m3: float
    stops: tuple[StopItinerary, ...]
    distance_km: float
    co2_grams: float
    duration_minutes: float
    capacity_excess_kg: float
    capacity_excess_m3: float
    shift_minutes: float
    shift_excess_minutes: float
    historic_entries: int


@dataclass(frozen=True)
class RouteSolution:
    """Mejor solución del GA y su comparación contra el FIFO."""

    itineraries: tuple[VehicleItinerary, ...]
    distance_km: float
    duration_minutes: float
    co2_grams: float
    co2_kg: float
    fifo_co2_kg: float
    fifo_distance_km: float
    sequential_baseline_co2_kg: float
    sequential_baseline_distance_km: float
    savings_co2_pct_vs_sequential: float
    savings_distance_pct_vs_sequential: float
    rn008_distance_goal_met: bool
    rn008_co2_goal_met: bool
    co2_saved_kg: float
    arboles_quinual_eq: float
    fitness: float
    feasible: bool
    late_minutes: float
    capacity_excess_kg: float
    capacity_excess_m3: float
    shift_excess_minutes: float
    unassigned_order_ids: tuple[int, ...]
    historic_entries: int
    generations: int
    population_size: int
    seed: int
    best_fitness_per_generation: tuple[float, ...]
    generations_executed: int
    ga_elapsed_seconds: float
    solver_elapsed_seconds: float
    stop_reason: str

    def metadata(self) -> dict[str, Any]:
        """Diccionario listo para `SolucionRuta.metadatos_ga`."""
        return {
            "algorithm": "ga_vrptw_ox",
            "generations": self.generations,
            "population_size": self.population_size,
            "seed": self.seed,
            "fitness": self.fitness,
            "best_fitness_per_generation": list(self.best_fitness_per_generation),
            "fifo_co2_kg": self.fifo_co2_kg,
            "fifo_distance_km": self.fifo_distance_km,
            "linea_base_secuencial_co2_kg": self.sequential_baseline_co2_kg,
            "linea_base_secuencial_km": self.sequential_baseline_distance_km,
            "ahorro_co2_pct_vs_secuencial": self.savings_co2_pct_vs_sequential,
            "ahorro_distancia_pct_vs_secuencial": self.savings_distance_pct_vs_sequential,
            "rn008_meta_distancia_cumplida": self.rn008_distance_goal_met,
            "rn008_meta_co2_cumplida": self.rn008_co2_goal_met,
            "co2_saved_kg": self.co2_saved_kg,
            "feasible": self.feasible,
            "late_minutes": self.late_minutes,
            "capacity_excess_kg": self.capacity_excess_kg,
            "capacity_excess_m3": self.capacity_excess_m3,
            "shift_excess_minutes": self.shift_excess_minutes,
            "unassigned_order_ids": list(self.unassigned_order_ids),
            "historic_entries": self.historic_entries,
            "generations_executed": self.generations_executed,
            "solver_elapsed_seconds": self.solver_elapsed_seconds,
            "stop_reason": self.stop_reason,
            "ga_elapsed_seconds": self.ga_elapsed_seconds,
        }


@dataclass(frozen=True)
class _OrderNode:
    id: int
    code: str
    customer: str
    latitude: float
    longitude: float
    altitude_m: float
    weight_kg: float
    volume_m3: float | None
    window_start: datetime
    window_end: datetime


@dataclass(frozen=True)
class _VehicleNode:
    id: int
    plate: str
    capacity_kg: float
    capacity_m3: float
    fuel: TipoCombustible
    base_g_per_km: float
    slope_penalty: float
    large: bool


@dataclass
class _Evaluation:
    fitness: float
    distance_km: float
    duration_minutes: float
    co2_grams: float
    late_minutes: float
    capacity_excess_kg: float
    capacity_excess_m3: float
    shift_excess_minutes: float
    unassigned_order_ids: tuple[int, ...]
    historic_entries: int
    itineraries: tuple[VehicleItinerary, ...]


@dataclass
class _Individual:
    routes: list[list[int]]
    evaluation: _Evaluation | None = None

    @property
    def fitness(self) -> float:
        if self.evaluation is None:
            raise RuntimeError("El individuo todavía no tiene fitness.")
        return self.evaluation.fitness


class _Problem:
    """Matrices de distancia, desnivel y cruce del Centro Histórico."""

    def __init__(
        self,
        orders: list[_OrderNode],
        vehicles: list[_VehicleNode],
        depot_lat: float,
        depot_lon: float,
        depot_altitude_m: float,
        depot_name: str,
        distance_adjuster: Callable[[float, float, float, float, float], float | None] | None = None,
    ) -> None:
        self.orders = orders
        self.vehicles = vehicles
        self.depot_lat = depot_lat
        self.depot_lon = depot_lon
        self.depot_altitude_m = depot_altitude_m
        self.depot_name = depot_name
        self.order_ids = [order.id for order in orders]
        self.orders_by_id = {order.id: order for order in orders}
        self.id_to_index = {order.id: index for index, order in enumerate(orders)}
        latitudes = [depot_lat, *[order.latitude for order in orders]]
        longitudes = [depot_lon, *[order.longitude for order in orders]]
        altitudes = [depot_altitude_m, *[order.altitude_m for order in orders]]
        size = len(latitudes)
        self.distance_km = [
            [0.0 for _ in range(size)] for _ in range(size)
        ]
        self.elevation_delta_m = [
            [0.0 for _ in range(size)] for _ in range(size)
        ]
        self.enters_historic = [
            [False for _ in range(size)] for _ in range(size)
        ]
        self.matrix_trusted = [[True for _ in range(size)] for _ in range(size)]
        self.distance_model = [
            [ModeloDistancia.GEODESICA for _ in range(size)] for _ in range(size)
        ]
        for origin in range(size):
            for destination in range(size):
                if origin == destination:
                    continue
                distance = haversine_km(
                    latitudes[origin],
                    longitudes[origin],
                    latitudes[destination],
                    longitudes[destination],
                )
                if distance_adjuster is not None:
                    adjusted = distance_adjuster(
                        latitudes[origin],
                        longitudes[origin],
                        latitudes[destination],
                        longitudes[destination],
                        distance,
                    )
                    if adjusted is None:
                        self.matrix_trusted[origin][destination] = False
                    else:
                        distance = max(0.0, float(adjusted))
                        self.distance_model[origin][destination] = ModeloDistancia.OSRM
                delta = altitudes[destination] - altitudes[origin]
                self.distance_km[origin][destination] = distance
                self.elevation_delta_m[origin][destination] = delta
                self.enters_historic[origin][destination] = leg_enters_historic_center(
                    latitudes[origin],
                    longitudes[origin],
                    latitudes[destination],
                    longitudes[destination],
                )

    def node_index(self, order_id: int | None) -> int:
        if order_id is None:
            return 0
        return self.id_to_index[order_id] + 1


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia en kilómetros entre dos puntos WGS84."""
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    chord = sin(delta_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(chord))


def positive_elevation_gain_m(origin_m: float, destination_m: float) -> float:
    """Desnivel positivo. La bajada no reduce la emisión."""
    return max(0.0, destination_m - origin_m)


def savings_percent(baseline: float, optimized: float) -> float:
    """Porcentaje de ahorro frente a la línea base (0 si la base no es positiva)."""
    if baseline <= 0:
        return 0.0
    return max(0.0, (baseline - optimized) / baseline * 100.0)


def travel_minutes(distance_km: float, speed_kmh: float = SPEED_KMH) -> float:
    """Minutos de viaje a la velocidad media de Huancayo."""
    if speed_kmh <= 0:
        raise ValueError("La velocidad debe ser positiva.")
    if distance_km < 0:
        raise ValueError("La distancia no puede ser negativa.")
    return distance_km / speed_kmh * 60.0


def leg_co2_grams(
    distance_km: float,
    base_g_per_km: float,
    slope_penalty: float,
    elevation_gain_m: float,
) -> float:
    """Gramos de CO2 del tramo según la fórmula VRPTW del MVP."""
    if distance_km < 0 or base_g_per_km < 0 or slope_penalty < 0:
        raise ValueError("Distancia, emisión base y penalización deben ser no negativas.")
    climb = positive_elevation_gain_m(0.0, elevation_gain_m)
    return distance_km * base_g_per_km * (1.0 + slope_penalty * (climb / 100.0))


def point_in_historic_center(latitude: float, longitude: float) -> bool:
    """True si el punto cae dentro del cuadrilátero del Centro Histórico."""
    return _point_in_polygon(latitude, longitude, HISTORIC_CENTER)


def leg_enters_historic_center(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> bool:
    """True si el tramo recto pisa el Centro Histórico, aunque sea de paso."""
    if point_in_historic_center(lat1, lon1) or point_in_historic_center(lat2, lon2):
        return True
    polygon = HISTORIC_CENTER
    origin = (lat1, lon1)
    destination = (lat2, lon2)
    for index, start in enumerate(polygon):
        end = polygon[(index + 1) % len(polygon)]
        if _segments_intersect(origin, destination, start, end):
            return True
    return False


def is_large_vehicle(capacity_kg: float, capacity_m3: float) -> bool:
    """Un furgón no debe cruzar el damero. Un motocarro sí puede."""
    return capacity_kg >= LARGE_VEHICLE_MIN_KG or capacity_m3 >= LARGE_VEHICLE_MIN_M3


def solve_vrptw(
    orders: Sequence[Pedido],
    vehicles: Sequence[Vehiculo],
    depot: Deposito,
    *,
    generations: int = GENERATIONS,
    population_size: int = POPULATION_SIZE,
    seed: int = 42,
    service_minutes: float = SERVICE_MINUTES,
    distance_adjuster: Callable[[float, float, float, float, float], float | None] | None = None,
    time_budget_seconds: float | None = None,
) -> RouteSolution:
    """Resuelve el VRPTW y devuelve el itinerario, el CO2 y el ahorro frente al FIFO.

    `generations` y `population_size` conservan los valores del MVP (100 y 50)
    si el llamador no los cambia. `seed` fija la secuencia aleatoria.
    """
    if generations < 1 or population_size < 2:
        raise ValueError("El GA necesita al menos 1 generación y población de 2.")
    if service_minutes < 0:
        raise ValueError("El tiempo de servicio no puede ser negativo.")

    settings = get_settings()
    budget = (
        time_budget_seconds
        if time_budget_seconds is not None
        else settings.optimizer_time_budget_seconds
    )
    budget = max(0.0, float(budget)) if budget is not None else None

    problem = _build_problem(orders, vehicles, depot, distance_adjuster=distance_adjuster)
    if not problem.orders:
        return _empty_solution(generations, population_size, seed)

    started = perf_counter()
    rng = random.Random(seed)
    cache: dict[tuple[tuple[int, ...], ...], _Evaluation] = {}

    def evaluate(routes: list[list[int]], *, already_repaired: bool = False) -> _Evaluation:
        normalized = routes if already_repaired else _repair(routes, problem)
        key = tuple(tuple(route) for route in normalized)
        cached = cache.get(key)
        if cached is None:
            cached = _evaluate(problem, normalized, service_minutes)
            cache[key] = cached
        return cached

    def _is_feasible_evaluation(evaluation: _Evaluation) -> bool:
        return (
            evaluation.late_minutes == 0.0
            and evaluation.capacity_excess_kg == 0.0
            and evaluation.capacity_excess_m3 == 0.0
            and evaluation.shift_excess_minutes == 0.0
            and not evaluation.unassigned_order_ids
        )

    population = _initial_population(problem, population_size, rng)
    for individual in population:
        individual.routes = _repair(individual.routes, problem)
        individual.evaluation = evaluate(individual.routes, already_repaired=True)

    history: list[float] = []
    stop_reason = "generations_complete"
    generations_executed = 0
    best_feasible: _Individual | None = None
    stagnation = 0
    last_feasible_fitness: float | None = None

    for generation_index in range(generations):
        generations_executed = generation_index + 1
        population.sort(key=lambda item: item.fitness)
        history.append(population[0].fitness)
        leader = population[0]
        if leader.evaluation is not None and _is_feasible_evaluation(leader.evaluation):
            if (
                best_feasible is None
                or leader.evaluation.fitness < best_feasible.evaluation.fitness  # type: ignore[union-attr]
            ):
                best_feasible = _Individual(
                    routes=_copy_routes(leader.routes),
                    evaluation=leader.evaluation,
                )
                stagnation = 0
                last_feasible_fitness = leader.evaluation.fitness
            else:
                stagnation += 1

        if budget is not None and perf_counter() - started >= budget:
            stop_reason = "time_budget"
            break
        if (
            settings.optimizer_early_stop_feasible
            and best_feasible is not None
            and stagnation >= settings.optimizer_stagnation_generations
        ):
            stop_reason = "feasible_stagnation"
            break
        if generation_index == generations - 1:
            break
        children: list[_Individual] = [
            _Individual(routes=_copy_routes(population[0].routes), evaluation=population[0].evaluation)
        ]
        while len(children) < population_size:
            parent_a = _tournament(population, rng)
            parent_b = _tournament(population, rng)
            child_routes = _order_crossover(parent_a.routes, parent_b.routes, rng)
            if rng.random() < MUTATION_RATE:
                child_routes = _swap_mutation(child_routes, rng)
            if rng.random() < TRANSFER_RATE:
                child_routes = _transfer_mutation(child_routes, rng)
            child_routes = _repair(child_routes, problem)
            children.append(
                _Individual(
                    routes=child_routes,
                    evaluation=evaluate(child_routes, already_repaired=True),
                )
            )
        population = children

    if stop_reason == "time_budget" and best_feasible is not None:
        best = best_feasible
    else:
        best = min(population, key=lambda item: item.fitness)
    ga_elapsed = perf_counter() - started
    fifo_routes = _repair(_fifo_routes(problem), problem)
    fifo = evaluate(fifo_routes, already_repaired=True)
    sequential_routes = _repair(_sequential_baseline_routes(problem), problem)
    sequential = evaluate(sequential_routes, already_repaired=True)
    elapsed = perf_counter() - started
    return _to_solution(
        best.evaluation if best.evaluation is not None else evaluate(best.routes),
        fifo_co2_grams=fifo.co2_grams,
        fifo_distance_km=fifo.distance_km,
        sequential_co2_grams=sequential.co2_grams,
        sequential_distance_km=sequential.distance_km,
        generations=generations,
        population_size=population_size,
        seed=seed,
        history=history,
        generations_executed=generations_executed,
        ga_elapsed_seconds=ga_elapsed,
        solver_elapsed_seconds=elapsed,
        stop_reason=stop_reason,
    )


def _build_problem(
    orders: Sequence[Pedido],
    vehicles: Sequence[Vehiculo],
    depot: Deposito,
    distance_adjuster: Callable[[float, float, float, float, float], float | None] | None = None,
) -> _Problem:
    active = [vehicle for vehicle in vehicles if getattr(vehicle, "activo", True)]
    if not active:
        raise ValueError("Se necesita al menos un vehículo activo.")
    adapted_orders = [_adapt_order(order) for order in orders]
    seen: set[int] = set()
    for order in adapted_orders:
        if order.id in seen:
            raise ValueError(f"El pedido {order.id} está repetido.")
        seen.add(order.id)
        if order.window_end <= order.window_start:
            raise ValueError(f"La ventana del pedido {order.code} está invertida.")
    adapted_vehicles = sorted(
        (_adapt_vehicle(vehicle) for vehicle in active),
        key=lambda vehicle: vehicle.id,
    )
    depot_lat, depot_lon = _lat_lon(depot.ubicacion)
    return _Problem(
        orders=sorted(adapted_orders, key=lambda order: order.id),
        vehicles=adapted_vehicles,
        depot_lat=depot_lat,
        depot_lon=depot_lon,
        depot_altitude_m=float(depot.altitud_msnm),
        depot_name=str(depot.nombre),
        distance_adjuster=distance_adjuster,
    )


def _adapt_order(order: Pedido) -> _OrderNode:
    latitude, longitude = _lat_lon(order.ubicacion)
    return _OrderNode(
        id=int(order.id),
        code=str(order.codigo_pedido),
        customer=str(order.cliente_nombre),
        latitude=latitude,
        longitude=longitude,
        altitude_m=float(order.altitud_msnm),
        weight_kg=float(order.peso_kg),
        volume_m3=float(order.volumen_m3) if order.volumen_m3 is not None else None,
        window_start=_as_aware(order.ventana_inicio),
        window_end=_as_aware(order.ventana_fin),
    )


def _adapt_vehicle(vehicle: Vehiculo) -> _VehicleNode:
    capacity_kg = float(vehicle.capacidad_kg)
    capacity_m3 = float(vehicle.capacidad_m3)
    return _VehicleNode(
        id=int(vehicle.id),
        plate=str(vehicle.placa),
        capacity_kg=capacity_kg,
        capacity_m3=capacity_m3,
        fuel=TipoCombustible(vehicle.tipo_combustible),
        base_g_per_km=float(vehicle.emision_base_co2_g_km),
        slope_penalty=float(vehicle.factor_penalizacion_pendiente),
        large=is_large_vehicle(capacity_kg, capacity_m3),
    )


def _lat_lon(geometry: Any) -> tuple[float, float]:
    geojson = geometry_to_geojson(geometry)
    longitude, latitude = geojson["coordinates"][:2]
    return float(latitude), float(longitude)


def _as_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=LIMA)
    return value


def _initial_population(
    problem: _Problem,
    population_size: int,
    rng: random.Random,
) -> list[_Individual]:
    if len(problem.orders) > 60:
        seeds = [
            _fifo_routes(problem),
            _sequential_baseline_routes(problem),
        ]
    else:
        seeds = [
            _fifo_routes(problem),
            _sequential_baseline_routes(problem),
            _eco_routes(problem),
            _nearest_routes(problem),
            _single_vehicle_routes(problem),
        ]
    population = [_Individual(routes=_copy_routes(routes)) for routes in seeds]
    while len(population) < population_size:
        population.append(_Individual(routes=_random_routes(problem, rng)))
    return population[:population_size]


def _remaining_capacities(problem: _Problem) -> tuple[list[float], list[float]]:
    return (
        [vehicle.capacity_kg for vehicle in problem.vehicles],
        [vehicle.capacity_m3 for vehicle in problem.vehicles],
    )


def _sequential_baseline_routes(problem: _Problem) -> list[list[int]]:
    """Línea base RN-008: pedidos por id, vehículos por id, sin reordenar visitas."""
    routes = [[] for _ in problem.vehicles]
    remaining_kg, remaining_m3 = _remaining_capacities(problem)
    orders_by_id = {order.id: order for order in problem.orders}
    vehicle_idx = 0
    for order_id in problem.order_ids:
        order = orders_by_id[order_id]
        placed = False
        while vehicle_idx < len(problem.vehicles):
            if remaining_kg[vehicle_idx] >= order.weight_kg and (
                order.volume_m3 is None or remaining_m3[vehicle_idx] >= order.volume_m3
            ):
                routes[vehicle_idx].append(order_id)
                remaining_kg[vehicle_idx] -= order.weight_kg
                if order.volume_m3 is not None:
                    remaining_m3[vehicle_idx] -= order.volume_m3
                placed = True
                break
            vehicle_idx += 1
        if not placed and problem.vehicles:
            last = len(problem.vehicles) - 1
            routes[last].append(order_id)
            remaining_kg[last] -= order.weight_kg
            if order.volume_m3 is not None:
                remaining_m3[last] -= order.volume_m3
    return routes


def _fifo_routes(problem: _Problem) -> list[list[int]]:
    """Asigna en orden de apertura de ventana, llenando vehículos por id."""
    routes = [[] for _ in problem.vehicles]
    remaining_kg, remaining_m3 = _remaining_capacities(problem)
    ordered = sorted(problem.orders, key=lambda order: (order.window_start, order.id))
    for order in ordered:
        _place_order(routes, remaining_kg, remaining_m3, problem, order.id, prefer_capacity=True)
    return routes


def _eco_routes(problem: _Problem) -> list[list[int]]:
    """Prefiere el vehículo de menor emisión base que todavía tiene cupo."""
    routes = [[] for _ in problem.vehicles]
    remaining_kg, remaining_m3 = _remaining_capacities(problem)
    ranked = sorted(range(len(problem.vehicles)), key=lambda index: problem.vehicles[index].base_g_per_km)
    ordered = sorted(problem.orders, key=lambda order: (order.window_start, order.id))
    orders_by_id = {order.id: order for order in problem.orders}
    for order in ordered:
        placed = False
        for index in ranked:
            item = orders_by_id[order.id]
            if remaining_kg[index] < item.weight_kg:
                continue
            if item.volume_m3 is not None and remaining_m3[index] < item.volume_m3:
                continue
            routes[index].append(order.id)
            remaining_kg[index] -= item.weight_kg
            if item.volume_m3 is not None:
                remaining_m3[index] -= item.volume_m3
            placed = True
            break
        if not placed:
            _place_order(routes, remaining_kg, remaining_m3, problem, order.id, prefer_capacity=False)
    return routes


def _nearest_routes(problem: _Problem) -> list[list[int]]:
    """Vecino más cercano con cupo, un vehículo detrás de otro."""
    routes = [[] for _ in problem.vehicles]
    remaining_kg, remaining_m3 = _remaining_capacities(problem)
    pending = {order.id for order in problem.orders}
    orders_by_id = {order.id: order for order in problem.orders}
    for index, _vehicle in enumerate(problem.vehicles):
        current = 0
        while True:
            candidates = []
            for order_id in pending:
                item = orders_by_id[order_id]
                if remaining_kg[index] < item.weight_kg:
                    continue
                if item.volume_m3 is not None and remaining_m3[index] < item.volume_m3:
                    continue
                candidates.append(order_id)
            if not candidates:
                break
            chosen = min(
                candidates,
                key=lambda order_id: problem.distance_km[current][problem.node_index(order_id)],
            )
            item = orders_by_id[chosen]
            routes[index].append(chosen)
            remaining_kg[index] -= item.weight_kg
            if item.volume_m3 is not None:
                remaining_m3[index] -= item.volume_m3
            pending.remove(chosen)
            current = problem.node_index(chosen)
    return routes


def _single_vehicle_routes(problem: _Problem) -> list[list[int]]:
    routes = [[] for _ in problem.vehicles]
    host = max(range(len(problem.vehicles)), key=lambda index: problem.vehicles[index].capacity_kg)
    routes[host] = [order.id for order in sorted(problem.orders, key=lambda order: order.window_start)]
    return routes


def _random_routes(problem: _Problem, rng: random.Random) -> list[list[int]]:
    routes = [[] for _ in problem.vehicles]
    remaining_kg, remaining_m3 = _remaining_capacities(problem)
    order_ids = list(problem.order_ids)
    rng.shuffle(order_ids)
    for order_id in order_ids:
        _place_order(
            routes,
            remaining_kg,
            remaining_m3,
            problem,
            order_id,
            prefer_capacity=True,
            rng=rng,
        )
    return routes


def _place_order(
    routes: list[list[int]],
    remaining_kg: list[float],
    remaining_m3: list[float],
    problem: _Problem,
    order_id: int,
    *,
    prefer_capacity: bool,
    rng: random.Random | None = None,
) -> None:
    order = next(item for item in problem.orders if item.id == order_id)
    feasible: list[int] = []
    for index, (cap_kg, cap_m3) in enumerate(zip(remaining_kg, remaining_m3, strict=True)):
        if cap_kg < order.weight_kg:
            continue
        if order.volume_m3 is not None and cap_m3 < order.volume_m3:
            continue
        feasible.append(index)
    if feasible:
        if rng is None or not prefer_capacity:
            chosen = feasible[0] if rng is None else rng.choice(feasible)
        else:
            chosen = rng.choice(feasible)
    else:
        chosen = max(range(len(remaining_kg)), key=lambda index: remaining_kg[index])
    routes[chosen].append(order_id)
    remaining_kg[chosen] -= order.weight_kg
    if order.volume_m3 is not None:
        remaining_m3[chosen] -= order.volume_m3


def _order_crossover(
    parent_a: list[list[int]],
    parent_b: list[list[int]],
    rng: random.Random,
) -> list[list[int]]:
    """Order Crossover (OX). Conserva un tramo de A y completa con el orden de B."""
    flat_a, sizes_a = _flatten(parent_a)
    flat_b, sizes_b = _flatten(parent_b)
    if len(flat_a) < 2:
        return _copy_routes(parent_a)
    child = _ox_permutation(flat_a, flat_b, rng)
    sizes = sizes_a if rng.random() < 0.5 else sizes_b
    return _unflatten(child, sizes)


def _ox_permutation(parent_a: list[int], parent_b: list[int], rng: random.Random) -> list[int]:
    length = len(parent_a)
    start, end = sorted(rng.sample(range(length), 2))
    child: list[int | None] = [None] * length
    child[start : end + 1] = parent_a[start : end + 1]
    placed = set(parent_a[start : end + 1])
    fill = [gene for gene in parent_b if gene not in placed]
    cursor = 0
    for index in range(length):
        if child[index] is None:
            child[index] = fill[cursor]
            cursor += 1
    return [gene for gene in child if gene is not None]


def _swap_mutation(routes: list[list[int]], rng: random.Random) -> list[list[int]]:
    """Intercambia dos pedidos de la permutación. Puede cambiar de vehículo."""
    flat, sizes = _flatten(routes)
    if len(flat) < 2:
        return _copy_routes(routes)
    left, right = rng.sample(range(len(flat)), 2)
    flat[left], flat[right] = flat[right], flat[left]
    return _unflatten(flat, sizes)


def _transfer_mutation(routes: list[list[int]], rng: random.Random) -> list[list[int]]:
    """Mueve un pedido a otro vehículo para cambiar el largo de las rutas."""
    mutated = _copy_routes(routes)
    donors = [index for index, route in enumerate(mutated) if route]
    if not donors or len(mutated) < 2:
        return mutated
    source = rng.choice(donors)
    target = rng.randrange(len(mutated))
    if source == target and len(mutated[source]) < 2:
        return mutated
    position = rng.randrange(len(mutated[source]))
    order_id = mutated[source].pop(position)
    insert_at = rng.randint(0, len(mutated[target]))
    mutated[target].insert(insert_at, order_id)
    return mutated


def _tournament(population: list[_Individual], rng: random.Random) -> _Individual:
    contenders = rng.sample(population, k=min(TOURNAMENT_SIZE, len(population)))
    return min(contenders, key=lambda individual: individual.fitness)


def _evaluate(
    problem: _Problem,
    routes: list[list[int]],
    service_minutes: float,
) -> _Evaluation:
    itineraries: list[VehicleItinerary] = []
    distance_km = 0.0
    duration_minutes = 0.0
    co2_grams = 0.0
    late_minutes = 0.0
    capacity_excess_kg = 0.0
    capacity_excess_m3 = 0.0
    shift_excess_minutes = 0.0
    historic_entries = 0
    orders_by_id = problem.orders_by_id
    unassigned = _unassigned_order_ids(routes, problem)
    for vehicle, order_ids in zip(problem.vehicles, routes, strict=True):
        itinerary = _schedule_vehicle(problem, vehicle, order_ids, orders_by_id, service_minutes)
        itineraries.append(itinerary)
        distance_km += itinerary.distance_km
        duration_minutes += itinerary.duration_minutes
        co2_grams += itinerary.co2_grams
        late_minutes += sum(stop.late_minutes for stop in itinerary.stops)
        capacity_excess_kg += itinerary.capacity_excess_kg
        capacity_excess_m3 += itinerary.capacity_excess_m3
        shift_excess_minutes += itinerary.shift_excess_minutes
        historic_entries += itinerary.historic_entries
    co2_kg = co2_grams / 1000.0
    fitness = (
        distance_km
        + CO2_KG_WEIGHT * co2_kg
        + LATE_PENALTY_PER_MIN * late_minutes
        + CAPACITY_PENALTY_PER_KG * capacity_excess_kg
        + VOLUME_PENALTY_PER_M3 * capacity_excess_m3
        + SHIFT_PENALTY_PER_MIN * shift_excess_minutes
        + UNASSIGNED_PENALTY * len(unassigned)
        + HISTORIC_PENALTY_PER_LEG * historic_entries
    )
    return _Evaluation(
        fitness=fitness,
        distance_km=distance_km,
        duration_minutes=duration_minutes,
        co2_grams=co2_grams,
        late_minutes=late_minutes,
        capacity_excess_kg=capacity_excess_kg,
        capacity_excess_m3=capacity_excess_m3,
        shift_excess_minutes=shift_excess_minutes,
        unassigned_order_ids=unassigned,
        historic_entries=historic_entries,
        itineraries=tuple(itineraries),
    )


def _schedule_vehicle(
    problem: _Problem,
    vehicle: _VehicleNode,
    order_ids: list[int],
    orders_by_id: dict[int, _OrderNode],
    service_minutes: float,
) -> VehicleItinerary:
    settings = get_settings()
    load_kg = sum(orders_by_id[order_id].weight_kg for order_id in order_ids)
    volume_orders = [
        orders_by_id[order_id].volume_m3
        for order_id in order_ids
        if orders_by_id[order_id].volume_m3 is not None
    ]
    load_m3 = sum(volume_orders)
    has_volume = bool(volume_orders)
    excess_kg = max(0.0, load_kg - vehicle.capacity_kg)
    excess_m3 = max(0.0, load_m3 - vehicle.capacity_m3) if has_volume else 0.0
    if not order_ids:
        return VehicleItinerary(
            vehicle_id=vehicle.id,
            plate=vehicle.plate,
            fuel=vehicle.fuel,
            capacity_kg=vehicle.capacity_kg,
            capacity_m3=vehicle.capacity_m3,
            load_kg=0.0,
            load_m3=0.0,
            stops=(),
            distance_km=0.0,
            co2_grams=0.0,
            duration_minutes=0.0,
            capacity_excess_kg=excess_kg,
            capacity_excess_m3=excess_m3,
            shift_minutes=0.0,
            shift_excess_minutes=0.0,
            historic_entries=0,
        )

    first = orders_by_id[order_ids[0]]
    first_travel = travel_minutes(problem.distance_km[0][problem.node_index(first.id)])
    departure = first.window_start - timedelta(minutes=first_travel)
    clock = departure
    previous = 0
    stops: list[StopItinerary] = [
        _depot_stop(
            sequence=0,
            stop_type=TipoParada.DEPOT_START,
            problem=problem,
            eta=departure,
        )
    ]
    distance_km = 0.0
    co2_grams = 0.0
    historic_entries = 0
    delivery_index = 0
    for order_id in order_ids:
        order = orders_by_id[order_id]
        delivery_index += 1
        stop, clock = _visit(
            problem=problem,
            vehicle=vehicle,
            order=order,
            previous=previous,
            clock=clock,
            sequence=len(stops),
            service_minutes=service_minutes,
            delivery_index=delivery_index,
        )
        stops.append(stop)
        distance_km += stop.distance_km
        co2_grams += stop.co2_grams
        historic_entries += int(stop.enters_historic_center)
        previous = problem.node_index(order_id)

    return_stop, clock = _return_to_depot(
        problem=problem,
        vehicle=vehicle,
        previous=previous,
        clock=clock,
        sequence=len(stops),
    )
    stops.append(return_stop)
    distance_km += return_stop.distance_km
    co2_grams += return_stop.co2_grams
    historic_entries += int(return_stop.enters_historic_center)
    duration = max(0.0, (clock - departure).total_seconds() / 60.0)
    shift_minutes = sum(stop.travel_minutes for stop in stops) + len(order_ids) * service_minutes
    shift_excess = 0.0
    if settings.enforce_shift_limit:
        shift_excess = max(0.0, shift_minutes - settings.max_shift_minutes)
    return VehicleItinerary(
        vehicle_id=vehicle.id,
        plate=vehicle.plate,
        fuel=vehicle.fuel,
        capacity_kg=vehicle.capacity_kg,
        capacity_m3=vehicle.capacity_m3,
        load_kg=load_kg,
        load_m3=load_m3,
        stops=tuple(stops),
        distance_km=distance_km,
        co2_grams=co2_grams,
        duration_minutes=duration,
        capacity_excess_kg=excess_kg,
        capacity_excess_m3=excess_m3,
        shift_minutes=shift_minutes,
        shift_excess_minutes=shift_excess,
        historic_entries=historic_entries,
    )


def _visit(
    *,
    problem: _Problem,
    vehicle: _VehicleNode,
    order: _OrderNode,
    previous: int,
    clock: datetime,
    sequence: int,
    service_minutes: float,
    delivery_index: int,
) -> tuple[StopItinerary, datetime]:
    current = problem.node_index(order.id)
    distance = problem.distance_km[previous][current]
    delta_h = problem.elevation_delta_m[previous][current]
    trusted = problem.matrix_trusted[previous][current]
    leg_model = problem.distance_model[previous][current]
    minutes = travel_minutes(distance)
    arrival = clock + timedelta(minutes=minutes)
    enters = vehicle.large and problem.enters_historic[previous][current]
    gain = positive_elevation_gain_m(0.0, delta_h)
    co2 = leg_co2_grams(distance, vehicle.base_g_per_km, vehicle.slope_penalty, gain)
    if not trusted:
        stop = StopItinerary(
            sequence=sequence,
            stop_type=TipoParada.DELIVERY,
            order_id=order.id,
            order_code=order.code,
            customer_name=order.customer,
            latitude=order.latitude,
            longitude=order.longitude,
            altitude_m=order.altitude_m,
            eta=None,
            distance_km=distance,
            elevation_delta_m=delta_h,
            travel_minutes=minutes,
            co2_grams=co2,
            late_minutes=0.0,
            enters_historic_center=enters,
            eta_estado=EstadoEta.REVISION_MATRIZ,
            wait_minutes=0.0,
            delivery_index=delivery_index,
            distance_model=leg_model,
            matrix_trusted=False,
        )
        return stop, service_start_after_arrival(arrival, order.window_start, service_minutes)
    eta_state, wait_min, late = classify_delivery_arrival(
        arrival,
        order.window_start,
        order.window_end,
        matrix_available=True,
    )
    stop = StopItinerary(
        sequence=sequence,
        stop_type=TipoParada.DELIVERY,
        order_id=order.id,
        order_code=order.code,
        customer_name=order.customer,
        latitude=order.latitude,
        longitude=order.longitude,
        altitude_m=order.altitude_m,
        eta=arrival,
        distance_km=distance,
        elevation_delta_m=delta_h,
        travel_minutes=minutes,
        co2_grams=co2,
        late_minutes=late,
        enters_historic_center=enters,
        eta_estado=eta_state,
        wait_minutes=wait_min,
        delivery_index=delivery_index,
        distance_model=leg_model,
        matrix_trusted=True,
    )
    return stop, service_start_after_arrival(arrival, order.window_start, service_minutes)


def _return_to_depot(
    *,
    problem: _Problem,
    vehicle: _VehicleNode,
    previous: int,
    clock: datetime,
    sequence: int,
) -> tuple[StopItinerary, datetime]:
    distance = problem.distance_km[previous][0]
    delta_h = problem.elevation_delta_m[previous][0]
    minutes = travel_minutes(distance)
    arrival = clock + timedelta(minutes=minutes)
    enters = vehicle.large and problem.enters_historic[previous][0]
    gain = positive_elevation_gain_m(0.0, delta_h)
    co2 = leg_co2_grams(distance, vehicle.base_g_per_km, vehicle.slope_penalty, gain)
    stop = _depot_stop(
        sequence=sequence,
        stop_type=TipoParada.DEPOT_END,
        problem=problem,
        eta=arrival,
        distance_km=distance,
        elevation_delta_m=delta_h,
        travel_minutes=minutes,
        co2_grams=co2,
        enters_historic_center=enters,
        eta_estado=EstadoEta.CALCULADO,
        distance_model=problem.distance_model[previous][0],
        matrix_trusted=problem.matrix_trusted[previous][0],
    )
    return stop, arrival


def _depot_stop(
    *,
    sequence: int,
    stop_type: TipoParada,
    problem: _Problem,
    eta: datetime | None,
    distance_km: float = 0.0,
    elevation_delta_m: float = 0.0,
    travel_minutes: float = 0.0,
    co2_grams: float = 0.0,
    enters_historic_center: bool = False,
    eta_estado: EstadoEta = EstadoEta.CALCULADO,
    distance_model: ModeloDistancia = ModeloDistancia.GEODESICA,
    matrix_trusted: bool = True,
) -> StopItinerary:
    return StopItinerary(
        sequence=sequence,
        stop_type=stop_type,
        order_id=None,
        order_code=None,
        customer_name=problem.depot_name,
        latitude=problem.depot_lat,
        longitude=problem.depot_lon,
        altitude_m=problem.depot_altitude_m,
        eta=eta,
        distance_km=distance_km,
        elevation_delta_m=elevation_delta_m,
        travel_minutes=travel_minutes,
        co2_grams=co2_grams,
        late_minutes=0.0,
        enters_historic_center=enters_historic_center,
        eta_estado=eta_estado,
        distance_model=distance_model,
        matrix_trusted=matrix_trusted,
    )


def _repair(routes: list[list[int]], problem: _Problem) -> list[list[int]]:
    """Garantiza que cada pedido aparezca una sola vez."""
    cleaned: list[list[int]] = [[] for _ in problem.vehicles]
    seen: set[int] = set()
    valid = set(problem.order_ids)
    for index, route in enumerate(routes):
        if index >= len(cleaned):
            break
        for order_id in route:
            if order_id in valid and order_id not in seen:
                cleaned[index].append(order_id)
                seen.add(order_id)
    return cleaned


def _unassigned_order_ids(routes: list[list[int]], problem: _Problem) -> tuple[int, ...]:
    assigned: set[int] = set()
    for route in routes:
        assigned.update(route)
    missing = [order_id for order_id in problem.order_ids if order_id not in assigned]
    return tuple(sorted(missing))


def _flatten(routes: list[list[int]]) -> tuple[list[int], list[int]]:
    flat: list[int] = []
    sizes: list[int] = []
    for route in routes:
        flat.extend(route)
        sizes.append(len(route))
    return flat, sizes


def _unflatten(flat: list[int], sizes: list[int]) -> list[list[int]]:
    routes: list[list[int]] = []
    cursor = 0
    for size in sizes:
        routes.append(flat[cursor : cursor + size])
        cursor += size
    if cursor < len(flat):
        if not routes:
            routes.append([])
        routes[-1].extend(flat[cursor:])
    return routes


def _copy_routes(routes: list[list[int]]) -> list[list[int]]:
    return [list(route) for route in routes]


def _to_solution(
    evaluation: _Evaluation,
    *,
    fifo_co2_grams: float,
    fifo_distance_km: float,
    sequential_co2_grams: float,
    sequential_distance_km: float,
    generations: int,
    population_size: int,
    seed: int,
    history: list[float],
    generations_executed: int,
    solver_elapsed_seconds: float,
    stop_reason: str,
    ga_elapsed_seconds: float | None = None,
) -> RouteSolution:
    fifo_co2_kg = fifo_co2_grams / 1000.0
    co2_kg = evaluation.co2_grams / 1000.0
    saved = fifo_co2_kg - co2_kg
    avoided = max(0.0, saved)
    sequential_co2_kg = sequential_co2_grams / 1000.0
    savings_dist = savings_percent(sequential_distance_km, evaluation.distance_km)
    savings_co2 = savings_percent(sequential_co2_kg, co2_kg)
    feasible = (
        evaluation.late_minutes == 0.0
        and evaluation.capacity_excess_kg == 0.0
        and evaluation.capacity_excess_m3 == 0.0
        and evaluation.shift_excess_minutes == 0.0
        and not evaluation.unassigned_order_ids
    )
    return RouteSolution(
        itineraries=evaluation.itineraries,
        distance_km=evaluation.distance_km,
        duration_minutes=evaluation.duration_minutes,
        co2_grams=evaluation.co2_grams,
        co2_kg=co2_kg,
        fifo_co2_kg=fifo_co2_kg,
        fifo_distance_km=fifo_distance_km,
        sequential_baseline_co2_kg=sequential_co2_kg,
        sequential_baseline_distance_km=sequential_distance_km,
        savings_co2_pct_vs_sequential=savings_co2,
        savings_distance_pct_vs_sequential=savings_dist,
        rn008_distance_goal_met=savings_dist >= RN008_MIN_DISTANCE_SAVINGS_PCT,
        rn008_co2_goal_met=savings_co2 >= RN008_MIN_CO2_SAVINGS_PCT,
        co2_saved_kg=saved,
        arboles_quinual_eq=quinual_equivalent(avoided),
        fitness=evaluation.fitness,
        feasible=feasible,
        late_minutes=evaluation.late_minutes,
        capacity_excess_kg=evaluation.capacity_excess_kg,
        capacity_excess_m3=evaluation.capacity_excess_m3,
        shift_excess_minutes=evaluation.shift_excess_minutes,
        unassigned_order_ids=evaluation.unassigned_order_ids,
        historic_entries=evaluation.historic_entries,
        generations=generations,
        population_size=population_size,
        seed=seed,
        best_fitness_per_generation=tuple(history),
        generations_executed=generations_executed,
        ga_elapsed_seconds=ga_elapsed_seconds if ga_elapsed_seconds is not None else solver_elapsed_seconds,
        solver_elapsed_seconds=solver_elapsed_seconds,
        stop_reason=stop_reason,
    )


def _empty_solution(generations: int, population_size: int, seed: int) -> RouteSolution:
    return RouteSolution(
        itineraries=(),
        distance_km=0.0,
        duration_minutes=0.0,
        co2_grams=0.0,
        co2_kg=0.0,
        fifo_co2_kg=0.0,
        fifo_distance_km=0.0,
        sequential_baseline_co2_kg=0.0,
        sequential_baseline_distance_km=0.0,
        savings_co2_pct_vs_sequential=0.0,
        savings_distance_pct_vs_sequential=0.0,
        rn008_distance_goal_met=False,
        rn008_co2_goal_met=False,
        co2_saved_kg=0.0,
        arboles_quinual_eq=0.0,
        fitness=0.0,
        feasible=True,
        late_minutes=0.0,
        capacity_excess_kg=0.0,
        capacity_excess_m3=0.0,
        shift_excess_minutes=0.0,
        unassigned_order_ids=(),
        historic_entries=0,
        generations=generations,
        population_size=population_size,
        seed=seed,
        best_fitness_per_generation=tuple(0.0 for _ in range(generations)),
        generations_executed=0,
        ga_elapsed_seconds=0.0,
        solver_elapsed_seconds=0.0,
        stop_reason="empty",
    )


def _point_in_polygon(
    latitude: float,
    longitude: float,
    polygon: Sequence[tuple[float, float]],
) -> bool:
    """Rayo hacia el este. El borde exacto puede quedar fuera; el polígono lo compensa."""
    inside = False
    count = len(polygon)
    for index in range(count):
        lat_i, lon_i = polygon[index]
        lat_j, lon_j = polygon[(index + 1) % count]
        if (lat_i > latitude) == (lat_j > latitude):
            continue
        intersect_lon = lon_i + (latitude - lat_i) * (lon_j - lon_i) / (lat_j - lat_i)
        if longitude < intersect_lon:
            inside = not inside
    return inside


def _segments_intersect(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> bool:
    d1 = _cross(p3, p4, p1)
    d2 = _cross(p3, p4, p2)
    d3 = _cross(p1, p2, p3)
    d4 = _cross(p1, p2, p4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and (
        (d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)
    ):
        return True
    epsilon = 1e-12
    if abs(d1) <= epsilon and _on_segment(p3, p4, p1):
        return True
    if abs(d2) <= epsilon and _on_segment(p3, p4, p2):
        return True
    if abs(d3) <= epsilon and _on_segment(p1, p2, p3):
        return True
    if abs(d4) <= epsilon and _on_segment(p1, p2, p4):
        return True
    return False


def _cross(
    origin: tuple[float, float],
    end: tuple[float, float],
    point: tuple[float, float],
) -> float:
    return (end[0] - origin[0]) * (point[1] - origin[1]) - (end[1] - origin[1]) * (point[0] - origin[0])


def _on_segment(
    start: tuple[float, float],
    end: tuple[float, float],
    point: tuple[float, float],
) -> bool:
    return (
        min(start[0], end[0]) - 1e-12 <= point[0] <= max(start[0], end[0]) + 1e-12
        and min(start[1], end[1]) - 1e-12 <= point[1] <= max(start[1], end[1]) + 1e-12
    )
