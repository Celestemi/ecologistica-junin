import { useEffect, useState } from "react";
import { fetchDepots, fetchOrders, fetchPublishedRoute, fetchVehicles, optimizeRoutes } from "./api";
import { Brand } from "./components/Brand";
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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const socket = new WebSocket(`${protocol}//${window.location.host}/ws/tracking/despacho`);
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
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "No se pudo optimizar.");
    } finally {
      setOptimizing(false);
    }
  }

  return (
    <div className="flex h-full min-h-screen flex-col bg-[#f3efe6] text-stone-900">
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-200 bg-white/80 px-4 py-3">
        <Brand title="EcoLogística Huancayo" />
        <nav className="flex gap-2 text-sm font-semibold" aria-label="Otras vistas">
          <a className="rounded-full bg-emerald-50 px-3 py-2 text-emerald-950 hover:bg-emerald-100" href="/seguimiento">
            Rastrear pedido
          </a>
          <a className="rounded-full bg-[#14532d] px-3 py-2 text-white hover:bg-emerald-950" href="/conductor">
            Modo conductor
          </a>
        </nav>
      </header>
      <Dashboard metadata={solution?.metadata ?? null} />
      <div className="flex min-h-0 flex-1 flex-col md:flex-row">
        <Sidebar
          loading={loading}
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
