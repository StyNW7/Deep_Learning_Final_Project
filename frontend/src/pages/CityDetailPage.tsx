/* eslint-disable @typescript-eslint/no-unused-vars */
import { useState, useEffect } from 'react';
import { ArrowLeft, Wind, TrendingUp, AlertCircle, Calendar, Clock, Activity } from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar 
} from 'recharts';

// Mock data - replace with actual API data
interface PollutantData {
  value: number | string;
  unit: string;
  status: 'Good' | 'Moderate' | 'Poor';
}

interface NextHourData {
  NO2: PollutantData;
  SO2: PollutantData;
  O3: PollutantData;
  CO: PollutantData;
  PM10: PollutantData;
  PM2_5: PollutantData;
}

interface HourlyForecast {
  time: string;
  hour24: number;
  aqi: number;
  dominant: string;
  temperature: number;
}

interface RadarDataPoint {
  pollutant: string;
  current: number;
  safe: number;
}

interface CityData {
  cityName: string;
  cityImage: string;
  currentTime: Date;
  next8Hours: HourlyForecast[];
  nextHour: NextHourData;
  dominantPollutant: string;
  radarData: RadarDataPoint[];
}

interface ActivityItem {
  icon: string;
  text: string;
  safe: boolean;
}

interface Recommendation {
  level: string;
  color: string;
  activities: ActivityItem[];
}

interface CityDetailPageProps {
  cityName?: string;
  cityImage?: string;
}

const generateMockData = (cityName: string, cityImage: string): CityData => {
  const pollutants = ['NO2', 'SO2', 'O3', 'CO', 'PM10', 'PM2.5'];
  const hours = Array.from({ length: 8 }, (_, i) => {
    const date = new Date();
    date.setHours(date.getHours() + i);
    return date;
  });

  return {
    cityName,
    cityImage: 'https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=800',
    currentTime: new Date(),
    next8Hours: hours.map((date, i) => ({
      time: date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
      hour24: date.getHours(),
      aqi: Math.floor(Math.random() * 100) + 50,
      dominant: pollutants[Math.floor(Math.random() * pollutants.length)] as string,
      temperature: Math.floor(Math.random() * 10) + 15,
    })),
    nextHour: {
      NO2: { value: Math.floor(Math.random() * 80) + 20, unit: 'µg/m³', status: 'Good' },
      SO2: { value: Math.floor(Math.random() * 50) + 10, unit: 'µg/m³', status: 'Good' },
      O3: { value: Math.floor(Math.random() * 90) + 30, unit: 'µg/m³', status: 'Moderate' },
      CO: { value: (Math.random() * 2 + 0.5).toFixed(1), unit: 'mg/m³', status: 'Good' },
      PM10: { value: Math.floor(Math.random() * 70) + 30, unit: 'µg/m³', status: 'Moderate' },
      PM2_5: { value: Math.floor(Math.random() * 50) + 20, unit: 'µg/m³', status: 'Moderate' },
    },
    dominantPollutant: 'O3',
    radarData: pollutants.map(p => ({
      pollutant: p,
      current: Math.floor(Math.random() * 80) + 20,
      safe: 50,
    })),
  };
};

