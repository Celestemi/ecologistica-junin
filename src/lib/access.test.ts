import { describe, expect, it } from "vitest";
import {
  canAudit,
  canCreateVehicle,
  canDownloadReport,
  canDrive,
  canEditVehicle,
  canManageOrders,
  canOpenDispatch,
  canOptimize,
  canSeeDesk,
  homeFor,
  rolePurpose,
  screenAllowed,
  watchNote,
} from "./access";
import type { Role } from "./session";

const roles: Role[] = ["admin", "operador", "conductor", "gerente", "auditor"];

describe("role access matrix", () => {
  it("assigns home pages and operational capabilities", () => {
    expect(roles.map(homeFor)).toEqual(["/", "/", "/conductor", "/", "/"]);
    expect(roles.filter(canOpenDispatch)).toEqual(["admin", "operador", "gerente", "auditor"]);
    expect(roles.filter(canOptimize)).toEqual(["operador"]);
    expect(roles.filter(canDrive)).toEqual(["operador", "conductor"]);
    expect(roles.filter(canAudit)).toEqual(["admin", "auditor"]);
    expect(roles.filter(canDownloadReport)).toEqual(["admin", "operador", "gerente", "auditor"]);
    expect(roles.filter(canSeeDesk)).toEqual(["admin", "operador", "gerente", "auditor"]);
    expect(roles.filter(canManageOrders)).toEqual(["admin", "operador"]);
    expect(roles.filter(canCreateVehicle)).toEqual(["admin"]);
    expect(roles.filter(canEditVehicle)).toEqual(["admin", "operador"]);
  });

  it("returns role-specific explanatory text", () => {
    expect(watchNote("gerente")).toMatch(/indicadores/);
    expect(watchNote("auditor")).toMatch(/bitácora/);
    expect(watchNote("admin")).toMatch(/operador/);
    expect(watchNote("operador")).toBeNull();
    for (const role of roles) expect(rolePurpose(role)).not.toHaveLength(0);
  });

  it("authorizes screens including query strings and rejects unknown paths", () => {
    for (const role of roles) {
      expect(screenAllowed(role, "/seguimiento/ABC?token=x")).toBe(true);
      expect(screenAllowed(role, "/ingresar")).toBe(true);
      expect(screenAllowed(role, "/no-existe")).toBe(false);
    }
    expect(screenAllowed("auditor", "/auditoria")).toBe(true);
    expect(screenAllowed("operador", "/auditoria")).toBe(false);
    expect(screenAllowed("conductor", "/conductor")).toBe(true);
    expect(screenAllowed("gerente", "/pedidos")).toBe(true);
    expect(screenAllowed("conductor", "/flota")).toBe(false);
    expect(screenAllowed("operador", "/")).toBe(true);
    expect(screenAllowed("conductor", "")).toBe(false);
  });
});
