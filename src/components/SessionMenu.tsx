import { clearSession, loadSession, roleLabel } from "../lib/session";

type SessionMenuProps = {
  light?: boolean;
};

export function SessionMenu({ light = false }: SessionMenuProps) {
  const session = loadSession();
  if (!session) {
    return null;
  }
  const { usuario } = session;
  const chip = light
    ? "inline-flex min-h-11 items-center rounded-full bg-white/15 px-3 text-sm font-semibold text-white"
    : "inline-flex min-h-11 items-center rounded-full bg-stone-100 px-3 text-sm font-semibold text-stone-800 hover:bg-stone-200";

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className={light ? "text-right text-sm text-emerald-50" : "text-right text-sm text-stone-700"}>
        <span className="block font-semibold leading-tight">{usuario.nombre}</span>
        <span className="block text-xs opacity-80">{roleLabel(usuario.rol)}</span>
      </span>
      <button
        type="button"
        className={chip}
        onClick={() => {
          clearSession();
          window.location.assign("/ingresar");
        }}
      >
        Salir
      </button>
    </div>
  );
}
