import random
import copy

from deap import base, creator, tools, algorithms


# ============================================================
# 1. CONFIGURACIÓN BASE DE DEAP
# ============================================================

if not hasattr(creator, "FitnessMin"):
    creator.create(
        "FitnessMin",
        base.Fitness,
        weights=(-1.0,)
    )

if not hasattr(creator, "Individuo"):
    creator.create(
        "Individuo",
        list,
        fitness=creator.FitnessMin
    )


# ============================================================
# 2. FUNCIÓN PRINCIPAL
# ============================================================

def ejecutar_optimizador(datos_front):
    """
    Ejecuta el algoritmo evolutivo para generar un horario.

    Recibe:
        datos_front: diccionario con grupos, materias, espacios,
                     días y bloques de tiempo.

    Devuelve:
        Diccionario JSON con:
        - mensaje
        - fitness_final
        - horario
    """

    # ========================================================
    # 3. OBTENER DATOS
    # ========================================================

    grupos = datos_front.get("grupos", [])
    materias = datos_front.get("materias", {})
    laboratorios = datos_front.get("laboratorios", [])
    aulas_teoricas = datos_front.get("aulas_teoricas", [])
    dias = datos_front.get("dias", [])
    bloques_tiempo = datos_front.get("bloques_tiempo", [])


    # ========================================================
    # 4. VALIDACIONES BÁSICAS
    # ========================================================

    if not grupos:
        raise ValueError("No se recibieron grupos.")

    if not materias:
        raise ValueError("No se recibieron materias.")

    if not dias:
        raise ValueError("No se recibieron días.")

    if not bloques_tiempo:
        raise ValueError("No se recibieron bloques de tiempo.")

    if not aulas_teoricas and not laboratorios:
        raise ValueError("No existen espacios disponibles.")


    # ========================================================
    # 5. IDENTIFICAR MATERIAS POR CUATRIMESTRE
    # ========================================================

    materias_1er = {
        "FSC",
        "FUP",
        "FUR",
        "FUM",
        "DHV",
        "CHD",
        "IN1"
    }

    materias_4 = {
        "AND",
        "CÁV",
        "DEA",
        "ESD",
        "APW",
        "IN4",
        "ÉTP"
    }


    # ========================================================
    # 6. CAJA DE HERRAMIENTAS DE DEAP
    # ========================================================

    toolbox = base.Toolbox()


    # ========================================================
    # 7. GENERADOR DE HORARIO ALEATORIO
    # ========================================================

    def generar_horario_aleatorio():

        horario_completo = []

        for grupo in grupos:

            # Determinar cuatrimestre por el nombre del grupo.
            prefijo = grupo[0]

            if prefijo == "1":
                materias_validas = materias_1er

            elif prefijo == "4":
                materias_validas = materias_4

            else:
                # Si aparece un grupo diferente,
                # no se le asignan materias.
                continue


            for codigo_materia, detalles in materias.items():

                # Si la materia no corresponde al cuatrimestre,
                # se ignora.
                if codigo_materia not in materias_validas:
                    continue


                nombre_materia = detalles.get(
                    "nombre",
                    codigo_materia
                )

                horas = int(
                    detalles.get("horas", 0)
                )

                requiere_lab = bool(
                    detalles.get("requiere_lab", False)
                )

                profesor = detalles.get(
                    "profesor",
                    "Sin profesor"
                )


                # ------------------------------------------------
                # Determinar espacios posibles
                # ------------------------------------------------

                if requiere_lab:

                    espacios_disponibles = laboratorios

                else:

                    espacios_disponibles = aulas_teoricas


                # Si una materia requiere laboratorio pero
                # no existen laboratorios, usamos una lista vacía.
                if not espacios_disponibles:
                    espacios_disponibles = (
                        laboratorios
                        if laboratorios
                        else aulas_teoricas
                    )


                # ------------------------------------------------
                # Crear cada hora de la materia
                # ------------------------------------------------

                for _ in range(horas):

                    gen_clase = {
                        "grupo": grupo,
                        "materia_codigo": codigo_materia,
                        "materia": nombre_materia,
                        "profesor": profesor,
                        "dia": random.choice(dias),
                        "bloque": random.choice(bloques_tiempo),
                        "espacio": random.choice(
                            espacios_disponibles
                        )
                    }

                    horario_completo.append(gen_clase)


        return horario_completo


    # ========================================================
    # 8. FUNCIÓN DE EVALUACIÓN / FITNESS
    # ========================================================

    def evaluar_horario(individuo):

        penalizaciones = 0


        # ----------------------------------------------------
        # Registros de recursos
        # ----------------------------------------------------

        registro_espacios = set()
        registro_profesores = set()
        registro_grupos = set()

        # Evita que una materia del mismo grupo
        # aparezca dos veces exactamente en el mismo bloque.
        registro_materias_grupo = set()


        # ====================================================
        # REVISAR CADA CLASE
        # ====================================================

        for gen in individuo:

            grupo = gen["grupo"]
            profesor = gen["profesor"]
            dia = gen["dia"]
            bloque = gen["bloque"]
            espacio = gen["espacio"]
            materia_codigo = gen.get(
                "materia_codigo",
                gen["materia"]
            )


            # =================================================
            # 1. CONFLICTO DE ESPACIO
            # =================================================

            llave_espacio = (
                espacio,
                dia,
                bloque
            )

            if llave_espacio in registro_espacios:

                # Dos grupos en el mismo salón/laboratorio.
                penalizaciones += 50

            else:

                registro_espacios.add(
                    llave_espacio
                )


            # =================================================
            # 2. CONFLICTO DE PROFESOR
            # =================================================

            llave_profesor = (
                profesor,
                dia,
                bloque
            )

            if llave_profesor in registro_profesores:

                # Un profesor no puede impartir
                # dos clases simultáneamente.
                penalizaciones += 100

            else:

                registro_profesores.add(
                    llave_profesor
                )


            # =================================================
            # 3. CONFLICTO DE GRUPO
            # =================================================

            llave_grupo = (
                grupo,
                dia,
                bloque
            )

            if llave_grupo in registro_grupos:

                # Un grupo no puede estar en dos materias
                # simultáneamente.
                penalizaciones += 100

            else:

                registro_grupos.add(
                    llave_grupo
                )


            # =================================================
            # 4. MISMA MATERIA DEL MISMO GRUPO
            # =================================================

            llave_materia_grupo = (
                grupo,
                materia_codigo,
                dia,
                bloque
            )

            if llave_materia_grupo in registro_materias_grupo:

                penalizaciones += 75

            else:

                registro_materias_grupo.add(
                    llave_materia_grupo
                )


        # ====================================================
        # 5. PENALIZACIÓN POR MATERIAS EN ESPACIO INCORRECTO
        # ====================================================

        for gen in individuo:

            materia_codigo = gen.get(
                "materia_codigo",
                ""
            )

            espacio = gen["espacio"]

            detalles = materias.get(
                materia_codigo,
                {}
            )

            requiere_lab = detalles.get(
                "requiere_lab",
                False
            )


            if requiere_lab:

                # Materia de laboratorio fuera de laboratorio.
                if espacio not in laboratorios:

                    penalizaciones += 200

            else:

                # Materia teórica dentro de un laboratorio.
                # No es necesariamente imposible, pero para
                # nuestro modelo queremos aulas teóricas.
                if espacio not in aulas_teoricas:

                    penalizaciones += 200


        return (penalizaciones,)


    # ========================================================
    # 9. MUTACIÓN
    # ========================================================

    def mutar_horario(individuo):

        if not individuo:
            return (individuo,)


        # Elegimos una clase al azar.
        indice = random.randrange(
            len(individuo)
        )

        gen = individuo[indice]


        # Cambiar día.
        gen["dia"] = random.choice(
            dias
        )


        # Cambiar bloque.
        gen["bloque"] = random.choice(
            bloques_tiempo
        )


        # ----------------------------------------------------
        # También podemos cambiar el espacio.
        # ----------------------------------------------------

        materia_codigo = gen.get(
            "materia_codigo",
            ""
        )

        detalles = materias.get(
            materia_codigo,
            {}
        )

        requiere_lab = detalles.get(
            "requiere_lab",
            False
        )


        if requiere_lab and laboratorios:

            gen["espacio"] = random.choice(
                laboratorios
            )

        elif not requiere_lab and aulas_teoricas:

            gen["espacio"] = random.choice(
                aulas_teoricas
            )


        return (individuo,)


    # ========================================================
    # 10. CRUZA SEGURA
    # ========================================================

    def cruzar_horarios(individuo1, individuo2):

        """
        Cruza dos horarios utilizando dos puntos.

        Se realizan copias profundas para evitar que
        los diccionarios internos queden compartidos
        entre individuos.
        """

        hijo1 = copy.deepcopy(individuo1)
        hijo2 = copy.deepcopy(individuo2)


        if len(hijo1) < 2 or len(hijo2) < 2:

            return (
                hijo1,
                hijo2
            )


        punto1 = random.randint(
            1,
            len(hijo1) - 1
        )

        punto2 = random.randint(
            1,
            len(hijo1) - 1
        )


        if punto1 > punto2:

            punto1, punto2 = (
                punto2,
                punto1
            )


        hijo1[punto1:punto2], hijo2[punto1:punto2] = (
            hijo2[punto1:punto2],
            hijo1[punto1:punto2]
        )


        # Invalidar fitness porque los hijos cambiaron.
        if hasattr(hijo1.fitness, "values"):
            del hijo1.fitness.values

        if hasattr(hijo2.fitness, "values"):
            del hijo2.fitness.values


        return (
            hijo1,
            hijo2
        )


    # ========================================================
    # 11. REGISTRO DEL TOOLBOX
    # ========================================================

    toolbox.register(
        "individuo",
        tools.initIterate,
        creator.Individuo,
        generar_horario_aleatorio
    )


    toolbox.register(
        "poblacion",
        tools.initRepeat,
        list,
        toolbox.individuo
    )


    toolbox.register(
        "evaluate",
        evaluar_horario
    )


    toolbox.register(
        "select",
        tools.selTournament,
        tournsize=3
    )


    toolbox.register(
        "mate",
        cruzar_horarios
    )


    toolbox.register(
        "mutate",
        mutar_horario
    )


    # ========================================================
    # 12. PARÁMETROS DEL ALGORITMO
    # ========================================================

    TAMANO_POBLACION = int(
        datos_front.get(
            "tamano_poblacion",
            300
        )
    )

    PROB_CRUZA = float(
        datos_front.get(
            "prob_cruza",
            0.85
        )
    )

    PROB_MUTACION = float(
        datos_front.get(
            "prob_mutacion",
            0.20
        )
    )

    GENERACIONES = int(
        datos_front.get(
            "generaciones",
            500
        )
    )


    # ========================================================
    # 13. CREAR POBLACIÓN
    # ========================================================

    poblacion = toolbox.poblacion(
        n=TAMANO_POBLACION
    )


    # ========================================================
    # 14. ESTADÍSTICAS
    # ========================================================

    estadisticas = tools.Statistics(
        lambda individuo:
        individuo.fitness.values
    )

    estadisticas.register(
        "Min",
        min
    )

    estadisticas.register(
        "Promedio",
        lambda valores:
        sum(
            v[0]
            for v in valores
        ) / len(valores)
        if valores
        else 0
    )


    # ========================================================
    # 15. EJECUTAR ALGORITMO EVOLUTIVO
    # ========================================================

    poblacion_final, registro_log = algorithms.eaSimple(
        poblacion,
        toolbox,
        cxpb=PROB_CRUZA,
        mutpb=PROB_MUTACION,
        ngen=GENERACIONES,
        stats=estadisticas,
        verbose=False
    )


    # ========================================================
    # 16. OBTENER MEJOR INDIVIDUO
    # ========================================================

    mejor_horario = tools.selBest(
        poblacion_final,
        1
    )[0]


    # ========================================================
    # 17. CALCULAR FITNESS FINAL
    # ========================================================

    fitness_final = mejor_horario.fitness.values[0]


    # ========================================================
    # 18. LIMPIAR HORARIO PARA JSON
    # ========================================================

    horario_limpio = []

    for gen in mejor_horario:

        horario_limpio.append(
            {
                "grupo": gen["grupo"],
                "materia_codigo": gen.get(
                    "materia_codigo",
                    ""
                ),
                "materia": gen["materia"],
                "profesor": gen["profesor"],
                "dia": gen["dia"],
                "bloque": gen["bloque"],
                "espacio": gen["espacio"]
            }
        )


    # ========================================================
    # 19. RESULTADO FINAL
    # ========================================================

    return {
        "mensaje": "Simulación completada con éxito",

        "fitness_final": fitness_final,

        "parametros": {
            "tamano_poblacion": TAMANO_POBLACION,
            "prob_cruza": PROB_CRUZA,
            "prob_mutacion": PROB_MUTACION,
            "generaciones": GENERACIONES
        },

        "horario": horario_limpio
    }