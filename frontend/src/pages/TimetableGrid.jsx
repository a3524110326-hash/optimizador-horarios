import { useState } from 'react';
import { Link } from 'react-router-dom';

import {
  CheckCircle2,
  AlertTriangle,
  MapPin,
  FlaskConical,
  User,
  Printer
} from 'lucide-react';

import { DIAS, BLOQUES, leerResultado } from '../api';


// ============================================================
// CONFIGURACIÓN DEL HORARIO
// ============================================================

// El receso va entre el bloque 3 y el 4 (09:30 - 10:00)
const INDICE_RECESO = 3;


// ============================================================
// PALETA DE COLORES
// ============================================================

const paleta = [
  {
    caja: "bg-blue-50 border-blue-500",
    titulo: "text-blue-900",
    detalle: "text-blue-700"
  },
  {
    caja: "bg-emerald-50 border-emerald-500",
    titulo: "text-emerald-900",
    detalle: "text-emerald-700"
  },
  {
    caja: "bg-violet-50 border-violet-500",
    titulo: "text-violet-900",
    detalle: "text-violet-700"
  },
  {
    caja: "bg-amber-50 border-amber-500",
    titulo: "text-amber-900",
    detalle: "text-amber-700"
  },
  {
    caja: "bg-rose-50 border-rose-500",
    titulo: "text-rose-900",
    detalle: "text-rose-700"
  },
  {
    caja: "bg-cyan-50 border-cyan-500",
    titulo: "text-cyan-900",
    detalle: "text-cyan-700"
  }
];


// ============================================================
// FUNCIONES AUXILIARES
// ============================================================

const filaDe = (indice) =>
  indice >= INDICE_RECESO
    ? indice + 2
    : indice + 1;

const horaInicio = (i) =>
  BLOQUES[i].split("-")[0];

const horaFin = (i) =>
  BLOQUES[i].split("-")[1];

const nombreLugar = (l) =>
  l.replace(/\_/g, " ");


// ============================================================
// CONFIGURACIÓN DE LA TABLA
// ============================================================

const COLUMNAS =
  "grid-cols-[110px_repeat(5,minmax(0,1fr))]";

const FILAS =
  "64px 64px 64px 28px 64px 64px 64px 64px 64px 64px";


// ============================================================
// ESTILOS PARA IMPRESIÓN
// ============================================================

const estilosImpresion = `
  @page {
    size: landscape;
    margin: 8mm;
  }

  @media print {

    html,
    body {
      width: 100% !important;
      height: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      background: white !important;
      overflow: visible !important;
    }

    body {
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    /*
      Ocultamos toda la aplicación.
      Solamente se mostrará .horario-impresion.
    */
    body * {
      visibility: hidden !important;
    }

    .horario-impresion,
    .horario-impresion * {
      visibility: visible !important;
    }

    .horario-impresion {
      position: absolute !important;
      left: 0 !important;
      top: 0 !important;

      width: 100% !important;
      max-width: none !important;

      margin: 0 !important;
      padding: 0 !important;

      background: white !important;
    }

    /*
      Encabezado que solamente aparece al imprimir.
    */
    .encabezado-impresion {
      display: block !important;
      margin-bottom: 12px !important;
      text-align: center !important;
    }

    /*
      Quitamos scroll y límites de ancho.
    */
    .tabla-contenedor {
      width: 100% !important;
      min-width: 0 !important;
      max-width: none !important;

      overflow: visible !important;

      border: 1px solid #d1d5db !important;
      border-radius: 0 !important;
      box-shadow: none !important;
    }

    .tabla {
      width: 100% !important;
      min-width: 0 !important;
      max-width: none !important;
    }

    /*
      La primera columna y los días se ajustan
      al ancho disponible.
    */
    .tabla .grid {
      width: 100% !important;
    }

    /*
      Tamaños de texto para que todo quepa.
    */
    .celda-horario {
      font-size: 9px !important;
    }

    .materia {
      font-size: 9px !important;
    }

    .detalle {
      font-size: 8px !important;
    }

    .receso {
      font-size: 8px !important;
    }

    /*
      Mantener colores de fondo y bordes.
    */
    .horario-impresion * {
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
  }

  @media screen {

    .encabezado-impresion {
      display: none;
    }
  }
`;


// ============================================================
// DETECTAR EMPALMES
// ============================================================

// Busca empalmes igual que el algoritmo:
// mismo espacio, mismo profesor o mismo grupo
// en el mismo día y bloque.

