import axios from 'axios';

// Dirección del backend. Para cambiarla sin tocar código, crea frontend/.env con:
// VITE_API_URL=http://localhost:8000
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Solo sirven para dibujar la tabla de Resultados. Deben coincidir con los bloques
// que están en Supabase (tabla bloques_horario).
export const DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];
export const BLOQUES = [
  "07:00-07:50", "07:50-08:40", "08:40-09:30",
  "10:00-10:50", "10:50-11:40", "11:40-12:30",
  "12:30-13:20", "13:20-14:10", "14:10-15:00",
];

// Parámetros del algoritmo. Para probar más rápido, baja estos números (ej. 100 y 100).
export const PARAMETROS = {
  tamano_poblacion: 300,
  generaciones: 500,
};

// Catálogo real (grupos, materias, profesores, espacios) leído de Supabase
export async function obtenerCatalogo() {
  const { data } = await api.get('/api/datos-supabase');
  return data;
}

export async function obtenerOpcionesCatalogo() {
  const { data } = await api.get('/api/opciones-catalogo');
  return data;
}

export async function crearProfesor(datos) {
  const { data } = await api.post('/api/profesores', datos);
  return data;
}

export async function crearMateria(datos) {
  const { data } = await api.post('/api/materias', datos);
  return data;
}

export async function crearGrupo(datos) {
  const { data } = await api.post('/api/grupos', datos);
  return data;
}

export async function crearEspacio(datos) {
  const { data } = await api.post('/api/espacios', datos);
  return data;
}

// El backend lee Supabase por su cuenta; aquí solo mandamos los parámetros.
// Puede tardar (el algoritmo corre completo antes de responder).
export async function generarHorario(parametros = PARAMETROS) {
  const { data } = await api.post('/api/generar-horario', parametros);
  return data;
}

export function mensajeDeError(e) {
  if (e.response) {
    return `El backend respondió con un error (${e.response.status}). Revisa la terminal donde corre uvicorn.`;
  }
  return 'No se pudo conectar con el backend. ¿Está corriendo uvicorn en el puerto 8000?';
}

// Guardamos el último resultado para que la pantalla de Resultados lo lea.
const CLAVE = 'ultimo_horario';

export function guardarResultado(entrada, resultado) {
  localStorage.setItem(CLAVE, JSON.stringify({ entrada, resultado }));
}

export function leerResultado() {
  try {
    const texto = localStorage.getItem(CLAVE);
    return texto ? JSON.parse(texto) : null;
  } catch {
    return null;
  }
}

// Limpieza: borra el catálogo local de la versión anterior (ya no se usa)
try {
  localStorage.removeItem('catalogo_horarios');
} catch {
  // nada que hacer
}
