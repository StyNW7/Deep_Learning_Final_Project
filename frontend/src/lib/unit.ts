const apiPollutantUnits = {
  CO: "mg/m3",
  NO2: "µg/m³",
  O3: "µg/m³",
  SO2: "µg/m³",
} as const;

const pollutantUnits = {
  CO: "ppm",
  NO2: "ppm",
  O3: "ppm",
  SO2: "ppm",
  pm25: "µg/m³",
} as const;

export function getUnit(pollutant: string): string | undefined {
  return pollutant in pollutantUnits
    ? pollutantUnits[pollutant as keyof typeof pollutantUnits]
    : undefined;
}

/*
ppm = (mass concentration × 24.45) / molecular weight
At 25 °C & 1 atm
*/

const molecularWeights = {
  CO: 28.01,
  NO2: 46.0055,
  O3: 48.0,
  SO2: 64.066,
} as const;

type Pollutant = keyof typeof molecularWeights;

/*
Convert mg/m³ → ppm
*/
function mgm3ToPpm(value: number, pollutant: Pollutant): number {
  return (value * 24.45) / molecularWeights[pollutant];
}

/*
Convert µg/m³ → ppm
*/
export function ugm3ToPpm(value: number, pollutant: Pollutant): number {
  return mgm3ToPpm(value / 1000, pollutant);
}

// function ppmToMgm3(ppm: number, mw: number): number {
//   return (ppm * mw) / 24.45;
// }

// export function convertUnit(
//   ppm: number,
//   pollutant: Pollutant
// ): { value: number; unit: string } {
//   const unit = apiPollutantUnits[pollutant];

//   const mgm3 = ppmToMgm3(ppm, molecularWeights[pollutant]);

//   if (unit === "mg/m3") {
//     return { value: mgm3, unit };
//   }

//   // µg/m³
//   return { value: mgm3 * 1000, unit };
// }

export function convertToPPM(
  value: number,
  pollutant: string
) {
  const unit = apiPollutantUnits[pollutant as Pollutant];

  // mg/m³ → ppm
  if (unit === "mg/m3") {
    return mgm3ToPpm(value, pollutant as Pollutant);
  }

  // µg/m³ → ppm
  return ugm3ToPpm(value, pollutant as Pollutant);
}

