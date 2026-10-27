// @vitest-environment jsdom

import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

afterEach(cleanup);

const mocks = vi.hoisted(() => ({
  loadSession: vi.fn(),
  fetchDay: vi.fn(),
  importDay: vi.fn(),
  updateOrderLocation: vi.fn(),
  updateOrderWindow: vi.fn(),
  createOrder: vi.fn(),
  fetchPlateRestrictionConfig: vi.fn(),
  fetchPlateRestrictionHistory: vi.fn(),
  updatePlateRestrictionConfig: vi.fn(),
}));

vi.mock("../lib/session", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../lib/session")>()),
  loadSession: mocks.loadSession,
}));
vi.mock("../api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../api")>()),
  fetchDay: mocks.fetchDay,
  importDay: mocks.importDay,
  updateOrderLocation: mocks.updateOrderLocation,
  updateOrderWindow: mocks.updateOrderWindow,
  createOrder: mocks.createOrder,
  fetchPlateRestrictionConfig: mocks.fetchPlateRestrictionConfig,
  fetchPlateRestrictionHistory: mocks.fetchPlateRestrictionHistory,
  updatePlateRestrictionConfig: mocks.updatePlateRestrictionConfig,
}));
vi.mock("../components/StaffHeader", () => ({ StaffHeader: ({ title }: { title: string }) => <header>{title}</header> }));
vi.mock("../components/PinMap", () => ({
  PinMap: ({ onPick }: { onPick: (lat: number, lon: number) => void }) => (
    <button type="button" onClick={() => onPick(-12.1, -75.2)}>Elegir punto simulado</button>
  ),
}));

import { ApiError } from "../api";
import type { Order } from "../types";
import { OrdersDay } from "./OrdersDay";
import { PlateRestrictions } from "./PlateRestrictions";

const order: Order = {
  id: 1,
  codigo_pedido: "PED-001",
  cliente_nombre: "Cliente Uno",
  direccion_referencia: "Jr. Real",
  ubicacion: null,
  altitud_msnm: null,
  peso_kg: 12,
  ventana_inicio: "2026-10-27T09:00:00-05:00",
  ventana_fin: "2026-10-27T12:00:00-05:00",
  estado: "pending",
  estado_ubicacion: "pendiente_validacion",
};

const report = {
  fecha: "2026-10-27",
  aceptados: 0,
  rechazados: 0,
  pendientes_punto: 1,
  total_filas: 1,
  resumen: "1 pedido pendiente de ubicación",
  filas: [{
    linea: 2,
    codigo_pedido: "PED-001",
    cliente_nombre: "Cliente Uno",
    direccion_referencia: "Jr. Real",
    peso_kg: 12,
    hora_inicio: "09:00",
    hora_fin: "12:00",
    lat: null,
    lon: null,
    altitud_msnm: null,
    resultado: "pendiente_punto" as const,
    motivo: "Falta coordenada",
    campo: "ubicacion",
    pedido_id: 1,
  }],
};

