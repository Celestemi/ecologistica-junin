// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";

const api = vi.hoisted(() => ({
  fetchDepots: vi.fn(),
  fetchOrders: vi.fn(),
  fetchPublishedRoute: vi.fn(),
  fetchVehicles: vi.fn(),
  optimizeRoutes: vi.fn(),
  assignOrderVehicle: vi.fn(),
}));
const loadSession = vi.hoisted(() => vi.fn());

vi.mock("./api", () => api);
vi.mock("./lib/session", () => ({ loadSession }));
vi.mock("./components/StaffHeader", () => ({ StaffHeader: () => <header>Cabecera</header> }));
vi.mock("./components/Dashboard", () => ({ Dashboard: () => <div>Indicadores</div> }));
vi.mock("./components/Sidebar", () => ({
  Sidebar: (props: { loading: boolean; error: string | null; orderCount: number; canOptimize: boolean; onOptimize: () => void }) => (
    <aside>
      <span>{props.loading ? "cargando" : "listo"}</span>
      <span>pedidos:{props.orderCount}</span>
      <span>optimiza:{String(props.canOptimize)}</span>
      {props.error ? <span>{props.error}</span> : null}
      <button onClick={props.onOptimize}>optimizar</button>
    </aside>
  ),
}));
vi.mock("./components/Map", () => ({
  MapView: (props: { onMapFailure: () => void }) => <button onClick={props.onMapFailure}>fallar mapa</button>,
}));
vi.mock("./components/RouteTable", () => ({
  RouteTable: () => <div>tabla de ruta</div>,
  StopDetail: () => <div>detalle de parada</div>,
}));

class FakeWebSocket {
  static instances: FakeWebSocket[] = [];
  onmessage: ((event: { data: unknown }) => void) | null = null;
  close = vi.fn();
  constructor(public url: string, public protocols?: string[]) {
    FakeWebSocket.instances.push(this);
  }
}

const emptySolution = { metadata: {}, features: [] };

