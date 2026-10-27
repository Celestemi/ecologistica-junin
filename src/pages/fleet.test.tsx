// @vitest-environment jsdom

import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

afterEach(cleanup);

const mocks = vi.hoisted(() => ({
  loadSession: vi.fn(),
  fetchFleet: vi.fn(),
  fetchDepots: vi.fn(),
  fetchVehicleHistory: vi.fn(),
  createVehicle: vi.fn(),
  updateVehicle: vi.fn(),
}));

vi.mock("../lib/session", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../lib/session")>()),
  loadSession: mocks.loadSession,
}));
vi.mock("../api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../api")>()),
  fetchFleet: mocks.fetchFleet,
  fetchDepots: mocks.fetchDepots,
  fetchVehicleHistory: mocks.fetchVehicleHistory,
  createVehicle: mocks.createVehicle,
  updateVehicle: mocks.updateVehicle,
}));
vi.mock("../components/StaffHeader", () => ({ StaffHeader: ({ title }: { title: string }) => <header>{title}</header> }));

import { ApiError } from "../api";
import type { Vehicle } from "../types";
import { Fleet } from "./Fleet";

const vehicle: Vehicle = {
  id: 1,
  deposito_id: 1,
  placa: "ABC-123",
  modelo: "Furgón",
  capacidad_kg: 900,
  capacidad_m3: 5,
  tipo_combustible: "diesel",
  rendimiento_km_gal: 12,
  emision_base_co2_g_km: 200,
  factor_penalizacion_pendiente: 0.04,
  estado_operativo: "activo",
  activo: true,
};

describe("fleet management page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.loadSession.mockReturnValue({ usuario: { rol: "admin" } });
    mocks.fetchFleet.mockResolvedValue([vehicle]);
    mocks.fetchDepots.mockResolvedValue([{ id: 1, nombre: "Central" }]);
    mocks.fetchVehicleHistory.mockResolvedValue([]);
    mocks.createVehicle.mockResolvedValue({ ...vehicle, id: 2, placa: "NEW-456" });
    mocks.updateVehicle.mockResolvedValue(vehicle);
  });

  it("loads fleet, validates maintenance and saves edits", async () => {
    render(<Fleet />);
    expect(await screen.findByText(/ABC-123 · Activo/)).toBeTruthy();
    expect(mocks.fetchVehicleHistory).toHaveBeenCalledWith(1);

    await userEvent.click(screen.getByRole("button", { name: "Pasar a Mantenimiento" }));
    expect(await screen.findByText(/Indica un motivo/)).toBeTruthy();
    await userEvent.type(screen.getByPlaceholderText(/revisión de frenos/), "Frenos");
    await userEvent.click(screen.getByRole("button", { name: "Pasar a Mantenimiento" }));
    await waitFor(() => expect(mocks.updateVehicle).toHaveBeenCalledWith(1, { estado_operativo: "mantenimiento", motivo: "Frenos" }));

    await userEvent.click(screen.getByRole("button", { name: "Guardar cambios" }));
    await waitFor(() => expect(mocks.updateVehicle).toHaveBeenCalledTimes(2));
    expect(await screen.findByText(/Cambios guardados/)).toBeTruthy();
  });

  it("registers a normalized vehicle and reports backend failures", async () => {
    const created = { ...vehicle, id: 2, placa: "NEW-456" };
    mocks.createVehicle.mockResolvedValue(created);
    mocks.fetchFleet.mockResolvedValueOnce([vehicle]).mockResolvedValue([vehicle, created]);
    render(<Fleet />);
    const form = await screen.findByRole("heading", { name: "Registrar vehículo" });
    const scope = within(form.closest("form")!);
    await userEvent.type(scope.getByLabelText("Placa"), "new-456");
    await userEvent.type(scope.getByLabelText("Modelo"), "Van");
    await userEvent.click(scope.getByRole("button", { name: "Guardar en la flota" }));
    await waitFor(() => expect(mocks.createVehicle).toHaveBeenCalledWith(expect.objectContaining({ placa: "NEW-456", deposito_id: 1 })));
    expect(await screen.findByText(/Vehículo NEW-456 registrado/)).toBeTruthy();

    mocks.updateVehicle.mockRejectedValue(new ApiError("Cambio rechazado", 409));
    await userEvent.click(screen.getByRole("button", { name: "Guardar cambios" }));
    expect(await screen.findByText("Cambio rechazado")).toBeTruthy();
  });

  it("shows load errors and read-only mode", async () => {
    mocks.fetchFleet.mockRejectedValue(new Error("Flota no disponible"));
    const { unmount } = render(<Fleet />);
    expect(await screen.findByText("Flota no disponible")).toBeTruthy();
    unmount();

    mocks.fetchFleet.mockResolvedValue([vehicle]);
    mocks.loadSession.mockReturnValue({ usuario: { rol: "auditor" } });
    render(<Fleet />);
    expect(await screen.findByText(/Consultas la flota/)).toBeTruthy();
    expect(screen.queryByText("Registrar vehículo")).toBeNull();
  });
});