function detectarEmpalmes(horario) {

  const tipos = [
    'espacio',
    'profesor',
    'grupo'
  ];

  const mapas = {
    espacio: {},
    profesor: {},
    grupo: {}
  };


  horario.forEach((g) => {

    tipos.forEach((tipo) => {

      const llave =
        `${g[tipo]}|${g.dia}|${g.bloque}`;

      if (!mapas[tipo][llave]) {
        mapas[tipo][llave] = [];
      }

      mapas[tipo][llave].push(g);

    });

  });


  const lista = [];


  tipos.forEach((tipo) => {

    Object.values(
      mapas[tipo]
    ).forEach((genes) => {

      if (genes.length > 1) {

        lista.push({
          tipo,
          dia: genes[0].dia,
          bloque: genes[0].bloque,
          valor: genes[0][tipo],
          genes
        });

      }

    });

  });


  return lista;
}


// ============================================================
// DESCRIBIR EMPALME
// ============================================================

function describir(e) {

  const grupos = [
    ...new Set(
      e.genes.map((g) => g.grupo)
    )
  ].join(', ');

  const n = e.genes.length;


  if (e.tipo === 'profesor') {

    return (
      `${e.valor} tiene ${n} clases al mismo tiempo ` +
      `(grupos ${grupos}).`
    );

  }


  if (e.tipo === 'espacio') {

    return (
      `${nombreLugar(e.valor)} está ocupada por ` +
      `${n} clases al mismo tiempo (grupos ${grupos}).`
    );

  }


  return (
    `El grupo ${e.valor} tiene ${n} materias ` +
    `al mismo tiempo ` +
    `(${e.genes.map((g) => g.materia).join(' y ')}).`
  );
}


// ============================================================
// CONSTRUIR CLASES
// ============================================================

// Convierte los genes sueltos (1 por hora)
// en tarjetas con bloques consecutivos fusionados.

function construirClases(
  horario,
  grupo,
  laboratorios,
  conflictivos
) {

  const genes = horario

    .filter(
      (g) => g.grupo === grupo
    )

    .map(
      (g) => ({
        ...g,

        i: BLOQUES.indexOf(
          g.bloque
        ),

        d: DIAS.indexOf(
          g.dia
        ),

        orig: g
      })
    )

    .filter(
      (g) =>
        g.i >= 0 &&
        g.d >= 0
    )

    .sort(
      (a, b) =>
        a.d - b.d ||
        a.i - b.i
    );


  const clases = [];

  let actual = null;


  for (const g of genes) {

    const mismaClase =
      actual &&
      actual.dia === g.d &&
      actual.materia === g.materia &&
      actual.profesor === g.profesor &&
      actual.lugar === g.espacio;


    const siguiente =
      mismaClase &&
      g.i ===
        actual.inicio +
        actual.duracion &&
      g.i !== INDICE_RECESO;


    const repetido =
      mismaClase &&
      g.i ===
        actual.inicio +
        actual.duracion -
        1;


    if (siguiente) {

      actual.duracion += 1;

      if (
        conflictivos.has(
          g.orig
        )
      ) {

        actual.conflicto = true;

      }

    }

    else if (repetido) {

      actual.conflicto = true;

    }

    else {

      actual = {

        dia: g.d,

        inicio: g.i,

        duracion: 1,

        materia: g.materia,

        lugar: g.espacio,

        profesor: g.profesor,

        lab: laboratorios.includes(
          g.espacio
        ),

        conflicto:
          conflictivos.has(
            g.orig
          )
      };


      clases.push(
        actual
      );

    }

  }


  return clases;
}


// ============================================================
// COMPONENTE
// ============================================================

