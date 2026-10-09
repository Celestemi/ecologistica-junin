import { useEffect, useState } from "react";
import {
  ApiError,
  createVehicle,
  fetchDepots,
  fetchFleet,
  fetchVehicleHistory,
  updateVehicle,
  type VehicleHistory,
} from "../api";
import { StaffHeader } from "../components/StaffHeader";
import { canCreateVehicle, canEditVehicle } from "../lib/access";
import { fuelLabel, formatDateTime, formatKg } from "../lib/format";
import { loadSession } from "../lib/session";
import type { Depot, Vehicle } from "../types";

export function Fleet() {
  const session = loadSession();
  const rol = session?.usuario.rol;
  const canCreate = rol ? canCreateVehicle(rol) : false;
  const canEdit = rol ? canEditVehicle(rol) : false;
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [depots, setDepots] = useState<Depot[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [history, setHistory] = useState<VehicleHistory[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [draft, setDraft] = useState({
    placa: "",
    capacidad_kg: "800",
    capacidad_m3: "4",
    tipo_combustible: "diesel",
    emision_base_co2_g_km: "200",
    factor_penalizacion_pendiente: "0.04",
  });

  async function reload() {
    const fleet = await fetchFleet();
    setVehicles(fleet);
    return fleet;
  }

  useEffect(() => {
    let active = true;
    Promise.all([fetchFleet(), fetchDepots()])
      .then(([fleet, places]) => {
        if (!active) {
          return;
        }
        setVehicles(fleet);
        setDepots(places);
        setSelected(fleet[0]?.id ?? null);
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(reason instanceof Error ? reason.message : "No se pudo leer la flota.");
        }
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (selected === null) {
      setHistory([]);
      return;
    }
    let active = true;
    fetchVehicleHistory(selected)
      .then((rows) => {
        if (active) {
          setHistory(rows);
        }
      })
      .catch(() => {
        if (active) {
          setHistory([]);
        }
      });
    return () => {
      active = false;
    };
  }, [selected]);

  async function onCreate() {
    const depot = depots[0];
    if (!depot) {
      setError("No hay depósito para asignar el vehículo.");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const created = await createVehicle({
        deposito_id: depot.id,
        placa: draft.placa.trim().toUpperCase(),
        capacidad_kg: Number(draft.capacidad_kg),
        capacidad_m3: Number(draft.capacidad_m3),
        tipo_combustible: draft.tipo_combustible,
        emision_base_co2_g_km: Number(draft.emision_base_co2_g_km),
        factor_penalizacion_pendiente: Number(draft.factor_penalizacion_pendiente),
      });
      const fleet = await reload();
      setSelected(created.id);
      setVehicles(fleet);
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo registrar el vehículo.");
    } finally {
      setBusy(false);
    }
  }

  async function onPatch(vehicle: Vehicle, body: Record<string, unknown>) {
    setBusy(true);
    setError(null);
    try {
      await updateVehicle(vehicle.id, body);
      await reload();
      const rows = await fetchVehicleHistory(vehicle.id);
      setHistory(rows);
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo actualizar el vehículo.");
    } finally {
      setBusy(false);
    }
  }

  const current = vehicles.find((vehicle) => vehicle.id === selected) ?? null;

  return (
    <div className="min-h-screen bg-[#f3efe6] text-stone-900">
      <StaffHeader title="Flota" />
      <main className="mx-auto grid max-w-6xl gap-4 px-4 py-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
        <section className="space-y-3">
          {error ? <p className="rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-800">{error}</p> : null}
          {canCreate ? (
            <form
              className="grid gap-3 rounded-2xl bg-white p-4 ring-1 ring-stone-200 sm:grid-cols-2"
              onSubmit={(event) => {
                event.preventDefault();
                void onCreate();
              }}
            >
              <h2 className="sm:col-span-2 text-base font-semibold">Registrar vehículo</h2>
              <label className="text-sm font-semibold">
                Placa
                <input className="mt-1 block min-h-11 w-full rounded-xl border border-stone-300 px-3" value={draft.placa} onChange={(event) => setDraft({ ...draft, placa: event.target.value })} required minLength={5} />
              </label>
              <label className="text-sm font-semibold">
                Combustible
                <select className="mt-1 block min-h-11 w-full rounded-xl border border-stone-300 px-3" value={draft.tipo_combustible} onChange={(event) => setDraft({ ...draft, tipo_combustible: event.target.value })}>
                  <option value="diesel">Diésel</option>
                  <option value="gasoline">Gasolina</option>
                  <option value="glp">GLP</option>
                  <option value="electric">Eléctrico</option>
                </select>
              </label>
              <label className="text-sm font-semibold">
                Capacidad (kg)
                <input className="mt-1 block min-h-11 w-full rounded-xl border border-stone-300 px-3" value={draft.capacidad_kg} onChange={(event) => setDraft({ ...draft, capacidad_kg: event.target.value })} required />
              </label>
              <label className="text-sm font-semibold">
                Capacidad (m³)
                <input className="mt-1 block min-h-11 w-full rounded-xl border border-stone-300 px-3" value={draft.capacidad_m3} onChange={(event) => setDraft({ ...draft, capacidad_m3: event.target.value })} required />
              </label>
              <button type="submit" className="min-h-11 rounded-full bg-[#14532d] px-4 text-sm font-semibold text-white disabled:opacity-50 sm:col-span-2" disabled={busy}>
                Guardar en la flota
              </button>
            </form>
          ) : null}
          <ul className="space-y-2">
            {vehicles.map((vehicle) => (
              <li key={vehicle.id}>
                <button
                  type="button"
                  className={`w-full rounded-2xl px-4 py-3 text-left ring-1 ${vehicle.id === selected ? "bg-emerald-50 ring-emerald-700" : "bg-white ring-stone-200"}`}
                  onClick={() => setSelected(vehicle.id)}
                >
                  <p className="text-sm font-semibold">
                    {vehicle.placa} · {vehicle.activo ? "Activa" : "Inactiva"}
                  </p>
                  <p className="text-sm text-stone-600">
                    {formatKg(vehicle.capacidad_kg)} · {fuelLabel(vehicle.tipo_combustible)}
                  </p>
                </button>
              </li>
            ))}
          </ul>
        </section>
        <aside className="rounded-2xl bg-white p-4 ring-1 ring-stone-200">
          {current ? (
            <>
              <h2 className="text-base font-semibold">{current.placa}</h2>
              <p className="mt-1 text-sm text-stone-600">La placa no se cambia. El historial queda aunque la unidad salga de servicio.</p>
              {canEdit ? (
                <div className="mt-3 flex flex-wrap gap-2">
                  <button
                    type="button"
                    className="min-h-11 rounded-full bg-stone-900 px-3 text-sm font-semibold text-white disabled:opacity-50"
                    disabled={busy}
                    onClick={() => void onPatch(current, { activo: !current.activo })}
                  >
                    {current.activo ? "Sacar de servicio" : "Volver a servicio"}
                  </button>
                </div>
              ) : (
                <p className="mt-3 text-sm text-stone-600">Consultas la flota. Los cambios los hace el operador o el administrador.</p>
              )}
              <h3 className="mt-4 text-sm font-semibold">Historial</h3>
              <ul className="mt-2 space-y-2">
                {history.length === 0 ? <li className="text-sm text-stone-500">Sin cambios registrados.</li> : null}
                {history.map((row) => (
                  <li key={`${row.creado_en}-${row.detalle}`} className="text-sm">
                    <p className="font-medium">{row.detalle}</p>
                    <p className="text-stone-500">{row.correo} · {formatDateTime(row.creado_en)}</p>
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p className="text-sm text-stone-600">Elige un vehículo.</p>
          )}
        </aside>
      </main>
    </div>
  );
}
