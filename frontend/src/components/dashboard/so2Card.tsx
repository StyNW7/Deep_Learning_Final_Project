import { Card } from "../ui/card";

const unit = "ppm";

//less than
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

interface So2CardProps {
    v: number;
}

export default function So2Card({ v }: So2CardProps) {
    return (
        <Card
            className="p-4 flex flex-col justify-between hover:shadow-md transition-shadow"
        >
            <div className="flex justify-between items-start mb-2">
                <span className="font-bold text-slate-700">SO2</span>
                <div
                    className={`w-2 h-2 rounded-full ${getSo2Background(v)}`}
                />
            </div>
            <div>
                <div className="text-2xl font-bold text-slate-900">
                    {v.toFixed(1)}
                </div>
                <div className="text-xs text-slate-500">{unit}</div>
            </div>
            <div className="mt-3 pt-3 border-t border-slate-100">
                <span
                    className={`text-xs font-medium ${getSo2TextColor(v)}`}
                >
                    {getSo2Status(v)}
                </span>
            </div>
        </Card>
    )
}