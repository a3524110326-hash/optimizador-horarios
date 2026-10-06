import { useState, useEffect } from 'react';



import {

  MapPin,

  FlaskConical,

  RefreshCw,

  Loader2,

  AlertCircle,

  Plus,

  X,

} from 'lucide-react';



import {

  obtenerCatalogo,

  obtenerOpcionesCatalogo,

  crearProfesor,

  crearMateria,

  crearGrupo,

  crearEspacio,

  mensajeDeError,

  DIAS,

  BLOQUES,

} from '../api';





// ============================================================

// CONFIGURACIÓN

// ============================================================



const HORAS_DISPONIBLES = DIAS.length * BLOQUES.length;



const SIN_PROFESOR = [

  'Sin profesor',

  'Profesor no asignado',

];





// ============================================================

// MODAL

// ============================================================



function Modal({ titulo, children, onClose }) {

  return (

    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">



      <div className="w-full max-w-lg bg-white rounded-2xl shadow-xl overflow-hidden">



        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">



          <h2 className="text-lg font-semibold text-gray-800">

            {titulo}

          </h2>



          <button

            type="button"

            onClick={onClose}

            className="p-2 rounded-lg text-gray-400 hover:text-gray-700 hover:bg-gray-100 transition-colors"

          >

            <X size={20} />

          </button>



        </div>



        <div className="p-6">

          {children}

        </div>



      </div>



    </div>

  );

}





// ============================================================

// INPUT

// ============================================================



function Input({ label, ...props }) {

  return (

    <div>



      <label className="block text-sm font-medium text-gray-700 mb-1">

        {label}

      </label>



      <input

        {...props}

        className="w-full border border-gray-300 rounded-lg px-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

      />



    </div>

  );

}





// ============================================================

// SELECT

// ============================================================



function Select({ label, children, ...props }) {

  return (

    <div>



      <label className="block text-sm font-medium text-gray-700 mb-1">

        {label}

      </label>



      <select

        {...props}

        className="w-full border border-gray-300 rounded-lg px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

      >

        {children}

      </select>



    </div>

  );

}





// ============================================================

// BOTONES DEL MODAL

// ============================================================



function BotonesModal({ guardando, onClose }) {

  return (

    <div className="flex justify-end gap-3 pt-4">



      <button

        type="button"

        onClick={onClose}

        disabled={guardando}

        className="px-4 py-2.5 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:opacity-50"

      >

        Cancelar

      </button>



      <button

        type="submit"

        disabled={guardando}

        className="px-5 py-2.5 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 disabled:bg-blue-400 flex items-center gap-2"

      >



        {guardando && (

          <Loader2

            size={17}

            className="animate-spin"

          />

        )}



        {guardando ? 'Guardando...' : 'Guardar'}



      </button>



    </div>

  );

}





// ============================================================

// MATERIAS

// ============================================================



