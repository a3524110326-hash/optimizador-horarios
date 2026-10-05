import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Settings, Play, Calendar } from 'lucide-react';
import Configuracion from './pages/Configuracion';
import Generador from './pages/Generador';
import TimetableGrid from './pages/TimetableGrid';

function Sidebar() {
  const location = useLocation();
  const getClase = (path) => 
    `flex items-center gap-3 px-6 py-4 transition-colors ${location.pathname === path ? 'bg-slate-800 text-white border-l-4 border-blue-500' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`;

  return (
    <div className="w-64 bg-slate-900 min-h-screen text-white flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold text-white">TSU Optimizer</h1>
        <p className="text-xs text-slate-400 mt-1">Motor DEAP</p>
      </div>
      <nav className="flex-1 mt-6">
        <Link to="/" className={getClase('/')}><Settings size={20} /> Configuración</Link>
        <Link to="/generador" className={getClase('/generador')}><Play size={20} /> Generador IA</Link>
        <Link to="/resultados" className={getClase('/resultados')}><Calendar size={20} /> Resultados</Link>
      </nav>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-gray-50 font-sans">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Configuracion />} />
            <Route path="/generador" element={<Generador />} />
            <Route path="/resultados" element={<TimetableGrid />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}