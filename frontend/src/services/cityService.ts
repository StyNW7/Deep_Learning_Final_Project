import type { AirQualityData, APIResponse, ForecastDetailResponse, ForecastResponse, PollutantType } from "@/lib/types";

export const JAKARTA_CITIES = [
  "Jakarta Pusat (Central)",
  "Jakarta Selatan (South)",
  "Jakarta Barat (West)",
  "Jakarta Timur (East)",
  "Jakarta Utara (North)",
  "Kepulauan Seribu",
];

export const getAQIColor = (aqi: number) => {
  if (aqi <= 50) return "text-green-500 bg-green-50 border-green-200";
  if (aqi <= 100) return "text-yellow-600 bg-yellow-50 border-yellow-200";
  if (aqi <= 150) return "text-orange-500 bg-orange-50 border-orange-200";
  if (aqi <= 200) return "text-red-500 bg-red-50 border-red-200";
  if (aqi <= 300) return "text-purple-500 bg-purple-50 border-purple-200";
  return "text-rose-900 bg-rose-100 border-rose-300";
};

export const getAQIStatus = (aqi: number) => {
  if (aqi <= 50) return "Good";
  if (aqi <= 100) return "Moderate";
  if (aqi <= 150) return "Unhealthy for Sensitive Groups";
  if (aqi <= 200) return "Unhealthy";
  if (aqi <= 300) return "Very Unhealthy";
  return "Hazardous";
};

export const getPollutantAdvice = (pollutant: PollutantType) => {
  switch (pollutant) {
    case "PM2.5":
      return "Particulates are fine enough to enter the bloodstream. Wear a N95 mask if outdoors and run an air purifier indoors.";
    case "PM10":
      return "Dust and pollen are high. Avoid outdoor exercise and keep windows closed.";
    case "O3":
      return "Ozone levels are high. Limit outdoor activity during the afternoon when sunlight is strongest.";
    case "NO2":
      return "High traffic pollution detected. Avoid walking near busy roads.";
    case "SO2":
      return "Industrial pollution detected. Sensitive groups should stay indoors.";
    case "CO":
      return "Carbon Monoxide levels elevated. Ensure good ventilation indoors but avoid high-traffic outdoor areas.";
    default:
      return "Monitor air quality closely.";
  }
};

export const fetchCityData = async (city: string): Promise<AirQualityData> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      // Randomize base AQI for demo variety
      const baseAQI = Math.floor(Math.random() * 150) + 30;

      resolve({
        city,
        currentAQI: baseAQI,
        lastUpdated: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
        temperature: 30 + Math.floor(Math.random() * 4),
        humidity: 60 + Math.floor(Math.random() * 20),
        windSpeed: Math.floor(Math.random() * 15),
        pollutants: {
          "PM2.5": { value: baseAQI * 0.8, unit: "µg/m³", status: "Moderate" },
          PM10: { value: baseAQI * 1.2, unit: "µg/m³", status: "Moderate" },
          NO2: { value: 20, unit: "ppb", status: "Good" },
          SO2: { value: 5, unit: "ppb", status: "Good" },
          CO: { value: 500, unit: "ppb", status: "Good" },
          O3: { value: 45, unit: "ppb", status: "Good" },
        },
        forecast: [
          {
            day: "Tomorrow",
            aqi: baseAQI + Math.floor(Math.random() * 40) - 20,
            primaryPollutant: Math.random() > 0.5 ? "PM2.5" : "O3",
            pollutants: {
              "PM2.5": 50,
              PM10: 60,
              NO2: 20,
              SO2: 5,
              CO: 400,
              O3: 90,
            },
          },
          {
            day: "Day After",
            aqi: baseAQI + Math.floor(Math.random() * 40) - 20,
            primaryPollutant: "PM2.5",
            pollutants: {
              "PM2.5": 45,
              PM10: 55,
              NO2: 18,
              SO2: 4,
              CO: 350,
              O3: 40,
            },
          },
        ],
        history: Array.from({ length: 8 }, (_, i) => ({
          time: `${i * 3}:00`,
          aqi: Math.floor(baseAQI + (Math.random() * 40 - 20)),
        })),
      });
    }, 800); // Simulate network delay
  });
};

const API_URL = import.meta.env.VITE_API_URL as string;
const API_TOKEN = import.meta.env.VITE_API_TOKEN as string;
const AI_API_URL = import.meta.env.VITE_AI_API_URL as string;

export async function fetchAirQuality(city: string): Promise<APIResponse> {
  try {
    const response = await fetch(`${API_URL}/korea/seoul/${city}/?token=${API_TOKEN}`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: APIResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching air quality data:", error);
    throw error;
  }
}

export async function fetchPMForecast(city: string): Promise<ForecastResponse> {
  try {
    // console.log(city)
    // const response = await fetch(`${AI_API_URL}predict?station=${city}`);
    const response = await fetch(`${AI_API_URL}predict?station=${city}`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: ForecastResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching forecast data:", error);
    throw error;
  }
}

export async function fetchForecastDetail(
  city: string
): Promise<ForecastDetailResponse> {
  try {
    const response = await fetch(`${AI_API_URL}predict-detail?station=${city}`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: ForecastDetailResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching forecast data:", error);
    throw error;
  }
}

export async function fetchMultistepForecast(
  city: string
): Promise<ForecastDetailResponse> {
  try {
    const response = await fetch(`${AI_API_URL}forecasts?station=${city}`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: ForecastDetailResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching forecast data:", error);
    throw error;
  }
}