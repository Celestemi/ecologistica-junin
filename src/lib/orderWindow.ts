/** Validación de ventanas horarias (RF-006), zona America/Lima en el payload ISO. */

export function validateWindowRange(ventanaInicio: string, ventanaFin: string): string | null {
  const start = Date.parse(ventanaInicio);
  const end = Date.parse(ventanaFin);
  if (Number.isNaN(start) || Number.isNaN(end)) {
    return "Indica horas de inicio y fin válidas.";
  }
  if (end <= start) {
    return "La hora de fin debe ser posterior a la de inicio.";
  }
  return null;
}

export function windowInputsFromOrder(ventanaInicio: string, ventanaFin: string): {
  inicio: string;
  fin: string;
} {
  const start = new Date(ventanaInicio);
  const end = new Date(ventanaFin);
  const pad = (value: number) => String(value).padStart(2, "0");
  const fmt = (date: Date) =>
    `${pad(date.getHours())}:${pad(date.getMinutes())}`;
  return { inicio: fmt(start), fin: fmt(end) };
}

export function buildWindowIso(fecha: string, horaInicio: string, horaFin: string): {
  ventana_inicio: string;
  ventana_fin: string;
} | null {
  const timePattern = /^([01]\d|2[0-3]):([0-5]\d)$/;
  if (!timePattern.test(horaInicio) || !timePattern.test(horaFin)) {
    return null;
  }
  const ventana_inicio = `${fecha}T${horaInicio}:00-05:00`;
  const ventana_fin = `${fecha}T${horaFin}:00-05:00`;
  return { ventana_inicio, ventana_fin };
}
