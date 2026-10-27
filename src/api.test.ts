import { beforeEach, describe, expect, it, vi } from "vitest";

const sessionMocks = vi.hoisted(() => ({
  loadSession: vi.fn(),
  clearSession: vi.fn(),
}));

vi.mock("./lib/session", async (importOriginal) => ({
  ...(await importOriginal<typeof import("./lib/session")>()),
  loadSession: sessionMocks.loadSession,
  clearSession: sessionMocks.clearSession,
}));

import {
  ApiError,
  confirmDelivery,
  createOrder,
  createVehicle,
  downloadSustainabilityPdf,
  fetchActiveRoute,
  fetchAuditLog,
  fetchDay,
  fetchDepots,
  fetchFleet,
  fetchOperationalIndicators,
  fetchOrders,
  fetchPlateRestrictionConfig,
  fetchPlateRestrictionHistory,
  fetchPublicTracking,
  fetchPublishedRoute,
  fetchTracking,
  fetchVehicleHistory,
  fetchVehicles,
  importDay,
  login,
  optimizeRoutes,
  updateOrderLocation,
  updateOrderWindow,
  updatePlateRestrictionConfig,
  updateVehicle,
} from "./api";

const fetchMock = vi.fn<typeof fetch>();

function jsonResponse(body: unknown = {}, init: ResponseInit = {}): Response {
  return new Response(JSON.stringify(body), {
    status: init.status ?? 200,
    statusText: init.statusText,
    headers: { "Content-Type": "application/json", ...init.headers },
  });
}

