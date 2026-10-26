import { formatCo2, formatTime, formatWindow, fuelLabel } from "../lib/format";
import { ROUTE_COLORS, type RouteOptimization, type Vehicle } from "../types";

type SidebarProps = {
  loading: boolean;
  canOptimize: boolean;
  roleNote: string | null;
  orderCount: number;
  vehicles: Vehicle[];
  optimizing: boolean;
  error: string | null;
  solution: RouteOptimization | null;
  onOptimize: () => void;
};

type ItineraryStop = {
  sequence: number;
  deliveryIndex: number | null;
  title: string;
  customer: string;
  eta: string | null;
  co2g: number;
  kind: string;
  windowStart: string | null;
  windowEnd: string | null;
  etaEstado: string | null;
  waitMinutes: number;
  lateMinutes: number;
  distanceNote: string | null;
};

export function Sidebar({
  loading,
  canOptimize,
  roleNote,
  orderCount,
  vehicles,
  optimizing,
  error,
  solution,
  onOptimize,
}: SidebarProps) {
  const groups = groupItinerary(solution, vehicles);

  return (
    <aside className="flex h-full w-full flex-col border-stone-200 bg-[#fbf9f4] md:w-80 md:border-r">
      <div className="border-b border-stone-200 px-4 py-4">
        <p className="text-xs tracking-[0.16em] text-emerald-900/70">{canOptimize ? "DESPACHO" : "LECTURA"}</p>
        <h2 className="mt-1 text-lg font-semibold text-stone-900">{canOptimize ? "Control de ruta" : "Ruta publicada"}</h2>
        <p className="mt-2 text-sm text-stone-600">
          {loading ? "Cargando el día de operación…" : `${orderCount} pedidos pendientes · ${vehicles.length} vehículos activos`}
        </p>
        {canOptimize ? (
          <button
            type="button"
            onClick={onOptimize}
            disabled={loading || optimizing || orderCount === 0}
            aria-busy={optimizing}
            className="mt-4 flex min-h-12 w-full items-center justify-center gap-2 rounded-2xl bg-[#14532d] px-3 py-3 text-center text-sm font-semibold leading-snug text-white hover:bg-emerald-950 disabled:cursor-not-allowed disabled:bg-stone-400"
          >
            {optimizing ? <Spinner /> : null}
            {optimizing ? "Calculando rutas…" : "Ejecutar Optimización Ecológica VRPTW"}
          </button>
        ) : null}
        {!loading && roleNote ? <p className="mt-3 text-sm leading-snug text-stone-600">{roleNote}</p> : null}
        {!loading && canOptimize && orderCount === 0 && !optimizing ? (
          <p className="mt-2 text-xs text-stone-500">No hay pedidos pendientes.</p>
        ) : null}
        {error ? <p className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-800">{error}</p> : null}
        {solution?.metadata.exclusiones_placa && solution.metadata.exclusiones_placa.length > 0 ? (
          <ul className="mt-3 space-y-1 rounded-lg bg-amber-50 px-3 py-2 text-xs text-amber-950">
            {solution.metadata.exclusiones_placa.map((item) => (
              <li key={item.placa}>
                <strong>{item.placa}</strong>: {item.motivo}
              </li>
            ))}
          </ul>
        ) : null}
        {solution && !solution.metadata.feasible ? (
          <p className="mt-3 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-900">
            La solución incumple alguna ventana o la capacidad.
          </p>
        ) : null}
        {solution?.metadata.pedidos_sin_asignar && solution.metadata.pedidos_sin_asignar.length > 0 ? (
          <p className="mt-3 rounded-lg bg-stone-100 px-3 py-2 text-xs text-stone-700">
            Sin asignar: {solution.metadata.pedidos_sin_asignar.join(", ")}
          </p>
        ) : null}
        {solution?.metadata.geometria_vial_disponible === false ? (
          <p className="mt-2 rounded-lg bg-amber-50 px-3 py-2 text-xs text-amber-950">
            Trazado vial no disponible: configure OSRM o revise la conectividad. No se muestran líneas rectas como calles.
          </p>
        ) : null}
        {solution?.metadata.nota_distancia ? (
          <p className="mt-2 text-[11px] leading-snug text-stone-500">{solution.metadata.nota_distancia}</p>
        ) : null}
      </div>
      <div className="flex-1 overflow-y-auto px-4 py-4">
        {groups.length === 0 ? (
          <p className="text-sm text-stone-500">El itinerario aparece aquí después de optimizar.</p>
        ) : (
          <div className="space-y-4">
            {groups.map((group) => (
              <section key={group.plate}>
                <header className="mb-2 flex items-baseline justify-between gap-2">
                  <h3 className="font-semibold text-stone-900" style={{ color: group.color }}>
                    {group.plate}
                  </h3>
                  <p className="text-xs text-stone-500">
                    {group.fuel} · {group.capacityKg} kg
                  </p>
                </header>
                <ol className="space-y-0 border-l-2 pl-3" style={{ borderColor: group.color }}>
                  {group.stops.map((stop) => (
                    <li key={`${group.plate}-${stop.sequence}`} className="relative pb-3 text-sm">
                      <span
                        className="absolute -left-[1.15rem] top-1 h-2.5 w-2.5 rounded-full ring-2 ring-[#fbf9f4]"
                        style={{ background: group.color }}
                      />
                      <p className="font-medium text-stone-800">
                        {stop.kind === "delivery" && stop.deliveryIndex != null
                          ? `#${stop.deliveryIndex} · `
                          : ""}
                        {stop.customer}
                      </p>
                      <p className="text-stone-600">{stop.title}</p>
                      <p className="text-xs text-stone-500">
                        {stop.kind === "delivery"
                          ? stop.etaEstado === "revision_matriz"
                            ? "ETA en revisión (matriz incompleta)"
                            : `ETA ${formatTime(stop.eta)} · ventana ${formatWindow(stop.windowStart, stop.windowEnd)}`
                          : stop.kind === "depot_start"
                            ? "Salida"
                            : "Retorno"}
                        {stop.waitMinutes > 0 ? ` · espera ${Math.round(stop.waitMinutes)} min` : ""}
                        {stop.lateMinutes > 0 ? ` · tarde ${Math.round(stop.lateMinutes)} min` : ""}
                        {stop.co2g > 0 ? ` · ${formatCo2(stop.co2g)}` : ""}
                      </p>
                      {stop.distanceNote ? (
                        <p className="text-[11px] text-stone-400">{stop.distanceNote}</p>
                      ) : null}
                    </li>
                  ))}
                </ol>
              </section>
            ))}
          </div>
        )}
      </div>
    </aside>
  );
}

function groupItinerary(solution: RouteOptimization | null, vehicles: Vehicle[]) {
  if (!solution) {
    return [];
  }
  const byPlate = new Map<string, ItineraryStop[]>();
  for (const feature of solution.features) {
    if (feature.geometry.type !== "Point" || !feature.properties.plate) {
      continue;
    }
    const plate = feature.properties.plate;
    const stop: ItineraryStop = {
      sequence: feature.properties.sequence ?? 0,
      deliveryIndex: feature.properties.delivery_index ?? null,
      title: feature.properties.title ?? "Parada",
      customer: feature.properties.customer ?? (feature.properties.stop_type === "delivery" ? "Cliente" : "Depósito"),
      eta: feature.properties.eta ?? null,
      co2g: feature.properties.co2_g ?? 0,
      kind: feature.properties.stop_type ?? "delivery",
      windowStart: feature.properties.window_start ?? null,
      windowEnd: feature.properties.window_end ?? null,
      etaEstado: feature.properties.eta_estado ?? null,
      waitMinutes: feature.properties.wait_minutes ?? 0,
      lateMinutes: feature.properties.late_minutes ?? 0,
      distanceNote: feature.properties.distance_note ?? null,
    };
    const list = byPlate.get(plate) ?? [];
    list.push(stop);
    byPlate.set(plate, list);
  }
  const plates = [...byPlate.keys()].sort();
  return plates.map((plate, index) => {
    const vehicle = vehicles.find((item) => item.placa === plate);
    return {
      plate,
      color: ROUTE_COLORS[index % ROUTE_COLORS.length] ?? ROUTE_COLORS[0],
      fuel: vehicle ? fuelLabel(vehicle.tipo_combustible) : "Flota",
      capacityKg: vehicle ? vehicle.capacidad_kg : 0,
      stops: (byPlate.get(plate) ?? []).sort((a, b) => a.sequence - b.sequence),
    };
  });
}

function Spinner() {
  return (
    <span
      className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white"
      aria-hidden="true"
    />
  );
}
