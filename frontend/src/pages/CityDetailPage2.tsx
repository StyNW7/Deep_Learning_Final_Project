/* eslint-disable @typescript-eslint/no-explicit-any */
"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Wind, Activity, AlertCircle, TrendingUp } from "lucide-react"
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts"
import { useParams } from "react-router"

// Mock data - replace with real API data
const getCityData = (id: string) => {
  const cities: Record<string, any> = {
    gangnam: {
      name: "Gangnam-gu",
      image: "/gangnam-seoul-skyline-at-sunset.jpg",
      currentAQI: 78,
      dominantPollution: "PM2.5",
      nextHourData: {
        NO2: 45,
        SO2: 12,
        O3: 38,
        CO: 0.6,
        PM10: 82,
        PM25: 56,
      },
      hourlyForecast: [
        { hour: "Now", aqi: 78, pm25: 56, pm10: 82 },
        { hour: "+1h", aqi: 82, pm25: 60, pm10: 85 },
        { hour: "+2h", aqi: 75, pm25: 52, pm10: 78 },
        { hour: "+3h", aqi: 68, pm25: 45, pm10: 70 },
        { hour: "+4h", aqi: 65, pm25: 42, pm10: 68 },
        { hour: "+5h", aqi: 70, pm25: 48, pm10: 72 },
        { hour: "+6h", aqi: 72, pm25: 50, pm10: 75 },
        { hour: "+7h", aqi: 69, pm25: 46, pm10: 71 },
      ],
    },
    jongno: {
      name: "Jongno-gu",
      image: "/jongno-seoul-traditional-buildings.jpg",
      currentAQI: 65,
      dominantPollution: "NO2",
      nextHourData: {
        NO2: 52,
        SO2: 8,
        O3: 42,
        CO: 0.5,
        PM10: 68,
        PM25: 48,
      },
      hourlyForecast: [
        { hour: "Now", aqi: 65, pm25: 48, pm10: 68 },
        { hour: "+1h", aqi: 68, pm25: 50, pm10: 70 },
        { hour: "+2h", aqi: 62, pm25: 45, pm10: 65 },
        { hour: "+3h", aqi: 58, pm25: 40, pm10: 60 },
        { hour: "+4h", aqi: 55, pm25: 38, pm10: 58 },
        { hour: "+5h", aqi: 60, pm25: 42, pm10: 62 },
        { hour: "+6h", aqi: 63, pm25: 44, pm10: 65 },
        { hour: "+7h", aqi: 61, pm25: 43, pm10: 63 },
      ],
    },
  }

  return cities[id] || cities.gangnam
}

const getAQILevel = (aqi: number) => {
  if (aqi <= 50) return { level: "Good", color: "text-green-600", bgColor: "bg-green-50" }
  if (aqi <= 100) return { level: "Moderate", color: "text-yellow-600", bgColor: "bg-yellow-50" }
  if (aqi <= 150) return { level: "Unhealthy for Sensitive", color: "text-orange-600", bgColor: "bg-orange-50" }
  return { level: "Unhealthy", color: "text-red-600", bgColor: "bg-red-50" }
}

const getPollutionRecommendations = (pollutant: string) => {
  const recommendations: Record<string, string[]> = {
    "PM2.5": [
      "Wear an N95 mask when outdoors",
      "Use air purifiers indoors",
      "Avoid strenuous outdoor activities",
      "Keep windows closed during peak hours",
    ],
    PM10: ["Limit outdoor exposure", "Wear protective masks", "Stay hydrated", "Monitor air quality regularly"],
    NO2: [
      "Reduce time near heavy traffic",
      "Ventilate indoor spaces carefully",
      "Avoid rush hour commutes if possible",
      "Consider public transit over driving",
    ],
    O3: [
      "Avoid outdoor activities during afternoon",
      "Stay in air-conditioned spaces",
      "Keep windows closed 12pm-6pm",
      "Reduce physical exertion outdoors",
    ],
    SO2: [
      "Avoid industrial areas",
      "Monitor symptoms if sensitive",
      "Use indoor air filtration",
      "Limit outdoor exposure time",
    ],
    CO: [
      "Ensure proper ventilation",
      "Check heating systems",
      "Avoid enclosed parking areas",
      "Install CO detectors indoors",
    ],
  }

  return recommendations[pollutant] || recommendations["PM2.5"]
}