const CityDetailPage = ({ cityName = 'Gangnam', cityImage = "x" }: CityDetailPageProps) => {
    
  const [data, setData] = useState<CityData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setData(generateMockData(cityName, cityImage));
      setIsLoading(false);
    }, 500);
  }, [cityName, cityImage]);

  const getRecommendations = (pollutant: string): Recommendation => {
    const recommendations: Record<string, Recommendation> = {
      NO2: {
        level: 'Moderate',
        color: 'bg-yellow-50 border-yellow-200',
        activities: [
          { icon: '🏃', text: 'Light outdoor exercise is safe', safe: true },
          { icon: '🚶', text: 'Walking and cycling recommended', safe: true },
          { icon: '⚠️', text: 'Sensitive groups should limit prolonged outdoor activities', safe: false },
        ],
      },
      SO2: {
        level: 'Good',
        color: 'bg-green-50 border-green-200',
        activities: [
          { icon: '✅', text: 'All outdoor activities safe', safe: true },
          { icon: '🏃', text: 'Perfect for exercise', safe: true },
          { icon: '🌳', text: 'Great day for outdoor activities', safe: true },
        ],
      },
      O3: {
        level: 'Moderate',
        color: 'bg-yellow-50 border-yellow-200',
        activities: [
          { icon: '🌅', text: 'Best to exercise in early morning or evening', safe: true },
          { icon: '⚠️', text: 'Limit intense outdoor activities during midday', safe: false },
          { icon: '💧', text: 'Stay hydrated if exercising outdoors', safe: true },
        ],
      },
      CO: {
        level: 'Good',
        color: 'bg-green-50 border-green-200',
        activities: [
          { icon: '✅', text: 'Air quality is excellent', safe: true },
          { icon: '🏃', text: 'All activities safe', safe: true },
          { icon: '🌟', text: 'Perfect conditions for outdoor plans', safe: true },
        ],
      },
      PM10: {
        level: 'Moderate',
        color: 'bg-yellow-50 border-yellow-200',
        activities: [
          { icon: '😷', text: 'Consider wearing a mask outdoors', safe: false },
          { icon: '🏠', text: 'Keep windows closed', safe: false },
          { icon: '🚶', text: 'Light activities are okay', safe: true },
        ],
      },
      PM2_5: {
        level: 'Moderate',
        color: 'bg-yellow-50 border-yellow-200',
        activities: [
          { icon: '😷', text: 'Mask recommended for sensitive groups', safe: false },
          { icon: '🏠', text: 'Limit prolonged outdoor exposure', safe: false },
          { icon: '💨', text: 'Use air purifiers indoors', safe: true },
        ],
      },
    };

    return recommendations[pollutant] || recommendations.O3;
  };

  const getPollutantStatus = (status: string): string => {
    const colors: Record<string, string> = {
      Good: 'text-green-600',
      Moderate: 'text-yellow-600',
      Poor: 'text-red-600',
    };
    return colors[status] || 'text-gray-600';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-black border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading city data...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">No data available</p>
        </div>
      </div>
    );
  }

  const recommendation = getRecommendations(data.dominantPollutant);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button 
              onClick={() => window.history.back()}
              className="flex items-center space-x-2 text-gray-600 hover:text-black transition-colors group"
            >
              <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
              <span>Back to Map</span>
            </button>
            <div className="flex items-center space-x-2">
              <Wind className="w-5 h-5" />
              <span className="font-bold">AeroSeoul</span>
            </div>
          </div>
        </div>
      </header>

      {/* City Header */}
      <div className="relative h-64 overflow-hidden animate-fadeIn">
        <img 
          src={data.cityImage} 
          alt={data.cityName}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
        <div className="absolute bottom-0 left-0 right-0 p-8">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-2 animate-slideUp">
              {data.cityName}
            </h1>
            <p className="text-white/90 flex items-center space-x-2 animate-slideUp" style={{animationDelay: '0.1s'}}>
              <Clock className="w-4 h-4" />
              <span>Updated: {data.currentTime.toLocaleString()}</span>
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Dominant Pollutant Alert */}
        <div className={`${recommendation.color} border-2 rounded-2xl p-6 mb-8 animate-slideUp`} style={{animationDelay: '0.1s'}}>
          <div className="flex items-start space-x-4">
            <div className="bg-white rounded-full p-3 shadow-sm">
              <AlertCircle className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-bold mb-2">
                Dominant Pollutant: {data.dominantPollutant} - {recommendation.level}
              </h3>
              <div className="grid md:grid-cols-3 gap-4 mt-4">
                {recommendation.activities.map((activity, idx) => (
                  <div key={idx} className="flex items-center space-x-2 bg-white rounded-lg p-3 shadow-sm">
                    <span className="text-2xl">{activity.icon}</span>
                    <span className="text-sm">{activity.text}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Bento Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* 8-Hour Forecast - Large Card */}
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-black transition-all duration-300 animate-slideUp" style={{animationDelay: '0.2s'}}>
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-2">
                <Calendar className="w-5 h-5" />
                <h2 className="text-xl font-bold">8-Hour Forecast</h2>
              </div>
              <span className="text-sm text-gray-500">Air Quality Index</span>
            </div>
            
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={data.next8Hours}>
                <defs>
                  <linearGradient id="aqiGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#000000" stopOpacity={0.1}/>
                    <stop offset="95%" stopColor="#000000" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="time" stroke="#666" fontSize={12} />
                <YAxis stroke="#666" fontSize={12} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '2px solid black',
                    borderRadius: '8px',
                    padding: '8px'
                  }}
                />
                <Area 
                  type="monotone" 
                  dataKey="aqi" 
                  stroke="#000000" 
                  strokeWidth={2}
                  fill="url(#aqiGradient)" 
                />
              </AreaChart>
            </ResponsiveContainer>

            <div className="grid grid-cols-4 md:grid-cols-8 gap-2 mt-6">
              {data.next8Hours.map((hour, idx) => (
                <div key={idx} className="text-center p-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="text-xs text-gray-600 mb-1">{hour.time.split(' ')[0]}</div>
                  <div className="font-bold text-lg">{hour.aqi}</div>
                  <div className="text-xs text-gray-500 mt-1">{hour.dominant}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Pollutant Radar Chart */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-black transition-all duration-300 animate-slideUp" style={{animationDelay: '0.3s'}}>
            <div className="flex items-center space-x-2 mb-6">
              <Activity className="w-5 h-5" />
              <h2 className="text-xl font-bold">Pollutant Levels</h2>
            </div>
            
            <ResponsiveContainer width="100%" height={250}>
              <RadarChart data={data.radarData}>
                <PolarGrid stroke="#e0e0e0" />
                <PolarAngleAxis dataKey="pollutant" stroke="#666" fontSize={12} />
                <PolarRadiusAxis stroke="#666" fontSize={10} />
                <Radar 
                  name="Current" 
                  dataKey="current" 
                  stroke="#000000" 
                  fill="#000000" 
                  fillOpacity={0.2} 
                  strokeWidth={2}
                />
                <Radar 
                  name="Safe Limit" 
                  dataKey="safe" 
                  stroke="#999999" 
                  fill="#999999" 
                  fillOpacity={0.1} 
                  strokeWidth={1}
                  strokeDasharray="5 5"
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '2px solid black',
                    borderRadius: '8px'
                  }}
                />
              </RadarChart>
            </ResponsiveContainer>

            <div className="flex justify-center space-x-4 mt-4 text-xs">
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-black rounded-full"></div>
                <span>Current</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 border-2 border-gray-400 border-dashed rounded-full"></div>
                <span>Safe Limit</span>
              </div>
            </div>
          </div>

          {/* Next Hour Pollutants Grid */}
          <div className="lg:col-span-3 grid grid-cols-2 md:grid-cols-3 gap-4">
            {Object.entries(data.nextHour).map((entry, idx) => {
              const [pollutant, details] = entry as [string, PollutantData];
              const numericValue = typeof details.value === 'string' ? parseFloat(details.value) : details.value;
              const percentage = Math.min((Number(numericValue) / 100) * 100, 100);
              
              return (
                <div 
                  key={pollutant}
                  className="bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-black hover:shadow-xl transition-all duration-300 group animate-slideUp"
                  style={{animationDelay: `${0.4 + idx * 0.05}s`}}
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-lg">{pollutant.replace('_', '.')}</h3>
                    <div className={`text-xs font-semibold px-2 py-1 rounded-full ${
                      details.status === 'Good' ? 'bg-green-100 text-green-700' :
                      details.status === 'Moderate' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {details.status}
                    </div>
                  </div>
                  
                  <div className="mb-2">
                    <div className="text-3xl font-bold group-hover:scale-110 transition-transform inline-block">
                      {String(details.value)}
                    </div>
                    <div className="text-sm text-gray-500 ml-1 inline">{details.unit}</div>
                  </div>

                  <div className="mt-4 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-1000 ${
                        details.status === 'Good' ? 'bg-green-500' :
                        details.status === 'Moderate' ? 'bg-yellow-500' :
                        'bg-red-500'
                      }`}
                      style={{ 
                        width: `${percentage}%`,
                        animationDelay: `${idx * 0.1}s`
                      }}
                    ></div>
                  </div>

                  <div className="mt-3 text-xs text-gray-500">
                    Next hour forecast
                  </div>
                </div>
              );
            })}
          </div>

          {/* Trend Insight Card */}
          <div className="lg:col-span-3 bg-gradient-to-br from-gray-50 to-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-black transition-all duration-300 animate-slideUp" style={{animationDelay: '0.7s'}}>
            <div className="flex items-start space-x-4">
              <div className="bg-black text-white rounded-full p-3">
                <TrendingUp className="w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold mb-3">Air Quality Insights</h3>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="bg-white rounded-xl p-4 border border-gray-200">
                    <div className="text-sm text-gray-600 mb-1">Overall Trend</div>
                    <div className="text-lg font-bold">Improving</div>
                    <div className="text-xs text-green-600 mt-1">↓ 12% from yesterday</div>
                  </div>
                  <div className="bg-white rounded-xl p-4 border border-gray-200">
                    <div className="text-sm text-gray-600 mb-1">Best Time Today</div>
                    <div className="text-lg font-bold">6:00 - 9:00 AM</div>
                    <div className="text-xs text-gray-500 mt-1">Lowest pollution levels</div>
                  </div>
                  <div className="bg-white rounded-xl p-4 border border-gray-200">
                    <div className="text-sm text-gray-600 mb-1">Weekly Average</div>
                    <div className="text-lg font-bold">Moderate</div>
                    <div className="text-xs text-gray-500 mt-1">AQI: 65-85 range</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fadeIn {
          animation: fadeIn 0.6s ease-out forwards;
        }

        .animate-slideUp {
          animation: slideUp 0.6s ease-out forwards;
        }

        .animate-spin {
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default CityDetailPage;