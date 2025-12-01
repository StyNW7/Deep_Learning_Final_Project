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
const GOOD_CO = 0.03;
const NORMAL_CO = 0.06;
const BAD_CO = 0.2;
const VERY_BAD_CO = 2.0;

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