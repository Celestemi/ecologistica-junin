// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Sidebar } from "./Sidebar";
import type { RouteOptimization, Vehicle } from "../types";

const vehicles = [
  { placa: "ABC-123", tipo_combustible: "electrico", capacidad_kg: 800 },
] as Vehicle[];

const solution = {
  metadata: {
    feasible: false,
    exclusiones_placa: [{ placa: "XYZ-999", motivo: "Restricción lunes" }],
    pedidos_sin_asignar: ["PED-9"],
    geometria_vial_disponible: false,
    nota_distancia: "Distancias aproximadas",
  },
  features: [
    {
      geometry: { type: "LineString", coordinates: [] },
      properties: { plate: "ABC-123" },
    },
    {
      geometry: { type: "Point", coordinates: [-75.2, -12.1] },
      properties: { plate: "ABC-123", sequence: 0, stop_type: "depot_start", title: "Central" },
    },
    {
      geometry: { type: "Point", coordinates: [-75.21, -12.11] },
      properties: {
        plate: "ABC-123",
        sequence: 1,
        delivery_index: 1,
        stop_type: "delivery",
        customer: "Cliente Uno",
        title: "Av. Principal",
        eta: "2026-10-27T15:00:00-05:00",
        window_start: "2026-10-27T14:00:00-05:00",
        window_end: "2026-10-27T16:00:00-05:00",
        wait_minutes: 2.4,
        late_minutes: 1.6,
        co2_g: 350,
        distance_note: "Tramo estimado",
      },
    },
    {
      geometry: { type: "Point", coordinates: [-75.2, -12.1] },
      properties: { plate: "ABC-123", sequence: 2, stop_type: "depot_end", eta_estado: "revision_matriz" },
    },
  ],
} as unknown as RouteOptimization;

describe("dispatch sidebar", () => {
  afterEach(() => cleanup());

  it("shows operational warnings and the ordered itinerary", () => {
    const onOptimize = vi.fn();
    render(
      <Sidebar
        loading={false}
        canOptimize
        roleNote={null}
        orderCount={3}
        vehicles={vehicles}
        optimizing={false}
        error="Advertencia de servicio"
        solution={solution}
        onOptimize={onOptimize}
      />,
    );

    expect(screen.getByText("Advertencia de servicio")).toBeTruthy();
    expect(screen.getByText(/XYZ-999/)).toBeTruthy();
    expect(screen.getByText(/Sin asignar: PED-9/)).toBeTruthy();
    expect(screen.getByText(/Trazado vial no disponible/)).toBeTruthy();
    expect(screen.getByText(/Cliente Uno/)).toBeTruthy();
    expect(screen.getByText(/espera 2 min/)).toBeTruthy();
    expect(screen.getByText(/tarde 2 min/)).toBeTruthy();
    expect(screen.getByText("Tramo estimado")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /Ejecutar/ }));
    expect(onOptimize).toHaveBeenCalledOnce();
  });

  it("renders loading, empty, read-only and optimizing states", () => {
    const { rerender } = render(
      <Sidebar loading canOptimize roleNote={null} orderCount={0} vehicles={[]} optimizing={false} error={null} solution={null} onOptimize={vi.fn()} />,
    );
    expect(screen.getByText(/Cargando el/)).toBeTruthy();
    expect((screen.getByRole("button", { name: /Ejecutar/ }) as HTMLButtonElement).disabled).toBe(true);

    rerender(
      <Sidebar loading={false} canOptimize roleNote={null} orderCount={0} vehicles={[]} optimizing error={null} solution={null} onOptimize={vi.fn()} />,
    );
    expect(screen.getByRole("button", { name: /Calculando rutas/ })).toBeTruthy();

    rerender(
      <Sidebar loading={false} canOptimize={false} roleNote="Solo lectura" orderCount={0} vehicles={[]} optimizing={false} error={null} solution={null} onOptimize={vi.fn()} />,
    );
    expect(screen.getByText("Ruta publicada")).toBeTruthy();
    expect(screen.getByText("Solo lectura")).toBeTruthy();
    expect(screen.getByText(/itinerario aparece/)).toBeTruthy();
    expect(screen.queryByRole("button")).toBeNull();
  });
});
