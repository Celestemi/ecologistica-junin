// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DriverApp } from "./DriverApp";
import type { ActiveRoute, Vehicle } from "../../types";

const api = vi.hoisted(() => ({
  confirmDelivery: vi.fn(),
  fetchActiveRoute: vi.fn(),
  fetchVehicles: vi.fn(),
}));
const offline = vi.hoisted(() => ({
  cachedRoute: vi.fn(),
  cachedValue: vi.fn(),
  cacheRoute: vi.fn(),
  cacheValue: vi.fn(),
  completedDeliveryCodes: vi.fn(),
  enqueueDelivery: vi.fn(),
  markDeliveryCompleted: vi.fn(),
  pendingDeliveries: vi.fn(),
  replacePendingDeliveries: vi.fn(),
}));
const loadSession = vi.hoisted(() => vi.fn());

vi.mock("../../api", () => api);
vi.mock("../../lib/offline", () => offline);
vi.mock("../../lib/session", () => ({ loadSession }));
vi.mock("../StaffHeader", () => ({ StaffHeader: () => <header>Modo conductor</header> }));

class FakeWebSocket {
  static OPEN = 1;
  static instances: FakeWebSocket[] = [];
  readyState = 1;
  onopen: (() => void) | null = null;
  onmessage: ((event: { data: unknown }) => void) | null = null;
  onclose: (() => void) | null = null;
  send = vi.fn();
  close = vi.fn();
  constructor(public url: string) {
    FakeWebSocket.instances.push(this);
  }
}

const vehicle = {
  id: 7,
  deposito_id: 1,
  placa: "ABC-123",
  modelo: "Furgón eléctrico",
  capacidad_kg: 900,
  capacidad_m3: 12,
  tipo_combustible: "electrico",
  rendimiento_km_gal: 1,
  emision_base_co2_g_km: 0,
  factor_penalizacion_pendiente: 1,
  estado_operativo: "activo",
  activo: true,
} satisfies Vehicle;

const route: ActiveRoute = {
  codigo: "RUTA-1",
  fecha_operacion: "2026-10-27",
  paradas: [
    { secuencia: 0, tipo_parada: "depot_start", vehiculo_id: 7, placa: "ABC-123", codigo_pedido: null, cliente_nombre: null, direccion_referencia: null, peso_kg: null, ventana_inicio: null, ventana_fin: null, lat: -12.05, lon: -75.2, eta: null, co2_tramo_g: 0 },
    { secuencia: 1, tipo_parada: "delivery", vehiculo_id: 7, placa: "ABC-123", codigo_pedido: "PED-1", cliente_nombre: "Cliente Uno", direccion_referencia: "Av. Real 100", peso_kg: 12.5, ventana_inicio: "2026-10-27T14:00:00-05:00", ventana_fin: "2026-10-27T16:00:00-05:00", lat: -12.06, lon: -75.21, eta: "2026-10-27T15:00:00-05:00", co2_tramo_g: 100 },
    { secuencia: 2, tipo_parada: "depot_end", vehiculo_id: 7, placa: "ABC-123", codigo_pedido: null, cliente_nombre: null, direccion_referencia: null, peso_kg: null, ventana_inicio: null, ventana_fin: null, lat: -12.05, lon: -75.2, eta: null, co2_tramo_g: 0 },
  ],
};

