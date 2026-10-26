import { describe, expect, it } from "vitest";
import { routeStops } from "./routePresentation";
import type { RouteOptimization } from "../types";

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
});
