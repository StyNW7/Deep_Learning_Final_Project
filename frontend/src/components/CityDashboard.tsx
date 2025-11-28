import type { AirQualityData, PollutantData, PollutantType } from "@/lib/types";
import { fetchCityData, getAQIColor, getAQIStatus, getPollutantAdvice } from "@/services/cityService";
import { Activity, ChevronLeft, Droplets, Info, Leaf, RefreshCw, ShieldAlert, Thermometer, Wind } from "lucide-react";
import { useEffect, useState } from "react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { Area, AreaChart, ResponsiveContainer, Tooltip } from "recharts";

export const CityDashboard = ({
  city,
  onBack,
}: {
  city: string;
  onBack: () => void;
}) => {
  const [data, setData] = useState<AirQualityData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    (async () => {
      if (mounted) setLoading(true);

      const result = await fetchCityData(city);

      if (mounted) {
        setData(result);
        setLoading(false);
      }
    })();

    return () => {
      mounted = false;
    };
  }, [city]);

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="animate-pulse flex flex-col items-center">
          <RefreshCw className="w-10 h-10 text-blue-500 animate-spin mb-4" />
          <p className="text-slate-500 font-medium">
            Analyzing Air Composition...
          </p>
        </div>
      </div>
    );
  }

  const statusColor = getAQIColor(data.currentAQI);
  const statusText = getAQIStatus(data.currentAQI);
  const tomorrow = data.forecast[0];
  const tomorrowPrimaryPollutant = tomorrow.primaryPollutant;

  return (
    <div className="min-h-screen bg-slate-50 pb-12">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-600"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
            <div>
              <h1 className="text-lg font-bold text-slate-900">{data.city}</h1>
              <p className="text-xs text-slate-500">
                Updated today at {data.lastUpdated}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm font-medium text-slate-600 bg-slate-100 px-3 py-1 rounded-full">
            <Thermometer className="w-4 h-4" />
            {data.temperature}°C
            <span className="mx-1 opacity-30">|</span>
            <Droplets className="w-4 h-4" />
            {data.humidity}%
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Top Section: Main AQI & Forecast */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Status Card */}
          <Card className="lg:col-span-2 p-6 flex flex-col md:flex-row items-center md:items-start gap-8">
            <div className="flex-1 space-y-4 w-full">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wide flex items-center gap-2">
                  <Activity className="w-4 h-4" /> Current Air Quality
                </h2>
                <Badge className={statusColor}>{statusText}</Badge>
              </div>

              <div className="flex items-baseline gap-2">
                <span
                  className={`text-6xl md:text-7xl font-bold tracking-tighter ${
                    statusColor.split(" ")[0]
                  }`}
                >
                  {data.currentAQI}
                </span>
                <span className="text-lg text-slate-400 font-medium">
                  US AQI
                </span>
              </div>

              <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden relative">
                <div
                  className={`h-full transition-all duration-1000 ease-out ${statusColor
                    .split(" ")[1]
                    .replace("bg-", "bg-")}`}
                  style={{
                    width: `${Math.min(data.currentAQI / 5, 100)}%`,
                    backgroundColor: "currentColor",
                  }}
                />
              </div>
              <p className="text-slate-600 text-sm">
                The air quality is <strong>{statusText.toLowerCase()}</strong>.
                {data.currentAQI > 100
                  ? " Sensitive groups should reduce outdoor exercise."
                  : " Ideal for outdoor activities."}
              </p>
            </div>

            {/* Mini Chart */}
            <div className="w-full md:w-64 h-48 bg-slate-50 rounded-lg border border-slate-100 p-4">
              <h3 className="text-xs font-semibold text-slate-400 mb-2">
                24h Trend
              </h3>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data.history}>
                  <defs>
                    <linearGradient id="colorAqi" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <Tooltip
                    contentStyle={{
                      borderRadius: "8px",
                      border: "none",
                      boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                    }}
                    itemStyle={{ fontSize: "12px" }}
                  />
                  <Area
                    type="monotone"
                    dataKey="aqi"
                    stroke="#6366f1"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorAqi)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>

          {/* Tomorrow Forecast Card */}
          <Card className="p-6 bg-slate-900 text-white border-slate-800 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-32 bg-blue-500 rounded-full blur-[80px] opacity-20 -mr-16 -mt-16 pointer-events-none"></div>

            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">
              Tomorrow's Forecast
            </h2>

            <div className="flex justify-between items-end mb-6">
              <div>
                <div className="text-4xl font-bold mb-1">{tomorrow.aqi}</div>
                <div
                  className={`text-sm font-medium px-2 py-0.5 rounded inline-block ${getAQIColor(
                    tomorrow.aqi
                  )}`}
                >
                  {getAQIStatus(tomorrow.aqi)}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-slate-400 mb-1">
                  Primary Pollutant
                </div>
                <div className="text-xl font-bold text-blue-400">
                  {tomorrowPrimaryPollutant}
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
                <div className="flex items-start gap-3">
                  <ShieldAlert className="w-5 h-5 text-yellow-400 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-300 uppercase mb-1">
                      Recommendation
                    </h4>
                    <p className="text-sm leading-relaxed text-slate-100">
                      {getPollutantAdvice(tomorrowPrimaryPollutant)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-center text-xs text-slate-400 mt-4">
                <div className="bg-white/5 p-2 rounded">
                  Wind: {Math.floor(0.3 * 20)} km/h
                </div>
                <div className="bg-white/5 p-2 rounded">
                  {/* Rain: {Math.random() > 0.7 ? "Likely" : "None"} */}
                  Rain: Likely
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Pollutants Grid */}
        <div>
          <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <Info className="w-5 h-5 text-slate-400" />
            Pollutant Breakdown
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {(
              Object.entries(data.pollutants) as [
                PollutantType,
                PollutantData
              ][]
            ).map(([key, info]) => (
              <Card
                key={key}
                className="p-4 flex flex-col justify-between hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="font-bold text-slate-700">{key}</span>
                  <div
                    className={`w-2 h-2 rounded-full ${
                      info.status === "Good"
                        ? "bg-green-500"
                        : info.status === "Moderate"
                        ? "bg-yellow-500"
                        : "bg-red-500"
                    }`}
                  />
                </div>
                <div>
                  <div className="text-2xl font-bold text-slate-900">
                    {info.value.toFixed(1)}
                  </div>
                  <div className="text-xs text-slate-500">{info.unit}</div>
                </div>
                <div className="mt-3 pt-3 border-t border-slate-100">
                  <span
                    className={`text-xs font-medium ${
                      info.status === "Good"
                        ? "text-green-600"
                        : info.status === "Moderate"
                        ? "text-yellow-600"
                        : "text-red-600"
                    }`}
                  >
                    {info.status}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Health Recommendations Section */}
        <div className="bg-blue-50 border border-blue-100 rounded-xl p-6">
          <div className="flex flex-col md:flex-row gap-6">
            <div className="md:w-1/3">
              <h3 className="text-lg font-bold text-blue-900 mb-2 flex items-center gap-2">
                <Leaf className="w-5 h-5" />
                Health Advice
              </h3>
              <p className="text-sm text-blue-700 leading-relaxed">
                Based on the current AQI of {data.currentAQI} and the forecasted
                high of {tomorrow.aqi}, here is what you should do to stay safe.
              </p>
            </div>
            <div className="md:w-2/3 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="flex items-start gap-3 bg-white p-4 rounded-lg shadow-sm">
                <div className="bg-green-100 p-2 rounded-full text-green-600">
                  <Wind className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-semibold text-slate-900 text-sm">
                    Ventilation
                  </h4>
                  <p className="text-xs text-slate-500 mt-1">
                    {data.currentAQI > 150
                      ? "Close windows to avoid outdoor pollutants entering."
                      : "It is safe to open windows for fresh air circulation."}
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3 bg-white p-4 rounded-lg shadow-sm">
                <div className="bg-rose-100 p-2 rounded-full text-rose-600">
                  <Activity className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-semibold text-slate-900 text-sm">
                    Exercise
                  </h4>
                  <p className="text-xs text-slate-500 mt-1">
                    {data.currentAQI > 100
                      ? "Consider indoor exercises. Avoid intense cardio outdoors."
                      : "Enjoy outdoor activities freely."}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
