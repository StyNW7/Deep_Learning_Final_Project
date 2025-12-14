import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router';
import HomePage from './pages/HomePage';
import MapPage from './pages/MapPage';
import LandingPage from './pages/LandingPage';
import CityDetailPage from './pages/CityDetailPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/city/:cityName" element={<CityDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App
