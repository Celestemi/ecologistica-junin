import { useEffect, useState } from "react";
import { ApiError, createOrder, fetchDay, importDay, type ImportReport, type ImportRow } from "../api";
import { PinMap } from "../components/PinMap";
import { StaffHeader } from "../components/StaffHeader";
import { canManageOrders } from "../lib/access";
import { formatKg, formatTime } from "../lib/format";
import { loadSession } from "../lib/session";
import type { Order } from "../types";

const EXAMPLE = `codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin,lat,lon,altitud
PED-110,Bodega Los Andes,"Jr. Puno 450, Huancayo",25,09:00,12:00,-12.06806,-75.21000,3271
PED-111,Bodega Centro,"Plaza Constitución, Huancayo",40,08:00,11:00,,,
PED-112,Puesto Sin Mapa,"Callejón sin nombre, El Tambo",15,10:00,13:00,,,
PED-113,Fuera del Valle,"Lima centro",10,09:00,11:00,-12.046,-77.043,150
`;

function limaToday(): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "America/Lima" }).format(new Date());
}

const RESULT: Record<ImportRow["resultado"], string> = {
  aceptado: "Aceptado",
  rechazado: "Rechazado",
  pendiente_punto: "Falta el punto",
};

export function OrdersDay() {
  const session = loadSession();
  const canWrite = session ? canManageOrders(session.usuario.rol) : false;
  const [fecha, setFecha] = useState(limaToday);
  const [csv, setCsv] = useState("");
  const [orders, setOrders] = useState<Order[]>([]);
  const [report, setReport] = useState<ImportReport | null>(null);
  const [selected, setSelected] = useState<ImportRow | null>(null);
  const [pin, setPin] = useState<[number, number] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let active = true;
    fetchDay(fecha)
      .then((day) => {
        if (active) {
          setOrders(day.pedidos);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(reason instanceof Error ? reason.message : "No se pudo leer la jornada.");
        }
      });
    return () => {
      active = false;
    };
  }, [fecha]);

  async function onImport() {
    setBusy(true);
    setError(null);
    try {
      const result = await importDay(fecha, csv);
      setReport(result);
      setSelected(null);
      setPin(null);
      const day = await fetchDay(fecha);
      setOrders(day.pedidos);
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo leer el archivo.");
    } finally {
      setBusy(false);
    }
  }

  async function onSavePin() {
    if (!selected || !pin) {
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await createOrder({
        codigo_pedido: selected.codigo_pedido,
        cliente_nombre: selected.cliente_nombre,
        direccion_referencia: selected.direccion_referencia,
        lat: pin[0],
        lon: pin[1],
        altitud_msnm: selected.altitud_msnm ?? 3270,
        peso_kg: selected.peso_kg ?? 1,
        ventana_inicio: `${fecha}T${selected.hora_inicio}:00-05:00`,
        ventana_fin: `${fecha}T${selected.hora_fin}:00-05:00`,
        fecha,
      });
      const day = await fetchDay(fecha);
      setOrders(day.pedidos);
      setReport((current) =>
        current
          ? {
              ...current,
              aceptados: current.aceptados + 1,
              filas: current.filas.map((row) =>
                row.codigo_pedido === selected.codigo_pedido
                  ? { ...row, resultado: "aceptado", motivo: "Punto marcado en el mapa.", lat: pin[0], lon: pin[1] }
                  : row,
              ),
            }
          : current,
      );
      setSelected(null);
      setPin(null);
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo guardar el punto.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#f3efe6] text-stone-900">
      <StaffHeader title="Pedidos del día" />
      <main className="mx-auto grid max-w-6xl gap-4 px-4 py-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
        <section className="space-y-4">
          <label className="block text-sm font-semibold">
            Jornada
            <input
              type="date"
              className="mt-1 block min-h-11 rounded-xl border border-stone-300 bg-white px-3"
              value={fecha}
              onChange={(event) => {
                setFecha(event.target.value);
                setReport(null);
                setSelected(null);
                setPin(null);
              }}
            />
          </label>
          {canWrite ? (
            <div className="rounded-2xl bg-white p-4 ring-1 ring-stone-200">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h2 className="text-base font-semibold">Cargar CSV</h2>
                <button type="button" className="min-h-11 rounded-full px-3 text-sm font-semibold text-emerald-900" onClick={() => setCsv(EXAMPLE)}>
                  Usar ejemplo
                </button>
              </div>
              <textarea
                className="mt-2 min-h-36 w-full rounded-xl border border-stone-300 px-3 py-2 font-mono text-sm"
                value={csv}
                onChange={(event) => setCsv(event.target.value)}
                placeholder="codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin"
              />
              <button
                type="button"
                className="mt-3 min-h-11 rounded-full bg-[#14532d] px-4 text-sm font-semibold text-white disabled:opacity-50"
                disabled={busy || csv.trim() === ""}
                onClick={() => void onImport()}
              >
                {busy ? "Cargando…" : "Importar jornada"}
              </button>
            </div>
          ) : (
            <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-600 ring-1 ring-stone-200">
              Consultas los pedidos de la jornada. La carga la hace el operador.
            </p>
          )}
          {error ? <p className="rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-800">{error}</p> : null}
          {report ? (
            <ul className="space-y-2">
              {report.filas.map((row) => (
                <li key={`${row.linea}-${row.codigo_pedido}`} className="rounded-2xl bg-white px-4 py-3 ring-1 ring-stone-200">
                  <p className="text-sm font-semibold">
                    {row.codigo_pedido || `Línea ${row.linea}`} · {RESULT[row.resultado]}
                  </p>
                  <p className="text-sm text-stone-700">{row.cliente_nombre}</p>
                  {row.motivo ? <p className="text-sm text-stone-500">{row.motivo}</p> : null}
                  {canWrite && row.resultado === "pendiente_punto" ? (
                    <button
                      type="button"
                      className="mt-2 min-h-11 rounded-full bg-amber-100 px-3 text-sm font-semibold text-amber-950"
                      onClick={() => {
                        setSelected(row);
                        setPin(null);
                      }}
                    >
                      Marcar en el mapa
                    </button>
                  ) : null}
                </li>
              ))}
            </ul>
          ) : null}
          <section>
            <h2 className="text-base font-semibold">En la jornada</h2>
            <ul className="mt-2 space-y-2">
              {orders.length === 0 ? <li className="text-sm text-stone-500">Todavía no hay pedidos en esta fecha.</li> : null}
              {orders.map((order) => (
                <li key={order.id} className="rounded-2xl bg-white px-4 py-3 ring-1 ring-stone-200">
                  <p className="text-sm font-semibold">{order.codigo_pedido}</p>
                  <p className="text-sm text-stone-700">{order.cliente_nombre}</p>
                  <p className="text-sm text-stone-500">
                    {formatKg(order.peso_kg)} · {formatTime(order.ventana_inicio)}–{formatTime(order.ventana_fin)}
                  </p>
                </li>
              ))}
            </ul>
          </section>
        </section>
        <aside className="rounded-2xl bg-white p-4 ring-1 ring-stone-200">
          <h2 className="text-base font-semibold">Punto en el valle</h2>
          <p className="mt-1 text-sm text-stone-600">
            {selected
              ? `Toca el mapa para ubicar ${selected.codigo_pedido}.`
              : "Elige un pedido que quedó sin coordenadas."}
          </p>
          <div className="mt-3 overflow-hidden rounded-2xl">
            <PinMap pin={pin} onPick={(lat, lon) => setPin([lat, lon])} />
          </div>
          <button
            type="button"
            className="mt-3 min-h-11 w-full rounded-full bg-[#14532d] text-sm font-semibold text-white disabled:opacity-50"
            disabled={!canWrite || !selected || !pin || busy}
            onClick={() => void onSavePin()}
          >
            Guardar este punto
          </button>
        </aside>
      </main>
    </div>
  );
}
