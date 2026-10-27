// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

afterEach(cleanup);

const mocks = vi.hoisted(() => ({
  loadSession: vi.fn(),
  clearSession: vi.fn(),
  saveSession: vi.fn(),
  downloadSustainabilityPdf: vi.fn(),
  fetchOperationalIndicators: vi.fn(),
  fetchAuditLog: vi.fn(),
  login: vi.fn(),
}));

vi.mock("../lib/session", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../lib/session")>()),
  loadSession: mocks.loadSession,
  clearSession: mocks.clearSession,
  saveSession: mocks.saveSession,
}));

vi.mock("../api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../api")>()),
  downloadSustainabilityPdf: mocks.downloadSustainabilityPdf,
  fetchOperationalIndicators: mocks.fetchOperationalIndicators,
  fetchAuditLog: mocks.fetchAuditLog,
  login: mocks.login,
}));

import { ApiError } from "../api";
import { AuditLog } from "../pages/AuditLog";
import { Login } from "../pages/Login";
import type { RouteStop } from "../lib/routePresentation";
import { Brand } from "./Brand";
import { Dashboard } from "./Dashboard";
import { RouteTable, StopDetail } from "./RouteTable";
import { SessionMenu } from "./SessionMenu";
import { StaffHeader } from "./StaffHeader";

const session = {
  token: "token",
  exp: Date.now() + 60_000,
  usuario: { id: 1, nombre: "Rosa", correo: "admin@example.com", rol: "admin" as const },
};

const stop: RouteStop = {
  key: "ABC-1",
  type: "delivery",
  sequence: 2,
  deliveryIndex: 1,
  plate: "ABC-123",
  orderCode: "PED-001",
  customer: "Ana",
  address: "Jr. Real",
  weightKg: 12,
  eta: "2026-10-27T15:30:00Z",
  etaStatus: "ok",
  windowStart: "2026-10-27T15:00:00Z",
  windowEnd: "2026-10-27T16:00:00Z",
  co2g: 800,
  coordinates: [-75.2, -12.1],
};

