export default function TimetableGrid() {
  const bloquesHora = [
    "07:00 - 07:50", "07:50 - 08:40", "08:40 - 09:30", 
    "10:00 - 10:50", "10:50 - 11:40", "11:40 - 12:30", 
    "12:30 - 13:20", "13:20 - 14:10"
  ];
  const dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];

  return (
    <div className="p-8">
      <div className="mb-6 flex justify-between items-center bg-white p-5 rounded-xl shadow-sm border border-gray-200">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Horarios Generados</h1>
          <p className="text-sm text-emerald-600 font-medium mt-1">✅ 0 Empalmes encontrados</p>
        </div>
        
        <div className="flex gap-4">
          <select className="bg-gray-50 border border-gray-200 text-gray-700 py-2 px-4 rounded-lg outline-none">
            <option>Grupo: 1º A - TSU Software</option>
            <option>Grupo: 4º A - TSU Software</option>
          </select>
          <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-lg font-medium">
            Imprimir PDF
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="grid grid-cols-6 bg-slate-800 text-white">
          <div className="py-3 px-2 text-center font-semibold border-r border-slate-700">Horario</div>
          {dias.map(dia => (
            <div key={dia} className="py-3 px-2 text-center font-semibold border-r border-slate-700">{dia}</div>
          ))}
        </div>

        <div className="divide-y divide-gray-100">
          {bloquesHora.map((hora) => (
            <div key={hora} className="grid grid-cols-6">
              <div className="py-3 px-2 flex items-center justify-center border-r border-gray-100 bg-gray-50/50">
                <span className="text-sm font-medium text-gray-600">{hora}</span>
              </div>

              {/* Ejemplo estático de materias */}
              <div className="p-2 border-r border-gray-100">
                <div className="h-full bg-blue-50 border-l-4 border-blue-500 rounded p-2">
                  <p className="text-xs font-bold text-blue-800">Álgebra Lineal</p>
                  <p className="text-[10px] text-blue-600 mt-1">📍 Aula 1 • Prof. Hernández</p>
                </div>
              </div>
              <div className="p-2 border-r border-gray-100"></div>
              <div className="p-2 border-r border-gray-100">
                 <div className="h-full bg-emerald-50 border-l-4 border-emerald-500 rounded p-2">
                  <p className="text-xs font-bold text-emerald-800">Programación</p>
                  <p className="text-[10px] text-emerald-600 mt-1">💻 Lab A • Prof. López</p>
                </div>
              </div>
              <div className="p-2 border-r border-gray-100"></div>
              <div className="p-2 border-r border-gray-100"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}