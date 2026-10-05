import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

export default function Generador() {
  const [procesando, setProcesando] = useState(false);
  const navigate = useNavigate();

  const ejecutarIA = () => {
    setProcesando(true);
    // Simulación de llamada a tu API Python
    setTimeout(() => {
      setProcesando(false);
      navigate('/resultados');
    }, 3000);
  };

  return (
    <div className="flex h-full items-center justify-center p-8">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="bg-slate-800 p-8 text-center">
          <h1 className="text-3xl font-bold text-white mb-2">Motor de Optimización DEAP</h1>
          <p className="text-slate-300">Resolución de Empalmes Evolutiva</p>
        </div>

        <div className="p-8 text-center">
          <div className="flex justify-center gap-8 mb-8">
            <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 min-w-[150px]">
              <p className="text-3xl font-bold text-blue-900">8</p>
              <p className="text-sm text-blue-700 font-medium">Grupos TSU</p>
            </div>
            <div className="bg-emerald-50 p-4 rounded-xl border border-emerald-100 min-w-[150px]">
              <p className="text-3xl font-bold text-emerald-900">4 / 2</p>
              <p className="text-sm text-emerald-700 font-medium">Aulas / Labs</p>
            </div>
          </div>

          {!procesando ? (
            <button 
              onClick={ejecutarIA}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white text-lg font-bold py-4 rounded-xl shadow-md transition-all"
            >
              ▶ Iniciar Optimización
            </button>
          ) : (
            <div className="bg-gray-50 border border-gray-200 p-6 rounded-xl flex flex-col items-center">
              <Loader2 className="w-10 h-10 text-blue-600 animate-spin mb-4" />
              <p className="font-bold text-gray-800">Evaluando generaciones...</p>
              <p className="text-sm text-gray-500 mt-1">Calculando cruzas y mutaciones para reducir empalmes a cero.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}