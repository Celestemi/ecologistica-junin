import type { Role } from "./session";

export function homeFor(rol: Role): string {
  return rol === "conductor" ? "/conductor" : "/";
}

export function canOpenDispatch(rol: Role): boolean {
  return rol !== "conductor";
}

export function canOptimize(rol: Role): boolean {
  return rol === "operador";
}

export function canDrive(rol: Role): boolean {
  return rol === "operador" || rol === "conductor";
}

export function canAudit(rol: Role): boolean {
  return rol === "admin" || rol === "auditor";
}

export function canDownloadReport(rol: Role): boolean {
  return rol === "admin" || rol === "operador" || rol === "gerente" || rol === "auditor";
}

export function canSeeDesk(rol: Role): boolean {
  return canDownloadReport(rol);
}

export function canManageOrders(rol: Role): boolean {
  return rol === "admin" || rol === "operador";
}

export function canCreateVehicle(rol: Role): boolean {
  return rol === "admin";
}

export function canEditVehicle(rol: Role): boolean {
  return rol === "admin" || rol === "operador";
}

export function watchNote(rol: Role): string | null {
  if (rol === "gerente") {
    return "Lees los indicadores del día. La ruta la publica el operador.";
  }
  if (rol === "auditor") {
    return "Revisas la ruta publicada y la bitácora. No puedes modificar el reparto.";
  }
  if (rol === "admin") {
    return "Ves la operación y la bitácora. La optimización la ejecuta el operador.";
  }
  return null;
}

export function rolePurpose(rol: Role): string {
  if (rol === "operador") {
    return "Armas la ruta del día y puedes salir a reparto.";
  }
  if (rol === "conductor") {
    return "Entregas la ruta de tu vehículo.";
  }
  if (rol === "gerente") {
    return "Lees el resultado del día y descargas el informe.";
  }
  if (rol === "auditor") {
    return "Revisas la operación y la bitácora, sin cambiarlas.";
  }
  return "Ves la operación. La ruta la publica el operador.";
}

export function screenAllowed(rol: Role, path: string): boolean {
  const clean = path.split("?")[0] ?? "/";
  if (clean.startsWith("/seguimiento")) {
    return true;
  }
  if (clean.startsWith("/ingresar")) {
    return true;
  }
  if (clean.startsWith("/auditoria")) {
    return canAudit(rol);
  }
  if (clean.startsWith("/conductor")) {
    return canDrive(rol);
  }
  if (clean.startsWith("/pedidos") || clean.startsWith("/flota")) {
    return canSeeDesk(rol);
  }
  if (clean === "/" || clean === "") {
    return canOpenDispatch(rol);
  }
  return false;
}
