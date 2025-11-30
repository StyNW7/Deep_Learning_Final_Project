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

//aqi type
export interface Attribution {
  url: string;
  name: string;
  logo?: string;
}

export interface City {
  geo: [number, number];
  name: string;
  url: string;
  location: string;
}

export interface IAQIValue {
  v: number;
}

export interface IAQI {
  dew: IAQIValue;
  h: IAQIValue;
  p: IAQIValue;
  pm25: IAQIValue;
  t: IAQIValue;
  w: IAQIValue;
}

export interface ForecastItem {
  avg: number;
  day: string;
  max: number;
  min: number;
}

export interface ForecastDaily {
  pm10: ForecastItem[];
  pm25: ForecastItem[];
  uvi: ForecastItem[];
}

export interface Forecast {
  daily: ForecastDaily;
}

export interface TimeInfo {
  s: string;
  tz: string;
  v: number;
  iso: string;
}

export interface Debug {
  sync: string;
}

export interface APIData {
  aqi: number;
  idx: number;
  attributions: Attribution[];
  city: City;
  dominentpol: string;
  iaqi: IAQI;
  time: TimeInfo;
  forecast: Forecast;
  debug: Debug;
}

export interface APIResponse {
  status: string;
  data: APIData;
}
