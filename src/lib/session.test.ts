import { beforeEach, describe, expect, it, vi } from "vitest";
import { clearSession, loadSession, roleLabel, saveSession, type SessionUser } from "./session";

class MemoryStorage implements Storage {
  private values = new Map<string, string>();
  get length() { return this.values.size; }
  clear() { this.values.clear(); }
  getItem(key: string) { return this.values.get(key) ?? null; }
  key(index: number) { return [...this.values.keys()][index] ?? null; }
  removeItem(key: string) { this.values.delete(key); }
  setItem(key: string, value: string) { this.values.set(key, value); }
}

const user: SessionUser = { id: 7, nombre: "QA", correo: "qa@example.com", rol: "auditor" };

function token(exp: number | undefined): string {
  const body = btoa(JSON.stringify(exp === undefined ? {} : { exp })).replace(/=/g, "").replace(/\+/g, "-").replace(/\//g, "_");
  return `header.${body}.signature`;
}

describe("session persistence", () => {
  beforeEach(() => {
    vi.stubGlobal("sessionStorage", new MemoryStorage());
    vi.stubGlobal("localStorage", new MemoryStorage());
  });

  it("maps every role label", () => {
    expect(["admin", "operador", "conductor", "gerente", "auditor"].map((role) => roleLabel(role as SessionUser["rol"])))
      .toEqual(["Administrador", "Operador de logística", "Conductor", "Gerente", "Auditor"]);
  });

  it("saves and loads a valid JWT expiry", () => {
    const valid = token(Math.floor(Date.now() / 1000) + 3600);
    saveSession(valid, user);
    expect(loadSession()).toMatchObject({ token: valid, usuario: user });
    expect(localStorage.getItem("eco-sesion")).toBeNull();
  });

  it("migrates a valid legacy localStorage session", () => {
    localStorage.setItem("eco-sesion", JSON.stringify({ token: "legacy", exp: Date.now() + 10000, usuario: user }));
    expect(loadSession()?.token).toBe("legacy");
    expect(localStorage.getItem("eco-sesion")).toBeNull();
    expect(sessionStorage.getItem("eco-sesion")).toContain("legacy");
  });

  it("removes expired, malformed and incomplete sessions", () => {
    for (const raw of [
      "not-json",
      JSON.stringify({ token: "x", exp: Date.now() - 1, usuario: user }),
      JSON.stringify({ token: "", exp: Date.now() + 1000, usuario: user }),
    ]) {
      sessionStorage.setItem("eco-sesion", raw);
      expect(loadSession()).toBeNull();
      expect(sessionStorage.getItem("eco-sesion")).toBeNull();
    }
    expect(loadSession()).toBeNull();
  });

  it("treats invalid JWT payloads as immediately expired", () => {
    saveSession("no-payload", user);
    expect(loadSession()).toBeNull();
    saveSession("header.invalid-json.signature", user);
    expect(loadSession()).toBeNull();
    saveSession(token(undefined), user);
    expect(loadSession()).toBeNull();
  });

  it("clears both storage locations without exposing an offline failure", async () => {
    sessionStorage.setItem("eco-sesion", "x");
    localStorage.setItem("eco-sesion", "x");
    clearSession();
    expect(sessionStorage.getItem("eco-sesion")).toBeNull();
    expect(localStorage.getItem("eco-sesion")).toBeNull();
    await new Promise((resolve) => setTimeout(resolve, 0));
  });
});
