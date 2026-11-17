import type { Order, Vehicle } from "../types";

export function OrderVehicleSelect({ order, vehicles, disabled, onChange }: {
  order: Order;
  vehicles: Vehicle[];
  disabled: boolean;
  onChange: (vehicleId: number | null) => void;
}) {
  return <label className="mt-3 block text-xs font-semibold text-stone-700">
    Vehículo asignado
    <select aria-label={`Vehículo para ${order.codigo_pedido}`} value={order.vehiculo_asignado_id ?? ""}
      disabled={disabled || order.estado !== "pending"}
      onChange={(event) => onChange(event.target.value ? Number(event.target.value) : null)}
      className="mt-1 block min-h-11 w-full rounded-xl border border-stone-300 bg-white px-2 text-sm disabled:opacity-60">
      <option value="">Automático al optimizar</option>
      {vehicles.map((vehicle) => <option key={vehicle.id} value={vehicle.id}
        disabled={vehicle.estado_operativo !== "activo" || !vehicle.activo || vehicle.capacidad_kg < order.peso_kg}>
        {vehicle.placa} · {vehicle.modelo} · {vehicle.capacidad_kg} kg{vehicle.estado_operativo !== "activo" ? ` · ${vehicle.estado_operativo}` : ""}
      </option>)}
    </select>
  </label>;
}
