import { useState, type FormEvent } from "react";
import { createOrder } from "../api";
import { buildWindowIso, validateWindowRange } from "../lib/orderWindow";
import type { Order } from "../types";
import { PinMap } from "./PinMap";

type Props = {
  fecha: string;
  disabled: boolean;
  onBusyChange: (busy: boolean) => void;
  onCreated: (order: Order) => void;
};

function newCode() {
  return `PED-${crypto.randomUUID().slice(0, 8).toUpperCase()}`;
}

export function NewOrderForm({ fecha, disabled, onBusyChange, onCreated }: Props) {
  const [codigo, setCodigo] = useState(newCode);
  const [cliente, setCliente] = useState("");
  const [direccion, setDireccion] = useState("");
  const [peso, setPeso] = useState("");
  const [inicio, setInicio] = useState("09:00");
  const [fin, setFin] = useState("12:00");
  const [pin, setPin] = useState<[number, number] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState<Order | null>(null);
  const [saving, setSaving] = useState(false);
  const inputClass = "mt-1 block min-h-11 w-full rounded-xl border border-stone-300 bg-white px-3 text-sm font-normal";

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (saving || disabled) return;
    setError(null);
    if (!pin) {
      setError("Toca el mapa para marcar el punto de entrega antes de guardar.");
      return;
    }
    const deliveryWindow = buildWindowIso(fecha, inicio, fin);
    const windowError = deliveryWindow ? validateWindowRange(deliveryWindow.ventana_inicio, deliveryWindow.ventana_fin) : "Indica un horario válido.";
    if (windowError || !deliveryWindow) {
      setError(windowError);
      return;
    }
    setSaving(true);
    onBusyChange(true);
    try {
      const order = await createOrder({
        codigo_pedido: codigo.trim(), cliente_nombre: cliente.trim(), direccion_referencia: direccion.trim(),
        peso_kg: Number(peso), lat: pin[0], lon: pin[1], altitud_msnm: 3270, fecha, ...deliveryWindow,
      });
      setSaved(order);
      onCreated(order);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "No se pudo guardar el pedido. Intenta nuevamente.");
    } finally {
      setSaving(false);
      onBusyChange(false);
    }
  }

  if (saved) return (
    <div className="mt-4 space-y-3 rounded-xl bg-emerald-50 p-4">
      <p role="status" className="font-semibold text-emerald-950">{saved.codigo_pedido}: pedido y punto de entrega guardados.</p>
      <p className="text-sm text-emerald-900">Ya puedes verlo en el mapa principal. Queda pendiente de asignar a una ruta.</p>
      <div className="flex flex-wrap gap-2">
        <a href="/" className="inline-flex min-h-11 items-center rounded-full bg-emerald-900 px-4 text-sm font-semibold text-white">Ver en el dashboard</a>
        <button type="button" className="min-h-11 rounded-full bg-white px-4 text-sm font-semibold text-emerald-950" onClick={() => {
          setSaved(null); setCodigo(newCode()); setCliente(""); setDireccion(""); setPeso(""); setPin(null); setError(null);
        }}>Agregar otro pedido</button>
      </div>
    </div>
  );

  return (
    <form aria-label="Nuevo punto de entrega" className="mt-4 space-y-4" onSubmit={(event) => void submit(event)}>
      <fieldset disabled={disabled || saving} className="space-y-3">
        <legend className="mb-2 text-sm font-semibold">1. Datos del pedido</legend>
        <div className="grid gap-3 sm:grid-cols-2">
          <label className="text-sm font-semibold">Cliente<input className={inputClass} required minLength={2} maxLength={160} value={cliente} onChange={(event) => setCliente(event.target.value)} placeholder="Nombre o negocio" /></label>
          <label className="text-sm font-semibold">Código del pedido<input className={inputClass} required minLength={3} maxLength={32} value={codigo} onChange={(event) => setCodigo(event.target.value)} /></label>
          <label className="text-sm font-semibold sm:col-span-2">Dirección o referencia<input className={inputClass} required minLength={3} maxLength={240} value={direccion} onChange={(event) => setDireccion(event.target.value)} placeholder="Calle, número y una referencia para la entrega" /></label>
          <label className="text-sm font-semibold">Peso (kg)<input className={inputClass} type="number" min="0.01" step="0.01" required value={peso} onChange={(event) => setPeso(event.target.value)} /></label>
          <div className="grid grid-cols-2 gap-2">
            <label className="text-sm font-semibold">Desde<input className={inputClass} type="time" required value={inicio} onChange={(event) => setInicio(event.target.value)} /></label>
            <label className="text-sm font-semibold">Hasta<input className={inputClass} type="time" required value={fin} onChange={(event) => setFin(event.target.value)} /></label>
          </div>
        </div>
      </fieldset>
      <section aria-label="Ubicación del nuevo pedido" className="space-y-2">
        <h3 className="text-sm font-semibold">2. Marca el punto de entrega</h3>
        <p className="text-sm text-stone-600">Toca el lugar exacto en el mapa. Puedes acercarte con + y arrastrar el marcador para ajustarlo.</p>
        <PinMap pin={pin} enabled={!disabled && !saving} onPick={(lat, lon) => { setPin([lat, lon]); setError(null); }} />
        <p className={`text-sm ${pin ? "text-emerald-900" : "text-amber-900"}`}>
          {pin ? "Punto seleccionado. Guarda el pedido para confirmar." : "Falta marcar el punto en el mapa."}
        </p>
      </section>
      {error ? <p role="alert" className="rounded-xl bg-rose-50 p-3 text-sm text-rose-800">{error}</p> : null}
      <button type="submit" disabled={disabled || saving} className="min-h-12 w-full rounded-full bg-[#14532d] px-4 text-sm font-semibold text-white disabled:opacity-50">
        {saving ? "Guardando pedido…" : "Guardar pedido y punto"}
      </button>
    </form>
  );
}
