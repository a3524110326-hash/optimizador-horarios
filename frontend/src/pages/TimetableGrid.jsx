import { CheckCircle2, MapPin, FlaskConical, User, Printer } from 'lucide-react';

const bloquesHora = [
  "07:00 - 07:50", "07:50 - 08:40", "08:40 - 09:30",
  "10:00 - 10:50", "10:50 - 11:40", "11:40 - 12:30",
  "12:30 - 13:20", "13:20 - 14:10",
];
const dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];

// El receso va entre el bloque 3 y el 4 (09:30 - 10:00)
const INDICE_RECESO = 3;

// Colores por materia (las clases van completas para que Tailwind las detecte)
const colores = {
  azul:    { caja: "bg-blue-50 border-blue-500",       titulo: "text-blue-900",    detalle: "text-blue-700" },
  verde:   { caja: "bg-emerald-50 border-emerald-500", titulo: "text-emerald-900", detalle: "text-emerald-700" },
  violeta: { caja: "bg-violet-50 border-violet-500",   titulo: "text-violet-900",  detalle: "text-violet-700" },
  ambar:   { caja: "bg-amber-50 border-amber-500",     titulo: "text-amber-900",   detalle: "text-amber-700" },
  rosa:    { caja: "bg-rose-50 border-rose-500",       titulo: "text-rose-900",    detalle: "text-rose-700" },
};

// DATOS DE EJEMPLO (luego los reemplazamos por los del backend).
// dia: 0 = Lunes ... 4 = Viernes
// inicio: posición en bloquesHora (0 = 07:00)
// duracion: cuántos bloques seguidos dura
const clases = [
  { dia: 0, inicio: 0, duracion: 2, materia: "Álgebra Lineal", lugar: "Aula 1",        profesor: "Hernández", lab: false, color: "azul" },
  { dia: 3, inicio: 0, duracion: 2, materia: "Álgebra Lineal", lugar: "Aula 1",        profesor: "Hernández", lab: false, color: "azul" },
  { dia: 2, inicio: 0, duracion: 3, materia: "Programación",   lugar: "Laboratorio A", profesor: "López",     lab: true,  color: "verde" },
  { dia: 4, inicio: 3, duracion: 3, materia: "Programación",   lugar: "Laboratorio A", profesor: "López",     lab: true,  color: "verde" },
];

// Convierte la posición del bloque a la fila del grid (saltando la fila del receso)
const filaDe = (indice) => (indice >= INDICE_RECESO ? indice + 2 : indice + 1);

const horaInicio = (i) => bloquesHora[i].split(" - ")[0];
const horaFin = (i) => bloquesHora[i].split(" - ")[1];

const COLUMNAS = "grid-cols-[110px_repeat(5,minmax(0,1fr))]";
const FILAS = "56px 56px 56px 28px 56px 56px 56px 56px 56px";

export default function TimetableGrid() {
  const totalBloques = clases.reduce((suma, c) => suma + c.duracion, 0);

  return (
    <div>
      {/* Encabezado */}
      <div className="mb-6 flex flex-wrap justify-between items-center gap-4 bg-white p-5 rounded-xl shadow-sm border border-gray-200">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Horarios Generados</h1>
          <p className="flex items-center gap-1.5 text-sm text-emerald-600 font-medium mt-1">
            <CheckCircle2 size={16} /> 0 empalmes encontrados
            <span className="text-gray-400 font-normal">· {totalBloques} bloques por semana</span>
          </p>
        </div>

        <div className="flex gap-3">
          <select className="bg-gray-50 border border-gray-200 text-gray-700 py-2 px-4 rounded-lg outline-none focus:ring-2 focus:ring-blue-500">
            <option>Grupo: 1º A - TSU Software</option>
            <option>Grupo: 4º A - TSU Software</option>
          </select>
          <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white py-2 px-5 rounded-lg font-medium transition-colors">
            <Printer size={18} /> Imprimir PDF
          </button>
        </div>
      </div>

      {/* Tabla de horario */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-x-auto">
        <div className="min-w-[800px]">
          {/* Días */}
          <div className={`grid ${COLUMNAS} bg-slate-800 text-white`}>
            <div className="py-3 px-2 text-center text-sm font-semibold border-r border-slate-700">Horario</div>
            {dias.map((dia) => (
              <div key={dia} className="py-3 px-2 text-center text-sm font-semibold border-r border-slate-700 last:border-r-0">
                {dia}
              </div>
            ))}
          </div>

          {/* Cuadrícula: celdas de fondo + tarjetas encima */}
          <div className={`grid ${COLUMNAS}`} style={{ gridTemplateRows: FILAS }}>
            {/* Celdas de fondo */}
            {bloquesHora.map((hora, i) => (
              <div key={`fila-${hora}`} className="contents">
                <div
                  className="flex items-center justify-center border-r border-b border-gray-100 bg-gray-50/60 text-xs font-medium text-gray-600"
                  style={{ gridRow: filaDe(i), gridColumn: 1 }}
                >
                  {hora}
                </div>
                {dias.map((dia, d) => (
                  <div
                    key={`${hora}-${dia}`}
                    className="border-r border-b border-gray-100 last:border-r-0"
                    style={{ gridRow: filaDe(i), gridColumn: d + 2 }}
                  />
                ))}
              </div>
            ))}

            {/* Fila de receso */}
            <div
              className="flex items-center justify-center border-b border-gray-100 bg-gray-100 text-xs font-medium text-gray-500"
              style={{ gridRow: INDICE_RECESO + 1, gridColumn: "1 / -1" }}
            >
              Receso · 09:30 - 10:00
            </div>

            {/* Tarjetas de materia (un solo bloque por clase) */}
            {clases.map((c, idx) => {
              const estilo = colores[c.color];
              const Icono = c.lab ? FlaskConical : MapPin;
              const filaInicio = filaDe(c.inicio);
              const filaFin = filaDe(c.inicio + c.duracion - 1) + 1;

              return (
                <div
                  key={idx}
                  className="p-1.5 z-10"
                  style={{ gridRow: `${filaInicio} / ${filaFin}`, gridColumn: c.dia + 2 }}
                >
                  <div className={`h-full rounded-md border-l-4 p-2.5 ${estilo.caja}`}>
                    <p className={`text-sm font-bold leading-tight ${estilo.titulo}`}>{c.materia}</p>
                    <p className={`text-xs mt-0.5 ${estilo.detalle}`}>
                      {horaInicio(c.inicio)} - {horaFin(c.inicio + c.duracion - 1)}
                    </p>
                    <p className={`flex items-center gap-1 text-xs mt-2 ${estilo.detalle}`}>
                      <Icono size={12} /> {c.lugar}
                    </p>
                    <p className={`flex items-center gap-1 text-xs mt-0.5 ${estilo.detalle}`}>
                      <User size={12} /> Prof. {c.profesor}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