describe("dispatch application", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
    FakeWebSocket.instances = [];
    Object.defineProperty(window, "WebSocket", { configurable: true, value: FakeWebSocket });
    loadSession.mockReturnValue({ token: "token seguro", usuario: { rol: "operador" } });
    api.fetchDepots.mockResolvedValue([{ id: 1, nombre: "Central", lat: -12, lon: -75 }]);
    api.fetchOrders.mockResolvedValue([{ id: 10, codigo_pedido: "PED-NUEVO", cliente_nombre: "Cliente nuevo", direccion_referencia: "Jr. Real 120", ventana_inicio: "2026-11-17T09:00:00-05:00", ubicacion: { type: "Point", coordinates: [-75.21, -12.06] } }]);
    api.fetchVehicles.mockResolvedValue([{ placa: "ABC-123" }]);
    api.fetchPublishedRoute.mockResolvedValue(emptySolution);
    api.optimizeRoutes.mockResolvedValue(emptySolution);
  });

  afterEach(() => cleanup());

  it("loads dispatch data, changes map view and optimizes routes", async () => {
    render(<App />);

    await waitFor(() => expect(screen.getByText("listo")).toBeTruthy());
    expect(screen.getByText("pedidos:1")).toBeTruthy();
    expect(screen.getByText("optimiza:true")).toBeTruthy();
    expect(FakeWebSocket.instances[0]?.url).not.toContain('token');
    expect(FakeWebSocket.instances[0]?.protocols).toEqual(['bearer.token seguro']);

    fireEvent.click(screen.getByRole("button", { name: "fallar mapa" }));
    expect(screen.getByText("tabla de ruta")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Reintentar mapa" }));
    expect(screen.getByRole("button", { name: "fallar mapa" })).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "optimizar" }));
    await waitFor(() => expect(api.optimizeRoutes).toHaveBeenCalledOnce());
    expect(api.fetchOrders).toHaveBeenCalledTimes(2);
  });

  it("refreshes the published route only for valid websocket updates", async () => {
    render(<App />);
    await waitFor(() => expect(screen.getByText("listo")).toBeTruthy());
    const socket = FakeWebSocket.instances[0]!;

    socket.onmessage?.({ data: "invalid" });
    socket.onmessage?.({ data: JSON.stringify({ type: "heartbeat" }) });
    expect(api.fetchPublishedRoute).toHaveBeenCalledTimes(1);
    socket.onmessage?.({ data: JSON.stringify({ type: "route_update" }) });
    await waitFor(() => expect(api.fetchPublishedRoute).toHaveBeenCalledTimes(2));
  });

  it("shows every fleet vehicle before any route exists, including maintenance", async () => {
    api.fetchPublishedRoute.mockResolvedValue(null);
    api.fetchVehicles.mockResolvedValue([
      { id: 1, placa: "ABC-123", estado_operativo: "activo", activo: true },
      { id: 2, placa: "DEF-456", estado_operativo: "activo", activo: true },
      { id: 3, placa: "GHI-789", estado_operativo: "mantenimiento", activo: false },
    ]);
    render(<App />);
    expect(await screen.findByRole("button", { name: "ABC-123" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "DEF-456" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "GHI-789 · mantenimiento" }));
    expect(screen.getByText("GHI-789 no tiene ruta publicada en esta jornada.")).toBeTruthy();
    expect(api.fetchVehicles).toHaveBeenCalledWith(true);
  });

  it("uses the selected operation date for orders, maps and optimization", async () => {
    render(<App />);
    await screen.findByText("listo");
    fireEvent.change(screen.getByLabelText("Jornada de rutas"), { target: { value: "2026-11-18" } });
    await waitFor(() => expect(api.fetchOrders).toHaveBeenLastCalledWith("2026-11-18"));
    expect(api.fetchPublishedRoute).toHaveBeenLastCalledWith("2026-11-18");
    await waitFor(() => expect(screen.getByText("listo")).toBeTruthy());
    fireEvent.click(screen.getByRole("button", { name: "optimizar" }));
    await waitFor(() => expect(api.optimizeRoutes).toHaveBeenCalledWith("2026-11-18"));
  });

  it("saves and clears an order vehicle assignment and shows API failures", async () => {
    const pending = { id: 10, codigo_pedido: "PED-NUEVO", estado: "pending", peso_kg: 10, ventana_inicio: "2026-11-17T09:00:00-05:00" };
    api.fetchOrders.mockResolvedValue([pending]);
    api.fetchVehicles.mockResolvedValue([
      { id: 1, placa: "ABC-123", estado_operativo: "activo", activo: true, capacidad_kg: 500 },
      { id: 2, placa: "DEF-456", estado_operativo: "mantenimiento", activo: false, capacidad_kg: 500 },
    ]);
    api.assignOrderVehicle.mockResolvedValue({ ...pending, vehiculo_asignado_id: 1 });
    render(<App />);
    const select = await screen.findByLabelText("Vehículo para PED-NUEVO") as HTMLSelectElement;
    await screen.findByText("listo");
    expect((screen.getByRole("option", { name: /DEF-456/ }) as HTMLOptionElement).disabled).toBe(true);
    fireEvent.change(select, { target: { value: "1" } });
    await waitFor(() => expect(select.value).toBe("1"));
    expect(api.assignOrderVehicle).toHaveBeenCalledWith(10, 1);
    api.assignOrderVehicle.mockRejectedValueOnce(new Error("Vehículo no disponible"));
    fireEvent.change(select, { target: { value: "" } });
    expect(await screen.findByText("Vehículo no disponible")).toBeTruthy();
    expect(select.value).toBe("1");
    api.assignOrderVehicle.mockResolvedValue({ ...pending, vehiculo_asignado_id: null });
    fireEvent.change(select, { target: { value: "" } });
    await waitFor(() => expect(select.value).toBe(""));
    expect(api.assignOrderVehicle).toHaveBeenLastCalledWith(10, null);
  });

  it("shows new orders beside the published route and links to location editing", async () => {
    render(<App />);
    expect(await screen.findByText("PED-NUEVO · Cliente nuevo")).toBeTruthy();
    expect(screen.getByText("1 pendientes de ruta · 1 con punto · 0 por ubicar")).toBeTruthy();
    expect(screen.getByRole("link", { name: /Agregar punto de entrega/ }).getAttribute("href")).toBe("/pedidos#nuevo-pedido");
    expect(screen.getByRole("link", { name: "Editar punto" }).getAttribute("href")).toBe("/pedidos?fecha=2026-11-17&pedido=10");
  });

  it("refreshes orders on demand and on returning to the dashboard", async () => {
    render(<App />);
    await screen.findByText("PED-NUEVO · Cliente nuevo");
    api.fetchOrders.mockResolvedValue([{ id: 11, codigo_pedido: "PED-SIN-PUNTO", cliente_nombre: "Otro cliente", direccion_referencia: "Calle nueva", ventana_inicio: "2026-11-17T10:00:00-05:00", ubicacion: null }]);
    fireEvent.click(screen.getByRole("button", { name: "Actualizar pedidos" }));
    expect(await screen.findByText("PED-SIN-PUNTO · Otro cliente")).toBeTruthy();
    expect(screen.queryByText("PED-NUEVO · Cliente nuevo")).toBeNull();
    expect(screen.getByRole("link", { name: "Ubicar en el mapa" })).toBeTruthy();
    const calls = api.fetchOrders.mock.calls.length;
    fireEvent(window, new Event("focus"));
    await waitFor(() => expect(api.fetchOrders).toHaveBeenCalledTimes(calls + 1));
  });

  it("keeps delivery creation unavailable for read-only users", async () => {
    loadSession.mockReturnValue({ usuario: { rol: "auditor" } });
    render(<App />);
    await screen.findByText("PED-NUEVO · Cliente nuevo");
    expect(screen.queryByRole("link", { name: /Agregar punto/ })).toBeNull();
    expect(screen.queryByRole("link", { name: "Editar punto" })).toBeNull();
  });

  it("reports loading and optimization failures without a session socket", async () => {
    loadSession.mockReturnValue(null);
    api.fetchDepots.mockRejectedValueOnce(new Error("No se pudo cargar"));
    render(<App />);

    expect(await screen.findByText("No se pudo cargar")).toBeTruthy();
    expect(FakeWebSocket.instances).toHaveLength(0);

    cleanup();
    api.fetchDepots.mockResolvedValue([]);
    api.optimizeRoutes.mockRejectedValueOnce(new Error("No se pudo optimizar"));
    render(<App />);
    await waitFor(() => expect(screen.getByText("listo")).toBeTruthy());
    fireEvent.click(screen.getByRole("button", { name: "optimizar" }));
    expect(await screen.findByText("No se pudo optimizar")).toBeTruthy();
  });
});
