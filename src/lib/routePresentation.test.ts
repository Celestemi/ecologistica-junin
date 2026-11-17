import { describe, expect, it } from "vitest";
import { orderLocationHref, routeStops } from "./routePresentation";
import type { Order, RouteOptimization } from "../types";

const solution = {
  type: "FeatureCollection",
  metadata: {},
  features: [
    { type: "Feature", geometry: { type: "Point", coordinates: [-75.2, -12.1] }, properties: { plate: "AAA-001", sequence: 2, stop_type: "delivery", customer: "Ana", address: "Jr. Uno", weight_kg: 12 } },
    { type: "Feature", geometry: { type: "Point", coordinates: [-75.21, -12.11] }, properties: { plate: "AAA-001", sequence: 1, stop_type: "depot_start" } },
    { type: "Feature", geometry: { type: "LineString", coordinates: [[-75.21, -12.11], [-75.2, -12.1]] }, properties: { plate: "AAA-001" } },
  ],
} as unknown as RouteOptimization;

describe("routeStops", () => {
  it("conserva los datos reales de detalle y ordena por secuencia", () => {
    const stops = routeStops(solution, "AAA-001");
    expect(stops.map((stop) => stop.sequence)).toEqual([1, 2]);
    expect(stops[1]).toMatchObject({ customer: "Ana", address: "Jr. Uno", weightKg: 12 });
  });

  it("permite una tabla aun cuando no existe geometría de línea", () => {
    expect(routeStops({ ...solution, features: solution.features.filter((feature) => feature.geometry.type === "Point") })).toHaveLength(2);
  });

  it("abre la jornada de Lima cuando el servidor devuelve una fecha en UTC", () => {
    expect(orderLocationHref({ id: 8, ventana_inicio: "2026-11-18T02:00:00Z" } as Order)).toBe("/pedidos?fecha=2026-11-17&pedido=8");
  });
});
