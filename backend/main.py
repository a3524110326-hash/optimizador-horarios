from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from supabase_client import supabase
from algoritmo import motor_evolutivo

import time


# ============================================================
# APLICACIÓN
# ============================================================

app = FastAPI()


# ============================================================
# CONFIGURACIÓN CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# FUNCIÓN PARA EJECUTAR CONSULTAS CON REINTENTOS
# ============================================================

def ejecutar_con_reintentos(consulta, intentos=3):
    """
    Ejecuta una consulta de Supabase.
    Si ocurre un error de conexión, vuelve a intentar.
    """

    ultimo_error = None

    for intento in range(1, intentos + 1):

        try:

            return consulta()

        except Exception as e:

            ultimo_error = e

            print(
                f"⚠️ Error de Supabase "
                f"(intento {intento}/{intentos}): {e}"
            )

            if intento < intentos:

                print(
                    "Esperando 1 segundo antes de reintentar..."
                )

                time.sleep(1)

    raise ultimo_error


# ============================================================
# OBTENER DATOS DE SUPABASE
# ============================================================

def obtener_datos_bd():

    # ========================================================
    # MATERIAS ACTIVAS
    # ========================================================

    materias_response = ejecutar_con_reintentos(
        lambda: supabase.table(
            "materias"
        ).select(
            "id, clave, nombre, horas_semana, "
            "requiere_laboratorio, cuatrimestre_id"
        ).eq(
            "activo",
            True
        ).execute()
    )

    materias_bd = materias_response.data or []


    # ========================================================
    # CUATRIMESTRES
    # ========================================================

    cuatrimestres_response = ejecutar_con_reintentos(
        lambda: supabase.table(
            "cuatrimestres"
        ).select(
            "id, numero"
        ).execute()
    )

    cuatrimestres_bd = (
        cuatrimestres_response.data or []
    )


    numero_por_cuatrimestre = {
        str(c["id"]): c["numero"]
        for c in cuatrimestres_bd
    }


    # ========================================================
    # PROFESORES ACTIVOS
    # ========================================================

    profesores_response = ejecutar_con_reintentos(
        lambda: supabase.table(
            "profesores"
        ).select(
            "id, nombre_completo"
        ).eq(
            "activo",
            True
        ).execute()
    )

    profesores_bd = (
        profesores_response.data or []
    )


    profesores_por_id = {
        str(p["id"]): p["nombre_completo"]
        for p in profesores_bd
    }


    # ========================================================
    # RELACIÓN PROFESOR - MATERIA
    # ========================================================

    profesor_materia_response = ejecutar_con_reintentos(
        lambda: supabase.table(
            "profesor_materia"
        ).select(
            "profesor_id, materia_id"
        ).execute()
    )

    profesor_materia_bd = (
        profesor_materia_response.data or []
    )


    profesor_por_materia = {}


    for relacion in profesor_materia_bd:

        materia_id = str(
            relacion["materia_id"]
        )

        profesor_id = str(
            relacion["profesor_id"]
        )

        profesor_por_materia[materia_id] = (
            profesores_por_id.get(
                profesor_id,
                "Sin profesor"
            )
        )


    # ========================================================
    # GRUPOS ACTIVOS
    # ========================================================

    grupos_response = ejecutar_con_reintentos(
        lambda: supabase.table(
            "grupos"
        ).select(
            "nombre"
        ).eq(
            "activo",
            True
        ).execute()
    )

    grupos_bd = (
        grupos_response.data or []
    )


    # ========================================================
    # ESPACIOS ACTIVOS
    # ========================================================

    espacios_response = ejecutar_con_reintentos(
        lambda: supabase.table(
            "espacios"
        ).select(
            "nombre, tipo, capacidad"
        ).eq(
            "activo",
            True
        ).execute()
    )

    espacios_bd = (
        espacios_response.data or []
    )


    # ========================================================
    # BLOQUES DE HORARIO
    # ========================================================

    bloques_response = ejecutar_con_reintentos(
        lambda: supabase.table(
            "bloques_horario"
        ).select(
            "dia_semana, hora_inicio, hora_fin"
        ).execute()
    )

    bloques_bd = (
        bloques_response.data or []
    )


    # ========================================================
    # CONSTRUIR DATOS PARA EL MOTOR
    # ========================================================

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


    # ========================================================
    # GRUPOS
    # ========================================================

    for grupo in grupos_bd:

        datos["grupos"].append(
            grupo["nombre"]
        )


    # ========================================================
    # MATERIAS
    # ========================================================

    for materia in materias_bd:

        materia_id = str(
            materia["id"]
        )

        clave = materia["clave"]


        datos["materias"][clave] = {

            "nombre": materia["nombre"],

            "cuatrimestre":
                numero_por_cuatrimestre.get(
                    str(
                        materia["cuatrimestre_id"]
                    )
                ),

            "horas":
                materia["horas_semana"],

            "requiere_lab":
                materia["requiere_laboratorio"],

            "profesor":
                profesor_por_materia.get(
                    materia_id,
                    "Sin profesor"
                )
        }


    # ========================================================
    # ESPACIOS
    # ========================================================

    for espacio in espacios_bd:

        if espacio["tipo"] == "LABORATORIO":

            datos["laboratorios"].append(
                espacio["nombre"]
            )

        elif espacio["tipo"] == "AULA":

            datos["aulas_teoricas"].append(
                espacio["nombre"]
            )


    # ========================================================
    # BLOQUES
    # ========================================================

    bloques_unicos = set()


    for bloque in bloques_bd:

        inicio = bloque["hora_inicio"][:5]

        fin = bloque["hora_fin"][:5]

        bloques_unicos.add(
            f"{inicio}-{fin}"
        )


    datos["bloques_tiempo"] = sorted(
        bloques_unicos
    )


    return datos


