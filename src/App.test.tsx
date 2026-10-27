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
  constructor(public url: string) {
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
    api.fetchOrders.mockResolvedValue([{ id: 10 }]);
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
    expect(FakeWebSocket.instances[0]?.url).toContain("token%20seguro");

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
