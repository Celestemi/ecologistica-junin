const TIME = new Intl.DateTimeFormat("es-PE", {
  hour: "2-digit",
  minute: "2-digit",
  hourCycle: "h23",
  timeZone: "America/Lima",
});

const NUMBER = new Intl.NumberFormat("es-PE", { maximumFractionDigits: 1 });

export function formatTime(iso: string | null | undefined): string {
  if (!iso) {
    return "—";
  }
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return "—";
  }
  return TIME.format(date);
}

export function formatWindow(start: string | null | undefined, end: string | null | undefined): string {
  if (!start || !end) {
    return "Sin ventana";
  }
  return `${formatTime(start)} – ${formatTime(end)}`;
}

export function formatKm(value: number): string {
  return `${NUMBER.format(value)} km`;
}

export function formatKg(value: number): string {
  return `${value.toFixed(2)} kg`;
}

export function formatCo2(grams: number | null): string {
  if (grams === null) {
    return "Se calcula al optimizar";
  }
  if (grams >= 1000) {
    return `${(grams / 1000).toFixed(2)} kg`;
  }
  return `${Math.round(grams)} g`;
}

export function limaHour(iso: string): number {
  const hour = new Intl.DateTimeFormat("en-GB", {
    hour: "numeric",
    hourCycle: "h23",
    timeZone: "America/Lima",
  }).format(new Date(iso));
  return Number(hour);
}

export function windowColor(iso: string | null | undefined): string {
  if (!iso) {
    return "#b45309";
  }
  const hour = limaHour(iso);
  if (hour < 9) {
    return "#c2410c";
  }
  if (hour < 12) {
    return "#d97706";
  }
  return "#4d7c0f";
}

export function reductionPercent(avoidedKg: number, referenceKg: number): number {
  if (referenceKg <= 0) {
    return 0;
  }
  return (avoidedKg / referenceKg) * 100;
}

const FUEL_LABELS: Record<string, string> = {
  diesel: "Diésel",
  electric: "Eléctrico",
  gasoline: "Gasolina",
  glp: "GLP",
};

export function fuelLabel(fuel: string): string {
  return FUEL_LABELS[fuel] ?? fuel;
}

const STATUS_LABELS: Record<string, string> = {
  pending: "Pendiente",
  assigned: "Asignado",
  in_transit: "En camino",
  delivered: "Entregado",
  incident: "Con incidencia",
  cancelled: "Cancelado",
};

export function statusLabel(status: string): string {
  return STATUS_LABELS[status] ?? status;
}

const DATE_TIME = new Intl.DateTimeFormat("es-PE", {
  dateStyle: "short",
  timeStyle: "short",
  timeZone: "America/Lima",
});

export function formatDateTime(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return "—";
  }
  return DATE_TIME.format(date);
}

const ACTION_LABELS: Record<string, string> = {
  ingreso_correcto: "Ingreso correcto",
  ingreso_fallido: "Ingreso fallido",
  ingreso_bloqueado: "Ingreso bloqueado",
  optimizar_rutas: "Optimización ejecutada",
  optimizar_denegado: "Optimización denegada",
  reporte_denegado: "Informe denegado",
  bitacora_denegada: "Lectura de bitácora denegada",
  importar_pedidos: "Pedidos cargados",
  importar_denegado: "Carga de pedidos denegada",
  flota_actualizada: "Flota actualizada",
  flota_denegada: "Cambio de flota denegado",
  jornada_denegada: "Consulta de jornada denegada",
};

export function actionLabel(action: string): string {
  return ACTION_LABELS[action] ?? action;
}