function MateriasTab({

  cat,

  opciones,

  onRecargar,

}) {



  const [modal, setModal] = useState(false);

  const [guardando, setGuardando] = useState(false);

  const [error, setError] = useState('');



  const [form, setForm] = useState({

    clave: '',

    nombre: '',

    horas_semana: 5,

    requiere_laboratorio: false,

    carrera_id: '',

    cuatrimestre_id: '',

    profesor_id: '',

  });





  const lista = Object.entries(

    cat.materias || {}

  ).map(([clave, m]) => ({

    clave,

    ...m,

  }));





  function cambiar(e) {



    const {

      name,

      value,

      type,

      checked,

    } = e.target;



    setForm((prev) => ({

      ...prev,

      [name]:

        type === 'checkbox'

          ? checked

          : value,

    }));

  }





  async function guardar(e) {



    e.preventDefault();



    setGuardando(true);

    setError('');



    try {



      await crearMateria({

        clave: form.clave.trim(),

        nombre: form.nombre.trim(),

        horas_semana: Number(form.horas_semana),

        requiere_laboratorio:

          form.requiere_laboratorio,

        carrera_id:

          form.carrera_id || null,

        cuatrimestre_id:

          form.cuatrimestre_id || null,

        profesor_id:

          form.profesor_id || null,

      });



      setModal(false);



      setForm({

        clave: '',

        nombre: '',

        horas_semana: 5,

        requiere_laboratorio: false,

        carrera_id: '',

        cuatrimestre_id: '',

        profesor_id: '',

      });



      await onRecargar();



    } catch (e) {



      setError(

        e?.response?.data?.detail ||

        mensajeDeError(e)

      );



    } finally {



      setGuardando(false);



    }

  }





  return (

    <>



      <div className="flex justify-end mb-4">



        <button

          onClick={() => {

            setError('');

            setModal(true);

          }}

          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2.5 rounded-lg transition-colors"

        >



          <Plus size={18} />



          Añadir materia



        </button>



      </div>





      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-x-auto">



        <table className="w-full text-left">



          <thead className="bg-gray-50 border-b border-gray-200">



            <tr>



              <th className="px-4 py-3 text-sm font-semibold text-gray-600">

                Materia

              </th>



              <th className="px-4 py-3 text-sm font-semibold text-gray-600">

                Cuat.

              </th>



              <th className="px-4 py-3 text-sm font-semibold text-gray-600">

                Horas

              </th>



              <th className="px-4 py-3 text-sm font-semibold text-gray-600">

                Profesor

              </th>



              <th className="px-4 py-3 text-sm font-semibold text-gray-600">

                Requisito

              </th>



            </tr>



          </thead>





          <tbody className="divide-y divide-gray-100">



            {lista.length === 0 && (



              <tr>



                <td

                  colSpan={5}

                  className="px-4 py-10 text-center text-gray-500"

                >

                  No hay materias en la base de datos.

                </td>



              </tr>



            )}





            {lista.map((m) => (



              <tr

                key={m.clave}

                className="hover:bg-gray-50"

              >



                <td className="px-4 py-3">



                  <p className="font-medium text-gray-800">

                    {m.nombre}

                  </p>



                  <p className="text-xs text-gray-500">

                    {m.clave}

                  </p>



                </td>





                <td className="px-4 py-3 text-gray-700 whitespace-nowrap">



                  {m.cuatrimestre

                    ? `${m.cuatrimestre}º`

                    : '—'}



                </td>





                <td className="px-4 py-3 text-gray-700 whitespace-nowrap">



                  {m.horas} hrs



                </td>





                <td

                  className={`px-4 py-3 text-sm ${

                    SIN_PROFESOR.includes(m.profesor)

                      ? 'text-amber-600 font-medium'

                      : 'text-gray-700'

                  }`}

                >

                  {m.profesor}

                </td>





                <td className="px-4 py-3">



                  {m.requiere_lab ? (



                    <span className="inline-flex items-center gap-1 bg-emerald-100 text-emerald-800 px-2 py-1 rounded text-xs font-bold whitespace-nowrap">



                      <FlaskConical size={12} />



                      Laboratorio



                    </span>



                  ) : (



                    <span className="inline-flex items-center gap-1 bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-bold whitespace-nowrap">



                      <MapPin size={12} />



                      Aula teórica



                    </span>



                  )}



                </td>



              </tr>



            ))}



          </tbody>



        </table>



      </div>





      {modal && (



        <Modal

          titulo="Añadir materia"

          onClose={() =>

            !guardando &&

            setModal(false)

          }

        >



          <form

            onSubmit={guardar}

            className="space-y-4"

          >



            <Input

              label="Clave"

              name="clave"

              value={form.clave}

              onChange={cambiar}

              placeholder="Ej. MAT-101"

              required

            />





            <Input

              label="Nombre de la materia"

              name="nombre"

              value={form.nombre}

              onChange={cambiar}

              placeholder="Ej. Matemáticas"

              required

            />





            <Input

              label="Horas por semana"

              name="horas_semana"

              type="number"

              min="1"

              max="20"

              value={form.horas_semana}

              onChange={cambiar}

              required

            />





            <Select

              label="Carrera"

              name="carrera_id"

              value={form.carrera_id}

              onChange={cambiar}

              required

            >



              <option value="">

                Selecciona una carrera

              </option>



              {(opciones?.carreras || []).map(

                (carrera) => (



                  <option

                    key={carrera.id}

                    value={carrera.id}

                  >

                    {carrera.nombre}

                  </option>



                )

              )}



            </Select>





            <Select

              label="Cuatrimestre"

              name="cuatrimestre_id"

              value={form.cuatrimestre_id}

              onChange={cambiar}

              required

            >



              <option value="">

                Selecciona un cuatrimestre

              </option>



              {(opciones?.cuatrimestres || []).map(

                (c) => (



                  <option

                    key={c.id}

                    value={c.id}

                  >

                    {c.numero}º - {c.nombre}

                  </option>



                )

              )}



            </Select>





            <Select

              label="Profesor"

              name="profesor_id"

              value={form.profesor_id}

              onChange={cambiar}

            >



              <option value="">

                Sin profesor

              </option>



              {(opciones?.profesores || []).map(

                (profesor) => (



                  <option

                    key={profesor.id}

                    value={profesor.id}

                  >

                    {profesor.nombre_completo}

                  </option>



                )

              )}



            </Select>





            <label className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 cursor-pointer hover:bg-gray-50">



              <input

                type="checkbox"

                name="requiere_laboratorio"

                checked={form.requiere_laboratorio}

                onChange={cambiar}

                className="w-4 h-4"

              />



              <div>



                <p className="font-medium text-gray-800">

                  Requiere laboratorio

                </p>



                <p className="text-xs text-gray-500">

                  La materia utilizará un laboratorio.

                </p>



              </div>



            </label>





            {error && (



              <p className="text-sm text-red-700 bg-red-50 border border-red-100 rounded-lg p-3">

                {error}

              </p>



            )}





            <BotonesModal

              guardando={guardando}

              onClose={() => setModal(false)}

            />



          </form>



        </Modal>



      )}



    </>

  );

}





