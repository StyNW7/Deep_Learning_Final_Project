import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { APIResponse, ForecastResponse } from "@/lib/types";
import { Wind, Activity, MapPin, Loader } from "lucide-react";
import { ScrollArea } from "./ui/scroll-area";
import { Separator } from "./ui/separator";
import { useEffect, useState } from "react";
import { fetchAirQuality, fetchPMForecast } from "@/services/cityService";

interface SidebarProps {
  selectedCity: string | null;
}

export function Sidebar({ selectedCity }: SidebarProps) {

  const [data, setData] = useState<APIResponse | null>(null);
  const [forecastData, setForecastData] = useState<ForecastResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isCancelled = false;

    const fetchData = async () => {
      setLoading(true);

      if (!selectedCity) {
        setData(null);
        setForecastData(null);
        setLoading(false);
        return;
      }

      try {
        const [resultApi, forecastResult] = await Promise.all([
          fetchAirQuality(selectedCity),
          fetchPMForecast(selectedCity),
        ]);

        if (!isCancelled) {
          setData(resultApi);
          setForecastData(forecastResult);
        }
      } finally {
        if (!isCancelled) {
          setLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      isCancelled = true;
    };
  }, [selectedCity]);

  if (!selectedCity) {
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

  if (loading) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-muted-foreground bg-muted/10">
        <Loader className="w-12 h-12 mb-4 opacity-20" />
        <h2 className="text-xl font-semibold">Loading...</h2>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-muted-foreground bg-muted/10">
        <h2 className="text-xl font-semibold">No data available</h2>
      </div>
    );
  }

  return (
    <ScrollArea className="h-full w-full bg-background border-r">
      <div className="p-6 space-y-6">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight">
            {data.data.city.name}
          </h1>
          <p className="text-sm text-muted-foreground flex items-center gap-2">
            <Wind className="w-4 h-4" /> Real-time Air Quality
          </p>
        </div>

        <Separator />

        {/* TODO: Forecast */}
        <Card className="bg-primary/5 border-primary/20 shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Activity className="w-4 h-4 text-primary" />
              Forecast PM2.5 (Next Hr)
            </CardTitle>
          </CardHeader>
          <CardContent>
            {forecastData ? (
              <div className="text-4xl font-extrabold">
                {forecastData.prediction.toFixed(2)}
                <span className="text-lg font-normal text-muted-foreground ml-1">
                  µg/m³
                </span>
              </div>
            ) : (
              <div className="text-muted-foreground text-sm">
                No forecast available
              </div>
            )}
          </CardContent>
        </Card>

        <div className="grid grid-cols-2 gap-4">
          <DetailItem label="PM10" value={data.data.iaqi.pm10.v} unit="µg/m³" />
          <DetailItem
            label="PM2.5"
            value={data.data.iaqi.pm25.v}
            unit="µg/m³"
          />
          <DetailItem label="NO₂" value={data.data.iaqi.no2.v} unit="ppm" />
          <DetailItem label="O₃" value={data.data.iaqi.o3.v} unit="ppm" />
          <DetailItem label="CO" value={data.data.iaqi.co.v} unit="ppm" />
          <DetailItem label="SO₂" value={data.data.iaqi.so2.v} unit="ppm" />
        </div>
      </div>
    </ScrollArea>
  );
}

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
