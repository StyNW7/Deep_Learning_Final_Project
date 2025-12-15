/* eslint-disable @typescript-eslint/no-unused-vars */
import { useState, useEffect } from "react";
import {
  ArrowLeft,
  Wind,
  TrendingUp,
  AlertCircle,
  Calendar,
  Clock,
  Activity,
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Bar,
  ReferenceLine,
  BarChart,
} from "recharts";
import { getRecommendations } from "@/lib/recommendation";
import type {
  APIResponse,
  ForecastDetailResponse,
  IAQI,
  MultistepForecastResponse,
  PollutantType,
} from "@/lib/types";
import {
  fetchAirQuality,
  fetchForecastDetail,
  fetchMultistepForecast,
} from "@/services/cityService";
import PollutantCard from "@/components/cityDetail/PollutantCard";
import { useParams } from "react-router";
import { POLLUTANT_THRESHOLDS } from "@/lib/color";
import { convertToPPM } from "@/lib/unit";

interface RadarDataPoint {
  pollutant: string;
  current: number;
  safe: number;
}

const SELECTED_POLLUTANTS = ["co", "no2", "o3", "so2"] as const;

function iaqiToRadarDataPoints(iaqi: IAQI): RadarDataPoint[] {
  return SELECTED_POLLUTANTS.map((pollutant) => ({
    pollutant,
    current:
      convertToPPM(iaqi[pollutant].v, pollutant.toUpperCase()) /
      POLLUTANT_THRESHOLDS[pollutant.toUpperCase() as PollutantType].normal * 100,
    safe: POLLUTANT_THRESHOLDS[pollutant.toUpperCase() as PollutantType].normal,
  }));
}

