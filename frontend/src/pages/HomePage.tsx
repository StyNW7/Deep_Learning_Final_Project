import { CityDashboard } from '@/components/CityDashboard';
import { CityList } from '@/components/CityList';
import { useState } from 'react'

export default function HomePage() {
  const [selectedCity, setSelectedCity] = useState<string | null>(null);

  // Simple router logic
  return (
    <div className="font-sans text-slate-900">
      {selectedCity ? (
        <CityDashboard
          city={selectedCity}
          onBack={() => setSelectedCity(null)}
        />
      ) : (
        <CityList onSelectCity={setSelectedCity} />
      )}
    </div>
  );
}
