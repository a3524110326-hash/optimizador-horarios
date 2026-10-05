import { useState } from 'react';

export default function Configuracion() {
  const [materias, setMaterias] = useState([
    { id: 1, clave: 'MAT101', nombre: 'Álgebra Lineal', horas: 4, lab: false },
    { id: 2, clave: 'PRG101', nombre: 'Fundamentos de Programación', horas: 6, lab: true }
  ]);

  return (
    <div className="p-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Configuración de Catálogos</h1>
        
        <div className="flex border-b border-gray-200 mb-6">
          <button className="px-6 py-3 border-b-2 border-blue-600 text-blue-600 font-medium">Materias</button>
          <button className="px-6 py-3 text-gray-500 hover:text-gray-700 font-medium">Profesores</button>
          <button className="px-6 py-3 text-gray-500 hover:text-gray-700 font-medium">Grupos y Espacios</button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1 bg-white p-6 rounded-xl shadow-sm border border-gray-200 h-fit">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Nueva Materia</h2>
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Clave</label>
                <input type="text" placeholder="Ej. BD201" className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:border-blue-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                <input type="text" placeholder="Ej. Bases de Datos" className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:border-blue-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Horas Semanales</label>
                <input type="number" defaultValue="4" className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:border-blue-500" />
              </div>
              <div className="flex items-center mt-2 bg-blue-50 p-3 rounded-lg border border-blue-100">
                <input type="checkbox" id="reqLab" className="h-4 w-4 text-blue-600 rounded border-gray-300" />
                <label htmlFor="reqLab" className="ml-2 block text-sm text-blue-800 font-medium">
                  Requiere Laboratorio
                </label>
              </div>
              <button type="button" className="w-full bg-slate-800 hover:bg-slate-900 text-white font-medium py-2 rounded-lg mt-4">
                Guardar Materia
              </button>
            </form>
          </div>

          <div className="md:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <table className="w-full text-left">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-sm font-semibold text-gray-600">Materia</th>
                  <th className="px-6 py-3 text-sm font-semibold text-gray-600">Horas</th>
                  <th className="px-6 py-3 text-sm font-semibold text-gray-600">Requisito</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {materias.map((m) => (
                  <tr key={m.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <p className="font-medium text-gray-800">{m.nombre}</p>
                      <p className="text-xs text-gray-500">{m.clave}</p>
                    </td>
                    <td className="px-6 py-4 text-gray-700">{m.horas} hrs</td>
                    <td className="px-6 py-4">
                      {m.lab 
                        ? <span className="bg-emerald-100 text-emerald-800 px-2 py-1 rounded text-xs font-bold">💻 Laboratorio</span>
                        : <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs font-bold">📍 Aula Teórica</span>
                      }
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}