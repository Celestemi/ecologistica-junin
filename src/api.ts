import { loadSession, clearSession, type SessionUser } from "./lib/session";
import type { ActiveRoute, Depot, Order, OrderTracking, RouteOptimization, Vehicle } from "./types";

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

function withAuth(init?: RequestInit): RequestInit {
  const headers = new Headers(init?.headers);
  const session = loadSession();
  if (session && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${session.token}`);
  }
  return { ...init, headers };
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, withAuth(init));
  if (response.status === 401 && loadSession()) {
    clearSession();
    const pathName = window.location.pathname;
    if (!pathName.startsWith("/ingresar") && !pathName.startsWith("/seguimiento")) {
      window.location.assign("/ingresar");
    }
  }
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

export type VehicleHistory = {
  activo: boolean;
  detalle: string;
  correo: string;
  creado_en: string;
};

export type ImportRow = {
  linea: number;
  codigo_pedido: string;
  cliente_nombre: string;
  direccion_referencia: string;
  peso_kg: number | null;
  hora_inicio: string;
  hora_fin: string;
  lat: number | null;
  lon: number | null;
  altitud_msnm: number | null;
  resultado: "aceptado" | "rechazado" | "pendiente_punto";
  motivo: string | null;
};

export type ImportReport = {
  fecha: string;
  aceptados: number;
  filas: ImportRow[];
};

export type DayOrders = {
  fecha: string;
  pedidos: Order[];
};

export function fetchDay(fecha: string): Promise<DayOrders> {
  return request<DayOrders>(`/api/v1/jornadas/${fecha}`);
}

export function importDay(fecha: string, csv: string): Promise<ImportReport> {
  return request<ImportReport>(`/api/v1/jornadas/${fecha}/importar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ csv }),
  });
}

export function createOrder(body: Record<string, unknown>): Promise<Order> {
  return request<Order>("/api/v1/pedidos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

export function fetchFleet(): Promise<Vehicle[]> {
  return request<Vehicle[]>("/api/v1/flota");
}

export function createVehicle(body: Record<string, unknown>): Promise<Vehicle> {
  return request<Vehicle>("/api/v1/flota", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

export function updateVehicle(id: number, body: Record<string, unknown>): Promise<Vehicle> {
  return request<Vehicle>(`/api/v1/flota/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

export function fetchVehicleHistory(id: number): Promise<VehicleHistory[]> {
  return request<VehicleHistory[]>(`/api/v1/flota/${id}/historial`);
}

export function fetchDepots(): Promise<Depot[]> {
  return request<Depot[]>("/api/v1/depositos");
}

export function fetchTracking(orderCode: string): Promise<OrderTracking> {
  return request<OrderTracking>(`/api/v1/seguimiento/${encodeURIComponent(orderCode)}`);
}

export async function fetchPublishedRoute(): Promise<RouteOptimization | null> {
  try {
    return await request<RouteOptimization>("/api/v1/rutas/mapa");
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return null;
    }
    throw error;
  }
}

export function fetchActiveRoute(plate?: string): Promise<ActiveRoute> {
  const query = plate ? `?placa=${encodeURIComponent(plate)}` : "";
  return request<ActiveRoute>(`/api/v1/rutas/activas${query}`);
}

export function optimizeRoutes(): Promise<RouteOptimization> {
  return request<RouteOptimization>("/api/v1/optimizar-rutas", { method: "POST" });
}

export type LoginResult = {
  access_token: string;
  token_type: string;
  usuario: SessionUser;
};

export function login(correo: string, clave: string): Promise<LoginResult> {
  return request<LoginResult>("/api/v1/auth/ingresar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correo, clave }),
  });
}

export type AuditEvent = {
  id: number;
  correo: string;
  accion: string;
  detalle: string | null;
  creado_en: string;
};

export function fetchAuditLog(): Promise<AuditEvent[]> {
  return request<AuditEvent[]>("/api/v1/auth/bitacora");
}

export async function downloadSustainabilityPdf(): Promise<void> {
  const response = await fetch("/api/v1/reportes/sostenibilidad/pdf", withAuth());
  if (response.status === 401 && loadSession()) {
    clearSession();
    window.location.assign("/ingresar");
  }
  if (!response.ok) {
    let detail = "No se pudo descargar el informe.";
    try {
      const body = (await response.json()) as { detail?: unknown };
      if (typeof body.detail === "string") {
        detail = body.detail;
      }
    } catch {
      detail = "No se pudo descargar el informe.";
    }
    throw new ApiError(detail, response.status);
  }
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName(response.headers.get("Content-Disposition")) ?? "sostenibilidad.pdf";
  link.click();
  URL.revokeObjectURL(url);
}

function fileName(disposition: string | null): string | null {
  const match = disposition?.match(/filename="([^"]+)"/);
  return match?.[1] ?? null;
}
