import type { ActiveRoute, Depot, Order, OrderTracking, RouteOptimization, Vehicle } from "./types";

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, init);
  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = (await response.json()) as { detail?: unknown };
      if (typeof body.detail === "string") {
        detail = body.detail;
      }
    } catch {
      detail = response.statusText;
    }
    throw new ApiError(detail || "No se pudo completar la solicitud.", response.status);
  }
  return (await response.json()) as T;
}

export function fetchOrders(): Promise<Order[]> {
  return request<Order[]>("/api/v1/pedidos");
}

export function fetchVehicles(): Promise<Vehicle[]> {
  return request<Vehicle[]>("/api/v1/vehiculos");
}

export function fetchDepots(): Promise<Depot[]> {
  return request<Depot[]>("/api/v1/depositos");
}

export function fetchTracking(orderCode: string): Promise<OrderTracking> {
  return request<OrderTracking>(`/api/v1/seguimiento/${encodeURIComponent(orderCode)}`);
}

export function fetchActiveRoute(plate?: string): Promise<ActiveRoute> {
  const query = plate ? `?placa=${encodeURIComponent(plate)}` : "";
  return request<ActiveRoute>(`/api/v1/rutas/activas${query}`);
}

export function optimizeRoutes(): Promise<RouteOptimization> {
  return request<RouteOptimization>("/api/v1/optimizar-rutas", { method: "POST" });
}
