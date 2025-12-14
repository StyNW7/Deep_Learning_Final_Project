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

export const getRecommendations = (pollutant: string): Recommendation => {
  const recommendations: Record<string, Recommendation> = {
    NO2: {
      level: "Moderate",
      color: "bg-yellow-50 border-yellow-200",
      activities: [
        { icon: "🏃", text: "Light outdoor exercise is safe", safe: true },
        { icon: "🚶", text: "Walking and cycling recommended", safe: true },
        {
          icon: "⚠️",
          text: "Sensitive groups should limit prolonged outdoor activities",
          safe: false,
        },
      ],
    },
    SO2: {
      level: "Good",
      color: "bg-green-50 border-green-200",
      activities: [
        { icon: "✅", text: "All outdoor activities safe", safe: true },
        { icon: "🏃", text: "Perfect for exercise", safe: true },
        { icon: "🌳", text: "Great day for outdoor activities", safe: true },
      ],
    },
    O3: {
      level: "Moderate",
      color: "bg-yellow-50 border-yellow-200",
      activities: [
        {
          icon: "🌅",
          text: "Best to exercise in early morning or evening",
          safe: true,
        },
        {
          icon: "⚠️",
          text: "Limit intense outdoor activities during midday",
          safe: false,
        },
        {
          icon: "💧",
          text: "Stay hydrated if exercising outdoors",
          safe: true,
        },
      ],
    },
    CO: {
      level: "Good",
      color: "bg-green-50 border-green-200",
      activities: [
        { icon: "✅", text: "Air quality is excellent", safe: true },
        { icon: "🏃", text: "All activities safe", safe: true },
        {
          icon: "🌟",
          text: "Perfect conditions for outdoor plans",
          safe: true,
        },
      ],
    },
    PM10: {
      level: "Moderate",
      color: "bg-yellow-50 border-yellow-200",
      activities: [
        { icon: "😷", text: "Consider wearing a mask outdoors", safe: false },
        { icon: "🏠", text: "Keep windows closed", safe: false },
        { icon: "🚶", text: "Light activities are okay", safe: true },
      ],
    },
    PM2_5: {
      level: "Moderate",
      color: "bg-yellow-50 border-yellow-200",
      activities: [
        {
          icon: "😷",
          text: "Mask recommended for sensitive groups",
          safe: false,
        },
        { icon: "🏠", text: "Limit prolonged outdoor exposure", safe: false },
        { icon: "💨", text: "Use air purifiers indoors", safe: true },
      ],
    },
  };

  return recommendations[pollutant] || recommendations.O3;
};