// ============================================================

// PROFESORES

// ============================================================



function colorCarga(proporcion) {



  if (proporcion > 1) {



    return {

      barra: 'bg-red-500',

      texto: 'text-red-600',

    };



  }



  if (proporcion >= 0.75) {



    return {

      barra: 'bg-amber-500',

      texto: 'text-amber-600',

    };



  }



  return {

    barra: 'bg-emerald-500',

    texto: 'text-emerald-600',

  };

}





function ProfesoresTab({

  cat,

  opciones,

  onRecargar,

}) {



  const [modal, setModal] = useState(false);

  const [guardando, setGuardando] = useState(false);

  const [error, setError] = useState('');



  const [form, setForm] = useState({

    nombre_completo: '',

    correo: '',

  });





  const materias = Object.values(

    cat.materias || {}

  );





  const hayCuatrimestre =

    materias.length > 0 &&

    materias.every(

      (m) => m.cuatrimestre

    );





  const carga = {};





  materias.forEach((m) => {



    const nGrupos = hayCuatrimestre

      ? cat.grupos.filter(

          (g) =>

            g.startsWith(

              String(m.cuatrimestre)

            )

        ).length

      : 1;





    if (!carga[m.profesor]) {



      carga[m.profesor] = {

        materias: [],

        horas: 0,

      };



    }





    carga[m.profesor].materias.push(

      m.nombre

    );





    carga[m.profesor].horas +=

      m.horas * nGrupos;



  });





  (

    opciones?.profesores || []

  ).forEach((profesor) => {



    if (!carga[profesor.nombre_completo]) {



      carga[profesor.nombre_completo] = {

        materias: [],

        horas: 0,

      };



    }



  });





  const filas = Object.entries(carga)

    .sort(

      (a, b) =>

        b[1].horas - a[1].horas

    );





  function cambiar(e) {



    const {

      name,

      value,

    } = e.target;



    setForm((prev) => ({

      ...prev,

      [name]: value,

    }));



  }





  async function guardar(e) {



    e.preventDefault();



    setGuardando(true);

    setError('');



    try {



      await crearProfesor({

        nombre_completo:

          form.nombre_completo.trim(),



        correo:

          form.correo.trim(),

      });





      setModal(false);



      setForm({

        nombre_completo: '',

        correo: '',

      });





      await onRecargar();



    } catch (e) {



      setError(

        e?.response?.data?.detail ||

        mensajeDeError(e)

      );



    } finally {



      setGuardando(false);



    }



  }





  return (

    <>



      <div className="flex justify-end mb-4">



        <button

          onClick={() => {

            setError('');

            setModal(true);

          }}

          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2.5 rounded-lg transition-colors"

        >



          <Plus size={18} />



          Añadir profesor



        </button>



      </div>





      <div className="bg-white rounded-xl shadow-sm border border-gray-200">



        <div className="p-6 border-b border-gray-100">



          <h2 className="text-lg font-semibold text-gray-800">

            Carga semanal por profesor

          </h2>



          <p className="text-sm text-gray-500 mt-1">

            Horas de cada materia por el número

            de grupos que la cursan.

            Límite visual: {HORAS_DISPONIBLES}

            horas semanales.

          </p>



        </div>





        {filas.length === 0 && (



          <p className="p-10 text-center text-gray-500">

            No hay profesores.

          </p>



        )}





        <ul className="divide-y divide-gray-100">



          {filas.map(

            ([nombre, datos]) => {



              const proporcion =

                datos.horas /

                HORAS_DISPONIBLES;



              const color =

                colorCarga(proporcion);





              return (



                <li

                  key={nombre}

                  className="px-6 py-4 grid grid-cols-1 md:grid-cols-3 gap-3 md:items-center"

                >



                  <div>



                    <p className="font-medium text-gray-800">

                      {nombre}

                    </p>



                    <p className="text-xs text-gray-500 mt-0.5">



                      {datos.materias.length

                        ? datos.materias.join(' · ')

                        : 'Sin materias asignadas'}



                    </p>



                  </div>





                  <div className="md:col-span-2">



                    <div className="flex justify-between text-sm mb-1">



                      <span

                        className={`font-medium ${color.texto}`}

                      >

                        {datos.horas} /{' '}

                        {HORAS_DISPONIBLES} h

                      </span>





                      {proporcion > 1 && (



                        <span className="text-red-600 text-xs font-medium">

                          Sobrecargado

                        </span>



                      )}



                    </div>





                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">



                      <div

                        className={`h-full rounded-full ${color.barra}`}

                        style={{

                          width: `${

                            Math.min(

                              proporcion,

                              1

                            ) * 100

                          }%`,

                        }}

                      />



                    </div>



                  </div>



                </li>



              );



            }

          )}



        </ul>



      </div>





      {modal && (



        <Modal

          titulo="Añadir profesor"

          onClose={() =>

            !guardando &&

            setModal(false)

          }

        >



          <form

            onSubmit={guardar}

            className="space-y-4"

          >



            <Input

              label="Nombre completo"

              name="nombre_completo"

              value={form.nombre_completo}

              onChange={cambiar}

              placeholder="Ej. Juan Pérez López"

              required

            />





            <Input

              label="Correo"

              name="correo"

              type="email"

              value={form.correo}

              onChange={cambiar}

              placeholder="Ej. juan\@universidad.edu.mx"

              required

            />





            {error && (



              <p className="text-sm text-red-700 bg-red-50 border border-red-100 rounded-lg p-3">

                {error}

              </p>



            )}





            <BotonesModal

              guardando={guardando}

              onClose={() => setModal(false)}

            />



          </form>



        </Modal>



      )}



    </>

  );

}





