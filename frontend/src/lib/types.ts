export type PollutantType = "PM2.5" | "PM10" | "CO" | "NO2" | "SO2" | "O3";

export interface PollutantData {
  value: number;
  unit: string;
  status: "Good" | "Moderate" | "Unhealthy" | "Hazardous";
}

export interface DailyForecast {
  day: string;
  aqi: number;
  primaryPollutant: PollutantType;
  pollutants: Record<PollutantType, number>;
}

export interface AirQualityData {
  city: string;
  currentAQI: number;
  lastUpdated: string;
  temperature: number;
  humidity: number;
  windSpeed: number;
  pollutants: Record<PollutantType, PollutantData>;
  forecast: DailyForecast[]; // Index 0 is tomorrow
  history: { time: string; aqi: number }[];
}
