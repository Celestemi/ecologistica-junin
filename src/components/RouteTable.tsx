import { formatCo2, formatTime, formatWindow } from "../lib/format";
import type { RouteStop } from "../lib/routePresentation";

type RouteTableProps = {
  stops: RouteStop[];
  selectedStop: RouteStop | null;
  onSelect: (stop: RouteStop) => void;
  compact?: boolean;
};

export function RouteTable({ stops, selectedStop, onSelect, compact = false }: RouteTableProps) {
  const deliveries = stops.filter((stop) => stop.type === "delivery");
  if (deliveries.length === 0) {
    return <p className="rounded-2xl bg-amber-50 p-4 text-sm text-amber-950">La ruta requiere revisión: no tiene paradas de entrega suficientes.</p>;
  }
  return (
    <div className={compact ? "overflow-x-auto" : "h-full overflow-auto p-4"}>
      <table className="min-w-full text-left text-sm">
        <thead className="sticky top-0 bg-[#fbf9f4] text-xs uppercase tracking-wide text-stone-500">
          <tr><th className="p-2">Orden</th><th className="p-2">Vehículo</th><th className="p-2">Cliente / parada</th><th className="p-2">ETA</th><th className="p-2">Ventana</th><th className="p-2">Carga</th></tr>
        </thead>
        <tbody>
          {deliveries.map((stop) => (
            <tr key={stop.key} className={`cursor-pointer border-t border-stone-200 ${selectedStop?.key === stop.key ? "bg-emerald-50" : "hover:bg-stone-50"}`} onClick={() => onSelect(stop)}>
              <td className="p-2 font-semibold">{stop.deliveryIndex ?? stop.sequence}</td><td className="p-2">{stop.plate}</td>
              <td className="p-2"><p className="font-medium">{stop.customer ?? "Pendiente"}</p><p className="text-xs text-stone-500">{stop.address ?? "Dirección pendiente"}</p></td>
              <td className="p-2">{stop.etaStatus === "revision_matriz" ? "En revisión" : stop.eta ? formatTime(stop.eta) : "Pendiente"}</td>
              <td className="p-2">{stop.windowStart && stop.windowEnd ? formatWindow(stop.windowStart, stop.windowEnd) : "Pendiente"}</td>
              <td className="p-2">{stop.weightKg == null ? "Pendiente" : `${stop.weightKg} kg`}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function StopDetail({ stop }: { stop: RouteStop | null }) {
  if (!stop || stop.type !== "delivery") return <p className="text-sm text-stone-500">Selecciona una parada para consultar su detalle.</p>;
  const field = (value: string | number | null, missing = "Pendiente") => value == null || value === "" ? missing : value;
  return <article className="space-y-2 rounded-2xl border border-stone-200 bg-white p-4 text-sm">
    <p className="text-xs font-semibold tracking-wide text-emerald-900">PARADA {stop.deliveryIndex ?? stop.sequence} · {stop.plate}</p>
    <p className="text-lg font-semibold">{field(stop.customer)}</p>
    <dl className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-stone-700">
      <dt className="text-stone-500">Pedido</dt><dd>{field(stop.orderCode)}</dd>
      <dt className="text-stone-500">Dirección</dt><dd>{field(stop.address)}</dd>
      <dt className="text-stone-500">ETA</dt><dd>{stop.etaStatus === "revision_matriz" ? "En revisión" : stop.eta ? formatTime(stop.eta) : "Pendiente"}</dd>
      <dt className="text-stone-500">Ventana</dt><dd>{stop.windowStart && stop.windowEnd ? formatWindow(stop.windowStart, stop.windowEnd) : "Pendiente"}</dd>
      <dt className="text-stone-500">Carga</dt><dd>{stop.weightKg == null ? "Pendiente" : `${stop.weightKg} kg`}</dd>
      <dt className="text-stone-500">CO2 tramo</dt><dd>{formatCo2(stop.co2g)}</dd>
    </dl>
  </article>;
}
