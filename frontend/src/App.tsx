import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router';
import HomePage from './pages/HomePage';
import MapPage from './pages/MapPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<HomePage />} />
        <Route path="/" element={<MapPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App
