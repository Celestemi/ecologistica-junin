import { useCallback, useEffect, useRef, useState } from "react";
import { assignOrderVehicle, fetchDepots, fetchOrders, fetchPublishedRoute, fetchVehicles, optimizeRoutes } from "./api";
import { OrderVehicleSelect } from "./components/OrderVehicleSelect";
import { Dashboard } from "./components/Dashboard";
import { MapView } from "./components/Map";
import { RouteTable, StopDetail } from "./components/RouteTable";
import { Sidebar } from "./components/Sidebar";
import { StaffHeader } from "./components/StaffHeader";
import { canManageOrders, canOptimize, watchNote } from "./lib/access";
import { loadSession } from "./lib/session";
import type { Depot, Order, RouteOptimization, Vehicle } from "./types";
import { orderLocationHref, ordersOutsideRoute, routeStops, type RouteStop } from "./lib/routePresentation";

export function App() {
  const session = loadSession();
  const rol = session?.usuario.rol;
  const optimize = rol ? canOptimize(rol) : false;
  const note = rol ? watchNote(rol) : null;
  const canWrite = rol ? canManageOrders(rol) : false;
  const [depot, setDepot] = useState<Depot | null>(null);
  const [fecha, setFecha] = useState(() => new Intl.DateTimeFormat("en-CA", { timeZone: "America/Lima" }).format(new Date()));
  const [assigningId, setAssigningId] = useState<number | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [solution, setSolution] = useState<RouteOptimization | null>(null);
  const [optimizing, setOptimizing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPlate, setSelectedPlate] = useState<string | null>(null);
  const [selectedStopKey, setSelectedStopKey] = useState<string | null>(null);
  const [mapAvailable, setMapAvailable] = useState(true);
  const [routeView, setRouteView] = useState<"map" | "table">("map");
  const loadVersion = useRef(0);
  const mutating = useRef(false);

  const refreshPanel = useCallback(async () => {
    if (mutating.current) return;
    const version = ++loadVersion.current;
    setLoading(true);
    setError(null);
    await Promise.all([fetchDepots(), fetchOrders(fecha), fetchVehicles(true), fetchPublishedRoute(fecha)])
      .then(([depots, pending, fleet, published]) => {
        if (version !== loadVersion.current) {
          return;
        }
        setDepot(depots[0] ?? null);
        setOrders(pending);
        setVehicles(fleet);
        setSolution(published);
      })
      .catch((reason: unknown) => {
        if (version !== loadVersion.current) {
          return;
        }
        setError(reason instanceof Error ? reason.message : "No se pudo cargar el panel.");
      })
      .finally(() => {
        if (version === loadVersion.current) {
          setLoading(false);
        }
      });
  }, [fecha]);

  useEffect(() => {
    const refresh = () => { void refreshPanel(); };
    refresh();
    window.addEventListener("focus", refresh);
    window.addEventListener("pageshow", refresh);
    return () => {
      loadVersion.current += 1;
      window.removeEventListener("focus", refresh);
      window.removeEventListener("pageshow", refresh);
    };
  }, [refreshPanel]);

  useEffect(() => {
    const token = loadSession()?.token;
    if (!token) {
      return;
    }
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const socket = new WebSocket(
      `${protocol}//${window.location.host}/ws/tracking/despacho`, [`bearer.${token}`],
    );
    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(String(event.data)) as { type?: string };
        if (message.type !== "route_update") {
          return;
        }
      } catch {
        return;
      }
      void refreshPanel();
    };
    return () => socket.close();
  }, [refreshPanel]);

  async function onOptimize() {
    if (optimizing || assigningId !== null || loading) return;
    mutating.current = true;
    setOptimizing(true);
    setError(null);
    try {
      const result = await optimizeRoutes(fecha);
      setSolution(result);
      setSelectedPlate(null);
      setSelectedStopKey(null);
      setNotice(`Rutas de ${fecha} optimizadas: ${result.metadata.pedidos} pedidos en ${result.metadata.vehiculos_usados} vehículos.`);
      try {
        setOrders(await fetchOrders(fecha));
      } catch {
        setError("Las rutas se guardaron. Pulsa Actualizar pedidos para refrescar la lista.");
      }
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "No se pudo optimizar.");
    } finally {
      mutating.current = false;
      setOptimizing(false);
    }
  }

  async function onAssign(order: Order, vehicleId: number | null) {
    if (assigningId !== null || optimizing) return;
    mutating.current = true;
    const version = loadVersion.current;
    setAssigningId(order.id);
    setError(null);
    try {
      const saved = await assignOrderVehicle(order.id, vehicleId);
      if (version !== loadVersion.current) return;
      setOrders((current) => current.map((item) => item.id === saved.id ? saved : item));
      setNotice(`Asignación de ${saved.codigo_pedido} guardada.`);
    } catch (reason) {
      if (version === loadVersion.current) setError(reason instanceof Error ? reason.message : "No se pudo asignar el vehículo.");
    } finally {
      mutating.current = false;
      setAssigningId(null);
    }
  }

  const stops = routeStops(solution, selectedPlate);
  const pendingOrders = ordersOutsideRoute(orders, solution);
  const locatedCount = pendingOrders.filter((order) => order.ubicacion).length;
  const selectedStop = stops.find((stop) => stop.key === selectedStopKey) ?? null;
  const plates = [...new Set([...vehicles.map((vehicle) => vehicle.placa), ...routeStops(solution).map((stop) => stop.plate)])].filter((plate) => plate !== "Sin vehículo").sort();
  function selectPlate(plate: string) {
    setSelectedPlate((current) => current === plate ? null : plate);
    setSelectedStopKey(null);
  }
  function selectStop(stop: RouteStop) {
    setSelectedPlate(stop.plate === "Sin vehículo" ? null : stop.plate);
    setSelectedStopKey(stop.key);
  }

  return (
    <div className="flex h-full min-h-screen flex-col bg-[#f3efe6] text-stone-900">
      <StaffHeader title="EcoLogística Huancayo" />
      <Dashboard metadata={solution?.metadata ?? null} />
      <section className="border-b border-stone-200 bg-white px-4 py-4" aria-label="Puntos de entrega pendientes">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="font-semibold">Puntos de entrega</h2>
            <p className="mt-1 text-sm text-stone-600">{pendingOrders.length} pendientes de ruta · {locatedCount} con punto · {pendingOrders.length - locatedCount} por ubicar</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <label className="text-xs font-semibold">Jornada
              <input type="date" aria-label="Jornada de rutas" value={fecha} disabled={optimizing || assigningId !== null}
                onChange={(event) => { if (event.target.value) { setFecha(event.target.value); setSelectedPlate(null); setSelectedStopKey(null); setNotice(null); setSolution(null); setOrders([]); } }}
                className="block min-h-11 rounded-xl border border-stone-300 bg-white px-3 text-sm" />
            </label>
            <button type="button" onClick={() => void refreshPanel()} disabled={loading || optimizing} className="min-h-11 rounded-full border border-stone-300 px-4 text-sm font-semibold disabled:opacity-50">Actualizar pedidos</button>
            {canWrite ? <a href="/pedidos#nuevo-pedido" className="inline-flex min-h-11 items-center rounded-full bg-[#14532d] px-4 text-sm font-semibold text-white">+ Agregar punto de entrega</a> : null}
          </div>
        </div>
        {notice ? <p role="status" className="mt-2 text-sm text-emerald-900">{notice}</p> : null}
        {pendingOrders.length > 0 ? (
          <details open className="mt-3">
            <summary className="cursor-pointer text-sm font-semibold text-emerald-950">Pedidos pendientes de ruta</summary>
            <ul className="mt-2 grid max-h-52 gap-2 overflow-y-auto sm:grid-cols-2 xl:grid-cols-3">
              {pendingOrders.map((order) => <li key={order.id} className="rounded-xl border border-stone-200 bg-stone-50 p-3 text-sm">
                <p className="font-semibold">{order.codigo_pedido} · {order.cliente_nombre}</p>
                <p className="mt-1 text-stone-600">{order.direccion_referencia}</p>
                <div className="mt-2 flex flex-wrap items-center justify-between gap-2">
                  <span className={order.ubicacion ? "text-emerald-900" : "font-semibold text-amber-900"}>{order.ubicacion ? "En el mapa (+) · Sin ruta" : "Falta marcar el punto"}</span>
                  {canWrite ? <a href={orderLocationHref(order)} className="font-semibold text-emerald-900 underline">{order.ubicacion ? "Editar punto" : "Ubicar en el mapa"}</a> : null}
                </div>
                {canWrite ? <OrderVehicleSelect order={order} vehicles={vehicles} disabled={optimizing || assigningId !== null || loading} onChange={(vehicleId) => void onAssign(order, vehicleId)} /> : null}
              </li>)}
            </ul>
            <p className="mt-2 text-xs text-stone-500">Los pedidos con punto aparecen en el mapa junto a las rutas publicadas. La optimización define su recorrido.</p>
          </details>
        ) : null}
      </section>
      <div className="flex min-h-0 flex-1 flex-col md:flex-row">
        <Sidebar
          loading={loading}
          canOptimize={optimize}
          roleNote={note}
          orderCount={orders.length}
          vehicles={vehicles.filter((vehicle) => vehicle.estado_operativo === "activo" && vehicle.activo)}
          optimizing={optimizing || assigningId !== null}
          error={error}
          solution={solution}
          onOptimize={() => {
            void onOptimize();
          }}
        />
        <main className="min-h-[420px] flex-1 bg-[#fbf9f4]">
          {vehicles.length > 0 || solution ? (
            <div className="border-b border-stone-200 p-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-medium">Vehículos:</span>
                <button type="button" onClick={() => { setSelectedPlate(null); setSelectedStopKey(null); }} className={`rounded-full px-3 py-1 text-sm ${selectedPlate === null ? "bg-emerald-800 text-white" : "bg-stone-200"}`}>Todas</button>
                {plates.map((plate) => {
                  const vehicle = vehicles.find((item) => item.placa === plate);
                  return <button key={plate} type="button" aria-pressed={selectedPlate === plate} onClick={() => selectPlate(plate)} className={`min-h-11 rounded-full px-3 py-1 text-sm ${selectedPlate === plate ? "bg-emerald-800 text-white" : "bg-stone-200"}`}>
                    {plate}{vehicle && vehicle.estado_operativo !== "activo" ? ` · ${vehicle.estado_operativo}` : ""}
                  </button>;
                })}
                <button type="button" aria-pressed={routeView === "table"} onClick={() => setRouteView((current) => current === "map" ? "table" : "map")} className="ml-auto min-h-11 rounded-full border border-stone-300 px-3 text-sm font-semibold">
                  {routeView === "map" ? "Vista tabular" : "Ver mapa"}
                </button>
              </div>
            </div>
          ) : null}
          {selectedPlate && stops.length === 0 ? <p role="status" className="px-4 py-2 text-sm text-stone-600">{selectedPlate} no tiene ruta publicada en esta jornada.</p> : null}
          {mapAvailable && routeView === "map" ? (
            <MapView depot={depot} orders={orders} vehicles={vehicles} solution={solution} selectedPlate={selectedPlate} onSelectPlate={selectPlate} onSelectStop={setSelectedStopKey} onMapFailure={() => setMapAvailable(false)} />
          ) : (
            <section className="space-y-3 p-4" aria-live="polite">
              {!mapAvailable ? (
                <div className="flex flex-wrap items-center justify-between gap-2 rounded-2xl bg-amber-50 p-3 text-sm text-amber-950">
                  <span>El servicio cartográfico no está disponible. Consulta la secuencia en la vista tabular.</span>
                  <button type="button" className="min-h-11 rounded-xl bg-amber-900 px-3 font-semibold text-white" onClick={() => setMapAvailable(true)}>Reintentar mapa</button>
                </div>
              ) : <p className="rounded-2xl bg-white p-3 text-sm text-stone-700 ring-1 ring-stone-200">La tabla ofrece la misma secuencia y detalle sin depender del mapa.</p>}
              <RouteTable stops={stops} selectedStop={selectedStop} onSelect={selectStop} />
            </section>
          )}
          {loading ? <p className="p-4 text-sm text-stone-500">Cargando rutas y paradas…</p> : null}
          {!loading && !error && !solution && orders.length === 0 ? <p className="p-4 text-sm text-stone-500">No hay rutas ni pedidos disponibles para esta jornada.</p> : null}
          {solution ? <section className="border-t border-stone-200 p-4"><StopDetail stop={selectedStop} /></section> : null}
        </main>
      </div>
    </div>
  );
}
