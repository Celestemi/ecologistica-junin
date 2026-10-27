// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Tracking } from "./Tracking";

const { fetchPublicTracking, loadSession } = vi.hoisted(() => ({
  fetchPublicTracking: vi.fn(),
  loadSession: vi.fn(),
}));

vi.mock("../api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../api")>()),
  fetchPublicTracking,
}));

vi.mock("../lib/session", () => ({ loadSession }));

vi.mock("leaflet", () => ({
  default: { divIcon: vi.fn(() => ({})) },
}));

const map = { setView: vi.fn(), fitBounds: vi.fn() };
vi.mock("react-leaflet", () => ({
  MapContainer: ({ children }: { children: React.ReactNode }) => <div data-testid="map">{children}</div>,
  Marker: () => <div data-testid="marker" />,
  Polyline: () => <div data-testid="route" />,
  TileLayer: () => null,
  useMap: () => map,
}));

class FakeWebSocket {
  static instances: FakeWebSocket[] = [];
  onopen: (() => void) | null = null;
  onmessage: ((event: { data: unknown }) => void) | null = null;
  onclose: (() => void) | null = null;
  close = vi.fn();

  constructor(public url: string) {
    FakeWebSocket.instances.push(this);
  }
}

const token = "123e4567-e89b-12d3-a456-426614174000";
const order = {
  estado: "en_ruta",
  zona_entrega: "El Tambo",
  lat_aprox: -12.05,
  lon_aprox: -75.21,
  ventana_inicio: "2026-10-27T14:00:00-05:00",
  ventana_fin: "2026-10-27T16:00:00-05:00",
  eta: "2026-10-27T15:00:00-05:00",
  paradas_previas: 2,
  co2_evitado_kg: 0.45,
};

describe("public tracking", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
    FakeWebSocket.instances = [];
    Object.defineProperty(window, "WebSocket", { configurable: true, value: FakeWebSocket });
    window.history.replaceState({}, "", `/seguimiento/${token}`);
    loadSession.mockReturnValue(null);
    fetchPublicTracking.mockResolvedValue(order);
  });

  afterEach(() => cleanup());

  it("loads the order and reacts to live location and arrival messages", async () => {
    render(<Tracking />);

    expect(await screen.findByText("El Tambo")).toBeTruthy();
    expect(fetchPublicTracking).toHaveBeenCalledWith(token);
    expect(screen.getByText(/2 paradas previas/)).toBeTruthy();
    expect(FakeWebSocket.instances).toHaveLength(1);

    const socket = FakeWebSocket.instances[0]!;
    fireEvent.click(screen.getByRole("button", { name: /Apagado.*SMS/ }));
    socket.onopen?.();
    socket.onmessage?.({
      data: JSON.stringify({
        lat: -12.04,
        lon: -75.2,
        eta: "2026-10-27T14:50:00-05:00",
        minutes: 4.4,
        paradas_previas: 0,
      }),
    });

    await waitFor(() => expect(screen.getByText("En vivo")).toBeTruthy());
    expect(screen.getByText("En 4 minutos")).toBeTruthy();
    expect(screen.getByText(/siguiente entrega/)).toBeTruthy();
    expect(screen.getAllByRole("status")).toHaveLength(2);
    expect(screen.queryByTestId("route")).toBeNull();
    expect(screen.getByText(/no representa un recorrido vial/i)).toBeTruthy();

    fireEvent.click(screen.getAllByRole("button", { name: "Cerrar" })[0]!);
    expect(screen.queryByRole("status")).toBeNull();

    socket.onmessage?.({ data: "not-json" });
    socket.onmessage?.({ data: JSON.stringify(null) });
    socket.onmessage?.({ data: new Uint8Array() });
  });

  it("shows service errors and supports a session link", async () => {
    loadSession.mockReturnValue({ usuario: { rol: "admin" } });
    fetchPublicTracking.mockRejectedValue(new Error("Pedido no encontrado"));

    render(<Tracking />);

    expect(await screen.findByText("Pedido no encontrado")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Volver a mi panel" }).getAttribute("href")).toBe("/");
  });

  it("does not query or open a socket when the URL has no valid token", () => {
    window.history.replaceState({}, "", "/seguimiento/codigo-invalido");

    render(<Tracking />);

    expect(fetchPublicTracking).not.toHaveBeenCalled();
    expect(FakeWebSocket.instances).toHaveLength(0);
    expect((screen.getByLabelText("Enlace de seguimiento") as HTMLInputElement).value).toBe("");
  });
});
