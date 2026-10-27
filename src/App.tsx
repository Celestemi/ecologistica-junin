import { useEffect, useState } from "react";
import { fetchDepots, fetchOrders, fetchPublishedRoute, fetchVehicles, optimizeRoutes } from "./api";
import { Dashboard } from "./components/Dashboard";
import { MapView } from "./components/Map";
import { RouteTable, StopDetail } from "./components/RouteTable";
import { Sidebar } from "./components/Sidebar";
import { StaffHeader } from "./components/StaffHeader";
import { canOptimize, watchNote } from "./lib/access";
import { loadSession } from "./lib/session";
import type { Depot, Order, RouteOptimization, Vehicle } from "./types";
import { routeStops, type RouteStop } from "./lib/routePresentation";

export function App() {
  const session = loadSession();
  const rol = session?.usuario.rol;
  const optimize = rol ? canOptimize(rol) : false;
  const note = rol ? watchNote(rol) : null;
  const [depot, setDepot] = useState<Depot | null>(null);
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

  useEffect(() => {
    let active = true;
    Promise.all([fetchDepots(), fetchOrders(), fetchVehicles(), fetchPublishedRoute()])
      .then(([depots, pending, fleet, published]) => {
        if (!active) {
          return;
        }
        setDepot(depots[0] ?? null);
        setOrders(pending);
        setVehicles(fleet);
        setSolution(published);
      })
      .catch((reason: unknown) => {
        if (!active) {
          return;
        }
        setError(reason instanceof Error ? reason.message : "No se pudo cargar el panel.");
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    const token = loadSession()?.token;
    if (!token) {
      return;
    }
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const socket = new WebSocket(
      `${protocol}//${window.location.host}/ws/tracking/despacho?token=${encodeURIComponent(token)}`,
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
      void fetchPublishedRoute().then((published) => {
        if (published) {
          setSolution(published);
        }
      });
    };
    return () => socket.close();
  }, []);

  async function onOptimize() {
    setOptimizing(true);
    setError(null);
    try {
      const result = await optimizeRoutes();
      const pending = await fetchOrders();
      setSolution(result);
      setOrders(pending);
      setSelectedPlate(null);
      setSelectedStopKey(null);
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "No se pudo optimizar.");
    } finally {
      setOptimizing(false);
    }
  }

  const stops = routeStops(solution, selectedPlate);
  const selectedStop = stops.find((stop) => stop.key === selectedStopKey) ?? null;
  const plates = [...new Set(routeStops(solution).map((stop) => stop.plate))].filter((plate) => plate !== "Sin vehículo");
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
      <div className="flex min-h-0 flex-1 flex-col md:flex-row">
        <Sidebar
          loading={loading}
          canOptimize={optimize}
          roleNote={note}
          orderCount={orders.length}
          vehicles={vehicles}
          optimizing={optimizing}
          error={error}
          solution={solution}
          onOptimize={() => {
            void onOptimize();
          }}
        />
        <main className="min-h-[420px] flex-1 bg-[#fbf9f4]">
          {solution ? (
            <div className="border-b border-stone-200 p-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-medium">Rutas:</span>
                <button type="button" onClick={() => { setSelectedPlate(null); setSelectedStopKey(null); }} className={`rounded-full px-3 py-1 text-sm ${selectedPlate === null ? "bg-emerald-800 text-white" : "bg-stone-200"}`}>Todas</button>
                {plates.map((plate) => <button key={plate} type="button" onClick={() => selectPlate(plate)} className={`rounded-full px-3 py-1 text-sm ${selectedPlate === plate ? "bg-emerald-800 text-white" : "bg-stone-200"}`}>{plate}</button>)}
                <button type="button" aria-pressed={routeView === "table"} onClick={() => setRouteView((current) => current === "map" ? "table" : "map")} className="ml-auto min-h-11 rounded-full border border-stone-300 px-3 text-sm font-semibold">
                  {routeView === "map" ? "Vista tabular" : "Ver mapa"}
                </button>
              </div>
            </div>
          ) : null}
          {mapAvailable && routeView === "map" ? (
            <MapView depot={depot} orders={orders} solution={solution} selectedPlate={selectedPlate} onSelectPlate={selectPlate} onSelectStop={setSelectedStopKey} onMapFailure={() => setMapAvailable(false)} />
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