describe("orders day", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.loadSession.mockReturnValue({ usuario: { rol: "operador" } });
    mocks.fetchDay.mockResolvedValue({ fecha: "2026-10-27", pedidos: [order] });
    mocks.importDay.mockResolvedValue(report);
    mocks.updateOrderLocation.mockResolvedValue(order);
    mocks.updateOrderWindow.mockResolvedValue(order);
  });

  it("imports CSV, resolves a pending point and edits a valid window", async () => {
    render(<OrdersDay />);
    expect(await screen.findByText("Cliente Uno")).toBeTruthy();
    await userEvent.click(screen.getByRole("button", { name: "Usar ejemplo" }));
    await userEvent.click(screen.getByRole("button", { name: "Importar jornada" }));
    expect(await screen.findByText(report.resumen)).toBeTruthy();

    await userEvent.click(screen.getByRole("button", { name: "Marcar en el mapa" }));
    await userEvent.click(screen.getByRole("button", { name: "Elegir punto simulado" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar este punto" }));
    await waitFor(() => expect(mocks.updateOrderLocation).toHaveBeenCalledWith(1, expect.objectContaining({ lat: -12.1, lon: -75.2 })));

    await userEvent.click(screen.getByRole("button", { name: "Editar ventana" }));
    await userEvent.clear(screen.getByLabelText("Inicio"));
    await userEvent.type(screen.getByLabelText("Inicio"), "10:00");
    await userEvent.click(screen.getByRole("button", { name: "Guardar ventana" }));
    await waitFor(() => expect(mocks.updateOrderWindow).toHaveBeenCalledWith(1, expect.objectContaining({ ventana_inicio: expect.stringContaining("T10:00") })));
  });

  it("shows API errors and read-only mode", async () => {
    mocks.fetchDay.mockRejectedValueOnce(new Error("Jornada no disponible"));
    const { unmount } = render(<OrdersDay />);
    expect(await screen.findByText("Jornada no disponible")).toBeTruthy();
    unmount();

    mocks.fetchDay.mockResolvedValue({ fecha: "2026-10-27", pedidos: [order] });
    mocks.loadSession.mockReturnValue({ usuario: { rol: "auditor" } });
    render(<OrdersDay />);
    expect(await screen.findByText(/Consultas los pedidos/)).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Importar jornada" })).toBeNull();
  });

  it("reports import errors without changing production behavior", async () => {
    mocks.importDay.mockRejectedValue(new ApiError("CSV inválido", 422));
    render(<OrdersDay />);
    await screen.findByText("Cliente Uno");
    await userEvent.click(screen.getByRole("button", { name: "Usar ejemplo" }));
    await userEvent.click(screen.getByRole("button", { name: "Importar jornada" }));
    expect(await screen.findByText("CSV inválido")).toBeTruthy();
  });
});

const restriction = {
  id: 1,
  ambito: "Huancayo",
  etiqueta_validacion: "Pendiente",
  validada_normativamente: false,
  activa: false,
  referencia_normativa: null,
  reglas: [{ id: 1, ultimo_digito: 0, dias_semana: [2] }],
  advertencia: "Validación normativa pendiente",
};

describe("plate restrictions", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.loadSession.mockReturnValue({ usuario: { rol: "admin" } });
    mocks.fetchPlateRestrictionConfig.mockResolvedValue(restriction);
    mocks.fetchPlateRestrictionHistory.mockResolvedValue([]);
    mocks.updatePlateRestrictionConfig.mockImplementation(async (body) => ({ ...restriction, ...body }));
  });

  it("loads, edits, validates and deactivates the rule", async () => {
    render(<PlateRestrictions />);
    expect(await screen.findByText("Validación normativa pendiente")).toBeTruthy();
    await userEvent.click(screen.getByLabelText("Lun"));
    await userEvent.click(screen.getByRole("button", { name: "Guardar reglas" }));
    await waitFor(() => expect(mocks.updatePlateRestrictionConfig).toHaveBeenCalledWith({ reglas: [{ ultimo_digito: 0, dias_semana: [1, 2] }] }));

    await userEvent.type(screen.getByPlaceholderText(/Acto u ordenanza/), "Ordenanza 10");
    await userEvent.click(screen.getByRole("button", { name: "Registrar validación normativa" }));
    await waitFor(() => expect(mocks.updatePlateRestrictionConfig).toHaveBeenCalledWith(expect.objectContaining({ validada_normativamente: true })));
    expect(await screen.findByText("Configuración guardada.")).toBeTruthy();

    await userEvent.click(screen.getByRole("button", { name: "Desactivar" }));
    await waitFor(() => expect(mocks.updatePlateRestrictionConfig).toHaveBeenCalledWith({ activa: false }));
  });

  it("shows backend failures and a read-only view", async () => {
    mocks.updatePlateRestrictionConfig.mockRejectedValue(new ApiError("Regla inválida", 422));
    const { unmount } = render(<PlateRestrictions />);
    await screen.findByText("Validación normativa pendiente");
    await userEvent.click(screen.getByRole("button", { name: "Guardar reglas" }));
    expect(await screen.findByText("Regla inválida")).toBeTruthy();
    unmount();

    mocks.loadSession.mockReturnValue({ usuario: { rol: "auditor" } });
    render(<PlateRestrictions />);
    expect(await screen.findByText(/Consulta la configuración/)).toBeTruthy();
  });
});
