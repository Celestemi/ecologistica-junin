import L from "leaflet";
import { MapContainer, Marker, TileLayer, useMapEvents } from "react-leaflet";
import { HUANCAYO_CENTER } from "../types";

type PinMapProps = {
  pin: [number, number] | null;
  onPick: (lat: number, lon: number) => void;
};

function ClickCatcher({ onPick }: { onPick: (lat: number, lon: number) => void }) {
  useMapEvents({
    click(event) {
      onPick(event.latlng.lat, event.latlng.lng);
    },
  });
  return null;
}

const pin = L.divIcon({
  className: "eco-pin",
  html: `<span style="display:block;width:18px;height:18px;border-radius:999px;background:#b45309;border:2px solid #fff;box-shadow:0 1px 4px rgba(28,25,23,.45)"></span>`,
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

export function PinMap({ pin: position, onPick }: PinMapProps) {
  return (
    <MapContainer
      center={HUANCAYO_CENTER}
      zoom={13}
      className="h-72 w-full rounded-2xl"
      zoomControl={false}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="© OpenStreetMap" />
      <ClickCatcher onPick={onPick} />
      {position ? <Marker position={position} icon={pin} /> : null}
    </MapContainer>
  );
}
