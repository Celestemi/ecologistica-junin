import { useEffect, useState } from "react";
import { fetchDepots, fetchOrders, fetchVehicles, optimizeRoutes } from "./api";
import { Dashboard } from "./components/Dashboard";
import { MapView } from "./components/Map";
import { Sidebar } from "./components/Sidebar";
import type { Depot, Order, RouteOptimization, Vehicle } from "./types";

export function App() {
  const [depot, setDepot] = useState<Depot | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [solution, setSolution] = useState<RouteOptimization | null>(null);
  const [optimizing, setOptimizing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    Promise.all([fetchDepots(), fetchOrders(), fetchVehicles()])
      .then(([depots, pending, fleet]) => {
        if (!active) {
          return;
        }
        setDepot(depots[0] ?? null);
        setOrders(pending);
        setVehicles(fleet);
      })
      .catch((reason: unknown) => {
        if (!active) {
          return;
        }
        setError(reason instanceof Error ? reason.message : "No se pudo cargar el panel.");
      });
    return () => {
      active = false;
    };
  }, []);

  async function onOptimize() {
    setOptimizing(true);
    setError(null);
    try {
      const result = await optimizeRoutes();
      const pending = await fetchOrders();
      setSolution(result);
      setOrders(pending);
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "No se pudo optimizar.");
    } finally {
      setOptimizing(false);
    }
  }

  return (
    <div className="flex h-full min-h-screen flex-col bg-[#f3efe6] text-stone-900">
      <header className="flex items-center justify-between border-b border-stone-200 px-4 py-3">
        <div>
          <p className="text-xs tracking-[0.18em] text-emerald-900/70">VALLE DEL MANTARO</p>
          <h1 className="text-xl font-semibold">EcoLogística Huancayo</h1>
        </div>
        <div className="flex gap-4 text-sm font-medium text-emerald-900">
          <a className="underline-offset-2 hover:underline" href="/seguimiento">
            Rastrear pedido
          </a>
          <a className="underline-offset-2 hover:underline" href="/conductor">
            Modo conductor
          </a>
        </div>
      </header>
      <Dashboard metadata={solution?.metadata ?? null} />
      <div className="flex min-h-0 flex-1 flex-col md:flex-row">
        <Sidebar
          orderCount={orders.length}
          vehicles={vehicles}
          optimizing={optimizing}
          error={error}
          solution={solution}
          onOptimize={() => {
            void onOptimize();
          }}
        />
        <main className="min-h-[420px] flex-1">
          <MapView depot={depot} orders={orders} solution={solution} />
        </main>
      </div>
    </div>
  );
}
