import { useEffect, useRef, useState } from "react";
import {
  ApiError,
  assignOrderVehicle,
  createOrder,
  fetchDay,
  fetchVehicles,
  importDay,
  updateOrderLocation,
  updateOrderWindow,
  type ImportReport,
  type ImportRow,
} from "../api";
import { buildWindowIso, validateWindowRange, windowInputsFromOrder } from "../lib/orderWindow";
import { PinMap } from "../components/PinMap";
import { NewOrderForm } from "../components/NewOrderForm";
import { OrderVehicleSelect } from "../components/OrderVehicleSelect";
import { StaffHeader } from "../components/StaffHeader";
import { canManageOrders } from "../lib/access";
import { formatKg, formatTime } from "../lib/format";
import { loadSession } from "../lib/session";
import type { Order, Vehicle } from "../types";

const DAY_PAGE_SIZE = 100;

type LocationSelection = {
  pedidoId: number | null;
  codigo: string;
  altitud: number | null;
  position: [number, number] | null;
  importRow?: ImportRow;
};

const EXAMPLE = `codigo,cliente,direccion,peso_kg,hora_inicio,hora_fin,lat,lon,altitud
PED-110,Bodega Los Andes,"Jr. Puno 450, Huancayo",25,09:00,12:00,-12.06806,-75.21000,3271
PED-111,Bodega Centro,"Plaza Constitución, Huancayo",40,08:00,11:00,,,
PED-112,Puesto Sin Mapa,"Callejón sin nombre, El Tambo",15,10:00,13:00,,,
PED-113,Fuera del Valle,"Lima centro",10,09:00,11:00,-12.046,-77.043,150
`;

function limaToday(): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "America/Lima" }).format(new Date());
}

function initialDate(): string {
  const value = new URLSearchParams(window.location.search).get("fecha");
  return value && /^\d{4}-\d{2}-\d{2}$/.test(value) ? value : limaToday();
}

const RESULT: Record<ImportRow["resultado"], string> = {
  aceptado: "Aceptado",
  rechazado: "Rechazado",
  pendiente_punto: "Falta el punto",
};

