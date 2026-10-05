from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from supabase_client import supabase
from algoritmo import motor_evolutivo


# ==========================================
# CONFIGURACIÓN DE FASTAPI
# ==========================================

app = FastAPI(
    title="API Optimizador de Horarios TSU"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# RUTA PRINCIPAL
# ==========================================

@app.get("/")
def estado_servidor():
    return {
        "estatus": "En línea",
        "mensaje": "API del Optimizador lista"
    }


# ==========================================
# OBTENER DATOS DESDE SUPABASE
# ==========================================

def obtener_datos_bd():

    # ------------------------------------------
    # 1. MATERIAS
    # ------------------------------------------

    materias_result = supabase.table("materias").select(
        "id, clave, nombre, horas_semana, requiere_laboratorio"
    ).execute()


    # ------------------------------------------
    # 2. PROFESORES
    # ------------------------------------------

    profesores_result = supabase.table("profesores").select(
        "id, nombre_completo"
    ).execute()


    # ------------------------------------------
    # 3. RELACIÓN PROFESOR - MATERIA
    # ------------------------------------------

    profesor_materia_result = supabase.table(
        "profesor_materia"
    ).select(
        "profesor_id, materia_id"
    ).execute()


    # ------------------------------------------
    # 4. GRUPOS
    # ------------------------------------------

    grupos_result = supabase.table("grupos").select(
        "nombre"
    ).execute()


    # ------------------------------------------
    # 5. ESPACIOS
    # ------------------------------------------

    espacios_result = supabase.table("espacios").select(
        "nombre, tipo, capacidad"
    ).execute()


    # ------------------------------------------
    # 6. BLOQUES DE HORARIO
    # ------------------------------------------

    bloques_result = supabase.table(
        "bloques_horario"
    ).select(
        "dia_semana, hora_inicio, hora_fin"
    ).execute()


    # ==========================================
    # DICCIONARIO DE PROFESORES
    # ==========================================

    profesores = {}

    for profesor in profesores_result.data:

        profesores[str(profesor["id"])] = (
            profesor["nombre_completo"]
        )


    # ==========================================
    # RELACIÓN MATERIA -> PROFESOR
    # ==========================================

    profesor_por_materia = {}

    for relacion in profesor_materia_result.data:

        profesor_id = str(
            relacion["profesor_id"]
        )

        materia_id = str(
            relacion["materia_id"]
        )

        profesor_nombre = profesores.get(
            profesor_id,
            "Sin profesor"
        )

        profesor_por_materia[materia_id] = (
            profesor_nombre
        )


    # ==========================================
    # ESTRUCTURA FINAL
    # ==========================================

    datos = {

        "grupos": [],

        "materias": {},

        "laboratorios": [],

        "aulas_teoricas": [],

        "dias": [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes"
        ],

        "bloques_tiempo": []
    }


    # ==========================================
    # CARGAR GRUPOS
    # ==========================================

    for grupo in grupos_result.data:

        datos["grupos"].append(
            grupo["nombre"]
        )


    # ==========================================
    # CARGAR MATERIAS
    # ==========================================

    for materia in materias_result.data:

        materia_id = str(
            materia["id"]
        )

        datos["materias"][
            materia["clave"]
        ] = {

            "nombre": materia["nombre"],

            "horas": materia["horas_semana"],

            "requiere_lab": (
                materia["requiere_laboratorio"]
            ),

            "profesor": (
                profesor_por_materia.get(
                    materia_id,
                    "Sin profesor"
                )
            )
        }


    # ==========================================
    # CARGAR ESPACIOS
    # ==========================================

    for espacio in espacios_result.data:

        if espacio["tipo"] == "LABORATORIO":

            datos["laboratorios"].append(
                espacio["nombre"]
            )

        elif espacio["tipo"] == "AULA":

            datos["aulas_teoricas"].append(
                espacio["nombre"]
            )


    # ==========================================
    # CARGAR BLOQUES DE HORARIO
    # ==========================================

    bloques_unicos = set()

    for bloque in bloques_result.data:

        inicio = bloque["hora_inicio"][:5]
        fin = bloque["hora_fin"][:5]

        bloques_unicos.add(
            f"{inicio}-{fin}"
        )

    datos["bloques_tiempo"] = sorted(
        bloques_unicos
    )


    # ==========================================
    # DEVOLVER DATOS
    # ==========================================

    return datos


# ==========================================
# PRUEBA DE DATOS DE SUPABASE
# ==========================================

@app.get("/api/datos-supabase")
def datos_supabase():

    return obtener_datos_bd()


# ==========================================
# GENERAR HORARIO
# ==========================================

@app.post("/api/generar-horario")
def arrancar_simulacion(
    datos_front: dict = None
):

    # ------------------------------------------
    # OBTENER DATOS REALES DE SUPABASE
    # ------------------------------------------

    datos_bd = obtener_datos_bd()


    # ------------------------------------------
    # RECIBIR PARÁMETROS DEL FRONTEND
    # ------------------------------------------

    if datos_front:

        datos_bd.update({

            "tamano_poblacion": datos_front.get(
                "tamano_poblacion",
                300
            ),

            "prob_cruza": datos_front.get(
                "prob_cruza",
                0.85
            ),

            "prob_mutacion": datos_front.get(
                "prob_mutacion",
                0.15
            ),

            "generaciones": datos_front.get(
                "generaciones",
                500
            )
        })


    # ------------------------------------------
    # EJECUTAR ALGORITMO EVOLUTIVO
    # ------------------------------------------

    resultado = (
        motor_evolutivo.ejecutar_optimizador(
            datos_bd
        )
    )


    # ------------------------------------------
    # DEVOLVER RESULTADO
    # ------------------------------------------

    return resultado