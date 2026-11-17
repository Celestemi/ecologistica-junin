import L from "leaflet";
import { useEffect } from "react";
import { MapContainer, Marker, TileLayer, useMap, useMapEvents } from "react-leaflet";
import { HUANCAYO_CENTER } from "../types";

type PinMapProps = {
  pin: [number, number] | null;
  onPick: (lat: number, lon: number) => void;
  enabled?: boolean;
};

function ClickCatcher({ onPick, enabled }: { onPick: (lat: number, lon: number) => void; enabled: boolean }) {
  useMapEvents({
    click(event) {
      if (enabled) onPick(event.latlng.lat, event.latlng.lng);
    },
  });
  return null;
}

function SyncMap({ position }: { position: [number, number] | null }) {
  const map = useMap();
  const lat = position?.[0];
  const lon = position?.[1];
  useEffect(() => {
    if (lat !== undefined && lon !== undefined) map.panTo([lat, lon], { animate: false });
  }, [map, lat, lon]);

  useEffect(() => {
    const container = map.getContainer();
    const resize = () => map.invalidateSize({ pan: false });
    resize();
    if (typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(resize);
    observer.observe(container);
    return () => observer.disconnect();
  }, [map]);
  return null;
}

const pin = L.divIcon({
  className: "eco-pin",
  html: `<span style="display:block;width:18px;height:18px;border-radius:999px;background:#b45309;border:2px solid #fff;box-shadow:0 1px 4px rgba(28,25,23,.45)"></span>`,
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

export function PinMap({ pin: position, onPick, enabled = true }: PinMapProps) {
  return (
    <MapContainer
      center={position ?? HUANCAYO_CENTER}
      zoom={13}
      className="h-72 w-full rounded-2xl"
      zoomControl
      keyboard
      aria-label="Mapa para elegir la ubicación del pedido"
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="© OpenStreetMap" />
      <SyncMap position={position} />
      <ClickCatcher onPick={onPick} enabled={enabled} />
      {position ? <Marker
        position={position}
        icon={pin}
        draggable={enabled}
        eventHandlers={{ dragend: (event) => {
          if (!enabled) return;
          const point = (event.target as L.Marker).getLatLng();
          onPick(point.lat, point.lng);
        } }}
        title="Ubicación seleccionada"
        alt="Ubicación seleccionada"
        keyboard
      /> : null}
    </MapContainer>
  );
}