// ============================================================

// LISTA DE GRUPOS / ESPACIOS

// ============================================================



function ListaFija({

  titulo,

  items,

  boton,

  onClickBoton,

  icono,

}) {



  return (



    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 h-fit">



      <div className="flex items-center justify-between gap-3 mb-4">



        <h2 className="text-lg font-semibold text-gray-800">



          {titulo}{' '}



          <span className="text-gray-400 font-normal">

            ({items.length})

          </span>



        </h2>





        {boton && (



          <button

            onClick={onClickBoton}

            className="flex items-center gap-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-3 py-2 rounded-lg transition-colors"

          >



            <Plus size={16} />



            Añadir



          </button>



        )}



      </div>





      <div className="flex flex-wrap gap-2">



        {items.length === 0 && (



          <p className="text-sm text-gray-400">

            Sin elementos.

          </p>



        )}





        {items.map((item) => (



          <span

            key={item}

            className="bg-slate-100 text-slate-700 rounded-full px-3 py-1 text-sm"

          >



            {icono}



            {item.replace(/\_/g, ' ')}



          </span>



        ))}



      </div>



    </div>



  );

}





// ============================================================

// GRUPOS Y ESPACIOS

// ============================================================



function EspaciosTab({

  cat,

  opciones,

  onRecargar,

}) {



  const [modal, setModal] = useState(null);



  const [guardando, setGuardando] = useState(false);



  const [error, setError] = useState('');





  const [form, setForm] = useState({

    nombre: '',

    tipo: 'AULA',

    capacidad: 30,

    cuatrimestre_id: '',

    periodo_id: '',

  });





  function abrir(tipo) {



    setError('');



    setForm({

      nombre: '',

      tipo,

      capacidad: 30,

      cuatrimestre_id: '',

      periodo_id: '',

    });



    setModal(tipo);



  }





  function cambiar(e) {



    const {

      name,

      value,

    } = e.target;



    setForm((prev) => ({

      ...prev,

      [name]: value,

    }));



  }





  // ==========================================================

  // CREAR GRUPO

  // ==========================================================



  async function guardarGrupo(e) {



    e.preventDefault();



    setGuardando(true);

    setError('');



    try {



      await crearGrupo({
        nombre: form.nombre.trim(),
        cuatrimestre_id: form.cuatrimestre_id,
        periodo_id: form.periodo_id,
        turno: form.turno,
      });





      setModal(null);



      await onRecargar();



    } catch (e) {



      setError(

        e?.response?.data?.detail ||

        mensajeDeError(e)

      );



    } finally {



      setGuardando(false);



    }



  }





  // ==========================================================

  // CREAR AULA / LABORATORIO

  // ==========================================================



  async function guardarEspacio(e) {



    e.preventDefault();



    setGuardando(true);

    setError('');



    try {



      await crearEspacio({



        nombre:

          form.nombre.trim(),



        tipo:

          form.tipo,



        capacidad:

          Number(form.capacidad),



      });





      setModal(null);



      await onRecargar();



    } catch (e) {



      setError(

        e?.response?.data?.detail ||

        mensajeDeError(e)

      );



    } finally {



      setGuardando(false);



    }



  }





  return (

    <>



      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">





        {/* GRUPOS */}



        <ListaFija

          titulo="Grupos"

          items={cat.grupos || []}

          boton="Añadir"

          onClickBoton={() =>

            abrir('GRUPO')

          }

        />





        {/* AULAS */}



        <ListaFija

          titulo="Aulas teóricas"

          items={cat.aulas_teoricas || []}

          boton="Añadir"

          onClickBoton={() =>

            abrir('AULA')

          }

          icono={

            <MapPin

              size={13}

              className="inline mr-1"

            />

          }

        />





        {/* LABORATORIOS */}



        <ListaFija

          titulo="Laboratorios"

          items={cat.laboratorios || []}

          boton="Añadir"

          onClickBoton={() =>

            abrir('LABORATORIO')

          }

          icono={

            <FlaskConical

              size={13}

              className="inline mr-1"

            />

          }

        />



      </div>





      {/* =====================================================

          MODAL GRUPO

      ===================================================== */}



      {modal === 'GRUPO' && (



        <Modal

          titulo="Añadir grupo"

          onClose={() =>

            !guardando &&

            setModal(null)

          }

        >



          <form

            onSubmit={guardarGrupo}

            className="space-y-4"

          >



            <Input

              label="Nombre del grupo"

              name="nombre"

              value={form.nombre}

              onChange={cambiar}

              placeholder="Ej. 1A"

              required

            />





            <Select

              label="Cuatrimestre"

              name="cuatrimestre_id"

              value={form.cuatrimestre_id}

              onChange={cambiar}

              required

            >



              <option value="">

                Selecciona un cuatrimestre

              </option>





              {(opciones?.cuatrimestres || []).map(

                (c) => (



                  <option

                    key={c.id}

                    value={c.id}

                  >

                    {c.numero}º - {c.nombre}

                  </option>



                )

              )}



            </Select>

            <Select
              label="Periodo académico"
              name="periodo_id"
              value={form.periodo_id}
              onChange={cambiar}
              required
            >
              <option value="">
                Selecciona un periodo académico
              </option>

              {(opciones?.periodos || []).map(
                (periodo) => (
                  <option
                    key={periodo.id}
                    value={periodo.id}
                  >
                    {periodo.nombre}
                  </option>
                )
              )}
            </Select>

            <Select
              label="Turno"
              name="turno"
              value={form.turno}
              onChange={cambiar}
              required
            >
              <option value="">
                Selecciona un turno
              </option>
              <option value="MATUTINO">
                Matutino
              </option>
              <option value="VESPERTINO">
                Vespertino
              </option>
            </Select>






            {error && (



              <p className="text-sm text-red-700 bg-red-50 border border-red-100 rounded-lg p-3">

                {error}

              </p>



            )}





            <BotonesModal

              guardando={guardando}

              onClose={() =>

                setModal(null)

              }

            />



          </form>



        </Modal>



      )}





      {/* =====================================================

          MODAL AULA / LABORATORIO

      ===================================================== */}



      {(modal === 'AULA' ||

        modal === 'LABORATORIO') && (



        <Modal

          titulo={

            modal === 'AULA'

              ? 'Añadir aula'

              : 'Añadir laboratorio'

          }

          onClose={() =>

            !guardando &&

            setModal(null)

          }

        >



          <form

            onSubmit={guardarEspacio}

            className="space-y-4"

          >



            <Input

              label={

                modal === 'AULA'

                  ? 'Nombre del aula'

                  : 'Nombre del laboratorio'

              }

              name="nombre"

              value={form.nombre}

              onChange={cambiar}

              placeholder={

                modal === 'AULA'

                  ? 'Ej. A-101'

                  : 'Ej. LAB-01'

              }

              required

            />





            <Input

              label="Capacidad"

              name="capacidad"

              type="number"

              min="1"

              value={form.capacidad}

              onChange={cambiar}

              required

            />





            <div className="bg-gray-50 rounded-lg p-3 text-sm text-gray-600">



              Tipo:



              <span className="font-semibold ml-1">



                {modal === 'AULA'

                  ? 'Aula teórica'

                  : 'Laboratorio'}



              </span>



            </div>





            {error && (



              <p className="text-sm text-red-700 bg-red-50 border border-red-100 rounded-lg p-3">

                {error}

              </p>



            )}





            <BotonesModal

              guardando={guardando}

              onClose={() =>

                setModal(null)

              }

            />



          </form>



        </Modal>



      )}



    </>

  );

}