describe("presentational and staff flows", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.loadSession.mockReturnValue(session);
    mocks.downloadSustainabilityPdf.mockResolvedValue(undefined);
    mocks.fetchAuditLog.mockResolvedValue([]);
    mocks.fetchOperationalIndicators.mockResolvedValue({ rutas: 0 });
    window.history.replaceState({}, "", "/");
  });

  it("renders both brand tones", () => {
    const { rerender } = render(<Brand title="EcoLogística" />);
    expect(screen.getByText("EcoLogística")).toBeTruthy();
    rerender(<Brand title="Campo" light />);
    expect(screen.getByText("Campo")).toBeTruthy();
  });

  it("renders route states, selects a delivery and shows complete details", async () => {
    const onSelect = vi.fn();
    const { rerender } = render(<RouteTable stops={[]} selectedStop={null} onSelect={onSelect} />);
    expect(screen.getByText(/no tiene paradas/)).toBeTruthy();
    rerender(<RouteTable stops={[stop]} selectedStop={stop} onSelect={onSelect} compact />);
    await userEvent.click(screen.getByText("Ana"));
    expect(onSelect).toHaveBeenCalledWith(stop);

    rerender(<StopDetail stop={stop} />);
    expect(screen.getByText("PED-001")).toBeTruthy();
    expect(screen.getByText("800 g")).toBeTruthy();
    rerender(<StopDetail stop={null} />);
    expect(screen.getByText(/Selecciona una parada/)).toBeTruthy();
  });

  it("renders session information and clears it on logout", async () => {
    const { rerender } = render(<SessionMenu />);
    expect(screen.getByText("Administrador")).toBeTruthy();
    await userEvent.click(screen.getByRole("button", { name: "Salir" }));
    expect(mocks.clearSession).toHaveBeenCalledOnce();
    mocks.loadSession.mockReturnValue(null);
    rerender(<SessionMenu light />);
    expect(screen.queryByRole("button", { name: "Salir" })).toBeNull();
  });

  it("shows role navigation and handles PDF success and failure", async () => {
    window.history.replaceState({}, "", "/pedidos");
    const { rerender } = render(<StaffHeader title="Operación" />);
    expect(screen.getByRole("link", { name: "Despacho" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Bitácora" })).toBeTruthy();
    await userEvent.click(screen.getByRole("button", { name: "Informe PDF" }));
    expect(mocks.downloadSustainabilityPdf).toHaveBeenCalledOnce();

    mocks.downloadSustainabilityPdf.mockRejectedValue(new ApiError("Sin informe", 503));
    rerender(<StaffHeader title="Campo" tone="field" />);
    await userEvent.click(screen.getByRole("button", { name: "Informe PDF" }));
    expect(await screen.findByText("Sin informe")).toBeTruthy();
  });

  it("renders no header without a session", () => {
    mocks.loadSession.mockReturnValue(null);
    const { container } = render(<StaffHeader title="Oculto" />);
    expect(container.innerHTML).toBe("");
  });
});

describe("dashboard, login and audit behavior", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.loadSession.mockReturnValue(null);
    mocks.fetchAuditLog.mockResolvedValue([]);
    window.history.replaceState({}, "", "/ingresar");
  });

  it("loads empty and populated dashboard indicators and supports date changes", async () => {
    mocks.fetchOperationalIndicators
      .mockResolvedValueOnce({ rutas: 0 })
      .mockResolvedValue({
        rutas: 2,
        distancia_total_km: 20,
        duracion_total_min: 65,
        consumo_estimado_gal: 1.25,
        co2_estimado_kg: 5,
        co2_evitado_kg: 2,
        arboles_quinual_eq: 0.17,
        quinual_kg_co2_por_ano: 12,
        linea_base_secuencial_km: 25,
        linea_base_secuencial_co2_kg: 7,
        ahorro_distancia_pct_vs_secuencial: 20,
        ahorro_co2_pct_vs_secuencial: -2,
      });
    render(<Dashboard metadata={null} />);
    expect(await screen.findByText(/No hay información/)).toBeTruthy();
    fireEvent.change(screen.getByLabelText("Desde"), { target: { value: "2026-10-01" } });
    expect(await screen.findByText("Consumo estimado")).toBeTruthy();
    expect(screen.getByText(/\+20.0%/)).toBeTruthy();
    expect(screen.getByText(/-2.0%/)).toBeTruthy();
  });

  it("shows dashboard failures", async () => {
    mocks.fetchOperationalIndicators.mockRejectedValue("offline");
    render(<Dashboard metadata={null} />);
    expect(await screen.findByText(/No se pudieron cargar/)).toBeTruthy();
  });

  it("fills a demo login and displays a backend authentication error", async () => {
    mocks.login.mockRejectedValue(new ApiError("Credenciales inválidas", 401));
    render(<Login />);
    await userEvent.click(screen.getByRole("button", { name: /Luis Huamán/ }));
    expect((screen.getByLabelText("Correo") as HTMLInputElement).value).toBe("operador@distrirapido.pe");
    await userEvent.click(screen.getByRole("button", { name: "Ingresar" }));
    expect(await screen.findByText("Credenciales inválidas")).toBeTruthy();
  });

  it("renders audit events, empty state and API failures", async () => {
    mocks.loadSession.mockReturnValue(session);
    mocks.fetchAuditLog.mockResolvedValueOnce([{ id: 1, correo: "qa@example.com", accion: "ingreso_correcto", detalle: "OK", creado_en: "2026-10-27T15:30:00Z" }]);
    const { unmount } = render(<AuditLog />);
    expect(await screen.findByText("Ingreso correcto")).toBeTruthy();
    expect(screen.getByText(/qa@example.com/)).toBeTruthy();
    unmount();

    mocks.fetchAuditLog.mockRejectedValue(new Error("Bitácora caída"));
    render(<AuditLog />);
    expect(await screen.findByText("Bitácora caída")).toBeTruthy();
  });
});
