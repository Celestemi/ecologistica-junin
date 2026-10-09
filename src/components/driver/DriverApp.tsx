import { useCallback, useEffect, useMemo, useRef, useState, type PointerEvent } from "react";
import { fetchActiveRoute, fetchVehicles } from "../../api";
import { StaffHeader } from "../StaffHeader";
import { formatKg, formatTime, formatWindow, fuelLabel } from "../../lib/format";
import { loadSession } from "../../lib/session";
import type { ActiveRoute, DriverStop, Vehicle } from "../../types";

type Coords = { lat: number; lon: number; alt: number };
type LinkState = "conectando" | "conectado" | "reconectando";

const DONE_KEY = "eco-driver-delivered";

const INCIDENTS = [
  {
    id: "traffic",
    label: "Tráfico denso",
    className: "bg-amber-500 text-stone-950",
  },
  {
    id: "blockade",
    label: "Vía bloqueada / lluvia",
    className: "bg-orange-700 text-white",
  },
  {
    id: "absent",
    label: "Cliente ausente",
    className: "bg-stone-900 text-white",
  },
] as const;

export function DriverApp() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [plate, setPlate] = useState<string | null>(null);
  const [route, setRoute] = useState<ActiveRoute | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [link, setLink] = useState<LinkState>("conectando");
  const [usingGps, setUsingGps] = useState(false);
  const [done, setDone] = useState<Set<string>>(() => readDone());
  const [etas, setEtas] = useState<Record<string, string>>({});
  const [signing, setSigning] = useState<DriverStop | null>(null);
  const [sending, setSending] = useState(false);

  const socketRef = useRef<WebSocket | null>(null);
  const coordsRef = useRef<Coords | null>(null);
  const nextRef = useRef<DriverStop | null>(null);
  const vehicleRef = useRef<Vehicle | null>(null);
  const sendPositionRef = useRef<() => void>(() => undefined);

  const vehicle = vehicles.find((item) => item.placa === plate) ?? null;
  const stops = route?.paradas ?? [];
  const nextDelivery = stops.find(
    (stop) => stop.tipo_parada === "delivery" && !done.has(stopKey(stop)),
  ) ?? null;

  useEffect(() => {
    nextRef.current = nextDelivery;
    vehicleRef.current = vehicle;
    sendPositionRef.current = () => {
      const socket = socketRef.current;
      const here = coordsRef.current ?? coordsFromStop(nextRef.current);
      if (!socket || socket.readyState !== WebSocket.OPEN || !here) {
        return;
      }
      socket.send(
        JSON.stringify({
          type: "position",
          lat: here.lat,
          lon: here.lon,
          altitud_msnm: here.alt,
          vehicle_id: vehicleRef.current?.id,
          order_code: nextRef.current?.codigo_pedido,
        }),
      );
    };
  }, [nextDelivery, vehicle]);

  const loadRoute = useCallback(async (selected: string) => {
    try {
      const active = await fetchActiveRoute(selected);
      setRoute(active);
      setLoadError(null);
    } catch (reason: unknown) {
      setRoute(null);
      setLoadError(reason instanceof Error ? reason.message : "No hay una ruta activa.");
    }
  }, []);

  useEffect(() => {
    const requested = new URLSearchParams(window.location.search).get("placa");
    fetchVehicles()
      .then((fleet) => {
        setVehicles(fleet);
        const match = fleet.find((item) => item.placa === requested) ?? fleet[0];
        setPlate(match?.placa ?? null);
      })
      .catch((reason: unknown) => {
        setLoadError(reason instanceof Error ? reason.message : "No se pudo leer la flota.");
      });
  }, []);

  useEffect(() => {
    if (!plate) {
      return;
    }
    void loadRoute(plate);
  }, [plate, loadRoute]);

  useEffect(() => {
    if (!navigator.geolocation) {
      return;
    }
    const watch = navigator.geolocation.watchPosition(
      (position) => {
        coordsRef.current = {
          lat: position.coords.latitude,
          lon: position.coords.longitude,
          alt: position.coords.altitude ?? 3270,
        };
        setUsingGps(true);
        sendPositionRef.current();
      },
      () => setUsingGps(false),
      { enableHighAccuracy: true, maximumAge: 4000, timeout: 8000 },
    );
    return () => navigator.geolocation.clearWatch(watch);
  }, []);

  useEffect(() => {
    if (!plate) {
      return;
    }
    let socket: WebSocket | null = null;
    let closed = false;
    let retry = 0;

    const connect = () => {
      const token = loadSession()?.token;
      if (!token) {
        return;
      }
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      socket = new WebSocket(
        `${protocol}//${window.location.host}/ws/driver/${encodeURIComponent(plate)}?token=${encodeURIComponent(token)}`,
      );
      socketRef.current = socket;
      socket.onopen = () => {
        setLink("conectado");
        sendPositionRef.current();
      };
      socket.onmessage = (event) => {
        const message = parseMessage(event.data);
        if (!message) {
          return;
        }
        if (message.type === "error" && typeof message.detail === "string") {
          setNotice(message.detail);
          setSending(false);
          return;
        }
        if (message.type === "eta" && typeof message.order_code === "string" && typeof message.eta === "string") {
          setEtas((current) => ({ ...current, [message.order_code as string]: message.eta as string }));
        }
        if (message.type === "route_update") {
          const reason = typeof message.reason === "string" ? message.reason : "ruta";
          setNotice(`Ruta recalculada (${reason}).`);
          setSending(false);
          void loadRoute(plate);
        }
        if (message.type === "order_status") {
          setSending(false);
          void loadRoute(plate);
        }
      };
      socket.onclose = () => {
        if (closed) {
          return;
        }
        setLink("reconectando");
        window.setTimeout(connect, Math.min(5000, 1000 + retry));
        retry += 1000;
      };
    };

    connect();
    return () => {
      closed = true;
      socket?.close();
      socketRef.current = null;
    };
  }, [plate, loadRoute]);

  function publishIncident(id: (typeof INCIDENTS)[number]["id"]) {
    const socket = socketRef.current;
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      setNotice("Sin enlace con el despacho. Reintenta en un momento.");
      return;
    }
    const here = coordsRef.current ?? coordsFromStop(nextRef.current);
    if (!here) {
      setNotice("Falta una coordenada para reportar el incidente.");
      return;
    }
    setSending(true);
    setNotice(null);
    socket.send(
      JSON.stringify({
        type: "position",
        lat: here.lat,
        lon: here.lon,
        altitud_msnm: here.alt,
        vehicle_id: vehicleRef.current?.id,
        order_code: nextRef.current?.codigo_pedido,
      }),
    );
    if (id === "absent") {
      const code = nextRef.current?.codigo_pedido;
      if (!code) {
        setSending(false);
        setNotice("No hay un cliente pendiente para marcar ausente.");
        return;
      }
      socket.send(JSON.stringify({ type: "cancel_order", order_code: code }));
      return;
    }
    socket.send(
      JSON.stringify({
        type: "incident",
        kind: id,
        lat: here.lat,
        lon: here.lon,
        radius_km: id === "traffic" ? 0.4 : 0.25,
        note: id === "traffic" ? "Tráfico denso" : "Vía bloqueada o lluvia",
      }),
    );
  }

  function confirmDelivery(stop: DriverStop) {
    const next = new Set(done);
    next.add(stopKey(stop));
    setDone(next);
    sessionStorage.setItem(DONE_KEY, JSON.stringify([...next]));
    setSigning(null);
    setNotice(`Entrega de ${stop.cliente_nombre ?? stop.codigo_pedido} registrada.`);
  }

  const progress = useMemo(() => {
    const deliveries = stops.filter((stop) => stop.tipo_parada === "delivery");
    const finished = deliveries.filter((stop) => done.has(stopKey(stop))).length;
    return { finished, total: deliveries.length };
  }, [stops, done]);

  return (
    <div className="min-h-screen bg-[#f6f3ec] text-stone-950">
      <StaffHeader title="Modo conductor" tone="field" />

      <main className="mx-auto flex max-w-lg flex-col gap-4 px-4 py-4 pb-8">
        <section className="flex gap-2 overflow-x-auto" aria-label="Vehículo">
          {vehicles.map((item) => (
            <button
              key={item.placa}
              type="button"
              aria-pressed={item.placa === plate}
              className={`min-h-14 shrink-0 rounded-2xl px-4 text-left ${
                item.placa === plate ? "bg-stone-950 text-white" : "bg-white text-stone-950 ring-1 ring-stone-300"
              }`}
              onClick={() => setPlate(item.placa)}
            >
              <span className="block text-base font-semibold">{item.placa}</span>
              <span className="block text-xs opacity-80">{fuelLabel(item.tipo_combustible)}</span>
            </button>
          ))}
        </section>

        <div className="flex flex-wrap gap-2 text-xs font-semibold">
          <span className={`rounded-full px-3 py-1 ${link === "conectado" ? "bg-emerald-100 text-emerald-950" : "bg-amber-100 text-amber-950"}`}>
            {link === "conectado" ? "Despacho en línea" : "Conectando con despacho"}
          </span>
          <span className="rounded-full bg-white px-3 py-1 text-stone-700 ring-1 ring-stone-200">
            {usingGps ? "GPS del teléfono" : "Sin GPS: se usa la parada"}
          </span>
          {progress.total > 0 ? (
            <span className="rounded-full bg-white px-3 py-1 text-stone-700 ring-1 ring-stone-200">
              {progress.finished} de {progress.total} entregas
            </span>
          ) : null}
        </div>
        {progress.total > 0 ? (
          <div className="h-2 overflow-hidden rounded-full bg-stone-200" aria-hidden="true">
            <div
              className="h-full rounded-full bg-[#14532d]"
              style={{ width: `${Math.round((progress.finished / progress.total) * 100)}%` }}
            />
          </div>
        ) : null}
        {notice ? <p className="rounded-2xl bg-emerald-50 px-4 py-3 text-sm text-emerald-950">{notice}</p> : null}
        {loadError ? <p className="rounded-2xl bg-amber-100 px-4 py-3 text-sm">{loadError}</p> : null}

        {nextDelivery ? (
          <NextStop
            stop={nextDelivery}
            eta={nextDelivery.codigo_pedido ? etas[nextDelivery.codigo_pedido] : null}
            onDeliver={() => setSigning(nextDelivery)}
          />
        ) : (
          <section className="rounded-3xl bg-white p-5 ring-1 ring-stone-200">
            <h2 className="text-2xl font-semibold">Ruta al día</h2>
            <p className="mt-2 text-stone-600">
              {stops.length === 0
                ? "Cuando el despacho optimice, las paradas aparecen aquí."
                : "No quedan entregas pendientes en este vehículo."}
            </p>
          </section>
        )}

        <section aria-label="Itinerario">
          <div className="mb-2 flex items-baseline justify-between">
            <h2 className="text-lg font-semibold">Itinerario</h2>
            <p className="text-sm text-stone-600">
              {progress.finished}/{progress.total} entregas
            </p>
          </div>
          <ol className="flex flex-col gap-2">
            {stops.map((stop) => (
              <StopRow key={stopKey(stop)} stop={stop} done={done.has(stopKey(stop))} />
            ))}
          </ol>
        </section>

        <section className="grid grid-cols-1 gap-2" aria-label="Imprevistos">
          <h2 className="text-lg font-semibold">Si la ruta cambia</h2>
          <p className="text-sm text-stone-600">El despacho recalcula lo que todavía no entregaste.</p>
          {INCIDENTS.map((incident) => (
            <button
              key={incident.id}
              type="button"
              disabled={sending || (incident.id === "absent" && !nextDelivery)}
              className={`min-h-16 rounded-2xl px-4 text-lg font-semibold disabled:opacity-40 ${incident.className}`}
              onClick={() => publishIncident(incident.id)}
            >
              {incident.label}
            </button>
          ))}
        </section>
      </main>

      {signing ? (
        <DeliveryModal stop={signing} onClose={() => setSigning(null)} onConfirm={() => confirmDelivery(signing)} />
      ) : null}
    </div>
  );
}

