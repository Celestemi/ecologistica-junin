import { useCallback, useEffect, useRef, useState } from "react";
import { fetchOperationalIndicators, downloadSustainabilityPdf } from "../api";
import { loadSession } from '../lib/session';
import { canDownloadReport } from '../lib/access';
import { formatKg, formatKm } from "../lib/format";
import type { OperationalIndicators, RouteMetadata } from "../types";

export function Dashboard({ metadata }: { metadata: RouteMetadata | null }) {
  const day = metadata?.fecha_operacion ?? new Intl.DateTimeFormat('en-CA', { timeZone:'America/Lima', year:'numeric',month:'2-digit',day:'2-digit' }).format(new Date());
  const role = loadSession()?.usuario.rol;
  const reportsAllowed = role ? canDownloadReport(role) : false;
  const [start, setStart] = useState(day); const [end, setEnd] = useState(day);
  const [data, setData] = useState<OperationalIndicators | null>(null); const [error, setError] = useState<string | null>(null); const [loading, setLoading] = useState(false);
  useEffect(() => { if (metadata?.fecha_operacion) { setStart(metadata.fecha_operacion); setEnd(metadata.fecha_operacion); } }, [metadata?.fecha_operacion]);
  const pending = useRef<AbortController | null>(null);
  const load = useCallback(async () => {
    pending.current?.abort();
    const controller = new AbortController();
    pending.current = controller;
    setLoading(true);
    setError(null);
    try {
      const result = await fetchOperationalIndicators(start, end, controller.signal);
      if (!controller.signal.aborted) setData(result);
    } catch (reason) {
      if (!controller.signal.aborted) {
        setData(null);
        setError(reason instanceof Error ? reason.message : "No se pudieron cargar los indicadores.");
      }
    } finally {
      if (!controller.signal.aborted) setLoading(false);
    }
  }, [start, end]);
  useEffect(() => {
    void load();
    return () => pending.current?.abort();
  }, [load, metadata?.id]);
  const comparable = data?.linea_base_secuencial_km != null && data?.linea_base_secuencial_co2_kg != null;
  return <section className="border-b border-stone-200 bg-[#f7f4ee] px-4 py-3">
    <div className="mb-3 flex flex-wrap items-end gap-2"><label className="text-xs text-stone-600">Desde<input type="date" value={start} onChange={(e) => setStart(e.target.value)} className="mt-1 block min-h-11 rounded border border-stone-300 bg-white p-2" /></label><label className="text-xs text-stone-600">Hasta<input type="date" value={end} onChange={(e) => setEnd(e.target.value)} className="mt-1 block min-h-11 rounded border border-stone-300 bg-white p-2" /></label><button type="button" onClick={() => void load()} className="min-h-11 rounded-xl bg-emerald-800 px-3 text-sm font-semibold text-white">Actualizar</button>{loading ? <span className="text-sm text-stone-600" role="status" aria-live="polite">Actualizando…</span> : null}</div>
    <p className="mb-2 text-xs text-stone-600">Estimaciones del plan vigente por jornada; no son consumos medidos ni gasto real.</p>
    {reportsAllowed ? <div className="mb-2 flex flex-wrap gap-2">{(['pdf','csv'] as const).map((format) => <button key={format} type="button" className="min-h-11 rounded border px-3" onClick={() => void downloadSustainabilityPdf(start, end, format).catch((reason: unknown) => setError(reason instanceof Error ? reason.message : 'No se pudo descargar el informe.'))}>Descargar {format.toUpperCase()} del periodo</button>)}</div> : null}
    {error ? <p className="rounded-xl bg-rose-50 p-3 text-sm text-rose-800" role="alert">{error}</p> : null}
    {data?.rutas === 0 ? <p className="rounded-xl bg-white p-3 text-sm text-stone-600">No hay información para el periodo seleccionado.</p> : null}
    {data && data.rutas > 0 ? <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      <Card label="Operación" value={formatKm(data.distancia_total_km)} hint={`${data.rutas} rutas · ${Math.round(data.duracion_total_min)} min`} />
      <Card label="Consumo estimado" value={[data.consumo_estimado_gal == null ? '' : `${data.consumo_estimado_gal.toFixed(2)} gal`, data.consumo_estimado_kwh == null ? '' : `${data.consumo_estimado_kwh.toFixed(2)} kWh`].filter(Boolean).join(' · ') || 'Pendiente'} hint="Combustible por rendimiento; electricidad inferida del CO₂ estimado" />
      {data.costo_estimado_pen != null ? <Card label="Costo estimado" value={`S/ ${data.costo_estimado_pen.toFixed(2)}`} hint="Supuestos referenciales de energía y mantenimiento; no gasto real" /> : null}
      <Card label="Emisiones estimadas" value={formatKg(data.co2_estimado_kg)} hint={data.referencia_comparable === false ? 'Ahorro no verificable: falta referencia comparable' : `CO₂ evitado: ${formatKg(data.co2_evitado_kg)}`} />
      <Card label="Equivalencia referencial" value={data.referencia_comparable === false || data.arboles_quinual_eq == null ? "No calculable" : `${data.arboles_quinual_eq.toFixed(2)} Quinuales`} hint={data.quinual_kg_co2_por_ano == null ? "Factor no configurado" : `CO₂ evitado / ${data.quinual_kg_co2_por_ano} kg/año; no son árboles plantados.`} />
      <article className="rounded-2xl border border-stone-200 bg-white p-4 md:col-span-2 xl:col-span-4"><p className="text-xs tracking-wide text-stone-500">LÍNEA BASE SECUENCIAL (RN-008)</p>{comparable ? <div className="mt-2 grid gap-2 md:grid-cols-2"><p><strong>Distancia:</strong> {formatKm(data.distancia_total_km)} vs {formatKm(data.linea_base_secuencial_km!)} · {signed(data.ahorro_distancia_pct_vs_secuencial)}%</p><p><strong>CO₂:</strong> {formatKg(data.co2_estimado_kg)} vs {formatKg(data.linea_base_secuencial_co2_kg!)} · {signed(data.ahorro_co2_pct_vs_secuencial)}%</p></div> : <p className="mt-2 text-sm text-amber-900">No es posible calcular porcentajes: falta una línea base válida y comparable.</p>}</article>
    </div> : null}
  </section>;
}
function Card({ label, value, hint }: { label: string; value: string; hint: string }) { return <article className="rounded-2xl border border-stone-200 bg-white p-4"><p className="text-xs tracking-wide text-stone-500">{label}</p><p className="mt-2 text-2xl font-semibold">{value}</p><p className="mt-1 text-xs text-stone-500">{hint}</p></article>; }
function signed(value: number | null): string { return value == null || !Number.isFinite(value) ? "—" : `${value >= 0 ? "+" : ""}${value.toFixed(1)}`; }
