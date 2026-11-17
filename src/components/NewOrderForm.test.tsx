// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { NewOrderForm } from "./NewOrderForm";

const createOrder = vi.hoisted(() => vi.fn());
vi.mock("../api", () => ({ createOrder }));
vi.mock("./PinMap", () => ({ PinMap: ({ onPick, enabled }: { onPick: (lat: number, lon: number) => void; enabled: boolean }) => <button type="button" disabled={!enabled} onClick={() => onPick(-12.068, -75.21)}>Marcar destino</button> }));

afterEach(cleanup);
beforeEach(() => {
  vi.clearAllMocks();
  createOrder.mockImplementation(async (body) => ({ ...body, id: 50, ubicacion: { type: "Point", coordinates: [body.lon, body.lat] } }));
});

async function fillOrder() {
  await userEvent.type(screen.getByLabelText("Cliente"), "Bodega nueva");
  await userEvent.type(screen.getByLabelText("Dirección o referencia"), "Jr. Puno 123");
  await userEvent.type(screen.getByLabelText("Peso (kg)"), "15.5");
}

describe("new delivery form", () => {
  it("requires a map point and creates a delivery with its location and Lima date", async () => {
    const onCreated = vi.fn();
    const onBusyChange = vi.fn();
    render(<NewOrderForm fecha="2026-11-17" disabled={false} onCreated={onCreated} onBusyChange={onBusyChange} />);
    await fillOrder();
    await userEvent.click(screen.getByRole("button", { name: "Guardar pedido y punto" }));
    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "Toca el mapa para marcar el punto de entrega antes de guardar.");
    expect(createOrder).not.toHaveBeenCalled();
    await userEvent.click(screen.getByRole("button", { name: "Marcar destino" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar pedido y punto" }));
    await screen.findByText(/pedido y punto de entrega guardados/);
    expect(createOrder).toHaveBeenCalledWith(expect.objectContaining({ cliente_nombre: "Bodega nueva", peso_kg: 15.5, lat: -12.068, lon: -75.21, fecha: "2026-11-17", ventana_inicio: "2026-11-17T09:00:00-05:00", ventana_fin: "2026-11-17T12:00:00-05:00" }));
    expect(onCreated).toHaveBeenCalledOnce();
    expect(onBusyChange.mock.calls).toEqual([[true], [false]]);
    expect(screen.getByRole("link", { name: "Ver en el dashboard" }).getAttribute("href")).toBe("/");
    await userEvent.click(screen.getByRole("button", { name: "Agregar otro pedido" }));
    expect((screen.getByLabelText("Cliente") as HTMLInputElement).value).toBe("");
    expect(screen.getByText("Falta marcar el punto en el mapa.")).toBeTruthy();
  });

  it("keeps entered data and the point when saving fails, and allows retrying", async () => {
    createOrder.mockRejectedValueOnce(new Error("Ya existe un pedido con ese código."));
    render(<NewOrderForm fecha="2026-11-17" disabled={false} onCreated={vi.fn()} onBusyChange={vi.fn()} />);
    await fillOrder();
    await userEvent.click(screen.getByRole("button", { name: "Marcar destino" }));
    await userEvent.click(screen.getByRole("button", { name: "Guardar pedido y punto" }));
    expect(await screen.findByText("Ya existe un pedido con ese código.")).toBeTruthy();
    expect((screen.getByLabelText("Cliente") as HTMLInputElement).value).toBe("Bodega nueva");
    expect(screen.getByText("Punto seleccionado. Guarda el pedido para confirmar.")).toBeTruthy();
    await userEvent.click(screen.getByRole("button", { name: "Guardar pedido y punto" }));
    await screen.findByText(/pedido y punto de entrega guardados/);
    expect(createOrder).toHaveBeenCalledTimes(2);
  });

  it("rejects an end time before the start without sending the order", async () => {
    render(<NewOrderForm fecha="2026-11-17" disabled={false} onCreated={vi.fn()} onBusyChange={vi.fn()} />);
    await fillOrder();
    await userEvent.click(screen.getByRole("button", { name: "Marcar destino" }));
    await userEvent.clear(screen.getByLabelText("Hasta"));
    await userEvent.type(screen.getByLabelText("Hasta"), "08:00");
    await userEvent.click(screen.getByRole("button", { name: "Guardar pedido y punto" }));
    expect(await screen.findByText("La hora de fin debe ser posterior a la de inicio.")).toBeTruthy();
    expect(createOrder).not.toHaveBeenCalled();
  });
});
