import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import Map from "@/components/Map";

// Dynamically import Map to avoid SSR issues with Leaflet
// const Map = dynamic(() => import("@/components/Map"), { ssr: false });

export default function AirPollutionPage() {
  const [selectedCity, setSelectedCity] = useState<string | null>(null);

  const handleStationSelect = (cityName: string) => {
    setSelectedCity(cityName);
  };

  return (
    <div className="flex h-screen w-screen flex-col md:flex-row bg-background overflow-hidden">
      {/* Left Sidebar */}
      <aside className="w-full md:w-[400px] h-[40vh] md:h-full shrink-0 z-10 shadow-lg order-2 md:order-1">
        <Sidebar selectedCity={selectedCity} />
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
