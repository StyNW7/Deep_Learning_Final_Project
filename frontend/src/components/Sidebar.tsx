import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { AirStationData } from "@/lib/types";
import { Wind, Activity, MapPin } from "lucide-react";
import { ScrollArea } from "./ui/scroll-area";
import { Separator } from "./ui/separator";

interface SidebarProps {
  data: AirStationData | null;
}

export function Sidebar({ data }: SidebarProps) {
  if (!data) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-muted-foreground bg-muted/10">
        <MapPin className="w-12 h-12 mb-4 opacity-20" />
        <h2 className="text-xl font-semibold">Select a Station</h2>
        <p className="text-sm text-center mt-2">
          Click on a marker on the map to view air quality details.
        </p>
      </div>
    );
  }

  // Helper for color coding Forecast PM2.5
  const getQualityColor = (value: number) => {
    if (value <= 15) return "text-green-500";
    if (value <= 35) return "text-yellow-500";
    return "text-red-500";
  };

  return (
    <ScrollArea className="h-full w-full bg-background border-r">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight">{data.city}</h1>
          <p className="text-sm text-muted-foreground flex items-center gap-2">
            <Wind className="w-4 h-4" /> Real-time Air Quality
          </p>
        </div>

        <Separator />

        {/* Forecast Card */}
        <Card className="bg-primary/5 border-primary/20 shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Activity className="w-4 h-4 text-primary" />
              Forecast PM2.5 (Next Hr)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div
              className={`text-4xl font-extrabold ${getQualityColor(
                data.forecastPm25
              )}`}
            >
              {data.forecastPm25}
              <span className="text-lg font-normal text-muted-foreground ml-1">
                µg/m³
              </span>
            </div>
          </CardContent>
        </Card>

        {/* Detail Grid */}
        <div className="grid grid-cols-2 gap-4">
          <DetailItem label="PM10" value={data.pm10} unit="µg/m³" />
          <DetailItem label="PM2.5" value={data.pm25} unit="µg/m³" />
          <DetailItem label="NO₂" value={data.no2} unit="ppm" />
          <DetailItem label="O₃" value={data.o3} unit="ppm" />
          <DetailItem label="CO" value={data.co} unit="ppm" />
          <DetailItem label="SO₂" value={data.so2} unit="ppm" />
        </div>
      </div>
    </ScrollArea>
  );
}

// Sub-component for grid items
function DetailItem({
  label,
  value,
  unit,
}: {
  label: string;
  value: number;
  unit: string;
}) {
  return (
    <div className="flex flex-col p-3 rounded-lg border bg-card text-card-foreground shadow-sm">
      <span className="text-xs text-muted-foreground font-medium uppercase">
        {label}
      </span>
      <span className="text-lg font-bold mt-1">
        {value}{" "}
        <span className="text-xs font-normal text-muted-foreground">
          {unit}
        </span>
      </span>
    </div>
  );
}
