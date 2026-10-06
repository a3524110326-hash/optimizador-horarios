import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Play, Loader2, AlertCircle } from 'lucide-react';
import { obtenerCatalogo, generarHorario, guardarResultado, mensajeDeError } from '../api';

export default function Generador() {
  const navigate = useNavigate();
  const [catalogo, setCatalogo] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  // Al abrir la pantalla, leemos el catálogo real desde Supabase (vía backend)
  useEffect(() => {
    obtenerCatalogo()
      .then(setCatalogo)
      .catch((e) => setError(mensajeDeError(e)));
  }, []);

  const incompleto =
    catalogo &&
    (!catalogo.grupos.length ||
      !catalogo.aulas_teoricas.length ||
      !catalogo.laboratorios.length ||
      !Object.keys(catalogo.materias).length);

  async function iniciar() {
    setCargando(true);
    setError('');
    try {
      const resultado = await generarHorario();
      guardarResultado(catalogo, resultado);
      navigate('/resultados');
    } catch (e) {
      setError(mensajeDeError(e));
    } finally {
      setCargando(false);
    }
  }

  return (
    <div className="flex items-center justify-center min-h-[80vh] p-8">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden">
        <div className="bg-slate-800 text-center px-6 py-8">
          <h1 className="text-3xl font-bold text-white">Motor de Optimización DEAP</h1>
          <p className="text-slate-300 mt-2">Resolución de empalmes evolutiva</p>
        </div>

        <div className="p-8">
          <div className="flex justify-center gap-4 mb-8">
            <div className="bg-blue-50 border border-blue-100 rounded-xl px-6 py-4 text-center">
              <p className="text-3xl font-bold text-blue-900">{catalogo ? catalogo.grupos.length : '—'}</p>
              <p className="text-sm font-medium text-blue-700">Grupos TSU</p>
            </div>
            <div className="bg-emerald-50 border border-emerald-100 rounded-xl px-6 py-4 text-center">
              <p className="text-3xl font-bold text-emerald-900">
                {catalogo ? `${catalogo.aulas_teoricas.length} / ${catalogo.laboratorios.length}` : '— / —'}
              </p>
              <p className="text-sm font-medium text-emerald-700">Aulas / Laboratorios</p>
            </div>
          </div>

          <button
            onClick={iniciar}
            disabled={cargando || !catalogo || incompleto}
            className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed text-white text-lg font-semibold py-4 rounded-xl transition-colors"
          >
            {cargando ? (
              <>
                <Loader2 size={22} className="animate-spin" /> Optimizando… puede tardar un par de minutos
              </>
            ) : (
              <>
                <Play size={22} /> Iniciar optimización
              </>
            )}
          </button>

          {incompleto && (
            <p className="mt-4 text-sm text-amber-700 bg-amber-50 border border-amber-100 rounded-lg p-3">
              Falta información en la base de datos (grupos, materias o espacios). Revísala en Supabase.
            </p>
          )}

          {error && (
            <p className="mt-4 flex items-start gap-2 text-sm text-red-700 bg-red-50 border border-red-100 rounded-lg p-3">
              <AlertCircle size={18} className="shrink-0 mt-0.5" /> {error}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
