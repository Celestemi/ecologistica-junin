// @vitest-environment jsdom

import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

afterEach(() => { cleanup(); window.history.replaceState({}, "", "/"); });

const mocks = vi.hoisted(() => ({
  loadSession: vi.fn(),
  fetchDay: vi.fn(),
  fetchVehicles: vi.fn().mockResolvedValue([]),
  assignOrderVehicle: vi.fn(),
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
  fetchVehicles: mocks.fetchVehicles,
  assignOrderVehicle: mocks.assignOrderVehicle,
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
  PinMap: ({ pin, onPick, enabled }: { pin: [number, number] | null; onPick: (lat: number, lon: number) => void; enabled: boolean }) => (
    <div data-testid="pin-map" data-position={pin?.join(",") ?? ""}>
      <button type="button" disabled={!enabled} onClick={() => onPick(-12.1, -75.2)}>Elegir punto simulado</button>
      <button type="button" disabled={!enabled} onClick={() => onPick(-12.08, -75.21)}>Mover punto simulado</button>
    </div>
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
    mocks.fetchVehicles.mockResolvedValue([]);
    mocks.fetchDay.mockResolvedValue({ fecha: "2026-10-27", pedidos: [order] });
    mocks.importDay.mockResolvedValue(report);
    mocks.updateOrderLocation.mockImplementation(async (id, body) => ({
      ...order,
      id,
      ubicacion: { type: "Point", coordinates: [body.lon, body.lat] },
      altitud_msnm: body.altitud_msnm,
      estado_ubicacion: "geocodificado",
    }));
    mocks.updateOrderWindow.mockResolvedValue(order);
  });

  it("assigns a pending order to a vehicle from the day page", async () => {
    mocks.fetchVehicles.mockResolvedValue([{ id: 2, placa: "E7M-304", modelo: "Eléctrico", estado_operativo: "activo", activo: true, capacidad_kg: 1500 }]);
    mocks.assignOrderVehicle.mockResolvedValue({ ...order, vehiculo_asignado_id: 2 });
    render(<OrdersDay />);
    const select = await screen.findByLabelText("Vehículo para PED-001") as HTMLSelectElement;
    await userEvent.selectOptions(select, "2");
    expect(await screen.findByText("Asignación de PED-001 guardada.")).toBeTruthy();
    expect(mocks.assignOrderVehicle).toHaveBeenCalledWith(1, 2);
    expect(select.value).toBe("2");
  });

  it("imports CSV, resolves a pending point and edits a valid window", async () => {
    render(<OrdersDay />);
    expect(await screen.findByText("Cliente Uno")).toBeTruthy();
    await userEvent.click(screen.getByText("Importar varios pedidos desde archivo"));
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
    expect(screen.queryByRole("button", { name: /Marcar ubicación/ })).toBeNull();
    expect((screen.getByRole("button", { name: "Elegir punto simulado" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("marks a persisted pending order without an import report and keeps the saved marker", async () => {
    const { unmount } = render(<OrdersDay />);
    await userEvent.click(await screen.findByRole("button", { name: "Marcar ubicación de PED-001" }));
    await userEvent.click(screen.getByRole("button", { name: "Elegir punto simulado" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar este punto" }));

    expect(await screen.findByText(/Ubicación de PED-001 guardada/)).toBeTruthy();
    expect(screen.getByTestId("pin-map").getAttribute("data-position")).toBe("-12.1,-75.2");
    expect(screen.queryByText(/Pendiente de validaci/)).toBeNull();
    expect((screen.getByRole("button", { name: "Guardar este punto" }) as HTMLButtonElement).disabled).toBe(true);
    expect(mocks.createOrder).not.toHaveBeenCalled();

    // Reopening the page must load the saved point, then update the same order.
    const saved = await mocks.updateOrderLocation.mock.results[0].value;
    unmount();
    mocks.fetchDay.mockResolvedValue({ pedidos: [saved] });
    render(<OrdersDay />);
    await userEvent.click(await screen.findByRole("button", { name: "Editar ubicación de PED-001" }));
    expect(screen.getByTestId("pin-map").getAttribute("data-position")).toBe("-12.1,-75.2");
    await userEvent.click(screen.getByRole("button", { name: "Mover punto simulado" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar este punto" }));
    await screen.findByText(/Ubicación de PED-001 guardada/);
    expect(mocks.updateOrderLocation).toHaveBeenCalledTimes(2);
    expect(mocks.updateOrderLocation).toHaveBeenLastCalledWith(1, expect.objectContaining({ lat: -12.08, lon: -75.21 }));
  });

  it("loads an existing location, edits it and preserves its altitude", async () => {
    mocks.fetchDay.mockResolvedValue({ pedidos: [{
      ...order,
      ubicacion: { type: "Point", coordinates: [-75.21, -12.06] },
      altitud_msnm: 3281,
      estado_ubicacion: "geocodificado",
    }] });
    render(<OrdersDay />);
    await userEvent.click(await screen.findByRole("button", { name: "Editar ubicación de PED-001" }));
    expect(screen.getByTestId("pin-map").getAttribute("data-position")).toBe("-12.06,-75.21");
    await userEvent.click(screen.getByRole("button", { name: "Elegir punto simulado" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar este punto" }));
    await screen.findByText(/Ubicación de PED-001 guardada/);
    expect(mocks.updateOrderLocation).toHaveBeenCalledWith(1, { lat: -12.1, lon: -75.2, altitud_msnm: 3281 });
  });

  it("updates an imported order by its ID even when it is outside the loaded page", async () => {
    mocks.fetchDay.mockResolvedValue({ pedidos: [], total_pedidos: 150, hay_mas: true });
    render(<OrdersDay />);
    await userEvent.click(screen.getByText("Importar varios pedidos desde archivo"));
    await userEvent.click(screen.getByRole("button", { name: "Usar ejemplo" }));
    await userEvent.click(screen.getByRole("button", { name: "Importar jornada" }));
    await userEvent.click(await screen.findByRole("button", { name: "Marcar en el mapa" }));
    await userEvent.click(screen.getByRole("button", { name: "Elegir punto simulado" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar este punto" }));
    await screen.findByText(/Ubicación de PED-001 guardada/);
    expect(mocks.updateOrderLocation).toHaveBeenCalledWith(1, expect.objectContaining({ lat: -12.1, lon: -75.2 }));
    expect(mocks.createOrder).not.toHaveBeenCalled();
    expect(screen.getByText("1 aceptados, 0 rechazados, 0 pendientes de punto.")).toBeTruthy();
    await userEvent.click(screen.getByRole("button", { name: "Mover punto simulado" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar este punto" }));
    await screen.findByText(/Ubicación de PED-001 guardada/);
    expect(screen.getByText("1 aceptados, 0 rechazados, 0 pendientes de punto.")).toBeTruthy();
  });

  it("keeps the selected point on a save failure and allows retrying", async () => {
    mocks.updateOrderLocation.mockRejectedValueOnce(new ApiError("Punto fuera del área de operación", 400));
    render(<OrdersDay />);
    await userEvent.click(await screen.findByRole("button", { name: "Marcar ubicación de PED-001" }));
    await userEvent.click(screen.getByRole("button", { name: "Elegir punto simulado" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar este punto" }));
    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "Punto fuera del área de operación");
    expect(screen.getByTestId("pin-map").getAttribute("data-position")).toBe("-12.1,-75.2");
    await userEvent.click(screen.getByRole("button", { name: "Guardar este punto" }));
    await screen.findByText(/Ubicación de PED-001 guardada/);
    expect(mocks.updateOrderLocation).toHaveBeenCalledTimes(2);
  });

  it("resets the draft when choosing another order and hides editing for assigned orders", async () => {
    mocks.fetchDay.mockResolvedValue({ pedidos: [order, { ...order, id: 2, codigo_pedido: "PED-002" }, { ...order, id: 3, codigo_pedido: "PED-003", estado: "assigned" }] });
    render(<OrdersDay />);
    await userEvent.click(await screen.findByRole("button", { name: "Marcar ubicación de PED-001" }));
    await userEvent.click(screen.getByRole("button", { name: "Elegir punto simulado" }));
    await userEvent.click(screen.getByRole("button", { name: "Marcar ubicación de PED-002" }));
    expect(screen.getByTestId("pin-map").getAttribute("data-position")).toBe("");
    expect((screen.getByRole("button", { name: "Guardar este punto" }) as HTMLButtonElement).disabled).toBe(true);
    expect(within(screen.getByText("PED-003").closest("li")!).queryByRole("button")).toBeNull();
  });

  it("reports import errors without changing production behavior", async () => {
    mocks.importDay.mockRejectedValue(new ApiError("CSV inválido", 422));
    render(<OrdersDay />);
    await screen.findByText("Cliente Uno");
    await userEvent.click(screen.getByText("Importar varios pedidos desde archivo"));
    await userEvent.click(screen.getByRole("button", { name: "Usar ejemplo" }));
    await userEvent.click(screen.getByRole("button", { name: "Importar jornada" }));
    expect(await screen.findByText("CSV inválido")).toBeTruthy();
  });

  it("opens the delivery editor from a dashboard link even beyond the first page", async () => {
    window.history.replaceState({}, "", "/pedidos?fecha=2026-11-17&pedido=2");
    mocks.fetchDay.mockResolvedValueOnce({ pedidos: [order], hay_mas: true, total_pedidos: 2 });
    mocks.fetchDay.mockResolvedValueOnce({ pedidos: [{ ...order, id: 2, codigo_pedido: "PED-002", ubicacion: { type: "Point", coordinates: [-75.21, -12.08] } }], hay_mas: false, total_pedidos: 2 });
    render(<OrdersDay />);
    await screen.findByText(/arrastra el marcador para ubicar PED-002/);
    expect(mocks.fetchDay).toHaveBeenCalledWith("2026-11-17", 1, 100);
    expect(screen.getByTestId("pin-map").getAttribute("data-position")).toBe("-12.08,-75.21");
  });

  it("opens the new delivery form from the dashboard action", async () => {
    window.history.replaceState({}, "", "/pedidos#nuevo-pedido");
    render(<OrdersDay />);
    expect(screen.getByRole("form", { name: "Nuevo punto de entrega" })).toBeTruthy();
    expect(screen.getByText("Importar varios pedidos desde archivo").closest("details")?.open).toBe(false);
    await screen.findByText("Cliente Uno");
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
