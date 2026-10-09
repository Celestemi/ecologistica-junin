import { useEffect, useState } from "react";
import { fetchDepots, fetchOrders, fetchPublishedRoute, fetchVehicles, optimizeRoutes } from "./api";
import { Dashboard } from "./components/Dashboard";
import { MapView } from "./components/Map";
import { Sidebar } from "./components/Sidebar";
import { StaffHeader } from "./components/StaffHeader";
import { canOptimize, watchNote } from "./lib/access";
import { loadSession } from "./lib/session";
import type { Depot, Order, RouteOptimization, Vehicle } from "./types";

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
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "No se pudo optimizar.");
    } finally {
      setOptimizing(false);
    }
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
        <main className="min-h-[420px] flex-1">
          <MapView depot={depot} orders={orders} solution={solution} />
        </main>
      </div>
    </div>
  );
}
