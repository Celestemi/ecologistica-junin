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

export function loadSession(): Session | null {
  const raw = localStorage.getItem(KEY);
  if (!raw) {
    return null;
  }
  try {
    const parsed = JSON.parse(raw) as Session;
    if (!parsed.token || !parsed.usuario || parsed.exp < Date.now()) {
      localStorage.removeItem(KEY);
      return null;
    }
    return parsed;
  } catch {
    localStorage.removeItem(KEY);
    return null;
  }
}

export function saveSession(token: string, usuario: SessionUser): void {
  const exp = readExpiry(token);
  localStorage.setItem(KEY, JSON.stringify({ token, exp, usuario }));
}

export function clearSession(): void {
  localStorage.removeItem(KEY);
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