// ============================================================

// PÁGINA PRINCIPAL

// ============================================================



export default function Configuracion() {



  const [cat, setCat] = useState(null);



  const [opciones, setOpciones] = useState(null);



  const [cargando, setCargando] = useState(true);



  const [error, setError] = useState('');



  const [pestana, setPestana] = useState('materias');





  // ==========================================================

  // CARGAR DATOS

  // ==========================================================



  async function cargar() {



    setCargando(true);

    setError('');



    try {



      // IMPORTANTE:

      // Primero obtenemos el catálogo.

      // Después obtenemos las opciones.

      // Ya no se hacen las dos peticiones simultáneamente.



      const catalogo = await obtenerCatalogo();



      setCat(catalogo);





      const opcionesCatalogo =

        await obtenerOpcionesCatalogo();



      setOpciones(opcionesCatalogo);



    } catch (e) {



      setError(

        e?.response?.data?.detail ||

        mensajeDeError(e)

      );



    } finally {



      setCargando(false);



    }



  }





  useEffect(() => {



    cargar();



  }, []);





  // ==========================================================

  // PESTAÑAS

  // ==========================================================



  const pestanas = [



    {

      id: 'materias',

      label: 'Materias',

      total: cat

        ? Object.keys(

            cat.materias || {}

          ).length

        : null,

    },





    {

      id: 'profesores',

      label: 'Profesores',

      total: opciones

        ? opciones.profesores.length

        : null,

    },





    {

      id: 'espacios',

      label: 'Grupos y Espacios',

      total: null,

    },



  ];





  return (



    <div className="p-8">



      <div className="max-w-6xl mx-auto">





        {/* ENCABEZADO */}



        <div className="flex flex-wrap items-center justify-between gap-3 mb-1">



          <h1 className="text-2xl font-bold text-gray-800">

            Configuración de Catálogos

          </h1>





          <button

            onClick={cargar}

            disabled={cargando}

            className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-800 disabled:opacity-50 transition-colors"

          >



            <RefreshCw

              size={16}

              className={

                cargando

                  ? 'animate-spin'

                  : ''

              }

            />



            Actualizar



          </button>



        </div>





        <p className="text-sm text-gray-500 mb-6">



          Datos en vivo desde Supabase.

          Puedes agregar nuevos elementos

          directamente desde aquí.



        </p>





        {/* ERROR */}



        {error && (



          <p className="flex items-start gap-2 text-sm text-red-700 bg-red-50 border border-red-100 rounded-lg p-3 mb-6">



            <AlertCircle

              size={18}

              className="shrink-0 mt-0.5"

            />



            {error}



          </p>



        )}





        {/* CARGANDO */}



        {cargando && !cat && (



          <p className="flex items-center gap-2 text-gray-500">



            <Loader2

              size={18}

              className="animate-spin"

            />



            Cargando catálogo…



          </p>



        )}





        {/* CONTENIDO */}



        {cat && (



          <>



            {/* TABS */}



            <div className="flex border-b border-gray-200 mb-6">



              {pestanas.map((p) => (



                <button

                  key={p.id}

                  onClick={() =>

                    setPestana(p.id)

                  }

                  className={`px-6 py-3 font-medium transition-colors ${

                    pestana === p.id

                      ? 'border-b-2 border-blue-600 text-blue-600'

                      : 'text-gray-500 hover:text-gray-700'

                  }`}

                >



                  {p.label}





                  {p.total !== null && (



                    <span className="ml-1.5 text-xs text-gray-400">



                      ({p.total})



                    </span>



                  )}



                </button>



              ))}



            </div>





            {/* MATERIAS */}



            {pestana === 'materias' && (



              <MateriasTab

                cat={cat}

                opciones={opciones}

                onRecargar={cargar}

              />



            )}





            {/* PROFESORES */}



            {pestana === 'profesores' && (



              <ProfesoresTab

                cat={cat}

                opciones={opciones}

                onRecargar={cargar}

              />



            )}





            {/* GRUPOS Y ESPACIOS */}



            {pestana === 'espacios' && (



              <EspaciosTab

                cat={cat}

                opciones={opciones}

                onRecargar={cargar}

              />



            )}



          </>



        )}



      </div>



    </div>



  );

}