const CityDetailPage = () => {
  const { cityName } = useParams<{ cityName: string }>();

  const [isLoading, setIsLoading] = useState(true);

  const [currentData, setCurrentData] = useState<APIResponse | null>(null);
  const [forecastDetailData, setForecastDetailData] =
    useState<ForecastDetailResponse | null>(null);
  const [multistepForecastData, setMultistepForecastData] = useState<
    MultistepForecastResponse[]
  >([]);

  useEffect(() => {
    let isCancelled = false;

    const fetchData = async () => {
      setIsLoading(true);

      if (!cityName) {
        setForecastDetailData(null);
        setIsLoading(false);
        return;
      }

      try {
        const [currentResult, multistepForecast, forecastResult] =
          await Promise.all([
            fetchAirQuality(cityName),
            fetchMultistepForecast(cityName),
            fetchForecastDetail(cityName),
          ]);
        if (!isCancelled) {
          setCurrentData(currentResult);
          setForecastDetailData(forecastResult);
          setMultistepForecastData(multistepForecast);
        }
      } finally {
        if (!isCancelled) {
          setIsLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      isCancelled = true;
    };
  }, [cityName]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-black border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading city data...</p>
        </div>
      </div>
    );
  }

  if (!forecastDetailData || !currentData) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">No data available</p>
        </div>
      </div>
    );
  }

  const radarData = iaqiToRadarDataPoints(currentData?.data.iaqi);

  const recommendation = getRecommendations(
    forecastDetailData.dominant_pollutant
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => window.history.back()}
              className="flex items-center space-x-2 text-gray-600 hover:text-black transition-colors group"
            >
              <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
              <span>Back to Map</span>
            </button>
            <div className="flex items-center space-x-2">
              <Wind className="w-5 h-5" />
              <span className="font-bold">AeroSeoul</span>
            </div>
          </div>
        </div>
      </header>

      {/* City Header */}
      <div className="relative h-64 overflow-hidden animate-fadeIn">
        <img
          src="https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=800"
          alt={cityName}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-linear-to-t from-black/60 to-transparent"></div>
        <div className="absolute bottom-0 left-0 right-0 p-8">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-2 animate-slideUp">
              {cityName}
            </h1>
            <p
              className="text-white/90 flex items-center space-x-2 animate-slideUp"
              style={{ animationDelay: "0.1s" }}
            >
              <Clock className="w-4 h-4" />
              <span>Updated: {currentData.data.time.s}</span>
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Dominant Pollutant Alert */}
        <div
          className={`${recommendation.color} border-2 rounded-2xl p-6 mb-8 animate-slideUp`}
          style={{ animationDelay: "0.1s" }}
        >
          <div className="flex items-start space-x-4">
            <div className="bg-white rounded-full p-3 shadow-sm">
              <AlertCircle className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-bold mb-2">
                Dominant Pollutant: {forecastDetailData.dominant_pollutant}
              </h3>
              <div className="grid md:grid-cols-3 gap-4 mt-4">
                {recommendation.activities.map((activity, idx) => (
                  <div
                    key={idx}
                    className="flex items-center space-x-2 bg-white rounded-lg p-3 shadow-sm"
                  >
                    <span className="text-2xl">{activity.icon}</span>
                    <span className="text-sm">{activity.text}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Bento Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 8-Hour Forecast - Large Card */}
          <div
            className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-black transition-all duration-300 animate-slideUp"
            style={{ animationDelay: "0.2s" }}
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-2">
                <Calendar className="w-5 h-5" />
                <h2 className="text-xl font-bold">6-Hour Forecast</h2>
              </div>
              <span className="text-sm text-gray-500">Air Quality Index</span>
            </div>

            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={multistepForecastData}>
                <defs>
                  <linearGradient id="aqiGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#000000" stopOpacity={0.1} />
                    <stop offset="95%" stopColor="#000000" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="hour24" stroke="#666" fontSize={12} />
                <YAxis stroke="#666" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "white",
                    border: "2px solid black",
                    borderRadius: "8px",
                    padding: "8px",
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="pm25"
                  stroke="#000000"
                  strokeWidth={2}
                  fill="url(#aqiGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>

            <div className="grid grid-cols-4 md:grid-cols-6 gap-2 mt-6">
              {multistepForecastData.map((hour, idx) => (
                <div
                  key={idx}
                  className="text-center p-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="text-xs text-gray-600 mb-1">
                    {hour.hour24}
                  </div>
                  <div className="font-bold text-lg">
                    {hour.pm25.toFixed(2)}
                  </div>
                  {/* <div className="text-xs text-gray-500 mt-1">{hour.dominant}</div> */}
                  <div className="text-xs text-gray-500 mt-1">PM2.5</div>
                </div>
              ))}
            </div>
          </div>

          {/* Pollutant Radar Chart */}
          <div
            className="bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-black transition-all duration-300 animate-slideUp"
            style={{ animationDelay: "0.3s" }}
          >
            <div className="flex items-center space-x-2 mb-6">
              <Activity className="w-5 h-5" />
              <h2 className="text-xl font-bold">Current Pollutant Levels</h2>
            </div>

            <div className="space-y-4">
              {radarData.map((p, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-sm">
                      {p.pollutant.toUpperCase()}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span
                        className={`text-sm font-bold ${
                          p.current > 100 ? "text-red-600" : "text-blue-600"
                        }`}
                      >
                        {p.current.toFixed(2)}%
                      </span>
                      {p.current > 100 && (
                        <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full">
                          Above Safe
                        </span>
                      )}
                      {p.current <= 100 && (
                        <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">
                          Safe
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="relative h-3 bg-gray-100 rounded-full overflow-hidden">
                    {/* Safe zone background */}
                    <div className="absolute inset-0 bg-green-50"></div>

                    {/* Danger zone (beyond 100%) */}
                    <div className="absolute left-[83.33%] right-0 h-full bg-red-50"></div>

                    {/* Safe limit marker line */}
                    <div className="absolute left-[83.33%] top-0 bottom-0 w-0.5 bg-gray-400 z-10"></div>

                    {/* Current level bar */}
                    <div
                      className={`absolute left-0 top-0 bottom-0 transition-all duration-500 ${
                        p.current > 100 ? "bg-red-500" : "bg-blue-500"
                      }`}
                      style={{ width: `${Math.min(p.current / 1.2, 100)}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-center space-x-6 mt-6 pt-4 border-t border-gray-100">
              <div className="flex items-center space-x-2 text-xs">
                <div className="w-4 h-3 bg-blue-500 rounded"></div>
                <span className="text-gray-600">Safe Level</span>
              </div>
              <div className="flex items-center space-x-2 text-xs">
                <div className="w-4 h-3 bg-red-500 rounded"></div>
                <span className="text-gray-600">Unsafe Level</span>
              </div>
              <div className="flex items-center space-x-2 text-xs">
                <div className="w-0.5 h-3 bg-gray-400"></div>
                <span className="text-gray-600">Safe Limit (100%)</span>
              </div>
            </div>
          </div>

          <div className="lg:col-span-3 grid grid-cols-2 md:grid-cols-3 gap-4">
            <PollutantCard
              idx={0}
              pollutant="CO"
              value={forecastDetailData.co_prediction}
            />
            <PollutantCard
              idx={1}
              pollutant="NO2"
              value={forecastDetailData.no2_prediction}
            />
            <PollutantCard
              idx={2}
              pollutant="O3"
              value={forecastDetailData.o3_prediction}
            />
            <PollutantCard
              idx={3}
              pollutant="SO2"
              value={forecastDetailData.so2_prediction}
            />
            <PollutantCard
              idx={4}
              pollutant="PM2.5"
              value={forecastDetailData.pm25_prediction}
            />
          </div>

          {/* Trend Insight Card */}
          <div
            className="lg:col-span-3 bg-gradient-to-br from-gray-50 to-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-black transition-all duration-300 animate-slideUp"
            style={{ animationDelay: "0.7s" }}
          >
            <div className="flex items-start space-x-4">
              <div className="bg-black text-white rounded-full p-3">
                <TrendingUp className="w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold mb-3">Air Quality Insights</h3>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="bg-white rounded-xl p-4 border border-gray-200">
                    <div className="text-sm text-gray-600 mb-1">
                      Overall Trend
                    </div>
                    <div className="text-lg font-bold">Improving</div>
                    <div className="text-xs text-green-600 mt-1">
                      ↓ 12% from yesterday
                    </div>
                  </div>
                  <div className="bg-white rounded-xl p-4 border border-gray-200">
                    <div className="text-sm text-gray-600 mb-1">
                      Best Time Today
                    </div>
                    <div className="text-lg font-bold">6:00 - 9:00 AM</div>
                    <div className="text-xs text-gray-500 mt-1">
                      Lowest pollution levels
                    </div>
                  </div>
                  <div className="bg-white rounded-xl p-4 border border-gray-200">
                    <div className="text-sm text-gray-600 mb-1">
                      Weekly Average
                    </div>
                    <div className="text-lg font-bold">Moderate</div>
                    <div className="text-xs text-gray-500 mt-1">
                      AQI: 65-85 range
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fadeIn {
          animation: fadeIn 0.6s ease-out forwards;
        }

        .animate-slideUp {
          animation: slideUp 0.6s ease-out forwards;
        }

        .animate-spin {
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default CityDetailPage;