import { getSo2Background, getSo2Status, getSo2TextColor } from "@/lib/color";
import { Card } from "../ui/card";

const unit = "ppm";

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