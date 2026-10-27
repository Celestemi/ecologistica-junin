// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MapView } from "./Map";
import { PinMap } from "./PinMap";
import type { Depot, Order, RouteOptimization } from "../types";

const leaflet = vi.hoisted(() => ({ divIcon: vi.fn((options) => options) }));
const map = vi.hoisted(() => ({ setView: vi.fn(), fitBounds: vi.fn() }));
const leafletState = vi.hoisted(() => ({
  clickHandler: null as null | ((event: { latlng: { lat: number; lng: number } }) => void),
  tileError: null as null | (() => void),
  markerIndex: 0,
}));

vi.mock("leaflet", () => ({ default: leaflet }));
vi.mock("react-leaflet", () => ({
  MapContainer: ({ children }: { children: React.ReactNode }) => <div data-testid="map-container">{children}</div>,
  Marker: ({ children, eventHandlers, position }: { children?: React.ReactNode; eventHandlers?: { click?: () => void }; position: [number, number] }) => {
    const index = leafletState.markerIndex++;
    return <div data-testid={`marker-${index}`} data-position={position.join(",")} onClick={eventHandlers?.click}>{children}</div>;
  },
  Polyline: ({ positions }: { positions: [number, number][] }) => <div data-testid="polyline" data-points={positions.length} />,
  Popup: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  TileLayer: ({ eventHandlers }: { eventHandlers?: { tileerror?: () => void } }) => {
    leafletState.tileError = eventHandlers?.tileerror ?? null;
    return <div data-testid="tiles" />;
  },
  useMap: () => map,
  useMapEvents: (handlers: { click: (event: { latlng: { lat: number; lng: number } }) => void }) => {
    leafletState.clickHandler = handlers.click;
    return map;
  },
}));

const depot = {
  id: 1,
  nombre: "Depósito Central",
  direccion: "El Tambo",
  ubicacion: { type: "Point", coordinates: [-75.2, -12.05] },
  altitud_msnm: 3264.7,
} as Depot;

const order = {
  id: 10,
  cliente_nombre: "Cliente sin ruta",
  direccion_referencia: "Jr. Lima 10",
  ubicacion: { type: "Point", coordinates: [-75.21, -12.06] },
  ventana_inicio: "2026-10-27T08:00:00-05:00",
  ventana_fin: "2026-10-27T09:00:00-05:00",
} as Order;

const solution = {
  metadata: {},
  features: [
    {
      type: "Feature",
      geometry: { type: "Point", coordinates: [-75.22, -12.07] },
      properties: { plate: "ABC-123", sequence: 1, order_code: "PED-1", stop_type: "delivery", customer: "Cliente ruta", title: "Av. Ferrocarril", window_start: "2026-10-27T10:00:00-05:00", window_end: "2026-10-27T12:00:00-05:00", co2_g: 240 },
    },
    {
      type: "Feature",
      geometry: { type: "Point", coordinates: [-75.2, -12.05] },
      properties: { plate: "ABC-123", sequence: 0, stop_type: "depot_start" },
    },
    {
      type: "Feature",
      geometry: { type: "LineString", coordinates: [[-75.2, -12.05], [-75.22, -12.07]] },
      properties: { plate: "ABC-123", geometry_kind: "road" },
    },
    {
      type: "Feature",
      geometry: { type: "Point", coordinates: [-75.24, -12.08] },
      properties: { plate: "XYZ-789", sequence: 2, order_code: "PED-2", stop_type: "delivery" },
    },
  ],
} as unknown as RouteOptimization;

describe("map components", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    leafletState.clickHandler = null;
    leafletState.tileError = null;
    leafletState.markerIndex = 0;
  });

  afterEach(() => cleanup());

  it("renders pending orders, depot details and reports tile failures", async () => {
    const onMapFailure = vi.fn();
    render(<MapView depot={depot} orders={[order]} solution={null} selectedPlate={null} onSelectPlate={vi.fn()} onSelectStop={vi.fn()} onMapFailure={onMapFailure} />);

    expect(screen.getByText("Depósito Central")).toBeTruthy();
    expect(screen.getByText("Cliente sin ruta")).toBeTruthy();
    expect(screen.getByText(/3265 m/)).toBeTruthy();
    await waitFor(() => expect(map.fitBounds).toHaveBeenCalled());
    leafletState.tileError?.();
    expect(onMapFailure).toHaveBeenCalledOnce();
  });

  it("renders optimized roads and selects delivery markers and route legend", async () => {
    const onSelectPlate = vi.fn();
    const onSelectStop = vi.fn();
    render(<MapView depot={depot} orders={[]} solution={solution} selectedPlate={null} onSelectPlate={onSelectPlate} onSelectStop={onSelectStop} onMapFailure={vi.fn()} />);

    expect(screen.getByText("Cliente ruta")).toBeTruthy();
    expect(screen.getByText("Vehículo ABC-123")).toBeTruthy();
    expect(screen.getByTestId("polyline").getAttribute("data-points")).toBe("2");
    fireEvent.click(screen.getByText("Cliente ruta").closest("[data-testid^='marker-']")!);
    expect(onSelectPlate).toHaveBeenCalledWith("ABC-123");
    expect(onSelectStop).toHaveBeenCalledWith("ABC-123:1:PED-1");
    fireEvent.click(screen.getByRole("button", { name: /XYZ-789/ }));
    expect(onSelectPlate).toHaveBeenCalledWith("XYZ-789");
  });

  it("filters a selected plate, warns without road geometry and handles empty bounds", async () => {
    const withoutRoads = {
      ...solution,
      features: solution.features.filter(
        (feature) => feature.geometry.type === "Point" && feature.properties.stop_type === "delivery" && feature.properties.plate === "ABC-123",
      ),
    };
    const { rerender } = render(<MapView depot={null} orders={[]} solution={withoutRoads} selectedPlate="ABC-123" onSelectPlate={vi.fn()} onSelectStop={vi.fn()} onMapFailure={vi.fn()} />);

    expect(screen.getByText(/Sin trazado vial/)).toBeTruthy();
    expect(screen.getByText("Cliente ruta")).toBeTruthy();
    expect(screen.queryByText("Cliente")).toBeNull();
    await waitFor(() => expect(map.setView).toHaveBeenCalledWith([-12.07, -75.22], 14));

    map.setView.mockClear();
    rerender(<MapView depot={null} orders={[]} solution={null} selectedPlate={null} onSelectPlate={vi.fn()} onSelectStop={vi.fn()} onMapFailure={vi.fn()} />);
    await waitFor(() => expect(map.setView).toHaveBeenCalledWith([-12.06513, -75.20486], 13));
  });

  it("captures manual coordinates and displays the selected pin", () => {
    const onPick = vi.fn();
    const { rerender } = render(<PinMap pin={null} onPick={onPick} />);
    expect(screen.queryByTestId("marker-0")).toBeNull();
    leafletState.clickHandler?.({ latlng: { lat: -12.1, lng: -75.3 } });
    expect(onPick).toHaveBeenCalledWith(-12.1, -75.3);

    leafletState.markerIndex = 0;
    rerender(<PinMap pin={[-12.1, -75.3]} onPick={onPick} />);
    expect(screen.getByTestId("marker-0").getAttribute("data-position")).toBe("-12.1,-75.3");
  });
});
