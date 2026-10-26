export type Role = "admin" | "operador" | "conductor" | "gerente" | "auditor";

export type SessionUser = {
  id: number;
  nombre: string;
  correo: string;
  rol: Role;
};

export type Session = {
  token: string;
  exp: number;
  usuario: SessionUser;
};

const KEY = "eco-sesion";

const ROLE_LABELS: Record<Role, string> = {
  admin: "Administrador",
  operador: "Operador de logística",
  conductor: "Conductor",
  gerente: "Gerente",
  auditor: "Auditor",
};

export function roleLabel(rol: Role): string {
  return ROLE_LABELS[rol];
}

function readStored(): Session | null {
  const raw = sessionStorage.getItem(KEY) ?? localStorage.getItem(KEY);
  if (!raw) {
    return null;
  }
  try {
    const parsed = JSON.parse(raw) as Session;
    if (!parsed.token || !parsed.usuario || parsed.exp < Date.now()) {
      sessionStorage.removeItem(KEY);
      localStorage.removeItem(KEY);
      return null;
    }
    return parsed;
  } catch {
    sessionStorage.removeItem(KEY);
    localStorage.removeItem(KEY);
    return null;
  }
}

export function loadSession(): Session | null {
  const session = readStored();
  if (session && localStorage.getItem(KEY)) {
    sessionStorage.setItem(KEY, JSON.stringify(session));
    localStorage.removeItem(KEY);
  }
  return session;
}

export function saveSession(token: string, usuario: SessionUser): void {
  const exp = readExpiry(token);
  sessionStorage.setItem(KEY, JSON.stringify({ token, exp, usuario }));
  localStorage.removeItem(KEY);
}

export function clearSession(): void {
  sessionStorage.removeItem(KEY);
  localStorage.removeItem(KEY);
  // La cola IndexedDB nunca contiene el token; se elimina también al salir.
  void import("./offline").then(({ clearOfflineData }) => clearOfflineData()).catch(() => undefined);
}

function readExpiry(token: string): number {
  const part = token.split(".")[1];
  if (!part) {
    return 0;
  }
  try {
    const padded = part.replace(/-/g, "+").replace(/_/g, "/");
    const payload = JSON.parse(atob(padded)) as { exp?: number };
    return typeof payload.exp === "number" ? payload.exp * 1000 : 0;
  } catch {
    return 0;
  }
}
