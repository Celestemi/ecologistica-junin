import { useState, type FormEvent } from "react";
import { ApiError, login } from "../api";
import { Brand } from "../components/Brand";
import { homeFor, rolePurpose, screenAllowed } from "../lib/access";
import { loadSession, saveSession, type Role } from "../lib/session";

const DEMO: { nombre: string; correo: string; clave: string; rol: "admin" | "operador" | "conductor" | "gerente" | "auditor"; etiqueta: string }[] = [
  { nombre: "Luis Huamán", correo: "operador@distrirapido.pe", clave: "Operador.2026", rol: "operador", etiqueta: "Operador" },
  { nombre: "Jorge Delgado", correo: "auditor@distrirapido.pe", clave: "Auditor.2026", rol: "auditor", etiqueta: "Auditor" },
  { nombre: "Rosa Camargo", correo: "admin@distrirapido.pe", clave: "Admin.2026", rol: "admin", etiqueta: "Administrador" },
  { nombre: "Elena Torres", correo: "gerente@distrirapido.pe", clave: "Gerente.2026", rol: "gerente", etiqueta: "Gerente" },
  { nombre: "Pedro Quispe", correo: "conductor@distrirapido.pe", clave: "Conductor.2026", rol: "conductor", etiqueta: "Conductor" },
];

function destination(rol: Role): string {
  const siguiente = new URLSearchParams(window.location.search).get("siguiente");
  if (siguiente && screenAllowed(rol, siguiente)) {
    return siguiente;
  }
  return homeFor(rol);
}

export function Login() {
  const existing = loadSession();
  const [correo, setCorreo] = useState(existing?.usuario.correo ?? "");
  const [clave, setClave] = useState("");
  const [purpose, setPurpose] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (existing) {
    window.location.replace(destination(existing.usuario.rol));
    return null;
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const result = await login(correo, clave);
      saveSession(result.access_token, result.usuario);
      window.location.assign(destination(result.usuario.rol));
    } catch (reason: unknown) {
      setError(reason instanceof ApiError ? reason.message : "No se pudo ingresar.");
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#f3efe6] px-4 py-10 text-stone-900">
      <div className="mx-auto w-full max-w-md">
        <Brand title="EcoLogística Huancayo" />
        <form onSubmit={(event) => void onSubmit(event)} className="mt-8 rounded-3xl bg-white p-6 ring-1 ring-stone-200">
          <h2 className="text-lg font-semibold">Ingresar</h2>
          <p className="mt-1 text-sm text-stone-600">
            {purpose ?? "Usa la cuenta de tu rol. El cliente final entra por el enlace de su pedido."}
          </p>
          <label className="mt-5 block text-sm font-semibold" htmlFor="correo">
            Correo
          </label>
          <input
            id="correo"
            type="email"
            autoComplete="username"
            required
            value={correo}
            onChange={(event) => setCorreo(event.target.value)}
            className="mt-1 w-full rounded-xl border border-stone-300 px-3 py-3 text-base"
          />
          <label className="mt-4 block text-sm font-semibold" htmlFor="clave">
            Contraseña
          </label>
          <input
            id="clave"
            type="password"
            autoComplete="current-password"
            required
            minLength={8}
            value={clave}
            onChange={(event) => setClave(event.target.value)}
            className="mt-1 w-full rounded-xl border border-stone-300 px-3 py-3 text-base"
          />
          {error ? <p className="mt-4 rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-800">{error}</p> : null}
          <button
            type="submit"
            disabled={submitting}
            className="mt-5 w-full rounded-2xl bg-[#14532d] px-3 py-3 text-sm font-semibold text-white hover:bg-emerald-950 disabled:bg-stone-400"
          >
            {submitting ? "Comprobando…" : "Ingresar"}
          </button>
        </form>
        <section className="mt-6">
          <h3 className="text-sm font-semibold text-stone-700">Cuentas de demostración</h3>
          <ul className="mt-2 space-y-2">
            {DEMO.map((account) => (
              <li key={account.correo}>
                <button
                  type="button"
                  className="w-full rounded-2xl bg-white px-3 py-3 text-left ring-1 ring-stone-200 hover:bg-emerald-50"
                  onClick={() => {
                    setCorreo(account.correo);
                    setClave(account.clave);
                    setPurpose(rolePurpose(account.rol));
                    setError(null);
                  }}
                >
                  <span className="block text-sm font-semibold">{account.nombre}</span>
                  <span className="block text-xs text-stone-600">
                    {account.etiqueta} · {account.correo}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
