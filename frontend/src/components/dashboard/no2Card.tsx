import { getNo2Background, getNo2Status, getNo2TextColor } from "@/lib/color";
import { Card } from "../ui/card";

const unit = "ppm";

interface No2CardProps {
  v: number;
}

export default function No2Card({ v }: No2CardProps) {
  return (
    <Card className="p-4 flex flex-col justify-between hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <span className="font-bold text-slate-700">NO2</span>
        <div className={`w-2 h-2 rounded-full ${getNo2Background(v)}`} />
      </div>
      <div>
        <div className="text-2xl font-bold text-slate-900">{v.toFixed(1)}</div>
        <div className="text-xs text-slate-500">{unit}</div>
      </div>
      <div className="mt-3 pt-3 border-t border-slate-100">
        <span className={`text-xs font-medium ${getNo2TextColor(v)}`}>
          {getNo2Status(v)}
        </span>
      </div>
    </Card>
  );
}