export default function TimetableGrid() {

  const guardado =
    leerResultado();


  const grupos =
    guardado?.entrada?.grupos ?? [];


  const [
    grupo,
    setGrupo
  ] = useState(
    grupos[0] ?? ''
  );


  // ==========================================================
  // SIN RESULTADO
  // ==========================================================

  if (!guardado) {

    return (

      <div className="p-8">

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-10 text-center">

          <h1 className="text-2xl font-bold text-gray-800">
            Aún no hay horarios
          </h1>

          <p className="text-gray-500 mt-2">
            Genera uno para ver aquí el resultado.
          </p>

          <Link
            to="/generador"
            className="
              inline-block
              mt-5
              bg-blue-600
              hover:bg-blue-700
              text-white
              py-2
              px-6
              rounded-lg
              font-medium
              transition-colors
            "
          >
            Ir al generador
          </Link>

        </div>

      </div>

    );

  }


  // ==========================================================
  // DATOS DEL RESULTADO
  // ==========================================================

  const {
    entrada,
    resultado
  } = guardado;


  const listaEmpalmes =
    detectarEmpalmes(
      resultado.horario
    );


  const conflictivos =
    new Set(
      listaEmpalmes.flatMap(
        (e) => e.genes
      )
    );


  const empalmes =
    listaEmpalmes.reduce(
      (suma, e) =>
        suma +
        e.genes.length -
        1,
      0
    );


  // ==========================================================
  // COLORES DE MATERIAS
  // ==========================================================

  const nombresMaterias =
    [
      ...new Set(
        resultado.horario.map(
          (g) => g.materia
        )
      )
    ];


  const colorDe =
    (materia) =>
      paleta[
        nombresMaterias.indexOf(
          materia
        ) %
        paleta.length
      ];


  // ==========================================================
  // CLASES DEL GRUPO
  // ==========================================================

  const clases =
    construirClases(
      resultado.horario,
      grupo,
      entrada.laboratorios ?? [],
      conflictivos
    );


  const totalBloques =
    clases.reduce(
      (suma, c) =>
        suma + c.duracion,
      0
    );


  // ==========================================================
  // RENDER
  // ==========================================================

  return (

    <>

      <style>
        {estilosImpresion}
      </style>


      <div className="p-8">

        {/* ==================================================
            ENCABEZADO NORMAL
        ================================================== */}

        <div
          className="
            mb-6
            flex
            flex-wrap
            justify-between
            items-center
            gap-4
            bg-white
            p-5
            rounded-xl
            shadow-sm
            border
            border-gray-200
          "
        >

          <div>

            <h1 className="text-2xl font-bold text-gray-800">
              Horarios Generados
            </h1>


            {empalmes === 0 ? (

              <p
                className="
                  flex
                  items-center
                  gap-1.5
                  text-sm
                  text-emerald-600
                  font-medium
                  mt-1
                "
              >

                <CheckCircle2 size={16} />

                0 empalmes encontrados

                <span
                  className="
                    text-gray-400
                    font-normal
                  "
                >
                  · {totalBloques} bloques por semana
                </span>

              </p>

            ) : (

              <p
                className="
                  flex
                  items-center
                  gap-1.5
                  text-sm
                  text-amber-600
                  font-medium
                  mt-1
                "
              >

                <AlertTriangle size={16} />

                {empalmes}{' '}

                {empalmes === 1
                  ? 'empalme encontrado'
                  : 'empalmes encontrados'
                }

                <span
                  className="
                    text-gray-400
                    font-normal
                  "
                >
                  · {totalBloques} bloques por semana
                </span>

              </p>

            )}

          </div>


          {/* ================================================
              CONTROLES
          ================================================= */}

          <div className="flex gap-3">

            <select
              value={grupo}
              onChange={(e) =>
                setGrupo(
                  e.target.value
                )
              }
              className="
                bg-gray-50
                border
                border-gray-200
                text-gray-700
                py-2
                px-4
                rounded-lg
                outline-none
                focus:ring-2
                focus:ring-blue-500
              "
            >

              {grupos.map(
                (g) => (

                  <option
                    key={g}
                    value={g}
                  >
                    Grupo: {g}
                  </option>

                )
              )}

            </select>


            <button
              onClick={() =>
                window.print()
              }
              className="
                flex
                items-center
                gap-2
                bg-blue-600
                hover:bg-blue-700
                text-white
                py-2
                px-5
                rounded-lg
                font-medium
                transition-colors
              "
            >

              <Printer size={18} />

              Imprimir PDF

            </button>

          </div>

        </div>


        {/* ==================================================
            ENCABEZADO PARA PDF
        ================================================== */}

        <div className="horario-impresion">

          <div
            className="
              encabezado-impresion
              mb-4
              text-center
            "
          >

            <h1
              className="
                text-2xl
                font-bold
                text-gray-800
              "
            >
              Horario académico
            </h1>


            <p
              className="
                text-lg
                font-semibold
                text-gray-600
              "
            >
              Grupo {grupo}
            </p>


            <p
              className="
                text-sm
                text-gray-500
              "
            >

              {empalmes === 0
                ? '0 empalmes encontrados'
                : `${empalmes} ${
                    empalmes === 1
                      ? 'empalme encontrado'
                      : 'empalmes encontrados'
                  }`
              }

              {' · '}

              {totalBloques}
              {' '}
              bloques por semana

            </p>

          </div>


          {/* ==================================================
              MENSAJE DE EMPALMES
          ================================================== */}

          {empalmes > 0 && (

            <div
              className="
                mb-6
                bg-amber-50
                border
                border-amber-200
                rounded-xl
                p-5
              "
            >

              <h2
                className="
                  flex
                  items-center
                  gap-2
                  font-semibold
                  text-amber-900
                "
              >

                <AlertTriangle size={18} />

                Dónde están los empalmes

              </h2>


              <ul
                className="
                  mt-3
                  space-y-3
                "
              >

                {listaEmpalmes.map(
                  (e, idx) => (

                    <li
                      key={idx}
                      className="
                        text-sm
                        text-amber-900
                      "
                    >

                      <p>

                        <span
                          className="
                            font-semibold
                          "
                        >
                          {e.dia}
                          {' · '}
                          {e.bloque.replace(
                            "-",
                            " - "
                          )}
                        </span>

                        :
                        {' '}
                        {describir(e)}

                      </p>


                      <div
                        className="
                          flex
                          flex-wrap
                          gap-2
                          mt-1.5
                        "
                      >

                        {[
                          ...new Set(
                            e.genes.map(
                              (g) =>
                                g.grupo
                            )
                          )
                        ].map(
                          (g) => (

                            <button
                              key={g}
                              onClick={() =>
                                setGrupo(g)
                              }
                              className="
                                px-2.5
                                py-0.5
                                rounded-full
                                bg-white
                                border
                                border-amber-300
                                text-xs
                                font-medium
                                hover:bg-amber-100
                                transition-colors
                              "
                            >
                              Ver grupo {g}
                            </button>

                          )
                        )}

                      </div>

                    </li>

                  )
                )}

              </ul>

            </div>

          )}


          {/* ==================================================
              TABLA DEL HORARIO
          ================================================== */}

          <div
            className="
              tabla-contenedor
              bg-white
              rounded-xl
              shadow-sm
              border
              border-gray-200
              overflow-x-auto
            "
          >

            <div
              className="
                tabla
                min-w-[800px]
              "
            >

              {/* ============================================
                  ENCABEZADO DE DÍAS
              ============================================ */}

              <div
                className={`
                  grid
                  ${COLUMNAS}
                  bg-slate-800
                  text-white
                `}
              >

                <div
                  className="
                    py-3
                    px-2
                    text-center
                    text-sm
                    font-semibold
                    border-r
                    border-slate-700
                  "
                >
                  Horario
                </div>


                {DIAS.map(
                  (dia) => (

                    <div
                      key={dia}
                      className="
                        py-3
                        px-2
                        text-center
                        text-sm
                        font-semibold
                        border-r
                        border-slate-700
                        last:border-r-0
                      "
                    >
                      {dia}
                    </div>

                  )
                )}

              </div>


              {/* ============================================
                  CUERPO DE LA TABLA
              ============================================ */}

              <div
                className={`
                  grid
                  ${COLUMNAS}
                `}
                style={{
                  gridTemplateRows:
                    FILAS
                }}
              >

                {/* ==========================================
                    BLOQUES DE HORARIO
                ========================================== */}

                {BLOQUES.map(
                  (hora, i) => (

                    <div
                      key={`fila-${hora}`}
                      className="contents"
                    >

                      {/* Hora */}

                      <div
                        className="
                          celda-horario
                          flex
                          items-center
                          justify-center
                          border-r
                          border-b
                          border-gray-100
                          bg-gray-50/60
                          text-xs
                          font-medium
                          text-gray-600
                        "
                        style={{
                          gridRow:
                            filaDe(i),

                          gridColumn:
                            1
                        }}
                      >

                        {hora.replace(
                          "-",
                          " - "
                        )}

                      </div>


                      {/* Celdas de cada día */}

                      {DIAS.map(
                        (dia, d) => (

                          <div
                            key={`${hora}-${dia}`}
                            className="
                              border-r
                              border-b
                              border-gray-100
                              last:border-r-0
                            "
                            style={{
                              gridRow:
                                filaDe(i),

                              gridColumn:
                                d + 2
                            }}
                          />

                        )
                      )}

                    </div>

                  )
                )}


                {/* ==========================================
                    RECESO
                ========================================== */}

                <div
                  className="
                    receso
                    flex
                    items-center
                    justify-center
                    border-b
                    border-gray-100
                    bg-gray-100
                    text-xs
                    font-medium
                    text-gray-500
                  "
                  style={{
                    gridRow:
                      INDICE_RECESO + 1,

                    gridColumn:
                      "1 / -1"
                  }}
                >

                  Receso · 09:30 - 10:00

                </div>


                {/* ==========================================
                    CLASES
                ========================================== */}

                {clases.map(
                  (c, idx) => {

                    const estilo =
                      colorDe(
                        c.materia
                      );


                    const Icono =
                      c.lab
                        ? FlaskConical
                        : MapPin;


                    // Si dos clases del grupo
                    // caen a la vez, se muestran lado a lado.

                    const solapadas =
                      clases.filter(
                        (o) =>
                          o !== c &&
                          o.dia === c.dia &&
                          o.inicio <
                            c.inicio +
                            c.duracion &&
                          c.inicio <
                            o.inicio +
                            o.duracion
                      );


                    const total =
                      solapadas.length +
                      1;


                    const carril =
                      solapadas.filter(
                        (o) =>
                          clases.indexOf(
                            o
                          ) < idx
                      ).length;


                    const aviso =
                      c.conflicto
                        ? ' ring-2 ring-red-500'
                        : '';


                    const alerta =
                      c.conflicto && (
                        <AlertTriangle
                          size={12}
                          className="
                            inline
                            -mt-0.5
                            mr-1
                            text-red-600
                          "
                        />
                      );


                    return (

                      <div
                        key={idx}
                        className="
                          p-1.5
                          z-10
                        "
                        style={{

                          gridRow:
                            `${filaDe(
                              c.inicio
                            )} / ${
                              filaDe(
                                c.inicio +
                                c.duracion -
                                1
                              ) + 1
                            }`,

                          gridColumn:
                            c.dia + 2,

                          ...(total > 1
                            ? {
                                width:
                                  `${100 / total}%`,

                                marginLeft:
                                  `${(
                                    carril *
                                    100
                                  ) / total}%`
                              }
                            : {})
                        }}
                      >

                        {/* ==================================
                            CLASE DE UN BLOQUE
                        ================================== */}

                        {c.duracion === 1 ? (

                          <div
                            className={`
                              h-full
                              overflow-hidden
                              rounded-md
                              border-l-4
                              px-2
                              py-1
                              ${estilo.caja}
                              ${aviso}
                            `}
                            title={`
                              ${c.materia}
                              ·
                              ${nombreLugar(c.lugar)}
                              ·
                              ${c.profesor}
                            `}
                          >

                            <p
                              className={`
                                materia
                                text-xs
                                font-bold
                                truncate
                                ${estilo.titulo}
                              `}
                            >

                              {alerta}

                              {c.materia}

                            </p>


                            <p
                              className={`
                                detalle
                                flex
                                items-center
                                gap-1
                                text-[11px]
                                truncate
                                ${estilo.detalle}
                              `}
                            >

                              <Icono
                                size={11}
                                className="shrink-0"
                              />

                              {nombreLugar(
                                c.lugar
                              )}

                              {' · '}

                              {c.profesor}

                            </p>

                          </div>

                        ) : (

                          /* =================================
                              CLASE DE VARIOS BLOQUES
                          ================================= */

                          <div
                            className={`
                              h-full
                              overflow-hidden
                              rounded-md
                              border-l-4
                              p-2.5
                              ${estilo.caja}
                              ${aviso}
                            `}
                          >

                            <p
                              className={`
                                materia
                                text-sm
                                font-bold
                                leading-tight
                                ${estilo.titulo}
                              `}
                            >

                              {alerta}

                              {c.materia}

                            </p>


                            <p
                              className={`
                                detalle
                                text-xs
                                mt-0.5
                                ${estilo.detalle}
                              `}
                            >

                              {horaInicio(
                                c.inicio
                              )}

                              {' - '}

                              {horaFin(
                                c.inicio +
                                c.duracion -
                                1
                              )}

                            </p>


                            <p
                              className={`
                                detalle
                                flex
                                items-center
                                gap-1
                                text-xs
                                mt-2
                                ${estilo.detalle}
                              `}
                            >

                              <Icono
                                size={12}
                              />

                              {nombreLugar(
                                c.lugar
                              )}

                            </p>


                            <p
                              className={`
                                detalle
                                flex
                                items-center
                                gap-1
                                text-xs
                                mt-0.5
                                ${estilo.detalle}
                              `}
                            >

                              <User
                                size={12}
                              />

                              {c.profesor}

                            </p>

                          </div>

                        )}

                      </div>

                    );

                  }
                )}

              </div>

            </div>

          </div>

        </div>

      </div>

    </>

  );
}