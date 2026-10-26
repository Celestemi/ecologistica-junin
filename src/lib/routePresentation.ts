import type { RouteFeature, RouteOptimization } from "../types";

export type RouteStop = {
  key: string;
  plate: string;
  sequence: number;
  deliveryIndex: number | null;
  type: string;
  orderCode: string | null;
  customer: string | null;
  address: string | null;
  weightKg: number | null;
  eta: string | null;
  windowStart: string | null;
  windowEnd: string | null;
  etaStatus: string | null;
  co2g: number;
  coordinates: [number, number];
};

export function routeStops(solution: RouteOptimization | null, plate?: string | null): RouteStop[] {
  if (!solution) return [];
  return solution.features
    .filter(isPoint)
    .filter((feature) => !plate || feature.properties.plate === plate)
    .map((feature) => ({
      key: `${feature.properties.plate ?? "route"}:${feature.properties.sequence ?? 0}:${feature.properties.order_code ?? feature.properties.stop_type ?? "stop"}`,
      plate: feature.properties.plate ?? "Sin vehículo",
      sequence: feature.properties.sequence ?? 0,
      deliveryIndex: feature.properties.delivery_index ?? null,
      type: feature.properties.stop_type ?? "delivery",
      orderCode: feature.properties.order_code ?? null,
      customer: feature.properties.customer ?? null,
      address: feature.properties.address ?? feature.properties.title ?? null,
      weightKg: feature.properties.weight_kg ?? null,
      eta: feature.properties.eta ?? null,
      windowStart: feature.properties.window_start ?? null,
      windowEnd: feature.properties.window_end ?? null,
      etaStatus: feature.properties.eta_estado ?? null,
      co2g: feature.properties.co2_g ?? 0,
      coordinates: feature.geometry.coordinates,
    }))
    .sort((left, right) => left.plate.localeCompare(right.plate) || left.sequence - right.sequence);
}

function isPoint(feature: RouteFeature): feature is RouteFeature & { geometry: { type: "Point"; coordinates: [number, number] } } {
  return feature.geometry.type === "Point";
}
