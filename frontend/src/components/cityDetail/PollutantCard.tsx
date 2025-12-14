import {
  getBgColor,
  getPollutantStatus,
  POLLUTANT_THRESHOLDS,
} from "@/lib/color";
import type { PollutantType } from "@/lib/types";
import { getUnit } from "@/lib/unit";

interface PollutantCardProps {
  idx: number;
  pollutant: string;
  value: number;
}

export default function PollutantCard({
  idx,
  pollutant,
  value,
}: PollutantCardProps) {
  const t = POLLUTANT_THRESHOLDS[pollutant as PollutantType];
  const percentage = (Number(value) / t.veryBad) * 100;

  return (
    <div
      key={pollutant}
      className="bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-black hover:shadow-xl transition-all duration-300 group animate-slideUp"
      style={{ animationDelay: `${0.4 + idx * 0.05}s` }}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-lg">{pollutant.replace("_", ".")}</h3>
        <div
          className={`text-xs font-semibold px-2 py-1 rounded-full ${getBgColor(
            pollutant as PollutantType,
            value
          )}`}
        >
          {getPollutantStatus(pollutant as PollutantType, value)}
        </div>
      </div>

      <div className="mb-2">
        <div className="text-3xl font-bold group-hover:scale-110 transition-transform inline-block">
          {Number(value.toFixed(2))}
        </div>
        <div className="text-sm text-gray-500 ml-1 inline">
          {getUnit(pollutant)}
        </div>
      </div>

      <div className="mt-4 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full transition-all duration-1000  ${getBgColor(
            pollutant as PollutantType,
            value
          )}`}
          style={{
            width: `${percentage}%`,
            animationDelay: `${idx * 0.1}s`,
          }}
        ></div>
      </div>

      <div className="mt-3 text-xs text-gray-500">Next hour forecast</div>
    </div>
  );
}