function NextStop({ stop, eta, onDeliver }: { stop: DriverStop; eta: string | null | undefined; onDeliver: () => void }) {
  const maps = `https://www.google.com/maps/dir/?api=1&destination=${stop.lat},${stop.lon}&travelmode=driving`;
  const waze = `https://www.waze.com/ul?ll=${stop.lat},${stop.lon}&navigate=yes`;
  return (
    <section className="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-stone-200">
      <p className="text-xs font-semibold tracking-[0.14em] text-emerald-900">PRÓXIMO CLIENTE</p>
      <h2 className="mt-1 text-3xl font-semibold leading-tight">{stop.cliente_nombre}</h2>
      <p className="mt-2 text-lg">{stop.direccion_referencia}</p>
      <dl className="mt-4 grid grid-cols-2 gap-3 text-sm">
        <div>
          <dt className="text-stone-500">Ventana</dt>
          <dd className="text-base font-semibold">{formatWindow(stop.ventana_inicio, stop.ventana_fin)}</dd>
        </div>
        <div>
          <dt className="text-stone-500">Peso</dt>
          <dd className="text-base font-semibold">{stop.peso_kg === null ? "—" : formatKg(stop.peso_kg)}</dd>
        </div>
        <div>
          <dt className="text-stone-500">Llegada</dt>
          <dd className="text-base font-semibold">{formatTime(eta ?? stop.eta)}</dd>
        </div>
        <div>
          <dt className="text-stone-500">Pedido</dt>
          <dd className="text-base font-semibold">{stop.codigo_pedido}</dd>
        </div>
      </dl>
      <div className="mt-4 grid grid-cols-2 gap-3">
        <a className="flex min-h-14 items-center justify-center rounded-2xl bg-[#14532d] text-center text-base font-semibold text-white" href={maps} target="_blank" rel="noreferrer">
          Google Maps
        </a>
        <a className="flex min-h-14 items-center justify-center rounded-2xl bg-[#33ccff] text-center text-base font-semibold text-stone-950" href={waze} target="_blank" rel="noreferrer">
          Waze
        </a>
      </div>
      <button type="button" className="mt-3 min-h-16 w-full rounded-2xl bg-stone-950 text-lg font-semibold text-white" onClick={onDeliver}>
        Confirmar entrega
      </button>
    </section>
  );
}

