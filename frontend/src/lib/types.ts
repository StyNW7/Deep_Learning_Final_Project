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

// export interface IAQI {
//   dew: IAQIValue;
//   h: IAQIValue;
//   p: IAQIValue;
//   pm25: IAQIValue;
//   t: IAQIValue;
//   w: IAQIValue;
// }

export interface IAQI {
  co: IAQIValue;
  h: IAQIValue;
  no2: IAQIValue;
  o3: IAQIValue;
  p: IAQIValue;
  pm10: IAQIValue;
  pm25: IAQIValue;
  r: IAQIValue;
  so2: IAQIValue;
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

export interface ForecastResponse {
  status: string;
  prediction: number;
  last_timestamp: string;
}

export interface ForecastDetailResponse {
  status: string;
  no2_prediction: number;
  o3_prediction: number;
  co_prediction: number;
  so2_prediction: number;
  pm25_prediction: number;
  dominant_pollutant: string;
  last_timestamp: string;
}

export interface MultistepForecastResponse {
  time: string;
  hour24: string;
  pm25: number;
}


//----------------------
// export interface AirStationData {
//   city: string;
//   co: number;
//   no2: number;
//   o3: number;
//   pm10: number;
//   pm25: number;
//   so2: number;
//   forecastPm25: number;
// }