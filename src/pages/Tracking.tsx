import L from "leaflet";
import { useEffect, useMemo, useState } from "react";
import { MapContainer, Marker, TileLayer, useMap } from "react-leaflet";
import { fetchPublicTracking } from "../api";
import { Brand } from "../components/Brand";
import { homeFor } from "../lib/access";
import { formatCo2, formatTime, formatWindow, statusLabel } from "../lib/format";
import { loadSession } from "../lib/session";
import { HUANCAYO_CENTER, type PublicOrderTracking } from "../types";

type LiveFix = {
  lat: number;
  lon: number;
  eta: string | null;
  minutes: number | null;
};

type Channel = "whatsapp" | "sms";

const FIVE_MINUTES = 5;

export function Tracking() {
  const initialToken = tokenFromPath();
  const [draft, setDraft] = useState(initialToken);
  const [order, setOrder] = useState<PublicOrderTracking | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [live, setLive] = useState<LiveFix | null>(null);
  const [linked, setLinked] = useState(false);
  const [channels, setChannels] = useState<Record<Channel, boolean>>({ whatsapp: true, sms: false });
  const [alerts, setAlerts] = useState<Channel[]>([]);
  const [stopsBefore, setStopsBefore] = useState<number | null>(null);
  const [loading, setLoading] = useState(Boolean(initialToken));

  useEffect(() => {
    if (!initialToken) {
      return;
    }
    let active = true;
    fetchPublicTracking(initialToken)
      .then((card) => {
        if (active) {
          setOrder(card);
          setStopsBefore(card.paradas_previas);
          setError(null);
          setLoading(false);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setOrder(null);
          setError(reason instanceof Error ? reason.message : "No se pudo seguir ese pedido.");
          setLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [initialToken]);

  useEffect(() => {
    if (!initialToken) {
      return;
    }
    let socket: WebSocket | null = null;
    let closed = false;
    let retry = 0;

    const connect = () => {
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      socket = new WebSocket(
        `${protocol}//${window.location.host}/ws/tracking/${encodeURIComponent(initialToken)}`,
      );
      socket.onopen = () => setLinked(true);
      socket.onmessage = (event) => {
        const message = parseMessage(event.data);
        if (!message) {
          return;
        }
        if (typeof message.paradas_previas === "number") {
          setStopsBefore(message.paradas_previas);
        }
        if (typeof message.lat === "number" || typeof message.minutes === "number" || typeof message.eta === "string") {
          setLive((current) => ({
            lat: typeof message.lat === "number" ? message.lat : (current?.lat ?? Number.NaN),
            lon: typeof message.lon === "number" ? message.lon : (current?.lon ?? Number.NaN),
            eta: typeof message.eta === "string" ? message.eta : (current?.eta ?? null),
            minutes: typeof message.minutes === "number" ? message.minutes : (current?.minutes ?? null),
          }));
        }
      };
      socket.onclose = () => {
        setLinked(false);
        if (!closed) {
          window.setTimeout(connect, Math.min(5000, 1000 + retry));
          retry += 1000;
        }
      };
    };

    connect();
    return () => {
      closed = true;
      socket?.close();
    };
  }, [initialToken]);

  useEffect(() => {
    const minutes = live?.minutes;
    if (minutes === null || minutes === undefined || minutes > FIVE_MINUTES || minutes < 0) {
      return;
    }
    const due = (Object.keys(channels) as Channel[]).filter((channel) => channels[channel]);
    setAlerts((current) => (current.length > 0 ? current : due));
  }, [live?.minutes, channels]);

  const etaLabel = live?.eta ?? order?.eta ?? null;
  const minutesLabel =
    live?.minutes !== null && live?.minutes !== undefined ? formatArrival(live.minutes) : "Esperando al repartidor";
  const session = loadSession();

  return (
    <div className="min-h-screen bg-[#f6f3ec] text-stone-950">
      <header className="border-b border-stone-200 bg-white px-4 py-3">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-3">
          <Brand title="Seguimiento de tu pedido" />
          <nav className="flex flex-wrap gap-2" aria-label="Seguimiento">
            <a className="inline-flex min-h-11 items-center rounded-full bg-emerald-50 px-3 text-sm font-semibold text-emerald-950" href="/seguimiento">
              Consultar otro pedido
            </a>
            {session ? (
              <a className="inline-flex min-h-11 items-center rounded-full bg-stone-100 px-3 text-sm font-semibold text-stone-800" href={homeFor(session.usuario.rol)}>
                Volver a mi panel
              </a>
            ) : null}
          </nav>
        </div>
      </header>

      <main className="mx-auto grid max-w-5xl gap-4 px-4 py-4 lg:grid-cols-[minmax(0,1fr)_360px]">
        <section className="overflow-hidden rounded-3xl bg-stone-200 ring-1 ring-stone-300 lg:min-h-[560px]">
          <div className="h-[46vh] min-h-[280px] lg:h-full">
            {order ? (
              <CustomerMap destination={[order.lat_aprox, order.lon_aprox]} driver={driverPoint(live)} />
            ) : (
              <div className="flex h-full items-center justify-center px-6 text-center text-stone-600">
                {loading ? "Buscando tu pedido…" : "Pega el enlace de seguimiento que te envió DistriRápido."}
              </div>
            )}
          </div>
        </section>

        <section className="flex flex-col gap-3">
          <form
            className="rounded-3xl bg-white p-4 ring-1 ring-stone-200"
            onSubmit={(event) => {
              event.preventDefault();
              const code = draft.trim();
              if (code) {
                window.location.assign(`/seguimiento/${encodeURIComponent(code)}`);
              }
            }}
          >
            <label className="text-sm font-medium" htmlFor="enlace">
              Enlace de seguimiento
            </label>
            <div className="mt-2 flex gap-2">
              <input
                id="enlace"
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
                placeholder="UUID del enlace seguro"
                className="min-h-12 flex-1 rounded-2xl border border-stone-300 px-3 text-lg"
              />
              <button type="submit" className="min-h-12 rounded-2xl bg-[#14532d] px-4 font-semibold text-white">
                Ver
              </button>
            </div>
          </form>

          {error ? <p className="rounded-2xl bg-amber-100 px-4 py-3 text-sm" role="alert">{error}</p> : null}

          {order ? (
            <>
              <article className="rounded-3xl bg-white p-4 ring-1 ring-stone-200">
                <p className="text-xs tracking-[0.14em] text-emerald-900">LLEGADA</p>
                <p className="mt-1 text-3xl font-semibold">{minutesLabel}</p>
                <p className="mt-1 text-stone-600">
                  {etaLabel ? `Hora estimada ${formatTime(etaLabel)}` : "La hora se confirma cuando el vehículo sale."}
                </p>
                <div className="mt-3 flex flex-wrap items-center gap-2">
                  <p className="text-lg font-medium">{order.zona_entrega}</p>
                  <span className="rounded-full bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-950">
                    {statusLabel(order.estado)}
                  </span>
                  <span className={`rounded-full px-2 py-1 text-xs font-semibold ${linked ? "bg-emerald-800 text-white" : "bg-stone-200 text-stone-700"}`}>
                    {linked ? "En vivo" : "Conectando"}
                  </span>
                </div>
                <p className="mt-2 text-sm text-stone-600">
                  Ventana {formatWindow(order.ventana_inicio, order.ventana_fin)}
                </p>
                <p className="mt-3 rounded-2xl bg-emerald-50 px-3 py-2 text-sm">
                  {(stopsBefore ?? order.paradas_previas) === 0
                    ? "Eres la siguiente entrega en la ruta eco-optimizada."
                    : `${stopsBefore ?? order.paradas_previas} ${(stopsBefore ?? order.paradas_previas) === 1 ? "parada previa" : "paradas previas"} antes de la tuya.`}
                </p>
              </article>

              <article className="rounded-3xl bg-[#14532d] p-4 text-white">
                <p className="text-xs tracking-[0.14em] text-emerald-100">TU HUELLA</p>
                <p className="mt-2 text-3xl font-semibold">{formatCo2(order.co2_evitado_kg * 1000)}</p>
                <p className="mt-1 text-emerald-50">
                  CO2 evitado en este pedido por ir en la ruta eco-optimizada, en lugar del reparto convencional.
                </p>
              </article>

              <article className="rounded-3xl bg-white p-4 ring-1 ring-stone-200">
                <p className="font-semibold">Aviso cuando falten 5 minutos</p>
                <p className="mt-1 text-sm text-stone-600">
                  Simulación local. No se envía un mensaje real de WhatsApp ni de SMS.
                </p>
                <div className="mt-3 grid grid-cols-2 gap-2">
                  <ChannelButton
                    label="WhatsApp"
                    pressed={channels.whatsapp}
                    onClick={() => setChannels((current) => ({ ...current, whatsapp: !current.whatsapp }))}
                  />
                  <ChannelButton
                    label="SMS"
                    pressed={channels.sms}
                    onClick={() => setChannels((current) => ({ ...current, sms: !current.sms }))}
                  />
                </div>
              </article>
            </>
          ) : null}
        </section>
      </main>

      {alerts.length > 0 && order ? (
        <div className="fixed inset-x-0 top-3 z-20 mx-auto flex max-w-md flex-col gap-2 px-3">
          {alerts.map((channel) => (
            <div
              key={channel}
              className={`rounded-2xl px-4 py-3 text-sm shadow-lg ${
                channel === "whatsapp" ? "bg-[#075e54] text-white" : "bg-stone-950 text-white"
              }`}
              role="status"
            >
              {channel === "whatsapp" ? "WhatsApp" : "SMS"} · Tu entrega está a menos de 5 minutos ({order.zona_entrega}).
              <button type="button" className="ml-2 font-semibold underline" onClick={() => setAlerts([])}>
                Cerrar
              </button>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

function CustomerMap({ destination, driver }: { destination: [number, number]; driver: [number, number] | null }) {
  const positions = driver ? [destination, driver] : [destination];
  const destinationIcon = useMemo(() => pin("#14532d"), []);
  const driverIcon = useMemo(() => pin("#0f766e"), []);
  return (
    <div className="relative h-full">
    <MapContainer
      center={destination}
      zoom={14}
      zoomControl={false}
      scrollWheelZoom={false}
      className="h-full w-full"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <FitTo positions={positions} />
      <Marker position={destination} icon={destinationIcon} />
      {driver ? <Marker position={driver} icon={driverIcon} /> : null}
    </MapContainer>
    <div className="pointer-events-none absolute bottom-3 left-3 z-[500] rounded-2xl bg-white/95 px-3 py-2 text-xs text-stone-700 shadow ring-1 ring-stone-200">
      <p className="flex items-center gap-2">
        <span className="inline-block h-2.5 w-2.5 rounded-full bg-[#14532d]" /> Destino
      </p>
      {driver ? (
        <p className="mt-1 flex items-center gap-2">
          <span className="inline-block h-2.5 w-2.5 rounded-full bg-[#0f766e]" /> Repartidor
        </p>
      ) : null}
      {driver ? <p className="mt-1 text-stone-500">La posición del repartidor no representa un recorrido vial.</p> : null}
    </div>
    </div>
  );
}

function FitTo({ positions }: { positions: [number, number][] }) {
  const map = useMap();
  const key = positions.map((position) => position.join(",")).join("|");
  useEffect(() => {
    const points = key.split("|").map((pair) => pair.split(",").map(Number) as [number, number]);
    if (points.length === 1) {
      map.setView(points[0] ?? HUANCAYO_CENTER, 15);
      return;
    }
    map.fitBounds(points, { padding: [36, 36], maxZoom: 15 });
  }, [key, map]);
  return null;
}

function ChannelButton({ label, pressed, onClick }: { label: string; pressed: boolean; onClick: () => void }) {
  return (
    <button
      type="button"
      aria-pressed={pressed}
      className={`min-h-12 rounded-2xl font-semibold ${pressed ? "bg-[#14532d] text-white" : "bg-stone-100 text-stone-700"}`}
      onClick={onClick}
    >
      {pressed ? "Activo · " : "Apagado · "}
      {label}
    </button>
  );
}

function pin(color: string): L.DivIcon {
  return L.divIcon({
    className: "eco-pin",
    html: `<span style="display:block;width:18px;height:18px;border-radius:999px;background:${color};border:3px solid #fff;box-shadow:0 1px 4px rgba(28,25,23,.4)"></span>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });
}

function driverPoint(live: LiveFix | null): [number, number] | null {
  if (!live || Number.isNaN(live.lat) || Number.isNaN(live.lon)) {
    return null;
  }
  return [live.lat, live.lon];
}

function formatArrival(minutes: number): string {
  if (minutes < 1) {
    return "Llegando ahora";
  }
  const rounded = Math.max(1, Math.round(minutes));
  return rounded === 1 ? "En 1 minuto" : `En ${rounded} minutos`;
}

const TOKEN_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function tokenFromPath(): string {
  const parts = window.location.pathname.split("/").filter(Boolean);
  if (parts[0] === "seguimiento" && parts[1]) {
    const candidate = decodeURIComponent(parts[1]);
    return TOKEN_RE.test(candidate) ? candidate : "";
  }
  return "";
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
