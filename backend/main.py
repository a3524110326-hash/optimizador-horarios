from fastapi import FastAPI, HTTPException
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
        "id, clave, nombre, horas_semana, "
        "requiere_laboratorio, cuatrimestre_id"
    ).execute()


    # ------------------------------------------
    # 2. CUATRIMESTRES
    # ------------------------------------------

    cuatrimestres_result = supabase.table(
        "cuatrimestres"
    ).select(
        "id, numero"
    ).execute()

    numero_por_cuatrimestre = {
        str(c["id"]): c["numero"]
        for c in cuatrimestres_result.data
    }


    # ------------------------------------------
    # 3. PROFESORES
    # ------------------------------------------

    profesores_result = supabase.table(
        "profesores"
    ).select(
        "id, nombre_completo"
    ).execute()


    # ------------------------------------------
    # 4. RELACIÓN PROFESOR - MATERIA
    # ------------------------------------------

    profesor_materia_result = supabase.table(
        "profesor_materia"
    ).select(
        "profesor_id, materia_id"
    ).execute()


    # ------------------------------------------
    # 5. GRUPOS
    # ------------------------------------------

    grupos_result = supabase.table(
        "grupos"
    ).select(
        "nombre"
    ).eq(
        "activo",
        True
    ).execute()


    # ------------------------------------------
    # 6. ESPACIOS
    # ------------------------------------------

    espacios_result = supabase.table(
        "espacios"
    ).select(
        "nombre, tipo, capacidad"
    ).eq(
        "activo",
        True
    ).execute()


    # ------------------------------------------
    # 7. BLOQUES DE HORARIO
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

        cuatrimestre = numero_por_cuatrimestre.get(
            str(materia["cuatrimestre_id"])
        )

        datos["materias"][
            materia["clave"]
        ] = {

            "nombre": materia["nombre"],

            "cuatrimestre": cuatrimestre,

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
# OPCIONES PARA LOS FORMULARIOS
# ==========================================

@app.get("/api/opciones-catalogo")
def opciones_catalogo():

    carreras = supabase.table(
        "carreras"
    ).select(
        "id, nombre, clave"
    ).eq(
        "activo",
        True
    ).execute()

    cuatrimestres = supabase.table(
        "cuatrimestres"
    ).select(
        "id, numero, nombre, carrera_id"
    ).execute()

    periodos = supabase.table(
        "periodos_academicos"
    ).select(
        "id, nombre, fecha_inicio, fecha_fin"
    ).eq(
        "activo",
        True
    ).execute()

    profesores = supabase.table(
        "profesores"
    ).select(
        "id, nombre_completo, correo"
    ).eq(
        "activo",
        True
    ).execute()

    return {
        "carreras": carreras.data,
        "cuatrimestres": cuatrimestres.data,
        "periodos": periodos.data,
        "profesores": profesores.data
    }


# ==========================================
# CREAR PROFESOR
# ==========================================

@app.post("/api/profesores")
def crear_profesor(datos: dict):

    nombre = datos.get(
        "nombre_completo",
        ""
    ).strip()

    correo = datos.get(
        "correo",
        ""
    ).strip()

    if not nombre:
        raise HTTPException(
            status_code=400,
            detail="El nombre del profesor es obligatorio."
        )

    try:

        resultado = supabase.table(
            "profesores"
        ).insert({
            "nombre_completo": nombre,
            "correo": correo or None,
            "activo": True
        }).execute()

        return resultado.data[0]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"No se pudo crear el profesor: {str(e)}"
        )


# ==========================================
# CREAR MATERIA
# ==========================================