export function OrdersDay() {
  const session = loadSession();
  const canWrite = session ? canManageOrders(session.usuario.rol) : false;
  const [fecha, setFecha] = useState(initialDate);
  const [showCreate, setShowCreate] = useState(() => window.location.hash === "#nuevo-pedido");
  const [csv, setCsv] = useState("");
  const [orders, setOrders] = useState<Order[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [assignmentNotice, setAssignmentNotice] = useState<string | null>(null);
  const [ordersHaveMore, setOrdersHaveMore] = useState(false);
  const [ordersTotal, setOrdersTotal] = useState(0);
  const [ordersLoadingMore, setOrdersLoadingMore] = useState(false);
  const [report, setReport] = useState<ImportReport | null>(null);
  const [selected, setSelected] = useState<LocationSelection | null>(null);
  const [pin, setPin] = useState<[number, number] | null>(null);
  const [pinNotice, setPinNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [windowInicio, setWindowInicio] = useState("09:00");
  const [windowFin, setWindowFin] = useState("12:00");
  const ordersVersion = useRef(0);
  const locationPanel = useRef<HTMLElement>(null);
  const linkedOrderId = useRef(Number(new URLSearchParams(window.location.search).get("pedido")) || null);
  const pinChanged = pin !== null && selected !== null && (
    !selected.position || pin[0] !== selected.position[0] || pin[1] !== selected.position[1]
  );

  useEffect(() => {
    let active = true;
    fetchVehicles(true).then((fleet) => { if (active) setVehicles(fleet); })
      .catch((reason: unknown) => { if (active) setError(reason instanceof Error ? reason.message : "No se pudo cargar la flota."); });
    return () => { active = false; };
  }, []);

  async function onAssign(order: Order, vehicleId: number | null) {
    if (busy) return;
    const version = ordersVersion.current;
    setBusy(true);
    setError(null);
    setAssignmentNotice(null);
    try {
      const saved = await assignOrderVehicle(order.id, vehicleId);
      if (version !== ordersVersion.current) return;
      setOrders((current) => current.map((item) => item.id === saved.id ? saved : item));
      setAssignmentNotice(`Asignación de ${saved.codigo_pedido} guardada.`);
    } catch (reason) {
      if (version === ordersVersion.current) setError(reason instanceof Error ? reason.message : "No se pudo asignar el vehículo.");
    } finally {
      setBusy(false);
    }
  }

  function selectLocation(selection: LocationSelection) {
    setSelected(selection);
    setPin(selection.position);
    setPinNotice(null);
    setError(null);
    locationPanel.current?.scrollIntoView?.({ behavior: "smooth", block: "nearest" });
  }

  useEffect(() => {
    let active = true;
    ordersVersion.current += 1;
    setOrders([]);
    setOrdersHaveMore(false);
    setOrdersTotal(0);
    fetchDay(fecha, 0, DAY_PAGE_SIZE)
      .then(async (firstPage) => {
        let day = firstPage;
        const pedidos = [...day.pedidos];
        while (active && linkedOrderId.current && !pedidos.some((order) => order.id === linkedOrderId.current) && day.hay_mas) {
          day = await fetchDay(fecha, pedidos.length, DAY_PAGE_SIZE);
          pedidos.push(...day.pedidos);
        }
        if (active) {
          setOrders(pedidos);
          setOrdersHaveMore(day.hay_mas);
          setOrdersTotal(day.total_pedidos);
          const linked = pedidos.find((order) => order.id === linkedOrderId.current);
          if (linked && canWrite && linked.estado === "pending") {
            selectLocation({ pedidoId: linked.id, codigo: linked.codigo_pedido, altitud: linked.altitud_msnm,
              position: linked.ubicacion ? [linked.ubicacion.coordinates[1], linked.ubicacion.coordinates[0]] : null });
          }
          linkedOrderId.current = null;
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
      setError(reason instanceof Error ? reason.message : "No se pudieron cargar más pedidos.");
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
      setPinNotice(null);
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
      setPinNotice(null);
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
    if (!canWrite || !selected || !pin || !pinChanged || busy) {
      return;
    }
    const version = ordersVersion.current;
    setBusy(true);
    setError(null);
    setPinNotice(null);
    try {
      const pedidoId = selected.pedidoId ?? orders.find((order) => order.codigo_pedido === selected.codigo)?.id;
      let saved: Order;
      if (pedidoId != null) {
        saved = await updateOrderLocation(pedidoId, {
          lat: pin[0],
          lon: pin[1],
          altitud_msnm: selected.altitud ?? 3270,
        });
      } else {
        const row = selected.importRow;
        if (!row) return;
        saved = await createOrder({
          codigo_pedido: row.codigo_pedido,
          cliente_nombre: row.cliente_nombre,
          direccion_referencia: row.direccion_referencia,
          lat: pin[0],
          lon: pin[1],
          altitud_msnm: selected.altitud ?? 3270,
          peso_kg: row.peso_kg ?? 1,
          ventana_inicio: `${fecha}T${row.hora_inicio}:00-05:00`,
          ventana_fin: `${fecha}T${row.hora_fin}:00-05:00`,
          fecha,
        });
      }
      if (version !== ordersVersion.current) return;
      setOrders((current) => current.map((order) => order.id === saved.id ? saved : order));
      const position: [number, number] = saved.ubicacion
        ? [saved.ubicacion.coordinates[1], saved.ubicacion.coordinates[0]]
        : pin;
      setReport((current) => {
        if (!current) return current;
        const filas = current.filas.map((row): ImportRow =>
          (row.pedido_id === saved.id || (row.linea === selected.importRow?.linea && row.codigo_pedido === saved.codigo_pedido))
            ? { ...row, pedido_id: saved.id, resultado: "aceptado", campo: null, motivo: "Punto marcado en el mapa.", lat: position[0], lon: position[1], altitud_msnm: saved.altitud_msnm }
            : row,
        );
        const aceptados = filas.filter((row) => row.resultado === "aceptado").length;
        const pendientes = filas.filter((row) => row.resultado === "pendiente_punto").length;
        return {
          ...current,
          filas,
          aceptados,
          pendientes_punto: pendientes,
          resumen: `${aceptados} aceptados, ${current.rechazados} rechazados, ${pendientes} pendientes de punto.`,
        };
      });
      setSelected({ ...selected, pedidoId: saved.id, altitud: saved.altitud_msnm, position });
      setPin(position);
      setPinNotice(`Ubicación de ${saved.codigo_pedido} guardada. Puedes mover el punto para editarla.`);
      if (pedidoId == null) {
        await refreshLoadedOrders().catch(() => setError("El punto se guardó, pero no se pudo actualizar la lista. Recarga la jornada."));
      }
    } catch (reason: unknown) {
      if (version === ordersVersion.current) {
        setError(reason instanceof Error ? reason.message : "No se pudo guardar el punto.");
      }
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
              disabled={busy}
              onChange={(event) => {
                setFecha(event.target.value);
                setReport(null);
                setSelected(null);
                setPin(null);
                setPinNotice(null);
                setEditingId(null);
                setAssignmentNotice(null);
                linkedOrderId.current = null;
              }}
            />
          </label>
          {canWrite ? <section id="nuevo-pedido" className="rounded-2xl bg-white p-4 ring-1 ring-emerald-200">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="font-semibold">Nuevo punto de entrega</h2>
                <p className="mt-1 text-sm text-stone-600">Completa los datos, marca el mapa y guarda el pedido.</p>
              </div>
              <button type="button" aria-expanded={showCreate} aria-controls="nuevo-pedido-formulario" disabled={busy} onClick={() => setShowCreate((current) => !current)} className="min-h-11 rounded-full bg-[#14532d] px-4 text-sm font-semibold text-white disabled:opacity-50">
                {showCreate ? "Cerrar formulario" : "+ Agregar punto de entrega"}
              </button>
            </div>
            {showCreate ? <div id="nuevo-pedido-formulario"><NewOrderForm key={fecha} fecha={fecha} disabled={busy} onBusyChange={setBusy} onCreated={() => {
              void refreshLoadedOrders().catch(() => setError("El pedido se guardó. Recarga la jornada para actualizar la lista."));
            }} /></div> : null}
          </section> : null}
          {canWrite ? (
            <details className="rounded-2xl bg-white p-4 ring-1 ring-stone-200">
              <summary className="cursor-pointer text-sm font-semibold text-emerald-950">Importar varios pedidos desde archivo</summary>
              <div className="mt-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h2 className="text-base font-semibold">Importar CSV o Excel</h2>
                <div className="flex flex-wrap gap-2">
                  <button type="button" disabled={busy} className="min-h-11 rounded-full px-3 text-sm font-semibold text-emerald-900" onClick={() => setCsv(EXAMPLE)}>
                    Usar ejemplo
                  </button>
                  <label className="inline-flex min-h-11 cursor-pointer items-center rounded-full bg-stone-100 px-3 text-sm font-semibold text-stone-900">
                    Elegir archivo
                    <input
                      type="file"
                      disabled={busy}
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
                {busy ? "Cargando…" : "Importar jornada"}
              </button>
              </div>
            </details>
          ) : (
            <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-600 ring-1 ring-stone-200">
              Consultas los pedidos de la jornada. La carga la hace el operador.
            </p>
          )}
          {error ? <p className="rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-800" role="alert">{error}</p> : null}
          {assignmentNotice ? <p role="status" className="text-sm text-emerald-900">{assignmentNotice}</p> : null}
          {report ? (
            <>
              <p className="rounded-xl bg-emerald-50 px-3 py-2 text-sm text-emerald-950" role="status" aria-live="polite">{report.resumen}</p>
              <ul className="space-y-2">
              {report.filas.map((row) => (
                <li key={`${row.linea}-${row.codigo_pedido}`} className="rounded-2xl bg-white px-4 py-3 ring-1 ring-stone-200">
                  <p className="text-sm font-semibold">
                    Línea {row.linea} · {row.codigo_pedido || "sin código"} · {RESULT[row.resultado]}
                  </p>
                  <p className="text-sm text-stone-700">{row.cliente_nombre}</p>
                  {row.campo ? <p className="text-xs text-stone-500">Campo: {row.campo}</p> : null}
                  {row.motivo ? <p className="text-sm text-stone-500">{row.motivo}</p> : null}
                  {canWrite && row.resultado === "pendiente_punto" ? (
                    <button
                      type="button"
                      disabled={busy}
                      className="mt-2 min-h-11 rounded-full bg-amber-100 px-3 text-sm font-semibold text-amber-950"
                      onClick={() => {
                        const existing = orders.find((order) => order.id === row.pedido_id);
                        selectLocation({
                          pedidoId: row.pedido_id,
                          codigo: row.codigo_pedido,
                          altitud: existing?.altitud_msnm ?? row.altitud_msnm,
                          position: existing?.ubicacion
                            ? [existing.ubicacion.coordinates[1], existing.ubicacion.coordinates[0]]
                            : null,
                          importRow: row,
                        });
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
              {orders.length === 0 ? <li className="text-sm text-stone-500">Todavía no hay pedidos en esta fecha.</li> : null}
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
                    {formatKg(order.peso_kg)} · {formatTime(order.ventana_inicio)}–{formatTime(order.ventana_fin)}
                  </p>
                  {order.estado_ubicacion === "pendiente_validacion" ? (
                    <p className="mt-1 text-xs font-semibold text-amber-800">Pendiente de validación en mapa</p>
                  ) : null}
                  {canWrite && order.estado === "pending" ? <OrderVehicleSelect order={order} vehicles={vehicles} disabled={busy} onChange={(vehicleId) => void onAssign(order, vehicleId)} /> : null}
                  {canWrite && order.estado === "pending" ? (
                    <button
                      type="button"
                      disabled={busy}
                      className="mr-2 mt-2 min-h-10 rounded-full bg-amber-100 px-3 text-xs font-semibold text-amber-950 disabled:opacity-50"
                      aria-label={`${order.ubicacion ? "Editar ubicación" : "Marcar ubicación"} de ${order.codigo_pedido}`}
                      onClick={() => selectLocation({
                        pedidoId: order.id,
                        codigo: order.codigo_pedido,
                        altitud: order.altitud_msnm,
                        position: order.ubicacion ? [order.ubicacion.coordinates[1], order.ubicacion.coordinates[0]] : null,
                      })}
                    >
                      {order.ubicacion ? "Editar ubicación" : "Marcar ubicación"}
                    </button>
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
                {ordersLoadingMore ? "Cargando…" : `Cargar más pedidos (${orders.length} de ${ordersTotal})`}
              </button>
            ) : null}
          </section>
        </section>
        <aside ref={locationPanel} className="self-start rounded-2xl bg-white p-4 ring-1 ring-stone-200 lg:sticky lg:top-4">
          <h2 className="text-base font-semibold">Editar punto de un pedido</h2>
          <p className="mt-1 text-sm text-stone-600">
            {selected
              ? `Toca el mapa o arrastra el marcador para ubicar ${selected.codigo}.`
              : "Elige un pedido de la lista para marcar o editar su ubicación."}
          </p>
          <div className="mt-3 overflow-hidden rounded-2xl">
            <PinMap pin={pin} enabled={canWrite && selected !== null && !busy} onPick={(lat, lon) => {
              if (!canWrite || !selected || busy) return;
              setPin([lat, lon]);
              setPinNotice(null);
            }} />
          </div>
          {pin ? <p className="mt-2 text-xs text-stone-600">Latitud: {pin[0].toFixed(6)} · Longitud: {pin[1].toFixed(6)}</p> : null}
          {pinChanged ? <p className="mt-2 text-sm text-amber-800">Punto seleccionado. Guarda para confirmar la ubicación.</p> : null}
          {pinNotice ? <p className="mt-2 text-sm text-emerald-900" role="status">{pinNotice}</p> : null}
          <button
            type="button"
            className="mt-3 min-h-11 w-full rounded-full bg-[#14532d] text-sm font-semibold text-white disabled:opacity-50"
            disabled={!canWrite || !pinChanged || busy}
            onClick={() => void onSavePin()}
          >
            Guardar este punto
          </button>
        </aside>
      </main>
    </div>
  );
}
