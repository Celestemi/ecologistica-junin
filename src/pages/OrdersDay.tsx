import { useEffect, useRef, useState } from "react";
import {
  ApiError,
  createOrder,
  fetchDay,
  importDay,
  updateOrderLocation,
  updateOrderWindow,
  type ImportReport,
  type ImportRow,
} from "../api";
import { buildWindowIso, validateWindowRange, windowInputsFromOrder } from "../lib/orderWindow";
import { PinMap } from "../components/PinMap";
import { StaffHeader } from "../components/StaffHeader";
import { canManageOrders } from "../lib/access";
import { formatKg, formatTime } from "../lib/format";
import { loadSession } from "../lib/session";
import type { Order } from "../types";

const DAY_PAGE_SIZE = 100;

const EXAMPLE = `codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin,lat,lon,altitud
PED-110,Bodega Los Andes,"Jr. Puno 450, Huancayo",25,09:00,12:00,-12.06806,-75.21000,3271
PED-111,Bodega Centro,"Plaza ConstituciÃ³n, Huancayo",40,08:00,11:00,,,
PED-112,Puesto Sin Mapa,"CallejÃ³n sin nombre, El Tambo",15,10:00,13:00,,,
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
  const [ordersHaveMore, setOrdersHaveMore] = useState(false);
  const [ordersTotal, setOrdersTotal] = useState(0);
  const [ordersLoadingMore, setOrdersLoadingMore] = useState(false);
  const [report, setReport] = useState<ImportReport | null>(null);
  const [selected, setSelected] = useState<ImportRow | null>(null);
  const [pin, setPin] = useState<[number, number] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [windowInicio, setWindowInicio] = useState("09:00");
  const [windowFin, setWindowFin] = useState("12:00");
  const ordersVersion = useRef(0);

  useEffect(() => {
    let active = true;
    ordersVersion.current += 1;
    setOrders([]);
    setOrdersHaveMore(false);
    setOrdersTotal(0);
    fetchDay(fecha, 0, DAY_PAGE_SIZE)
      .then((day) => {
        if (active) {
          setOrders(day.pedidos);
          setOrdersHaveMore(day.hay_mas);
          setOrdersTotal(day.total_pedidos);
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

  async function loadMoreOrders() {
    if (ordersLoadingMore || !ordersHaveMore) return;
    const version = ordersVersion.current;
    const currentLength = orders.length;
    const requestedDate = fecha;
    setOrdersLoadingMore(true);
    try {
      const page = await fetchDay(requestedDate, currentLength, DAY_PAGE_SIZE);
      if (version === ordersVersion.current) {
        setOrders((current) => current.length === currentLength ? [...current, ...page.pedidos] : current);
        setOrdersHaveMore(page.hay_mas);
        setOrdersTotal(page.total_pedidos);
      }
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "No se pudieron cargar mÃ¡s pedidos.");
    } finally {
      setOrdersLoadingMore(false);
    }
  }

  async function refreshLoadedOrders() {
    const offsets = Array.from(
      { length: Math.max(1, Math.ceil(orders.length / DAY_PAGE_SIZE)) },
      (_, index) => index * DAY_PAGE_SIZE,
    );
    const version = ordersVersion.current;
    const requestedDate = fecha;
    const pages = await Promise.all(offsets.map((offset) => fetchDay(requestedDate, offset, DAY_PAGE_SIZE)));
    if (version === ordersVersion.current) {
      setOrders(pages.flatMap((page) => page.pedidos));
      setOrdersHaveMore(pages.at(-1)?.hay_mas ?? false);
      setOrdersTotal(pages[0]?.total_pedidos ?? 0);
    }
  }

  async function onImportFromFile(file: File) {
    setBusy(true);
    setError(null);
    try {
      const lower = file.name.toLowerCase();
      let result: ImportReport;
      if (lower.endsWith(".xlsx")) {
        const buffer = await file.arrayBuffer();
        const bytes = new Uint8Array(buffer);
        let binary = "";
        bytes.forEach((byte) => {
          binary += String.fromCharCode(byte);
        });
        result = await importDay(fecha, { xlsx_base64: btoa(binary) });
      } else if (lower.endsWith(".csv") || lower.endsWith(".txt")) {
        const text = await file.text();
        setCsv(text);
        result = await importDay(fecha, { csv: text });
      } else {
        setError("Formato no permitido. Usa CSV o Excel (.xlsx).");
        return;
      }
      setReport(result);
      setSelected(null);
      setPin(null);
      const day = await fetchDay(fecha, 0, DAY_PAGE_SIZE);
      setOrders(day.pedidos);
      setOrdersHaveMore(day.hay_mas);
      setOrdersTotal(day.total_pedidos);
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo leer el archivo.");
    } finally {
      setBusy(false);
    }
  }

  async function onImport() {
    setBusy(true);
    setError(null);
    try {
      const result = await importDay(fecha, { csv });
      setReport(result);
      setSelected(null);
      setPin(null);
      const day = await fetchDay(fecha, 0, DAY_PAGE_SIZE);
      setOrders(day.pedidos);
      setOrdersHaveMore(day.hay_mas);
      setOrdersTotal(day.total_pedidos);
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo leer el archivo.");
    } finally {
      setBusy(false);
    }
  }

  async function onSaveWindow(order: Order) {
    const built = buildWindowIso(fecha, windowInicio, windowFin);
    if (!built) {
      setError("Usa el formato HH:MM para inicio y fin.");
      return;
    }
    const localError = validateWindowRange(built.ventana_inicio, built.ventana_fin);
    if (localError) {
      setError(localError);
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await updateOrderWindow(order.id, built);
      await refreshLoadedOrders();
      setEditingId(null);
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo guardar la ventana.");
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
      const existing =
        orders.find((order) => order.codigo_pedido === selected.codigo_pedido) ??
        (selected.pedido_id != null ? orders.find((order) => order.id === selected.pedido_id) : undefined);
      if (existing) {
        await updateOrderLocation(existing.id, {
          lat: pin[0],
          lon: pin[1],
          altitud_msnm: selected.altitud_msnm ?? 3270,
        });
      } else {
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
      }
      await refreshLoadedOrders();
      setReport((current) =>
        current
          ? {
              ...current,
              aceptados: current.aceptados + 1,
              pendientes_punto: Math.max(0, current.pendientes_punto - 1),
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
      <StaffHeader title="Pedidos del dÃ­a" />
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
                <h2 className="text-base font-semibold">Importar CSV o Excel</h2>
                <div className="flex flex-wrap gap-2">
                  <button type="button" className="min-h-11 rounded-full px-3 text-sm font-semibold text-emerald-900" onClick={() => setCsv(EXAMPLE)}>
                    Usar ejemplo
                  </button>
                  <label className="inline-flex min-h-11 cursor-pointer items-center rounded-full bg-stone-100 px-3 text-sm font-semibold text-stone-900">
                    Elegir archivo
                    <input
                      type="file"
                      accept=".csv,.txt,.xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                      className="sr-only"
                      onChange={(event) => {
                        const file = event.target.files?.[0];
                        if (file) {
                          void onImportFromFile(file);
                        }
                        event.target.value = "";
                      }}
                    />
                  </label>
                </div>
              </div>
              <p className="mt-2 text-xs text-stone-500">Hasta 150 pedidos por archivo. Columnas obligatorias en la primera fila.</p>
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
                {busy ? "Cargandoâ€¦" : "Importar jornada"}
              </button>
            </div>
          ) : (
            <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-600 ring-1 ring-stone-200">
              Consultas los pedidos de la jornada. La carga la hace el operador.
            </p>
          )}
          {error ? <p className="rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-800" role="alert">{error}</p> : null}
          {report ? (
            <>
              <p className="rounded-xl bg-emerald-50 px-3 py-2 text-sm text-emerald-950" role="status" aria-live="polite">{report.resumen}</p>
              <ul className="space-y-2">
              {report.filas.map((row) => (
                <li key={`${row.linea}-${row.codigo_pedido}`} className="rounded-2xl bg-white px-4 py-3 ring-1 ring-stone-200">
                  <p className="text-sm font-semibold">
                    LÃ­nea {row.linea} Â· {row.codigo_pedido || "sin cÃ³digo"} Â· {RESULT[row.resultado]}
                  </p>
                  <p className="text-sm text-stone-700">{row.cliente_nombre}</p>
                  {row.campo ? <p className="text-xs text-stone-500">Campo: {row.campo}</p> : null}
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
            </>
          ) : null}
          <section>
            <h2 className="text-base font-semibold">En la jornada</h2>
            <ul className="mt-2 space-y-2">
              {orders.length === 0 ? <li className="text-sm text-stone-500">TodavÃ­a no hay pedidos en esta fecha.</li> : null}
              {orders.map((order) => (
                <li key={order.id} className="rounded-2xl bg-white px-4 py-3 ring-1 ring-stone-200">
                  <p className="text-sm font-semibold">
                    {order.codigo_pedido}
                    {order.estado !== "pending" ? (
                      <span className="ml-2 text-xs font-normal text-stone-500">({order.estado})</span>
                    ) : null}
                  </p>
                  <p className="text-sm text-stone-700">{order.cliente_nombre}</p>
                  <p className="text-sm text-stone-500">
                    {formatKg(order.peso_kg)} Â· {formatTime(order.ventana_inicio)}â€“{formatTime(order.ventana_fin)}
                  </p>
                  {order.estado_ubicacion === "pendiente_validacion" ? (
                    <p className="mt-1 text-xs font-semibold text-amber-800">Pendiente de validaciÃ³n en mapa</p>
                  ) : null}
                  {canWrite && order.estado === "pending" ? (
                    editingId === order.id ? (
                      <div className="mt-2 space-y-2">
                        <div className="flex flex-wrap gap-2">
                          <label className="text-xs font-semibold">
                            Inicio
                            <input
                              type="time"
                              className="mt-1 block min-h-10 rounded-lg border border-stone-300 px-2"
                              value={windowInicio}
                              onChange={(event) => setWindowInicio(event.target.value)}
                            />
                          </label>
                          <label className="text-xs font-semibold">
                            Fin
                            <input
                              type="time"
                              className="mt-1 block min-h-10 rounded-lg border border-stone-300 px-2"
                              value={windowFin}
                              onChange={(event) => setWindowFin(event.target.value)}
                            />
                          </label>
                        </div>
                        <div className="flex gap-2">
                          <button
                            type="button"
                            className="min-h-10 rounded-full bg-[#14532d] px-3 text-xs font-semibold text-white"
                            disabled={busy}
                            onClick={() => void onSaveWindow(order)}
                          >
                            Guardar ventana
                          </button>
                          <button
                            type="button"
                            className="min-h-10 rounded-full bg-stone-200 px-3 text-xs font-semibold"
                            onClick={() => setEditingId(null)}
                          >
                            Cancelar
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button
                        type="button"
                        className="mt-2 min-h-10 rounded-full bg-emerald-50 px-3 text-xs font-semibold text-emerald-950"
                        onClick={() => {
                          const inputs = windowInputsFromOrder(order.ventana_inicio, order.ventana_fin);
                          setWindowInicio(inputs.inicio);
                          setWindowFin(inputs.fin);
                          setEditingId(order.id);
                        }}
                      >
                        Editar ventana
                      </button>
                    )
                  ) : null}
                </li>
              ))}
            </ul>
            {ordersHaveMore ? (
              <button
                type="button"
                className="mt-3 min-h-11 rounded-full bg-stone-200 px-4 text-sm font-semibold text-stone-900 disabled:opacity-50"
                disabled={ordersLoadingMore}
                onClick={() => void loadMoreOrders()}
              >
                {ordersLoadingMore ? "Cargandoâ€¦" : `Cargar mÃ¡s pedidos (${orders.length} de ${ordersTotal})`}
              </button>
            ) : null}
          </section>
        </section>
        <aside className="rounded-2xl bg-white p-4 ring-1 ring-stone-200">
          <h2 className="text-base font-semibold">Punto en el valle</h2>
          <p className="mt-1 text-sm text-stone-600">
            {selected
              ? `Toca el mapa para ubicar ${selected.codigo_pedido}.`
              : "Elige un pedido que quedÃ³ sin coordenadas."}
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