describe("API client", () => {
  beforeEach(() => {
    fetchMock.mockReset();
    sessionMocks.loadSession.mockReset().mockReturnValue(null);
    sessionMocks.clearSession.mockReset();
    vi.stubGlobal("fetch", fetchMock);
    vi.stubGlobal("window", { location: { pathname: "/pedidos", assign: vi.fn() } });
  });

  it("builds every resource endpoint and mutation payload", async () => {
    fetchMock.mockImplementation(async () => jsonResponse({ ok: true }));

    await fetchOrders();
    await fetchVehicles();
    await fetchDay("2026-10-27");
    await importDay("2026-10-27", { csv: "codigo,peso" });
    await createOrder({ codigo_pedido: "P-1" });
    await updateOrderWindow(4, { ventana_inicio: "a", ventana_fin: "b" });
    await updateOrderLocation(4, { lat: -12.1, lon: -75.2 });
    await fetchFleet();
    await createVehicle({ placa: "ABC-123" });
    await updateVehicle(3, { activo: false });
    await fetchVehicleHistory(3);
    await fetchPlateRestrictionConfig();
    await updatePlateRestrictionConfig({ activa: true });
    await fetchPlateRestrictionHistory();
    await fetchDepots();
    await fetchTracking("PED / 1");
    await fetchOperationalIndicators("2026/10/01", "2026/10/31");
    await fetchActiveRoute();
    await fetchActiveRoute("ABC 123");
    await confirmDelivery("PED / 1", { operation_id: "op-1", delivered_at: "now" });
    await optimizeRoutes();
    await login("qa@example.com", "secret");
    await fetchAuditLog();

    expect(fetchMock).toHaveBeenCalledTimes(23);
    expect(fetchMock.mock.calls.map(([path]) => path)).toContain("/api/v1/seguimiento/PED%20%2F%201");
    expect(fetchMock.mock.calls.map(([path]) => path)).toContain("/api/v1/rutas/activas?placa=ABC%20123");
    const delivery = fetchMock.mock.calls.find(([path]) => String(path).includes("/entrega"));
    const headers = new Headers(delivery?.[1]?.headers);
    expect(delivery?.[1]?.method).toBe("POST");
    expect(headers.get("Idempotency-Key")).toBe("op-1");
  });

  it("adds authentication unless the caller already supplied it", async () => {
    sessionMocks.loadSession.mockReturnValue({
      token: "jwt-token",
      exp: Date.now() + 1000,
      usuario: { id: 1, nombre: "Op", correo: "op@example.com", rol: "operador" },
    });
    fetchMock.mockResolvedValue(jsonResponse([]));
    await fetchOrders();
    const headers = new Headers(fetchMock.mock.calls[0]?.[1]?.headers);
    expect(headers.get("Authorization")).toBe("Bearer jwt-token");
  });

  it("uses backend details for forbidden and generic errors", async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ detail: "Rol insuficiente" }, { status: 403 }));
    await expect(fetchOrders()).rejects.toMatchObject({ status: 403, message: "Rol insuficiente" });

    fetchMock.mockResolvedValueOnce(jsonResponse({ detail: { code: "invalid" } }, { status: 422, statusText: "Unprocessable" }));
    await expect(fetchOrders()).rejects.toEqual(new ApiError("Unprocessable", 422));

    fetchMock.mockResolvedValueOnce(new Response("not-json", { status: 500, statusText: "Server Error" }));
    await expect(fetchOrders()).rejects.toMatchObject({ status: 500, message: "Server Error" });
  });

  it("clears an authenticated session and redirects after 401", async () => {
    sessionMocks.loadSession.mockReturnValue({ token: "expired" });
    fetchMock.mockResolvedValue(jsonResponse({ detail: "Expiró" }, { status: 401 }));
    await expect(fetchOrders()).rejects.toMatchObject({ status: 401 });
    expect(sessionMocks.clearSession).toHaveBeenCalledOnce();
    expect(window.location.assign).toHaveBeenCalledWith("/ingresar");
  });

  it("does not redirect public or login pages after 401", async () => {
    sessionMocks.loadSession.mockReturnValue({ token: "expired" });
    vi.stubGlobal("window", { location: { pathname: "/seguimiento/token", assign: vi.fn() } });
    fetchMock.mockResolvedValue(jsonResponse({}, { status: 401 }));
    await expect(fetchOrders()).rejects.toBeInstanceOf(ApiError);
    expect(window.location.assign).not.toHaveBeenCalled();
  });

  it("handles public tracking success, API errors and invalid error bodies", async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ estado: "in_transit" }));
    await expect(fetchPublicTracking("a/b")).resolves.toMatchObject({ estado: "in_transit" });
    expect(fetchMock.mock.calls[0]?.[0]).toBe("/api/v1/seguimiento/publico/a%2Fb");

    fetchMock.mockResolvedValueOnce(jsonResponse({ detail: "Token vencido" }, { status: 410 }));
    await expect(fetchPublicTracking("x")).rejects.toMatchObject({ status: 410, message: "Token vencido" });

    fetchMock.mockResolvedValueOnce(new Response("", { status: 404 }));
    await expect(fetchPublicTracking("x")).rejects.toMatchObject({ status: 404, message: "Enlace de seguimiento inválido." });
  });

  it("maps an absent published route to null and propagates other errors", async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ detail: "No existe" }, { status: 404 }));
    await expect(fetchPublishedRoute()).resolves.toBeNull();
    fetchMock.mockResolvedValueOnce(jsonResponse({ detail: "Fallo" }, { status: 500 }));
    await expect(fetchPublishedRoute()).rejects.toMatchObject({ status: 500 });
  });

  it("downloads the sustainability PDF with the server filename", async () => {
    const click = vi.fn();
    vi.stubGlobal("document", { createElement: vi.fn(() => ({ href: "", download: "", click })) });
    vi.spyOn(URL, "createObjectURL").mockReturnValue("blob:test");
    vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => undefined);
    fetchMock.mockResolvedValue(new Response(new Blob(["pdf"]), {
      headers: { "Content-Disposition": 'attachment; filename="eco.pdf"' },
    }));
    await downloadSustainabilityPdf();
    expect(click).toHaveBeenCalledOnce();
    expect(URL.revokeObjectURL).toHaveBeenCalledWith("blob:test");
  });

  it("reports PDF download errors with a stable fallback", async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ detail: "Informe no disponible" }, { status: 503 }));
    await expect(downloadSustainabilityPdf()).rejects.toMatchObject({ status: 503, message: "Informe no disponible" });
    fetchMock.mockResolvedValueOnce(new Response("invalid", { status: 500 }));
    await expect(downloadSustainabilityPdf()).rejects.toMatchObject({ status: 500, message: "No se pudo descargar el informe." });
  });
});
