import L from "leaflet";
import { useEffect, useMemo } from "react";
import { MapContainer, Marker, Polyline, Popup, TileLayer, useMap } from "react-leaflet";
import { formatCo2, formatWindow, windowColor } from "../lib/format";
import { HUANCAYO_CENTER, ROUTE_COLORS, type Depot, type Order, type RouteFeature, type RouteOptimization } from "../types";

type MapProps = {
  depot: Depot | null;
  orders: Order[];
  solution: RouteOptimization | null;
};

type LatLng = [number, number];

function pinIcon(color: string, warehouse: boolean): L.DivIcon {
  const mark = warehouse
    ? `<svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true">
        <path d="M14 2 3 9v15h7v-7h8v7h7V9Z" fill="#14532d" stroke="#fff" stroke-width="1.5"/>
      </svg>`
    : `<span style="display:block;width:18px;height:18px;border-radius:999px;background:${color};border:2px solid #fff;box-shadow:0 1px 4px rgba(28,25,23,.45)"></span>`;
  return L.divIcon({
    className: "eco-pin",
    html: mark,
    iconSize: warehouse ? [28, 28] : [18, 18],
    iconAnchor: warehouse ? [14, 26] : [9, 9],
    popupAnchor: [0, warehouse ? -24 : -12],
  });
}

function toLatLng(coordinates: [number, number]): LatLng {
  return [coordinates[1], coordinates[0]];
}

function colorForPlate(plate: string, plates: string[]): string {
  const index = Math.max(0, plates.indexOf(plate));
  return ROUTE_COLORS[index % ROUTE_COLORS.length] ?? ROUTE_COLORS[0];
}

function FitTo({ boundsKey, positions }: { boundsKey: string; positions: LatLng[] }) {
  const map = useMap();
  useEffect(() => {
    if (positions.length === 0) {
      map.setView(HUANCAYO_CENTER, 13);
      return;
    }
    if (positions.length === 1) {
      map.setView(positions[0], 14);
      return;
    }
    map.fitBounds(positions, { padding: [40, 40], maxZoom: 14 });
  }, [boundsKey, map, positions]);
  return null;
}

function pointFeatures(solution: RouteOptimization | null): RouteFeature[] {
  if (!solution) {
    return [];
  }
  return solution.features.filter((feature) => feature.geometry.type === "Point");
}

function lineFeatures(solution: RouteOptimization | null): RouteFeature[] {
  if (!solution) {
    return [];
  }
  return solution.features.filter((feature) => feature.geometry.type === "LineString");
}

