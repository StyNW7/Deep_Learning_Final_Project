import type { PollutantType } from "./types";

//SO2
const GOOD_SO2 = 0.02;
const NORMAL_SO2 = 0.05;
const BAD_SO2 = 0.15;
const VERY_BAD_SO2 = 1.0;

export const getSo2Background = (v: number) => {
  if (v < GOOD_SO2) return "bg-blue-500";
  if (v <= NORMAL_SO2) return "bg-green-500";
  if (v <= BAD_SO2) return "bg-yellow-500";
  if (v <= VERY_BAD_SO2) return "bg-red-500";
  return "bg-rose-100";
};

export const getSo2TextColor = (v: number) => {
  if (v < GOOD_SO2) return "text-blue-600";
  if (v <= NORMAL_SO2) return "text-green-600";
  if (v <= BAD_SO2) return "text-yellow-600";
  if (v <= VERY_BAD_SO2) return "text-red-600";
  return "text-rose-600";
};

export const getSo2Status = (v: number) => {
  if (v < GOOD_SO2) return "Good";
  if (v <= NORMAL_SO2) return "Normal";
  if (v <= BAD_SO2) return "Bad";
  if (v <= VERY_BAD_SO2) return "Very Bad";
  return "Likely Wrong";
};

//NO2
const GOOD_NO2 = 0.03;
const NORMAL_NO2 = 0.06;
const BAD_NO2 = 0.2;
const VERY_BAD_NO2 = 2.0;

export const getNo2Background = (v: number) => {
  if (v < GOOD_NO2) return "bg-blue-500";
  if (v <= NORMAL_NO2) return "bg-green-500";
  if (v <= BAD_NO2) return "bg-yellow-500";
  if (v <= VERY_BAD_NO2) return "bg-red-500";
  return "bg-rose-100";
};

export const getNo2TextColor = (v: number) => {
  if (v < GOOD_NO2) return "text-blue-600";
  if (v <= NORMAL_NO2) return "text-green-600";
  if (v <= BAD_NO2) return "text-yellow-600";
  if (v <= VERY_BAD_NO2) return "text-red-600";
  return "text-rose-600";
};

export const getNo2Status = (v: number) => {
  if (v < GOOD_NO2) return "Good";
  if (v <= NORMAL_NO2) return "Normal";
  if (v <= BAD_NO2) return "Bad";
  if (v <= VERY_BAD_NO2) return "Very Bad";
  return "Likely Wrong";
};

//CO
const GOOD_CO = 2.0;
const NORMAL_CO = 9.0;
const BAD_CO = 15.0;
const VERY_BAD_CO = 50.0;

export const getCoBackground = (v: number) => {
  if (v < GOOD_CO) return "bg-blue-500";
  if (v <= NORMAL_CO) return "bg-green-500";
  if (v <= BAD_CO) return "bg-yellow-500";
  if (v <= VERY_BAD_CO) return "bg-red-500";
  return "bg-rose-100";
};

export const getCoTextColor = (v: number) => {
  if (v < GOOD_CO) return "text-blue-600";
  if (v <= NORMAL_CO) return "text-green-600";
  if (v <= BAD_CO) return "text-yellow-600";
  if (v <= VERY_BAD_CO) return "text-red-600";
  return "text-rose-600";
};

export const getCoStatus = (v: number) => {
  if (v < GOOD_CO) return "Good";
  if (v <= NORMAL_CO) return "Normal";
  if (v <= BAD_CO) return "Bad";
  if (v <= VERY_BAD_CO) return "Very Bad";
  return "Likely Wrong";
};

//CO
const GOOD_O3 = 0.03;
const NORMAL_O3 = 0.09;
const BAD_O3 = 0.15;
const VERY_BAD_O3 = 0.5;

export const getO3Background = (v: number) => {
  if (v < GOOD_O3) return "bg-blue-500";
  if (v <= NORMAL_O3) return "bg-green-500";
  if (v <= BAD_O3) return "bg-yellow-500";
  if (v <= VERY_BAD_O3) return "bg-red-500";
  return "bg-rose-100";
};

export const getO3TextColor = (v: number) => {
  if (v < GOOD_O3) return "text-blue-600";
  if (v <= NORMAL_O3) return "text-green-600";
  if (v <= BAD_O3) return "text-yellow-600";
  if (v <= VERY_BAD_O3) return "text-red-600";
  return "text-rose-600";
};

export const getO3Status = (v: number) => {
  if (v < GOOD_O3) return "Good";
  if (v <= NORMAL_O3) return "Normal";
  if (v <= BAD_O3) return "Bad";
  if (v <= VERY_BAD_O3) return "Very Bad";
  return "Likely Wrong";
};

//---
type Status = "Good" | "Normal" | "Bad" | "Very Bad" | "Likely Wrong";
type BgColor =
  | "bg-blue-500"
  | "bg-green-500"
  | "bg-yellow-500"
  | "bg-red-500"
  | "bg-rose-100";
  type TextColor =
    | "text-blue-500"
    | "text-green-500"
    | "text-yellow-500"
    | "text-red-500"
    | "text-rose-100";
// export type PollutantType = "SO2" | "NO2" | "CO" | "O3";

export const POLLUTANT_THRESHOLDS: Record<
  PollutantType,
  { good: number; normal: number; bad: number; veryBad: number }
> = {
  "SO2": {
    good: 0.02,
    normal: 0.05,
    bad: 0.15,
    veryBad: 1.0,
  },
  "NO2": {
    good: 0.03,
    normal: 0.06,
    bad: 0.2,
    veryBad: 2.0,
  },
  "CO": {
    good: 2.0,
    normal: 9.0,
    bad: 15.0,
    veryBad: 50.0,
  },
  "O3": {
    good: 0.03,
    normal: 0.09,
    bad: 0.15,
    veryBad: 0.5,
  },
  "PM10": {
    good: 30.0,
    normal: 80.0,
    bad: 150.0,
    veryBad: 600.0,
  },
  "PM2.5": {
    good: 15.0,
    normal: 35.0,
    bad: 75.0,
    veryBad: 500.0,
  },
};

export const getPollutantStatus = (
  pollutant: PollutantType,
  value: number
): Status => {
  const t = POLLUTANT_THRESHOLDS[pollutant];

  if (value < t.good) return "Good";
  if (value <= t.normal) return "Normal";
  if (value <= t.bad) return "Bad";
  if (value <= t.veryBad) return "Very Bad";
  return "Likely Wrong";
};

export const getBgColor = (pollutant: PollutantType, value: number): BgColor => {
  const t = POLLUTANT_THRESHOLDS[pollutant];

  if (value < t.good) return "bg-blue-500";
  if (value <= t.normal) return "bg-green-500";
  if (value <= t.bad) return "bg-yellow-500";
  if (value <= t.veryBad) return "bg-red-500";
  return "bg-rose-100";
};

export const getTextColor = (pollutant: PollutantType, value: number): TextColor => {
  const t = POLLUTANT_THRESHOLDS[pollutant];

  if (value < t.good) return "text-blue-500";
  if (value <= t.normal) return "text-green-500";
  if (value <= t.bad) return "text-yellow-500";
  if (value <= t.veryBad) return "text-red-500";
  return "text-rose-100";
};