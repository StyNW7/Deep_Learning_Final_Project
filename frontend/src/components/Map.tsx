import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useEffect } from "react";
import { cities } from "@/lib/city";

// Custom icon dengan fallback URL
const createCustomIcon = () => {
  // Coba beberapa URL sebagai fallback
  const iconUrls = {
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  };

  return L.icon({
    ...iconUrls,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });
};

const defaultIcon = createCustomIcon();

interface MapProps {
  onStationSelect: (cityName: string) => void;
  selectedCity: string | null;
}

function MapController({ selectedCity }: { selectedCity: string | null }) {
  const map = useMap();

  useEffect(() => {
    if (selectedCity) {
      const city = cities.find((c) => c.name === selectedCity);
      if (city) {
        map.flyTo([city.latitude, city.longitude], 13, { duration: 1.5 });
      }
    }
  }, [selectedCity, map]);

  return null;
}

export default function Map({ onStationSelect, selectedCity }: MapProps) {
  const SEOUL_CENTER: [number, number] = [37.5665, 126.978];

  return (
    <MapContainer
      center={SEOUL_CENTER}
      zoom={11}
      scrollWheelZoom={true}
      className="h-full w-full z-0"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <MapController selectedCity={selectedCity} />

      {cities.map((city, index) => (
        <Marker
          key={index}
          position={[city.latitude, city.longitude]}
          icon={defaultIcon}
          eventHandlers={{
            click: () => onStationSelect(city.name),
          }}
        >
          <Popup>
            <div className="text-center">
              <span className="font-bold">{city.name}</span>
              <br />
              <button
                className="text-xs text-primary underline mt-1"
                onClick={() => onStationSelect(city.name)}
              >
                View Analytics
              </button>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}