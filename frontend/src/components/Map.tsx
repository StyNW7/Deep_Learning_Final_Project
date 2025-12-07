import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { cities } from "@/lib/city";

function Map() {
  return (
    <MapContainer
      center={[cities[0].latitude, cities[0].longitude]}
      zoom={12}
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {cities.map((city, index) => {
        return (
          <Marker key={index} position={[city.latitude, city.longitude]}>
            <Popup>{city.name}</Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}

export default Map;
