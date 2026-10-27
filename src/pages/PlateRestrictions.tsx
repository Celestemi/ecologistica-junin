import { useEffect, useState } from "react";
import {
  ApiError,
  fetchPlateRestrictionConfig,
  fetchPlateRestrictionHistory,
  updatePlateRestrictionConfig,
  type PlateRestrictionConfig,
  type PlateRestrictionHistory,
} from "../api";
import { StaffHeader } from "../components/StaffHeader";
import { formatDateTime } from "../lib/format";
import { loadSession } from "../lib/session";

const WEEKDAYS: { value: number; label: string }[] = [
  { value: 1, label: "Lun" },
  { value: 2, label: "Mar" },
  { value: 3, label: "Mié" },
  { value: 4, label: "Jue" },
  { value: 5, label: "Vie" },
  { value: 6, label: "Sáb" },
  { value: 7, label: "Dom" },
];

export function PlateRestrictions() {
  const session = loadSession();
  const rol = session?.usuario.rol;
  const canEdit = rol === "admin" || rol === "operador";
  const canValidate = rol === "admin";
  const [config, setConfig] = useState<PlateRestrictionConfig | null>(null);
  const [history, setHistory] = useState<PlateRestrictionHistory[]>([]);
  const [digit, setDigit] = useState("0");
  const [days, setDays] = useState<number[]>([2]);
  const [referencia, setReferencia] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function reload() {
    const [cfg, rows] = await Promise.all([
      fetchPlateRestrictionConfig(),
      fetchPlateRestrictionHistory(),
    ]);
    setConfig(cfg);
    setHistory(rows);
    setReferencia(cfg.referencia_normativa ?? "");
    if (cfg.reglas[0]) {
      setDigit(String(cfg.reglas[0].ultimo_digito));
      setDays(cfg.reglas[0].dias_semana);
    }
  }

  useEffect(() => {
    reload().catch((reason: unknown) => {
      setError(reason instanceof Error ? reason.message : "No se pudo leer la configuración.");
    });
  }, []);

  async function onSave(body: Record<string, unknown>) {
    setBusy(true);
    setError(null);
    setSuccess(null);
    try {
      const updated = await updatePlateRestrictionConfig(body);
      setConfig(updated);
      const rows = await fetchPlateRestrictionHistory();
      setHistory(rows);
      setSuccess("Configuración guardada.");
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo guardar.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#f3efe6] text-stone-900">
      <StaffHeader title="Restricción por placa" />
      <main className="mx-auto max-w-3xl space-y-4 px-4 py-6">
        <p className="text-sm">
          <a className="font-semibold text-emerald-900 underline" href="/flota">
            ← Volver a flota
          </a>
        </p>
        {error ? <p className="rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-800" role="alert">{error}</p> : null}
        {success ? <p className="rounded-xl bg-emerald-50 px-3 py-2 text-sm text-emerald-900" role="status" aria-live="polite">{success}</p> : null}
        {config ? (
          <section className="space-y-3 rounded-2xl bg-white p-4 ring-1 ring-stone-200">
            <h2 className="text-base font-semibold">RN-002 / RF-002</h2>
            <p className="rounded-xl bg-amber-50 px-3 py-2 text-sm text-amber-950">{config.advertencia}</p>
            <p className="text-sm text-stone-600">
              Ámbito: <strong>{config.ambito}</strong> · Etiqueta: {config.etiqueta_validacion}
            </p>
            <p className="text-sm text-stone-600">
              Validada normativamente: {config.validada_normativamente ? "Sí" : "No"} · Activa:{" "}
              {config.activa ? "Sí" : "No"}
            </p>
            {canEdit ? (
              <div className="space-y-3 border-t border-stone-200 pt-3">
                <label className="block text-sm font-semibold">
                  Último dígito restringido (0–9)
                  <input
                    className="mt-1 block min-h-11 w-full rounded-xl border border-stone-300 px-3"
                    value={digit}
                    onChange={(event) => setDigit(event.target.value)}
                    min={0}
                    max={9}
                  />
                </label>
                <fieldset>
                  <legend className="text-sm font-semibold">Días de restricción (ISO)</legend>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {WEEKDAYS.map((day) => (
                      <label key={day.value} className="inline-flex items-center gap-1 text-sm">
                        <input
                          type="checkbox"
                          checked={days.includes(day.value)}
                          onChange={(event) => {
                            setDays((current) =>
                              event.target.checked
                                ? [...current, day.value].sort()
                                : current.filter((item) => item !== day.value),
                            );
                          }}
                        />
                        {day.label}
                      </label>
                    ))}
                  </div>
                </fieldset>
                {canValidate ? (
                  <label className="block text-sm font-semibold">
                    Referencia normativa (solo tras validación legal)
                    <input
                      className="mt-1 block min-h-11 w-full rounded-xl border border-stone-300 px-3"
                      value={referencia}
                      onChange={(event) => setReferencia(event.target.value)}
                      placeholder="Acto u ordenanza confirmada"
                    />
                  </label>
                ) : null}
                <div className="flex flex-wrap gap-2">
                  <button
                    type="button"
                    disabled={busy}
                    className="min-h-11 rounded-full bg-[#14532d] px-4 text-sm font-semibold text-white disabled:opacity-50"
                    onClick={() =>
                      void onSave({
                        reglas: [{ ultimo_digito: Number(digit), dias_semana: days }],
                      })
                    }
                  >
                    Guardar reglas
                  </button>
                  {canValidate ? (
                    <button
                      type="button"
                      disabled={busy}
                      className="min-h-11 rounded-full bg-stone-900 px-4 text-sm font-semibold text-white disabled:opacity-50"
                      onClick={() =>
                        void onSave({
                          validada_normativamente: true,
                          referencia_normativa: referencia.trim() || null,
                        })
                      }
                    >
                      Registrar validación normativa
                    </button>
                  ) : null}
                  <button
                    type="button"
                    disabled={busy || !config.validada_normativamente}
                    className="min-h-11 rounded-full bg-emerald-800 px-4 text-sm font-semibold text-white disabled:opacity-50"
                    onClick={() => void onSave({ activa: true })}
                  >
                    Activar regla
                  </button>
                  <button
                    type="button"
                    disabled={busy}
                    className="min-h-11 rounded-full bg-stone-500 px-4 text-sm font-semibold text-white disabled:opacity-50"
                    onClick={() => void onSave({ activa: false })}
                  >
                    Desactivar
                  </button>
                </div>
                {!config.validada_normativamente ? (
                  <p className="text-sm text-stone-600">
                    La activación en rutas queda bloqueada hasta que un administrador registre la
                    validación normativa.
                  </p>
                ) : null}
              </div>
            ) : (
              <p className="text-sm text-stone-600">Consulta la configuración. Los cambios los hace operador o administrador.</p>
            )}
          </section>
        ) : null}
        <section className="rounded-2xl bg-white p-4 ring-1 ring-stone-200">
          <h3 className="text-sm font-semibold">Historial de cambios</h3>
          <ul className="mt-2 space-y-2">
            {history.length === 0 ? (
              <li className="text-sm text-stone-500">Sin cambios registrados.</li>
            ) : (
              history.map((row) => (
                <li key={`${row.creado_en}-${row.detalle}`} className="text-sm">
                  <p>{row.detalle}</p>
                  <p className="text-stone-500">
                    {row.correo} · {formatDateTime(row.creado_en)}
                  </p>
                </li>
              ))
            )}
          </ul>
        </section>
      </main>
    </div>
  );
}
