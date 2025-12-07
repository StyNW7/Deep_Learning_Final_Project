import { JAKARTA_CITIES } from "@/services/cityService";
import { MapPin, Wind } from "lucide-react";

export const CityList = ({
  onSelectCity,
}: {
  onSelectCity: (city: string) => void;
}) => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6">
      <div className="max-w-3xl w-full space-y-8">
        <div className="text-center space-y-4">
          <div className="inline-flex items-center justify-center p-3 bg-blue-100 rounded-full mb-4">
            <Wind className="w-8 h-8 text-blue-600" />
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight">
            Jakarta Air Monitor
          </h1>
          <p className="text-lg text-slate-600 max-w-xl mx-auto">
            Real-time air quality metrics, pollutant breakdowns, and health
            forecasts for every district in Jakarta.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {JAKARTA_CITIES.map((city) => (
            <button
              key={city}
              onClick={() => onSelectCity(city)}
              className="group relative flex items-center p-6 bg-white rounded-xl shadow-sm border border-slate-200 hover:border-blue-400 hover:shadow-md transition-all duration-200 text-left"
            >
              <div className="mr-4 bg-slate-100 p-3 rounded-full group-hover:bg-blue-50 transition-colors">
                <MapPin className="w-6 h-6 text-slate-500 group-hover:text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900">{city}</h3>
                <span className="text-xs text-slate-500">
                  View Dashboard &rarr;
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
