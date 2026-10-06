from supabase_client import supabase


# ============================================================
# DATOS GENERALES DEL PROYECTO
# ============================================================

NOMBRE_CARRERA = "Tecnologias de la Informacion e Inovacion Digital"
NOMBRE_PERIODO = "sep-dic 2026"


# ============================================================
# DATOS TOMADOS DE datos_prueba.py
# ============================================================

aulas_teoricas = [
    "Aula_1",
    "Aula_2",
    "Aula_3",
    "Aula_4"
]

laboratorios = [
    "Lab_1",
    "Lab_2"
]

grupos = [
    "1A",
    "1B",
    "1C",
    "1D",
    "4A",
    "4B",
    "4C"
]

dias = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes"
]

bloques_tiempo = [
    "07:00-07:50",
    "07:50-08:40",
    "08:40-09:30",
    "10:00-10:50",
    "10:50-11:40",
    "11:40-12:30",
    "12:30-13:20",
    "13:20-14:10",
    "14:10-15:00"
]


materias = {
    # PRIMER CUATRIMESTRE

    "FSC": {
        "nombre": "Física",
        "horas": 6,
        "requiere_lab": False,
        "profesor": "Mtro. Juan Carlos De Los Santos Barbosa"
    },

    "FUP": {
        "nombre": "Fundamentos de Programación",
        "horas": 2,
        "requiere_lab": True,
        "profesor": "Dr. Julio César Alfaro Herrera"
    },

    "FUR": {
        "nombre": "Fundamentos de Redes",
        "horas": 2,
        "requiere_lab": True,
        "profesor": "Dra. Rosario Vargas Flores"
    },

    "FUM": {
        "nombre": "Fundamentos Matemáticos",
        "horas": 7,
        "requiere_lab": False,
        "profesor": "Mtro. Alfonso Noguerón Soto"
    },

    "DHV": {
        "nombre": "Desarrollo Humano y Valores",
        "horas": 4,
        "requiere_lab": False,
        "profesor": "Mtro. Erik Roque Mendoza"
    },

    "CHD": {
        "nombre": "Comunicación y Habilidades Digitales",
        "horas": 5,
        "requiere_lab": True,
        "profesor": "Mtro. Luis Roberto Bravo Torrescano"
    },

    "IN1": {
        "nombre": "Inglés I",
        "horas": 5,
        "requiere_lab": False,
        "profesor": "Mtra. Adriana Patricia Quizamán Olguín"
    },

    # CUARTO CUATRIMESTRE

    "AND": {
        "nombre": "Análisis y diseño de software",
        "horas": 3,
        "requiere_lab": False,
        "profesor": "Dra. Rosario Vargas Flores"
    },

    "CÁV": {
        "nombre": "Cálculo de varias variables",
        "horas": 5,
        "requiere_lab": False,
        "profesor": "Mtro. José Alberto Castelán De La Rosa"
    },

    "DEA": {
        "nombre": "Desarrollo de aplicaciones Móviles",
        "horas": 4,
        "requiere_lab": True,
        "profesor": "Dr. Héctor Bernardo Ortega Gines"
    },

    "ESD": {
        "nombre": "Estructura de datos",
        "horas": 3,
        "requiere_lab": True,
        "profesor": "Dra. Yedid Curloca Varela"
    },

    "APW": {
        "nombre": "Aplicaciones Web",
        "horas": 4,
        "requiere_lab": True,
        "profesor": "Dra. Yedid Curloca Varela"
    },

    "IN4": {
        "nombre": "Inglés IV",
        "horas": 5,
        "requiere_lab": False,
        "profesor": "Mtra. Adriana Patricia Quizamán Olguín"
    },

    "ÉTP": {
        "nombre": "Ética profesional",
        "horas": 5,
        "requiere_lab": False,
        "profesor": "Mtro. Erik Roque Mendoza"
    }
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_o_crear_carrera():
    respuesta = (
        supabase
        .table("carreras")
        .select("*")
        .eq("nombre", NOMBRE_CARRERA)
        .execute()
    )

    if respuesta.data:
        return respuesta.data[0]

    respuesta = (
        supabase
        .table("carreras")
        .insert({
            "nombre": NOMBRE_CARRERA,
            "clave": "TICSD"
        })
        .execute()
    )

    return respuesta.data[0]


def obtener_o_crear_periodo():
    respuesta = (
        supabase
        .table("periodos_academicos")
        .select("*")
        .eq("nombre", NOMBRE_PERIODO)
        .execute()
    )

    if respuesta.data:
        return respuesta.data[0]

    respuesta = (
        supabase
        .table("periodos_academicos")
        .insert({
            "nombre": NOMBRE_PERIODO,
            "activo": True
        })
        .execute()
    )

    return respuesta.data[0]


def obtener_o_crear_cuatrimestre(numero, carrera_id):
    nombre = f"{numero}° Cuatrimestre"

    respuesta = (
        supabase
        .table("cuatrimestres")
        .select("*")
        .eq("numero", numero)
        .eq("carrera_id", carrera_id)
        .execute()
    )

    if respuesta.data:
        return respuesta.data[0]

    respuesta = (
        supabase
        .table("cuatrimestres")
        .insert({
            "numero": numero,
            "nombre": nombre,
            "carrera_id": carrera_id
        })
        .execute()
    )

    return respuesta.data[0]


def obtener_o_crear_grupo(nombre, cuatrimestre_id, periodo_id):
    respuesta = (
        supabase
        .table("grupos")
        .select("*")
        .eq("nombre", nombre)
        .eq("periodo_id", periodo_id)
        .execute()
    )

    if respuesta.data:
        return respuesta.data[0]

    respuesta = (
        supabase
        .table("grupos")
        .insert({
            "nombre": nombre,
            "cuatrimestre_id": cuatrimestre_id,
            "periodo_id": periodo_id,
            "activo": True
        })
        .execute()
    )

    return respuesta.data[0]


def obtener_o_crear_profesor(nombre):
    respuesta = (
        supabase
        .table("profesores")
        .select("*")
        .eq("nombre_completo", nombre)
        .execute()
    )

    if respuesta.data:
        return respuesta.data[0]

    respuesta = (
        supabase
        .table("profesores")
        .insert({
            "nombre_completo": nombre
        })
        .execute()
    )

    return respuesta.data[0]


def obtener_o_crear_materia(
    clave,
    datos,
    carrera_id,
    cuatrimestre_id
):
    respuesta = (
        supabase
        .table("materias")
        .select("*")
        .eq("clave", clave)
        .execute()
    )

    if respuesta.data:
        return respuesta.data[0]

    respuesta = (
        supabase
        .table("materias")
        .insert({
            "clave": clave,
            "nombre": datos["nombre"],
            "horas_semana": datos["horas"],
            "requiere_laboratorio": datos["requiere_lab"],
            "carrera_id": carrera_id,
            "cuatrimestre_id": cuatrimestre_id,
            "activo": True
        })
        .execute()
    )

    return respuesta.data[0]


# ============================================================
# CARGA PRINCIPAL
# ============================================================

def cargar_datos():

    print("\n==========================================")
    print(" CARGANDO DATOS EN SUPABASE")
    print("==========================================\n")

    # --------------------------------------------------------
    # 1. CARRERA
    # --------------------------------------------------------

    carrera = obtener_o_crear_carrera()
    carrera_id = carrera["id"]

    print(f"✓ Carrera: {carrera['nombre']}")


    # --------------------------------------------------------
    # 2. PERIODO
    # --------------------------------------------------------

    periodo = obtener_o_crear_periodo()
    periodo_id = periodo["id"]

    print(f"✓ Periodo: {periodo['nombre']}")


    # --------------------------------------------------------
    # 3. CUATRIMESTRES
    # --------------------------------------------------------

    cuatri_1 = obtener_o_crear_cuatrimestre(
        1,
        carrera_id
    )

    cuatri_4 = obtener_o_crear_cuatrimestre(
        4,
        carrera_id
    )

    print("✓ Cuatrimestres 1 y 4")


    # --------------------------------------------------------
    # 4. GRUPOS
    # --------------------------------------------------------

    grupos_db = {}

    for nombre_grupo in grupos:

        if nombre_grupo.startswith("1"):
            cuatrimestre_id = cuatri_1["id"]
        else:
            cuatrimestre_id = cuatri_4["id"]

        grupo = obtener_o_crear_grupo(
            nombre_grupo,
            cuatrimestre_id,
            periodo_id
        )

        grupos_db[nombre_grupo] = grupo

    print(f"✓ Grupos cargados: {len(grupos_db)}")


    # --------------------------------------------------------
    # 5. PROFESORES
    # --------------------------------------------------------

    profesores_db = {}

    for datos in materias.values():

        nombre_profesor = datos["profesor"]

        if nombre_profesor not in profesores_db:

            profesor = obtener_o_crear_profesor(
                nombre_profesor
            )

            profesores_db[nombre_profesor] = profesor

    print(
        f"✓ Profesores cargados: "
        f"{len(profesores_db)}"
    )


    # --------------------------------------------------------
    # 6. MATERIAS
    # --------------------------------------------------------

    materias_db = {}

    for clave, datos in materias.items():

        if clave in [
            "FSC",
            "FUP",
            "FUR",
            "FUM",
            "DHV",
            "CHD",
            "IN1"
        ]:
            cuatrimestre_id = cuatri_1["id"]
        else:
            cuatrimestre_id = cuatri_4["id"]

        materia = obtener_o_crear_materia(
            clave,
            datos,
            carrera_id,
            cuatrimestre_id
        )

        materias_db[clave] = materia

    print(
        f"✓ Materias cargadas: "
        f"{len(materias_db)}"
    )


    # --------------------------------------------------------
    # 7. PROFESOR - MATERIA
    # --------------------------------------------------------

    relaciones_profesor_materia = 0

    for clave, datos in materias.items():

        profesor = profesores_db[
            datos["profesor"]
        ]

        materia = materias_db[clave]

        existente = (
            supabase
            .table("profesor_materia")
            .select("id")
            .eq("profesor_id", profesor["id"])
            .eq("materia_id", materia["id"])
            .execute()
        )

        if not existente.data:

            supabase.table(
                "profesor_materia"
            ).insert({
                "profesor_id": profesor["id"],
                "materia_id": materia["id"]
            }).execute()

            relaciones_profesor_materia += 1

    print(
        "✓ Relaciones profesor-materia: "
        f"{relaciones_profesor_materia}"
    )


    # --------------------------------------------------------
    # 8. GRUPO - MATERIA
    # --------------------------------------------------------

    relaciones_grupo_materia = 0

    materias_1 = [
        "FSC",
        "FUP",
        "FUR",
        "FUM",
        "DHV",
        "CHD",
        "IN1"
    ]

    materias_4 = [
        "AND",
        "CÁV",
        "DEA",
        "ESD",
        "APW",
        "IN4",
        "ÉTP"
    ]

    for nombre_grupo, grupo in grupos_db.items():

        if nombre_grupo.startswith("1"):
            materias_grupo = materias_1
        else:
            materias_grupo = materias_4

        for clave in materias_grupo:

            materia = materias_db[clave]

            existente = (
                supabase
                .table("grupo_materia")
                .select("id")
                .eq("grupo_id", grupo["id"])
                .eq("materia_id", materia["id"])
                .execute()
            )

            if not existente.data:

                supabase.table(
                    "grupo_materia"
                ).insert({
                    "grupo_id": grupo["id"],
                    "materia_id": materia["id"]
                }).execute()

                relaciones_grupo_materia += 1

    print(
        "✓ Relaciones grupo-materia: "
        f"{relaciones_grupo_materia}"
    )


    # --------------------------------------------------------
    # 9. ESPACIOS
    # --------------------------------------------------------

    espacios = []

    for nombre in aulas_teoricas:

        espacios.append({
            "nombre": nombre,
            "tipo": "AULA",
            "capacidad": 40,
            "activo": True
        })

    for nombre in laboratorios:

        espacios.append({
            "nombre": nombre,
            "tipo": "LABORATORIO",
            "capacidad": 36,
            "activo": True
        })

    espacios_creados = 0

    for espacio in espacios:

        existente = (
            supabase
            .table("espacios")
            .select("id")
            .eq("nombre", espacio["nombre"])
            .execute()
        )

        if not existente.data:

            supabase.table(
                "espacios"
            ).insert(espacio).execute()

            espacios_creados += 1

    print(
        f"✓ Espacios cargados: {len(espacios)}"
    )


    # --------------------------------------------------------
    # 10. BLOQUES DE HORARIO
    # --------------------------------------------------------

    bloques_creados = 0

    for dia_numero, dia in enumerate(dias, start=1):

        for numero_bloque, rango in enumerate(
            bloques_tiempo,
            start=1
        ):

            hora_inicio, hora_fin = rango.split("-")

            existente = (
                supabase
                .table("bloques_horario")
                .select("id")
                .eq("dia_semana", dia_numero)
                .eq("numero_bloque", numero_bloque)
                .execute()
            )

            if not existente.data:

                supabase.table(
                    "bloques_horario"
                ).insert({
                    "dia_semana": dia_numero,
                    "numero_bloque": numero_bloque,
                    "hora_inicio": hora_inicio,
                    "hora_fin": hora_fin,
                    "es_receso": False
                }).execute()

                bloques_creados += 1

    print(
        f"✓ Bloques de horario: "
        f"{len(dias) * len(bloques_tiempo)}"
    )


    print("\n==========================================")
    print(" CARGA COMPLETADA")
    print("==========================================")
    print("✓ Supabase contiene los datos iniciales.")
    print("✓ Puedes revisar las tablas desde Table Editor.")
    print("==========================================\n")


if __name__ == "__main__":
    cargar_datos()