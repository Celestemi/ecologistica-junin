import { describe, expect, it } from "vitest";
import {
  actionLabel,
  formatCo2,
  formatDateTime,
  formatKg,
  formatKm,
  formatTime,
  formatWindow,
  fuelLabel,
  limaHour,
  reductionPercent,
  statusLabel,
  windowColor,
} from "./format";

describe("format helpers", () => {
  it("formats times in Lima and handles absent or invalid values", () => {
    expect(formatTime(null)).toBe("—");
    expect(formatTime("not-a-date")).toBe("—");
    expect(formatTime("2026-10-27T15:30:00Z")).toMatch(/10:30/);
    expect(formatWindow(null, "2026-10-27T15:30:00Z")).toBe("Sin ventana");
    expect(formatWindow("2026-10-27T14:00:00Z", "2026-10-27T15:30:00Z")).toMatch(/09:00.*10:30/);
    expect(formatDateTime("invalid")).toBe("—");
    expect(formatDateTime("2026-10-27T15:30:00Z")).not.toBe("—");
  });

  it("formats quantities and carbon values at their boundaries", () => {
    expect(formatKm(12.34)).toMatch(/12[,.]3 km/);
    expect(formatKg(7)).toBe("7.00 kg");
    expect(formatCo2(null)).toBe("Se calcula al optimizar");
    expect(formatCo2(999.6)).toBe("1000 g");
    expect(formatCo2(1000)).toBe("1.00 kg");
    expect(reductionPercent(15, 60)).toBe(25);
    expect(reductionPercent(2, 0)).toBe(0);
    expect(reductionPercent(2, -1)).toBe(0);
  });

  it("classifies Lima windows into the three operational colors", () => {
    expect(limaHour("2026-10-27T12:30:00Z")).toBe(7);
    expect(windowColor(null)).toBe("#b45309");
    expect(windowColor("2026-10-27T12:30:00Z")).toBe("#c2410c");
    expect(windowColor("2026-10-27T15:00:00Z")).toBe("#d97706");
    expect(windowColor("2026-10-27T18:00:00Z")).toBe("#4d7c0f");
  });

  it("maps known labels and preserves unknown backend values", () => {
    expect(fuelLabel("diesel")).toBe("Diésel");
    expect(fuelLabel("hydrogen")).toBe("hydrogen");
    expect(statusLabel("delivered")).toBe("Entregado");
    expect(statusLabel("custom")).toBe("custom");
    expect(actionLabel("optimizar_rutas")).toBe("Optimización ejecutada");
    expect(actionLabel("custom_action")).toBe("custom_action");
  });
});
