import { getCoBackground, getCoStatus, getCoTextColor } from "@/lib/color";
import { Card } from "../ui/card";

const unit = "ppm";

interface CoCardProps {
  v: number;
}

export default function CoCard({ v }: CoCardProps) {
  return (
    <Card className="p-4 flex flex-col justify-between hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <span className="font-bold text-slate-700">CO</span>
        <div className={`w-2 h-2 rounded-full ${getCoBackground(v)}`} />
      </div>
      <div>
        <div className="text-2xl font-bold text-slate-900">{v.toFixed(1)}</div>
        <div className="text-xs text-slate-500">{unit}</div>
      </div>
      <div className="mt-3 pt-3 border-t border-slate-100">
        <span className={`text-xs font-medium ${getCoTextColor(v)}`}>
          {getCoStatus(v)}
        </span>
      </div>
    </Card>
  );
}