export default function CityDetailPage() {
  const params = useParams()
  const cityId = params.id as string
  const cityData = getCityData(cityId)
  const aqiInfo = getAQILevel(cityData.currentAQI)
  const recommendations = getPollutionRecommendations(cityData.dominantPollution)

  return (
    <div className="min-h-screen bg-background">

      <main className="container mx-auto px-4 py-8 mt-20">
        {/* Back Button */}
        <div className="mb-6 animate-fadeInDown">
          <a href="/map">
            <Button variant="ghost" className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Map
            </Button>
          </a>
        </div>

        {/* City Header */}
        <div className="mb-8 animate-fadeInUp">
          <div className="relative h-64 md:h-80 rounded-2xl overflow-hidden mb-6 shadow-lg group">
            <img
              src={cityData.image || "/placeholder.svg"}
              alt={cityData.name}
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-linear-to-t from-black/70 via-black/30 to-transparent flex items-end">
              <div className="p-6 md:p-8 w-full">
                <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">{cityData.name}</h1>
                <div className="flex items-center gap-4 flex-wrap">
                  <div className={`px-4 py-2 rounded-lg ${aqiInfo.bgColor} ${aqiInfo.color} font-semibold`}>
                    AQI: {cityData.currentAQI} - {aqiInfo.level}
                  </div>
                  <div className="text-white/90 text-sm">Updated: Just now</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Dashboard Grid - Bento Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Dominant Pollutant - Large Card */}
          <Card className="lg:col-span-2 animate-slideInLeft border-2 hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-3 bg-primary/10 rounded-lg">
                  <Wind className="h-6 w-6" />
                </div>
                <div>
                  <CardTitle>Dominant Pollutant (Next Hour)</CardTitle>
                  <CardDescription>Primary air quality concern</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-6">
                <div>
                  <div className="text-5xl font-bold mb-2">{cityData.dominantPollution}</div>
                  <div className="text-muted-foreground">Main concern for the next hour</div>
                </div>
                <div className="p-6 bg-primary/5 rounded-2xl">
                  <Activity className="h-16 w-16 text-primary" />
                </div>
              </div>

              {/* Pollutant Bars */}
              <div className="space-y-3">
                {Object.entries(cityData.nextHourData).map(([key, value]) => {
                  const isMax = key === cityData.dominantPollution.replace(".", "")
                  return (
                    <div key={key} className="transition-all duration-300 hover:translate-x-1">
                      <div className="flex justify-between mb-1">
                        <span className={`text-sm font-medium ${isMax ? "text-primary" : "text-muted-foreground"}`}>
                          {key}
                        </span>
                        <span className={`text-sm ${isMax ? "font-bold text-primary" : "text-muted-foreground"}`}>
                          {Number(value)} {key.includes("PM") ? "µg/m³" : "ppb"}
                        </span>
                      </div>
                      <div className="h-2 bg-secondary rounded-full overflow-hidden">
                        <div
                          className={`h-full transition-all duration-500 ${isMax ? "bg-primary" : "bg-muted"}`}
                          style={{ width: `${isMax ? 100 : (Number(value) / 100) * 100}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {/* Current Conditions - Compact Cards */}
          <div className="space-y-6 animate-slideInRight">
            <Card className="hover:shadow-xl transition-all duration-300">
              <CardHeader>
                <CardTitle className="text-lg">PM2.5</CardTitle>
                <CardDescription>Fine particles</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold">{cityData.nextHourData.PM25}</div>
                <div className="text-sm text-muted-foreground mt-1">µg/m³</div>
              </CardContent>
            </Card>

            <Card className="hover:shadow-xl transition-all duration-300">
              <CardHeader>
                <CardTitle className="text-lg">PM10</CardTitle>
                <CardDescription>Coarse particles</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold">{cityData.nextHourData.PM10}</div>
                <div className="text-sm text-muted-foreground mt-1">µg/m³</div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* 8 Hour Forecast Chart */}
        <Card className="mb-8 animate-fadeInUp border-2 hover:shadow-xl transition-all duration-300">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-3 bg-primary/10 rounded-lg">
                <TrendingUp className="h-6 w-6" />
              </div>
              <div>
                <CardTitle>8-Hour Forecast</CardTitle>
                <CardDescription>Air quality index and particulate matter trends</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={cityData.hourlyForecast} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="hour" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="aqi"
                    stroke="hsl(var(--primary))"
                    strokeWidth={2}
                    name="AQI"
                    dot={{ fill: "hsl(var(--primary))", r: 4 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="pm25"
                    stroke="hsl(var(--chart-1))"
                    strokeWidth={2}
                    name="PM2.5"
                    dot={{ fill: "hsl(var(--chart-1))", r: 4 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="pm10"
                    stroke="hsl(var(--chart-2))"
                    strokeWidth={2}
                    name="PM10"
                    dot={{ fill: "hsl(var(--chart-2))", r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Pollutant Details Bar Chart */}
        <Card className="mb-8 animate-fadeInUp border-2 hover:shadow-xl transition-all duration-300">
          <CardHeader>
            <CardTitle>Next Hour Pollutant Levels</CardTitle>
            <CardDescription>Detailed breakdown of all pollutants</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={Object.entries(cityData.nextHourData).map(([key, value]) => ({
                    name: key,
                    value: value,
                    unit: key.includes("PM") ? "µg/m³" : key === "CO" ? "mg/m³" : "ppb",
                  }))}
                  margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                    formatter={(value: any, props: any) => [`${value} ${props.payload.unit}`, "Level"]}
                  />
                  <Bar dataKey="value" fill="hsl(var(--primary))" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Recommendations */}
        <Card className="animate-fadeInUp border-2 hover:shadow-xl transition-all duration-300">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-3 bg-primary/10 rounded-lg">
                <AlertCircle className="h-6 w-6" />
              </div>
              <div>
                <CardTitle>Health Recommendations</CardTitle>
                <CardDescription>Based on {cityData.dominantPollution} levels</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recommendations.map((rec, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-4 bg-secondary/50 rounded-lg hover:bg-secondary transition-all duration-300 hover:translate-x-1"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="mt-1">
                    <div className="w-2 h-2 rounded-full bg-primary" />
                  </div>
                  <p className="text-sm leading-relaxed">{rec}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
