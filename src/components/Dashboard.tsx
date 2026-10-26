import { useEffect, useState } from "react";
import { fetchOperationalIndicators } from "../api";
import { formatKg, formatKm } from "../lib/format";
import type { OperationalIndicators, RouteMetadata } from "../types";

export function Dashboard({ metadata }: { metadata: RouteMetadata | null }) {
  const day = metadata?.fecha_operacion ?? new Date().toISOString().slice(0, 10);
  const [start, setStart] = useState(day); const [end, setEnd] = useState(day);
  const [data, setData] = useState<OperationalIndicators | null>(null); const [error, setError] = useState<string | null>(null); const [loading, setLoading] = useState(false);
  useEffect(() => { if (metadata?.fecha_operacion) { setStart(metadata.fecha_operacion); setEnd(metadata.fecha_operacion); } }, [metadata?.fecha_operacion]);
  async function load() { setLoading(true); setError(null); try { setData(await fetchOperationalIndicators(start, end)); } catch (reason) { setData(null); setError(reason instanceof Error ? reason.message : "No se pudieron cargar los indicadores."); } finally { setLoading(false); } }
  useEffect(() => { void load(); }, [start, end]);
  const comparable = data?.linea_base_secuencial_km != null && data?.linea_base_secuencial_co2_kg != null;
  return <section className="border-b border-stone-200 bg-[#f7f4ee] px-4 py-3">
    <div className="mb-3 flex flex-wrap items-end gap-2"><label className="text-xs text-stone-600">Desde<input aria-label="Desde" type="date" value={start} onChange={(e) => setStart(e.target.value)} className="mt-1 block rounded border border-stone-300 bg-white p-2" /></label><label className="text-xs text-stone-600">Hasta<input aria-label="Hasta" type="date" value={end} onChange={(e) => setEnd(e.target.value)} className="mt-1 block rounded border border-stone-300 bg-white p-2" /></label><button type="button" onClick={() => void load()} className="rounded-xl bg-emerald-800 px-3 py-2 text-sm font-semibold text-white">Actualizar</button>{loading ? <span className="text-sm text-stone-500">Actualizando…</span> : null}</div>
    {error ? <p className="rounded-xl bg-rose-50 p-3 text-sm text-rose-800">{error}</p> : null}
    {data?.rutas === 0 ? <p className="rounded-xl bg-white p-3 text-sm text-stone-600">No hay información para el periodo seleccionado.</p> : null}
    {data && data.rutas > 0 ? <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      <Card label="Operación" value={formatKm(data.distancia_total_km)} hint={`${data.rutas} rutas · ${Math.round(data.duracion_total_min)} min`} />
      <Card label="Consumo estimado" value={data.consumo_estimado_gal == null ? "Pendiente" : `${data.consumo_estimado_gal.toFixed(2)} gal`} hint="Tramos / rendimiento real del vehículo" />
      <Card label="Emisiones estimadas" value={formatKg(data.co2_estimado_kg)} hint={`CO₂ evitado: ${formatKg(data.co2_evitado_kg)}`} />
      <Card label="Equivalencia referencial" value={data.arboles_quinual_eq == null ? "No calculable" : `${data.arboles_quinual_eq.toFixed(2)} Quinuales`} hint={data.quinual_kg_co2_por_ano == null ? "Factor no configurado" : `CO₂ evitado / ${data.quinual_kg_co2_por_ano} kg/año; no son árboles plantados.`} />
      <article className="rounded-2xl border border-stone-200 bg-white p-4 md:col-span-2 xl:col-span-4"><p className="text-xs tracking-wide text-stone-500">LÍNEA BASE SECUENCIAL (RN-008)</p>{comparable ? <div className="mt-2 grid gap-2 md:grid-cols-2"><p><strong>Distancia:</strong> {formatKm(data.distancia_total_km)} vs {formatKm(data.linea_base_secuencial_km!)} · {signed(data.ahorro_distancia_pct_vs_secuencial)}%</p><p><strong>CO₂:</strong> {formatKg(data.co2_estimado_kg)} vs {formatKg(data.linea_base_secuencial_co2_kg!)} · {signed(data.ahorro_co2_pct_vs_secuencial)}%</p></div> : <p className="mt-2 text-sm text-amber-900">No es posible calcular porcentajes: falta una línea base válida y comparable.</p>}</article>
    </div> : null}
  </section>;
}
function Card({ label, value, hint }: { label: string; value: string; hint: string }) { return <article className="rounded-2xl border border-stone-200 bg-white p-4"><p className="text-xs tracking-wide text-stone-500">{label}</p><p className="mt-2 text-2xl font-semibold">{value}</p><p className="mt-1 text-xs text-stone-500">{hint}</p></article>; }
function signed(value: number | null): string { return value == null || !Number.isFinite(value) ? "—" : `${value >= 0 ? "+" : ""}${value.toFixed(1)}`; }
