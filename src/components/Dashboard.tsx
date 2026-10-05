import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { formatKg, formatKm, reductionPercent } from "../lib/format";
import type { RouteMetadata } from "../types";

type DashboardProps = {
  metadata: RouteMetadata | null;
};

export function Dashboard({ metadata }: DashboardProps) {
  const avoided = metadata?.co2_evitado_kg ?? 0;
  const reference = metadata?.co2_referencia_kg ?? 0;
  const percent = metadata ? reductionPercent(avoided, reference) : 0;
  const trees = metadata?.arboles_quinual_eq ?? 0;
  const chart = metadata
    ? [
        { nombre: "Convencional", co2: metadata.co2_referencia_kg },
        { nombre: "Eco-optimizada", co2: metadata.co2_estimado_kg },
      ]
    : [];

  return (
    <section className="grid gap-3 border-b border-stone-200 bg-[#f7f4ee] px-4 py-3 md:grid-cols-[1.1fr_1fr_1.2fr_1.4fr]">
      <Kpi
        label="Distancia total optimizada"
        value={metadata ? formatKm(metadata.distancia_total_km) : "—"}
        hint={metadata ? metadata.codigo : "Aún sin corrida"}
      />
      <Kpi
        label="Reducción de CO2"
        value={metadata ? formatKg(avoided) : "—"}
        hint={metadata ? `${percent.toFixed(0)} % frente al FIFO` : "kg y porcentaje"}
      />
      <article className="rounded-2xl border border-emerald-900/10 bg-emerald-950 px-4 py-3 text-emerald-50">
        <p className="text-xs tracking-wide text-emerald-200/80">Impacto local</p>
        <p className="mt-2 text-sm leading-snug">
          Equivalente a{" "}
          <span className="text-lg font-semibold text-white">{metadata ? trees.toFixed(2) : "—"}</span>{" "}
          Árboles Quinual/Alisos sembrados en el Valle del Mantaro
        </p>
      </article>
      <article className="rounded-2xl border border-stone-200 bg-white px-3 py-2">
        <p className="px-1 text-xs tracking-wide text-stone-500">Emisiones</p>
        {metadata ? (
          <div className="h-28">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chart} barCategoryGap="32%">
                <CartesianGrid vertical={false} stroke="#e7e5e4" />
                <XAxis dataKey="nombre" tick={{ fill: "#44403c", fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis
                  tick={{ fill: "#78716c", fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                  width={32}
                />
                <Tooltip
                  formatter={(value) => {
                    const numeric = typeof value === "number" ? value : Number(value ?? 0);
                    return [`${numeric.toFixed(2)} kg`, "CO2"];
                  }}
                />
                <Bar dataKey="co2" radius={[6, 6, 0, 0]}>
                  <Cell fill="#a8a29e" />
                  <Cell fill="#047857" />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="px-1 py-8 text-sm text-stone-500">Ejecuta la optimización para comparar las emisiones.</p>
        )}
      </article>
    </section>
  );
}

function Kpi({ label, value, hint }: { label: string; value: string; hint: string }) {
  return (
    <article className="rounded-2xl border border-stone-200 bg-white px-4 py-3">
      <p className="text-xs tracking-wide text-stone-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-stone-900">{value}</p>
      <p className="mt-1 text-xs text-stone-500">{hint}</p>
    </article>
  );
}
