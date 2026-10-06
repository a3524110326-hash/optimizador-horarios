from supabase_client import supabase


def obtener_datos_para_algoritmo():
    """
    Obtiene de Supabase los datos que actualmente
    necesita motor_evolutivo.py.
    """

    # ==========================================
    # 1. GRUPOS
    # ==========================================

    respuesta_grupos = (
        supabase
        .table("grupos")
        .select("id, nombre, cuatrimestre_id")
        .eq("activo", True)
        .execute()
    )

    grupos_db = respuesta_grupos.data or []

    grupos = [
        grupo["nombre"]
        for grupo in grupos_db
    ]


    # ==========================================
    # 2. CUATRIMESTRES DE LOS GRUPOS
    # ==========================================

    cuatrimestres_ids = list({
        grupo["cuatrimestre_id"]
        for grupo in grupos_db
    })

    respuesta_cuatrimestres = (
        supabase
        .table("cuatrimestres")
        .select("id, numero")
        .execute()
    )

    cuatrimestres_db = respuesta_cuatrimestres.data or []

    cuatrimestre_por_id = {
        item["id"]: item["numero"]
        for item in cuatrimestres_db
    }


    # ==========================================
    # 3. MATERIAS
    # ==========================================

    respuesta_materias = (
        supabase
        .table("materias")
        .select(
            "id, clave, nombre, horas_semana, "
            "requiere_laboratorio, cuatrimestre_id"
        )
        .eq("activo", True)
        .execute()
    )

    materias_db = respuesta_materias.data or []


    # ==========================================
    # 4. PROFESORES
    # ==========================================

    respuesta_profesores = (
        supabase
        .table("profesores")
        .select("id, nombre_completo")
        .eq("activo", True)
        .execute()
    )

    profesores_db = respuesta_profesores.data or []

    profesores_por_id = {
        profesor["id"]: profesor["nombre_completo"]
        for profesor in profesores_db
    }


    # ==========================================
    # 5. RELACIÓN PROFESOR - MATERIA
    # ==========================================

    respuesta_profesor_materia = (
        supabase
        .table("profesor_materia")
        .select("profesor_id, materia_id")
        .execute()
    )

    relaciones = respuesta_profesor_materia.data or []

    profesor_por_materia = {}

    for relacion in relaciones:

        profesor_id = relacion["profesor_id"]
        materia_id = relacion["materia_id"]

        if profesor_id in profesores_por_id:
            profesor_por_materia[materia_id] = (
                profesores_por_id[profesor_id]
            )


    # ==========================================
    # 6. CONVERTIR MATERIAS AL FORMATO DEL MOTOR
    # ==========================================

    materias = {}

    for materia in materias_db:

        materias[materia["clave"]] = {
            "nombre": materia["nombre"],
            "horas": materia["horas_semana"],
            "requiere_lab": materia["requiere_laboratorio"],
            "profesor": profesor_por_materia.get(
                materia["id"],
                "Profesor no asignado"
            )
        }


    # ==========================================
    # 7. ESPACIOS
    # ==========================================

    respuesta_espacios = (
        supabase
        .table("espacios")
        .select("nombre, tipo")
        .eq("activo", True)
        .execute()
    )

    espacios_db = respuesta_espacios.data or []

    aulas_teoricas = [
        espacio["nombre"]
        for espacio in espacios_db
        if espacio["tipo"] == "AULA"
    ]

    laboratorios = [
        espacio["nombre"]
        for espacio in espacios_db
        if espacio["tipo"] == "LABORATORIO"
    ]


    # ==========================================
    # 8. BLOQUES DE HORARIO
    # ==========================================

    respuesta_bloques = (
        supabase
        .table("bloques_horario")
        .select(
            "dia_semana, numero_bloque, "
            "hora_inicio, hora_fin, es_receso"
        )
        .eq("es_receso", False)
        .order("dia_semana")
        .order("numero_bloque")
        .execute()
    )

    bloques_db = respuesta_bloques.data or []


    nombres_dias = {
        1: "Lunes",
        2: "Martes",
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes"
    }

    dias = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes"
    ]

    bloques_tiempo = []

    bloques_vistos = set()

    for bloque in bloques_db:

        rango = (
            f"{bloque['hora_inicio'][:5]}"
            f"-"
            f"{bloque['hora_fin'][:5]}"
        )

        if rango not in bloques_vistos:
            bloques_tiempo.append(rango)
            bloques_vistos.add(rango)


    # ==========================================
    # 9. RESULTADO FINAL
    # ==========================================

    return {
        "grupos": grupos,
        "materias": materias,
        "laboratorios": laboratorios,
        "aulas_teoricas": aulas_teoricas,
        "dias": dias,
        "bloques_tiempo": bloques_tiempo
    }