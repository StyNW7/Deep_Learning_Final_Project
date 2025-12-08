import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import type { AirStationData } from "@/lib/types";
import Map from "@/components/Map";

// Dynamically import Map to avoid SSR issues with Leaflet
// const Map = dynamic(() => import("@/components/Map"), { ssr: false });

export default function AirPollutionPage() {
  const [selectedCity, setSelectedCity] = useState<string | null>(null);
  const [stationData, setStationData] = useState<AirStationData | null>(null);

  // Mock function to simulate fetching data
  const handleStationSelect = (cityName: string) => {
    setSelectedCity(cityName);

    // Replace this with your actual API call logic
    const mockData: AirStationData = {
      city: cityName,
      co: 0.5,
      no2: 0.03,
      o3: 0.04,
      pm10: Math.floor(Math.random() * 50) + 20, // Random values for demo
      pm25: Math.floor(Math.random() * 30) + 10,
      so2: 0.005,
      forecastPm25: Math.floor(Math.random() * 40) + 10,
    };

    setStationData(mockData);
  };

  return (
    <div className="flex h-screen w-screen flex-col md:flex-row bg-background overflow-hidden">
      {/* Left Sidebar */}
      <aside className="w-full md:w-[400px] h-[40vh] md:h-full shrink-0 z-10 shadow-lg order-2 md:order-1">
        <Sidebar data={stationData} />
      </aside>

      {/* Main Map Area */}
      <main className="flex-1 h-[60vh] md:h-full relative order-1 md:order-2">
        <Map
          onStationSelect={handleStationSelect}
          selectedCity={selectedCity}
        />

        {/* Floating Overlay Title */}
        <div className="absolute bottom-4 left-4 z-500 pointer-events-none">
          <div className="bg-background/90 backdrop-blur border shadow-sm rounded-md px-4 py-2 pointer-events-auto">
            <h1 className="font-bold text-sm">Seoul Pollution Forecast</h1>
          </div>
        </div>
      </main>
    </div>
  );
}