# ============================================================
# RUTA PRINCIPAL
# ============================================================

@app.get("/")
def inicio():

    return {
        "mensaje":
            "Backend del optimizador de horarios funcionando"
    }


# ============================================================
# OBTENER DATOS DE SUPABASE
# ============================================================

@app.get("/api/datos-supabase")
def datos_supabase():

    try:

        return obtener_datos_bd()

    except Exception as e:

        print(
            "ERROR EN /api/datos-supabase:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# OPCIONES PARA CATÁLOGOS
# ============================================================

@app.get("/api/opciones-catalogo")
def opciones_catalogo():

    try:

        carreras = ejecutar_con_reintentos(
            lambda: supabase.table(
                "carreras"
            ).select(
                "id, nombre, clave"
            ).eq(
                "activo",
                True
            ).execute()
        ).data or []


        cuatrimestres = ejecutar_con_reintentos(
            lambda: supabase.table(
                "cuatrimestres"
            ).select(
                "id, numero, nombre, carrera_id"
            ).execute()
        ).data or []


        periodos = ejecutar_con_reintentos(
            lambda: supabase.table(
                "periodos_academicos"
            ).select(
                "id, nombre, fecha_inicio, fecha_fin"
            ).eq(
                "activo",
                True
            ).execute()
        ).data or []


        profesores = ejecutar_con_reintentos(
            lambda: supabase.table(
                "profesores"
            ).select(
                "id, nombre_completo, correo"
            ).eq(
                "activo",
                True
            ).execute()
        ).data or []


        return {

            "carreras":
                carreras,

            "cuatrimestres":
                cuatrimestres,

            "periodos":
                periodos,

            "profesores":
                profesores
        }


    except Exception as e:

        print(
            "ERROR EN /api/opciones-catalogo:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# CREAR PROFESOR
# ============================================================

@app.post("/api/profesores")
def crear_profesor(datos: dict):

    try:

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
                detail=(
                    "El nombre del profesor "
                    "es obligatorio."
                )
            )


        resultado = ejecutar_con_reintentos(
            lambda: supabase.table(
                "profesores"
            ).insert({

                "nombre_completo":
                    nombre,

                "correo":
                    correo,

                "activo":
                    True

            }).execute()
        )


        if not resultado.data:

            raise HTTPException(
                status_code=500,
                detail=(
                    "No se pudo crear el profesor."
                )
            )


        return resultado.data[0]


    except HTTPException:

        raise


    except Exception as e:

        print(
            "ERROR AL CREAR PROFESOR:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# CREAR MATERIA
# ============================================================

@app.post("/api/materias")
def crear_materia(datos: dict):

    try:

        clave = datos.get(
            "clave",
            ""
        ).strip()


        nombre = datos.get(
            "nombre",
            ""
        ).strip()


        horas_semana = datos.get(
            "horas_semana",
            0
        )


        requiere_laboratorio = datos.get(
            "requiere_laboratorio",
            False
        )


        cuatrimestre_id = datos.get(
            "cuatrimestre_id"
        )


        if not clave:

            raise HTTPException(
                status_code=400,
                detail=(
                    "La clave de la materia "
                    "es obligatoria."
                )
            )


        if not nombre:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El nombre de la materia "
                    "es obligatorio."
                )
            )


        if not cuatrimestre_id:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El cuatrimestre "
                    "es obligatorio."
                )
            )


        resultado = ejecutar_con_reintentos(
            lambda: supabase.table(
                "materias"
            ).insert({

                "clave":
                    clave,

                "nombre":
                    nombre,

                "horas_semana":
                    horas_semana,

                "requiere_laboratorio":
                    requiere_laboratorio,

                "cuatrimestre_id":
                    cuatrimestre_id,

                "activo":
                    True

            }).execute()
        )


        if not resultado.data:

            raise HTTPException(
                status_code=500,
                detail=(
                    "No se pudo crear la materia."
                )
            )


        return resultado.data[0]


    except HTTPException:

        raise


    except Exception as e:

        print(
            "ERROR AL CREAR MATERIA:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# CREAR GRUPO
# ============================================================

@app.post("/api/grupos")
def crear_grupo(datos: dict):

    try:

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
                detail=(
                    "El nombre del grupo "
                    "es obligatorio."
                )
            )


        if not cuatrimestre_id:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El cuatrimestre "
                    "es obligatorio."
                )
            )


        if not periodo_id:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El periodo académico "
                    "es obligatorio."
                )
            )


        if not turno:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El turno "
                    "es obligatorio."
                )
            )


        resultado = ejecutar_con_reintentos(
            lambda: supabase.table(
                "grupos"
            ).insert({

                "nombre":
                    nombre,

                "cuatrimestre_id":
                    cuatrimestre_id,

                "periodo_id":
                    periodo_id,

                "turno":
                    turno,

                "activo":
                    True

            }).execute()
        )


        if not resultado.data:

            raise HTTPException(
                status_code=500,
                detail=(
                    "No se pudo crear el grupo."
                )
            )


        return resultado.data[0]


    except HTTPException:

        raise


    except Exception as e:

        print(
            "ERROR AL CREAR GRUPO:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# CREAR ESPACIO
# ============================================================

@app.post("/api/espacios")
def crear_espacio(datos: dict):

    try:

        nombre = datos.get(
            "nombre",
            ""
        ).strip()


        tipo = datos.get(
            "tipo",
            "AULA"
        ).strip()


        capacidad = datos.get(
            "capacidad",
            0
        )


        if not nombre:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El nombre del espacio "
                    "es obligatorio."
                )
            )


        if tipo not in [
            "AULA",
            "LABORATORIO"
        ]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "El tipo debe ser AULA "
                    "o LABORATORIO."
                )
            )


        resultado = ejecutar_con_reintentos(
            lambda: supabase.table(
                "espacios"
            ).insert({

                "nombre":
                    nombre,

                "tipo":
                    tipo,

                "capacidad":
                    capacidad,

                "activo":
                    True

            }).execute()
        )


        if not resultado.data:

            raise HTTPException(
                status_code=500,
                detail=(
                    "No se pudo crear el espacio."
                )
            )


        return resultado.data[0]


    except HTTPException:

        raise


    except Exception as e:

        print(
            "ERROR AL CREAR ESPACIO:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# ELIMINAR / DESACTIVAR MATERIA
# ============================================================

@app.delete("/api/materias/{clave}")
def eliminar_materia(clave: str):

    try:

        resultado = ejecutar_con_reintentos(
            lambda: supabase.table(
                "materias"
            ).update({
                "activo": False
            }).eq(
                "clave",
                clave
            ).execute()
        )


        if not resultado.data:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No se encontró la materia."
                )
            )


        return {

            "mensaje":
                "Materia eliminada correctamente",

            "clave":
                clave
        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "ERROR AL ELIMINAR MATERIA:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# ELIMINAR / DESACTIVAR PROFESOR
# ============================================================

@app.delete("/api/profesores/{nombre}")
def eliminar_profesor(nombre: str):

    try:

        resultado = ejecutar_con_reintentos(
            lambda: supabase.table(
                "profesores"
            ).update({
                "activo": False
            }).eq(
                "nombre_completo",
                nombre
            ).execute()
        )


        if not resultado.data:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No se encontró el profesor."
                )
            )


        return {

            "mensaje":
                "Profesor eliminado correctamente",

            "nombre":
                nombre
        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "ERROR AL ELIMINAR PROFESOR:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# ELIMINAR / DESACTIVAR GRUPO
# ============================================================

@app.delete("/api/grupos/{nombre}")
def eliminar_grupo(nombre: str):

    try:

        resultado = ejecutar_con_reintentos(
            lambda: supabase.table(
                "grupos"
            ).update({
                "activo": False
            }).eq(
                "nombre",
                nombre
            ).execute()
        )


        if not resultado.data:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No se encontró el grupo."
                )
            )


        return {

            "mensaje":
                "Grupo eliminado correctamente",

            "nombre":
                nombre
        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "ERROR AL ELIMINAR GRUPO:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# ELIMINAR / DESACTIVAR ESPACIO
# ============================================================

@app.delete("/api/espacios/{nombre}")
def eliminar_espacio(nombre: str):

    try:

        resultado = ejecutar_con_reintentos(
            lambda: supabase.table(
                "espacios"
            ).update({
                "activo": False
            }).eq(
                "nombre",
                nombre
            ).execute()
        )


        if not resultado.data:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No se encontró el espacio."
                )
            )


        return {

            "mensaje":
                "Espacio eliminado correctamente",

            "nombre":
                nombre
        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "ERROR AL ELIMINAR ESPACIO:"
        )

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# GENERAR HORARIO
# ============================================================