export function MapView({ depot, orders, solution }: MapProps) {
  const lines = lineFeatures(solution);
  const points = pointFeatures(solution);
  const plates = useMemo(() => {
    const found = new Set<string>();
    for (const feature of solution?.features ?? []) {
      if (feature.properties.plate) {
        found.add(feature.properties.plate);
      }
    }
    return [...found].sort();
  }, [solution]);

  const positions = useMemo(() => {
    const next: LatLng[] = [];
    if (depot) {
      next.push(toLatLng(depot.ubicacion.coordinates));
    }
    if (solution) {
      for (const feature of points) {
        if (feature.geometry.type === "Point") {
          next.push(toLatLng(feature.geometry.coordinates));
        }
      }
      return next;
    }
    for (const order of orders) {
      next.push(toLatLng(order.ubicacion.coordinates));
    }
    return next;
  }, [depot, orders, points, solution]);

  const boundsKey = positions.map((pair) => pair.join(",")).join("|");

  return (
    <div className="relative h-full min-h-[420px] w-full">
      <MapContainer center={HUANCAYO_CENTER} zoom={13} className="h-full w-full" scrollWheelZoom>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <FitTo boundsKey={boundsKey} positions={positions} />
        {depot ? (
          <Marker position={toLatLng(depot.ubicacion.coordinates)} icon={pinIcon("#14532d", true)}>
            <Popup>
              <div className="text-sm text-stone-800">
                <p className="font-semibold">{depot.nombre}</p>
                <p>{depot.direccion}</p>
                <p className="text-stone-500">{Math.round(depot.altitud_msnm)} m s. n. m.</p>
              </div>
            </Popup>
          </Marker>
        ) : null}
        {solution
          ? points.map((feature) => {
              if (feature.geometry.type !== "Point" || feature.properties.stop_type !== "delivery") {
                return null;
              }
              const plate = feature.properties.plate ?? "";
              const [lon, lat] = feature.geometry.coordinates;
              return (
                <Marker
                  key={`${plate}-${feature.properties.sequence}-${feature.properties.order_code}`}
                  position={[lat, lon]}
                  icon={pinIcon(windowColor(feature.properties.window_start), false)}
                >
                  <Popup>
                    <DeliveryPopup
                      customer={feature.properties.customer ?? "Cliente"}
                      address={feature.properties.title ?? "Sin referencia"}
                      windowLabel={formatWindow(feature.properties.window_start, feature.properties.window_end)}
                      co2={formatCo2(feature.properties.co2_g ?? null)}
                      plate={plate}
                    />
                  </Popup>
                </Marker>
              );
            })
          : orders.map((order) => {
              const [lon, lat] = order.ubicacion.coordinates;
              return (
                <Marker
                  key={order.id}
                  position={[lat, lon]}
                  icon={pinIcon(windowColor(order.ventana_inicio), false)}
                >
                  <Popup>
                    <DeliveryPopup
                      customer={order.cliente_nombre}
                      address={order.direccion_referencia}
                      windowLabel={formatWindow(order.ventana_inicio, order.ventana_fin)}
                      co2={formatCo2(null)}
                      plate={null}
                    />
                  </Popup>
                </Marker>
              );
            })}
        {lines.map((feature) => {
          if (feature.geometry.type !== "LineString") {
            return null;
          }
          const plate = feature.properties.plate ?? "ruta";
          const positionsForLine = feature.geometry.coordinates.map(toLatLng);
          return (
            <Polyline
              key={`${plate}-${positionsForLine.map((pair) => pair.join(":")).join("|")}`}
              positions={positionsForLine}
              pathOptions={{ color: colorForPlate(plate, plates), weight: 5, opacity: 0.9 }}
            />
          );
        })}
      </MapContainer>
      <Legend plates={plates} />
    </div>
  );
}

function DeliveryPopup({
  customer,
  address,
  windowLabel,
  co2,
  plate,
}: {
  customer: string;
  address: string;
  windowLabel: string;
  co2: string;
  plate: string | null;
}) {
  return (
    <div className="min-w-44 space-y-1 text-sm text-stone-800">
      <p className="font-semibold">{customer}</p>
      <p>{address}</p>
      <p>Ventana: {windowLabel}</p>
      <p>CO2 estimado: {co2}</p>
      {plate ? <p className="text-stone-500">Vehículo {plate}</p> : null}
    </div>
  );
}

function Legend({ plates }: { plates: string[] }) {
  return (
    <div className="pointer-events-none absolute bottom-3 left-3 z-[500] max-w-xs rounded-xl bg-white/95 px-3 py-2 text-xs text-stone-700 shadow">
      <p className="mb-1 font-semibold text-stone-900">Ventanas</p>
      <ul className="space-y-1">
        <li className="flex items-center gap-2">
          <Dot color="#c2410c" /> Antes de las 9:00
        </li>
        <li className="flex items-center gap-2">
          <Dot color="#d97706" /> De 9:00 a 12:00
        </li>
        <li className="flex items-center gap-2">
          <Dot color="#4d7c0f" /> Después de las 12:00
        </li>
      </ul>
      {plates.length > 0 ? (
        <ul className="mt-2 space-y-1 border-t border-stone-200 pt-2">
          {plates.map((plate) => (
            <li key={plate} className="flex items-center gap-2">
              <span
                className="inline-block h-1.5 w-5 rounded"
                style={{ background: colorForPlate(plate, plates) }}
              />
              {plate}
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

function Dot({ color }: { color: string }) {
  return <span className="inline-block h-2.5 w-2.5 rounded-full" style={{ background: color }} />;
}
