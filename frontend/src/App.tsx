import { useState } from 'react'
import './App.css'
import { CityDashboard } from './components/CityDashboard';
import { LandingPage } from './components/LandingPage';

function App() {
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
        <LandingPage onSelectCity={setSelectedCity} />
      )}
    </div>
  );
}

export default App