@app.post("/api/materias")
def crear_materia(datos: dict):

    clave = datos.get(
        "clave",
        ""
    ).strip()

    nombre = datos.get(
        "nombre",
        ""
    ).strip()

    horas = datos.get(
        "horas_semana"
    )

    requiere_laboratorio = datos.get(
        "requiere_laboratorio",
        False
    )

    carrera_id = datos.get(
        "carrera_id"
    )

    cuatrimestre_id = datos.get(
        "cuatrimestre_id"
    )

    profesor_id = datos.get(
        "profesor_id"
    )


    if not clave:

        raise HTTPException(
            status_code=400,
            detail="La clave de la materia es obligatoria."
        )


    if not nombre:

        raise HTTPException(
            status_code=400,
            detail="El nombre de la materia es obligatorio."
        )


    if horas is None:

        raise HTTPException(
            status_code=400,
            detail="Las horas por semana son obligatorias."
        )


    if not carrera_id:

        raise HTTPException(
            status_code=400,
            detail="Selecciona una carrera."
        )


    if not cuatrimestre_id:

        raise HTTPException(
            status_code=400,
            detail="Selecciona un cuatrimestre."
        )


    try:

        materia_result = supabase.table(
            "materias"
        ).insert({

            "clave": clave,

            "nombre": nombre,

            "horas_semana": int(horas),

            "requiere_laboratorio": bool(
                requiere_laboratorio
            ),

            "carrera_id": carrera_id,

            "cuatrimestre_id": cuatrimestre_id,

            "activo": True

        }).execute()


        materia_creada = materia_result.data[0]


        # --------------------------------------
        # RELACIONAR PROFESOR
        # --------------------------------------

        if profesor_id:

            supabase.table(
                "profesor_materia"
            ).insert({

                "profesor_id": profesor_id,

                "materia_id": materia_creada["id"]

            }).execute()


        return materia_creada


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"No se pudo crear la materia: {str(e)}"
        )


# ==========================================
# CREAR GRUPO
# ==========================================

@app.post("/api/grupos")
def crear_grupo(datos: dict):

    nombre = datos.get(
        "nombre",
        ""
    ).strip()

    cuatrimestre_id = datos.get(
        "cuatrimestre_id"
    )

    periodo_id = datos.get(
        "periodo_id"
    )

    turno = datos.get(
        "turno",
        ""
    ).strip()


    if not nombre:

        raise HTTPException(
            status_code=400,
            detail="El nombre del grupo es obligatorio."
        )


    if not cuatrimestre_id:

        raise HTTPException(
            status_code=400,
            detail="Selecciona un cuatrimestre."
        )


    if not periodo_id:

        raise HTTPException(
            status_code=400,
            detail="Selecciona un periodo académico."
        )


    if not turno:

        raise HTTPException(
            status_code=400,
            detail="Selecciona un turno."
        )


    try:

        resultado = supabase.table(
            "grupos"
        ).insert({

            "nombre": nombre,

            "cuatrimestre_id": cuatrimestre_id,

            "periodo_id": periodo_id,

            "turno": turno,

            "activo": True

        }).execute()


        return resultado.data[0]


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"No se pudo crear el grupo: {str(e)}"
        )


# ==========================================
# CREAR ESPACIO
# ==========================================

@app.post("/api/espacios")
def crear_espacio(datos: dict):

    nombre = datos.get(
        "nombre",
        ""
    ).strip()

    tipo = datos.get(
        "tipo",
        ""
    ).strip().upper()

    capacidad = datos.get(
        "capacidad"
    )


    if not nombre:

        raise HTTPException(
            status_code=400,
            detail="El nombre del espacio es obligatorio."
        )


    if tipo not in [
        "AULA",
        "LABORATORIO"
    ]:

        raise HTTPException(
            status_code=400,
            detail="El tipo debe ser AULA o LABORATORIO."
        )


    if capacidad is None:

        raise HTTPException(
            status_code=400,
            detail="La capacidad es obligatoria."
        )


    try:

        resultado = supabase.table(
            "espacios"
        ).insert({

            "nombre": nombre,

            "tipo": tipo,

            "capacidad": int(capacidad),

            "activo": True

        }).execute()


        return resultado.data[0]


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"No se pudo crear el espacio: {str(e)}"
        )


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