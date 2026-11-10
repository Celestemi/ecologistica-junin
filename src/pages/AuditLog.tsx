import { useEffect, useState } from "react";
import { fetchAuditLog, type AuditEvent } from "../api";
import { StaffHeader } from "../components/StaffHeader";
import { actionLabel, formatDateTime } from "../lib/format";

export function AuditLog() {
  const [rows, setRows] = useState<AuditEvent[]>([]);
  const [hasMore, setHasMore] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    fetchAuditLog(51)
      .then((events) => {
        if (active) {
          setRows(events.slice(0, 50));
          setHasMore(events.length > 50);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(reason instanceof Error ? reason.message : "No se pudo leer la bitácora.");
        }
      });
    return () => {
      active = false;
    };
  }, []);

  async function loadMore() {
    const beforeId = rows.at(-1)?.id;
    if (!hasMore || beforeId === undefined || loadingMore) return;
    setLoadingMore(true);
    try {
      const events = await fetchAuditLog(51, beforeId);
      setRows((current) => [...current, ...events.slice(0, 50)]);
      setHasMore(events.length > 50);
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "No se pudo leer más de la bitácora.");
    } finally {
      setLoadingMore(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#f3efe6] text-stone-900">
      <StaffHeader title="Bitácora" />
      <main className="mx-auto max-w-3xl px-4 py-6">
        <p className="text-sm text-stone-600">
          Ingresos y cambios de ruta. Desde aquí solo se consulta: no hay forma de borrar un evento.
        </p>
        {error ? <p className="mt-4 rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-800">{error}</p> : null}
        <ul className="mt-4 space-y-2">
          {rows.map((row) => (
            <li key={row.id} className="rounded-2xl bg-white px-4 py-3 ring-1 ring-stone-200">
              <p className="text-sm font-semibold">{actionLabel(row.accion)}</p>
              <p className="text-sm text-stone-700">{row.correo}</p>
              <p className="text-xs text-stone-500">
                {formatDateTime(row.creado_en)}
                {row.detalle ? ` · ${row.detalle}` : ""}
              </p>
            </li>
          ))}
        </ul>
        {hasMore ? (
          <button
            type="button"
            className="mt-3 min-h-11 rounded-full bg-stone-200 px-4 text-sm font-semibold text-stone-900 disabled:opacity-50"
            disabled={loadingMore}
            onClick={() => void loadMore()}
          >
            {loadingMore ? "Cargando…" : "Cargar eventos anteriores"}
          </button>
        ) : null}
        {rows.length === 0 && !error ? <p className="mt-4 text-sm text-stone-500">Todavía no hay eventos.</p> : null}
      </main>
    </div>
  );
}