describe("driver application", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
    FakeWebSocket.instances = [];
    Object.defineProperty(window, "WebSocket", { configurable: true, value: FakeWebSocket });
    Object.defineProperty(navigator, "onLine", { configurable: true, value: true });
    Object.defineProperty(navigator, "geolocation", { configurable: true, value: undefined });
    Object.defineProperty(navigator, "serviceWorker", {
      configurable: true,
      value: {
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        ready: Promise.resolve({ sync: { register: vi.fn().mockResolvedValue(undefined) } }),
      },
    });
    window.history.replaceState({}, "", "/conductor?placa=ABC-123");
    loadSession.mockReturnValue({ token: "token conductor", usuario: { id: 22, rol: "conductor" } });
    api.fetchVehicles.mockResolvedValue([vehicle]);
    api.fetchActiveRoute.mockResolvedValue(route);
    api.confirmDelivery.mockResolvedValue({});
    offline.cachedRoute.mockResolvedValue(null);
    offline.cachedValue.mockResolvedValue(null);
    offline.cacheRoute.mockResolvedValue(undefined);
    offline.cacheValue.mockResolvedValue(undefined);
    offline.completedDeliveryCodes.mockResolvedValue([]);
    offline.enqueueDelivery.mockResolvedValue(undefined);
    offline.markDeliveryCompleted.mockResolvedValue(undefined);
    offline.pendingDeliveries.mockResolvedValue([]);
    offline.replacePendingDeliveries.mockResolvedValue(undefined);
    vi.spyOn(crypto, "randomUUID").mockReturnValue("00000000-0000-4000-8000-000000000001");
  });

  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("loads the selected route and renders the next delivery", async () => {
    render(<DriverApp />);

    expect((await screen.findAllByText("Cliente Uno"))).toHaveLength(2);
    expect(api.fetchActiveRoute).toHaveBeenCalledWith("ABC-123");
    expect(offline.cacheRoute).toHaveBeenCalledWith(22, route);
    expect(screen.getByText("0 de 1 entregas")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Google Maps" }).getAttribute("href")).toContain("-12.06,-75.21");
    expect(FakeWebSocket.instances[0]?.url).toContain("ABC-123");
  });

  it("records proof of delivery and synchronizes the queued operation", async () => {
    render(<DriverApp />);
    await screen.findAllByText("Cliente Uno");

    fireEvent.click(screen.getByRole("button", { name: "Confirmar entrega" }));
    const file = new File(["evidencia"], "entrega.jpg", { type: "image/jpeg" });
    fireEvent.change(screen.getByLabelText(/Foto del comprobante/), { target: { files: [file] } });
    const queued = { id: "00000000-0000-4000-8000-000000000001", userId: 22, orderCode: "PED-1", deliveredAt: "fecha", attempts: 0 };
    offline.pendingDeliveries.mockResolvedValueOnce([queued]).mockResolvedValueOnce([queued]).mockResolvedValue([]);
    fireEvent.click(screen.getByRole("button", { name: "Registrar entrega" }));

    await waitFor(() => expect(offline.enqueueDelivery).toHaveBeenCalled());
    expect(offline.markDeliveryCompleted).toHaveBeenCalledWith(22, "PED-1");
    await waitFor(() => expect(api.confirmDelivery).toHaveBeenCalledWith("PED-1", expect.objectContaining({ operation_id: expect.any(String) })));
    expect(await screen.findByText(/Entregas pendientes sincronizadas/)).toBeTruthy();
  });

  it("uses cached fleet and route when the network is unavailable", async () => {
    Object.defineProperty(navigator, "onLine", { configurable: true, value: false });
    api.fetchVehicles.mockRejectedValue(new Error("Sin red"));
    api.fetchActiveRoute.mockRejectedValue(new Error("Ruta inaccesible"));
    offline.cachedValue.mockResolvedValue([vehicle]);
    offline.cachedRoute.mockResolvedValue(route);

    render(<DriverApp />);

    expect((await screen.findAllByText("Cliente Uno"))).toHaveLength(2);
    expect(screen.getByText(/última ruta guardada/)).toBeTruthy();
    expect(api.confirmDelivery).not.toHaveBeenCalled();
  });

  it("publishes incidents and processes dispatcher messages", async () => {
    render(<DriverApp />);
    await screen.findAllByText("Cliente Uno");
    const socket = FakeWebSocket.instances[0]!;
    socket.onopen?.();
    await waitFor(() => expect(screen.getByText("Despacho en línea")).toBeTruthy());

    fireEvent.click(screen.getByRole("button", { name: "Tráfico denso" }));
    expect(socket.send).toHaveBeenCalledWith(expect.stringContaining('"kind":"traffic"'));
    socket.onmessage?.({ data: JSON.stringify({ type: "error", detail: "Incidente rechazado" }) });
    expect(await screen.findByText("Incidente rechazado")).toBeTruthy();

    socket.onmessage?.({ data: JSON.stringify({ type: "eta", order_code: "PED-1", eta: "2026-10-27T14:30:00-05:00" }) });
    expect(await screen.findByText("14:30")).toBeTruthy();
    socket.onmessage?.({ data: JSON.stringify({ type: "route_update", reason: "bloqueo" }) });
    expect(await screen.findByText("Ruta recalculada (bloqueo)." )).toBeTruthy();
    socket.onmessage?.({ data: JSON.stringify({ type: "order_status" }) });
    socket.onmessage?.({ data: "invalid" });
    await waitFor(() => expect(api.fetchActiveRoute.mock.calls.length).toBeGreaterThan(1));
  });

  it("uses GPS positions and warns when the dispatcher link is unavailable", async () => {
    let success: ((position: GeolocationPosition) => void) | undefined;
    const clearWatch = vi.fn();
    Object.defineProperty(navigator, "geolocation", {
      configurable: true,
      value: {
        watchPosition: vi.fn((handler) => { success = handler; return 9; }),
        clearWatch,
      },
    });
    render(<DriverApp />);
    await screen.findAllByText("Cliente Uno");
    success?.({ coords: { latitude: -12.03, longitude: -75.19, altitude: 3300 } } as GeolocationPosition);
    expect(await screen.findByText("GPS del teléfono")).toBeTruthy();

    const socket = FakeWebSocket.instances[0]!;
    socket.readyState = 0;
    fireEvent.click(screen.getByRole("button", { name: "Vía bloqueada / lluvia" }));
    expect(await screen.findByText(/Sin enlace con el despacho/)).toBeTruthy();
  });
});