function StopRow({ stop, done }: { stop: DriverStop; done: boolean }) {
  const title = stop.tipo_parada === "delivery" ? stop.cliente_nombre : stop.tipo_parada === "depot_start" ? "Salida del depósito" : "Retorno al depósito";
  return (
    <li className={`rounded-2xl px-4 py-3 ring-1 ring-stone-200 ${done ? "bg-emerald-50 text-stone-500" : "bg-white"}`}>
      <div className="flex items-start gap-3">
        <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-stone-950 text-sm font-semibold text-white">
          {stop.secuencia}
        </span>
        <div>
          <p className="font-semibold">{title}</p>
          <p className="text-sm">{stop.direccion_referencia ?? "Depósito El Tambo"}</p>
          {stop.tipo_parada === "delivery" ? (
            <p className="text-sm text-stone-600">
              {formatWindow(stop.ventana_inicio, stop.ventana_fin)}
              {stop.peso_kg !== null ? ` · ${formatKg(stop.peso_kg)}` : ""}
              {done ? " · Entregado" : ""}
            </p>
          ) : null}
        </div>
      </div>
    </li>
  );
}

function DeliveryModal({
  stop,
  onClose,
  onConfirm,
}: {
  stop: DriverStop;
  onClose: () => void;
  onConfirm: () => void;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const drawing = useRef(false);
  const [ink, setInk] = useState(false);
  const [photoName, setPhotoName] = useState<string | null>(null);

  function pointer(event: PointerEvent<HTMLCanvasElement>) {
    const canvas = canvasRef.current;
    if (!canvas) {
      return { x: 0, y: 0 };
    }
    const rect = canvas.getBoundingClientRect();
    return {
      x: ((event.clientX - rect.left) / rect.width) * canvas.width,
      y: ((event.clientY - rect.top) / rect.height) * canvas.height,
    };
  }

  function startDraw(event: PointerEvent<HTMLCanvasElement>) {
    const canvas = canvasRef.current;
    const context = canvas?.getContext("2d");
    if (!canvas || !context) {
      return;
    }
    canvas.setPointerCapture(event.pointerId);
    const point = pointer(event);
    context.strokeStyle = "#14532d";
    context.lineWidth = 4;
    context.lineCap = "round";
    context.beginPath();
    context.moveTo(point.x, point.y);
    drawing.current = true;
    setInk(true);
  }

  function draw(event: PointerEvent<HTMLCanvasElement>) {
    if (!drawing.current) {
      return;
    }
    const context = canvasRef.current?.getContext("2d");
    if (!context) {
      return;
    }
    const point = pointer(event);
    context.lineTo(point.x, point.y);
    context.stroke();
  }

  function clearCanvas() {
    const canvas = canvasRef.current;
    const context = canvas?.getContext("2d");
    if (!canvas || !context) {
      return;
    }
    context.clearRect(0, 0, canvas.width, canvas.height);
    setInk(false);
  }

  return (
    <div className="fixed inset-0 z-20 flex items-end justify-center bg-stone-950/70 sm:items-center">
      <div className="max-h-[100dvh] w-full max-w-lg overflow-y-auto rounded-t-3xl bg-[#f6f3ec] p-4 sm:rounded-3xl" role="dialog" aria-modal="true" aria-labelledby="firma-titulo">
        <h2 id="firma-titulo" className="text-2xl font-semibold">Firma de entrega</h2>
        <p className="mt-1 text-stone-600">{stop.cliente_nombre} · {stop.codigo_pedido}</p>
        <p className="mt-1 text-sm text-stone-500">Firma con el dedo o adjunta una foto. Con una de las dos basta.</p>
        <canvas
          ref={canvasRef}
          width={640}
          height={280}
          className="mt-4 h-44 w-full touch-none rounded-2xl bg-white ring-1 ring-stone-300"
          onPointerDown={startDraw}
          onPointerMove={draw}
          onPointerUp={() => {
            drawing.current = false;
          }}
          onPointerCancel={() => {
            drawing.current = false;
          }}
        />
        <div className="mt-3 flex gap-3">
          <button type="button" className="min-h-12 flex-1 rounded-2xl bg-white ring-1 ring-stone-300" onClick={clearCanvas}>
            Borrar firma
          </button>
          <label className="flex min-h-12 flex-1 cursor-pointer items-center justify-center rounded-2xl bg-white text-center ring-1 ring-stone-300">
            {photoName ?? "Foto del comprobante"}
            <input
              className="sr-only"
              type="file"
              accept="image/*"
              capture="environment"
              onChange={(event) => setPhotoName(event.target.files?.[0]?.name ?? null)}
            />
          </label>
        </div>
        <button
          type="button"
          disabled={!ink && !photoName}
          className="mt-3 min-h-16 w-full rounded-2xl bg-[#14532d] text-lg font-semibold text-white disabled:opacity-40"
          onClick={onConfirm}
        >
          Registrar entrega
        </button>
        <button type="button" className="mt-2 min-h-12 w-full text-stone-600" onClick={onClose}>
          Cancelar
        </button>
      </div>
    </div>
  );
}

function coordsFromStop(stop: DriverStop | null): Coords | null {
  if (!stop) {
    return null;
  }
  return { lat: stop.lat, lon: stop.lon, alt: 3270 };
}

function stopKey(stop: DriverStop): string {
  return `${stop.placa}:${stop.secuencia}:${stop.codigo_pedido ?? stop.tipo_parada}`;
}

function readDone(): Set<string> {
  try {
    const raw = sessionStorage.getItem(DONE_KEY);
    const parsed = raw ? (JSON.parse(raw) as unknown) : [];
    return new Set(Array.isArray(parsed) ? parsed.filter((item) => typeof item === "string") : []);
  } catch {
    return new Set();
  }
}

function parseMessage(raw: unknown): Record<string, unknown> | null {
  if (typeof raw !== "string") {
    return null;
  }
  try {
    const message = JSON.parse(raw) as unknown;
    if (!message || typeof message !== "object") {
      return null;
    }
    return message as Record<string, unknown>;
  } catch {
    return null;
  }
}
