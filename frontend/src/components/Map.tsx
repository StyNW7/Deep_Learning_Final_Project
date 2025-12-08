import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
// import L from "leaflet";
import { useEffect } from "react";
import { cities } from "@/lib/city";

// Leaflet Icon Fix for React
// import icon from "leaflet/dist/images/marker-icon.png";
// import iconShadow from "leaflet/dist/images/marker-shadow.png";

// const DefaultIcon = L.icon({
//   iconUrl: typeof icon === "string" ? icon : (icon as any).src,
//   shadowUrl:
//     typeof iconShadow === "string" ? iconShadow : (iconShadow as any).src,
//   iconSize: [25, 41],
//   iconAnchor: [12, 41],
// });

// L.Marker.prototype.options.icon = DefaultIcon;

interface MapProps {
  onStationSelect: (cityName: string) => void;
  selectedCity: string | null;
}

// Component to handle flying to selected city
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
  // Center on Seoul by default
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