@app.post("/api/generar-horario")
def arrancar_simulacion(
    datos_front: dict = None
):

    try:

        # ----------------------------------------------------
        # OBTENER DATOS
        # ----------------------------------------------------

        datos_bd = obtener_datos_bd()


        # ----------------------------------------------------
        # DIAGNÓSTICO
        # ----------------------------------------------------

        print("\n")

        print(
            "=============================================="
        )

        print(
            "       DATOS PARA EL ALGORITMO"
        )

        print(
            "=============================================="
        )


        print("\nGRUPOS:")

        print(
            datos_bd.get(
                "grupos"
            )
        )


        print("\nMATERIAS:")

        print(
            list(
                datos_bd.get(
                    "materias",
                    {}
                ).keys()
            )
        )


        print("\nDETALLE DE MATERIAS:")


        for codigo, materia in datos_bd.get(
            "materias",
            {}
        ).items():

            print(
                codigo,
                "->",
                materia
            )


        print("\nAULAS:")

        print(
            datos_bd.get(
                "aulas_teoricas"
            )
        )


        print("\nLABORATORIOS:")

        print(
            datos_bd.get(
                "laboratorios"
            )
        )


        print("\nDIAS:")

        print(
            datos_bd.get(
                "dias"
            )
        )


        print("\nBLOQUES:")

        print(
            datos_bd.get(
                "bloques_tiempo"
            )
        )


        print(
            "\n=============================================="
        )

        print(
            "       FIN DATOS PARA EL ALGORITMO"
        )

        print(
            "=============================================="
        )

        print("\n")


        # ----------------------------------------------------
        # PARÁMETROS DEL FRONTEND
        # ----------------------------------------------------

        if datos_front:

            datos_bd.update({

                "tamano_poblacion":
                    datos_front.get(
                        "tamano_poblacion",
                        300
                    ),

                "prob_cruza":
                    datos_front.get(
                        "prob_cruza",
                        0.85
                    ),

                "prob_mutacion":
                    datos_front.get(
                        "prob_mutacion",
                        0.15
                    ),

                "generaciones":
                    datos_front.get(
                        "generaciones",
                        500
                    )
            })


        # ----------------------------------------------------
        # MOTOR EVOLUTIVO
        # ----------------------------------------------------

        print(
            "=============================================="
        )

        print(
            "       INICIANDO MOTOR EVOLUTIVO"
        )

        print(
            "=============================================="
        )


        resultado = (
            motor_evolutivo
            .ejecutar_optimizador(
                datos_bd
            )
        )


        # ----------------------------------------------------
        # DIAGNÓSTICO DEL RESULTADO
        # ----------------------------------------------------

        print("\n")

        print(
            "=============================================="
        )

        print(
            "       RESULTADO DEL MOTOR EVOLUTIVO"
        )

        print(
            "=============================================="
        )


        print(
            "Mensaje:",
            resultado.get(
                "mensaje"
            )
        )


        print(
            "Fitness:",
            resultado.get(
                "fitness_final"
            )
        )


        horario = resultado.get(
            "horario",
            []
        )


        print(
            "Número de clases generadas:",
            len(horario)
        )


        if horario:

            print(
                "\nPRIMERAS 5 CLASES:"
            )


            for clase in horario[:5]:

                print(
                    clase
                )


        else:

            print(
                "\n⚠️ EL MOTOR DEVOLVIÓ 0 CLASES ⚠️"
            )


        print(
            "\n=============================================="
        )

        print(
            "       FIN DEL RESULTADO"
        )

        print(
            "=============================================="
        )

        print("\n")


        return resultado


    except HTTPException:

        raise


    except Exception as e:

        print("\n")

        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )

        print(
            "ERROR AL GENERAR HORARIO"
        )

        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )

        print(e)

        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )

        print("\n")


        raise HTTPException(
            status_code=500,
            detail=str(e)
        )