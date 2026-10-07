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
# 2. OBTENER CUATRIMESTRE DEL GRUPO
# ============================================================

def obtener_cuatrimestre_grupo(grupo):

    """
    Obtiene el número de cuatrimestre a partir
    del nombre del grupo.

    Ejemplos:

        1A -> 1
        1B -> 1
        1E -> 1
        4A -> 4
        4B -> 4
    """

    if not grupo:
        return None

    texto = str(grupo).strip()

    digitos = ""

    for caracter in texto:

        if caracter.isdigit():

            digitos += caracter

        else:

            break

    if not digitos:

        return None

    return int(digitos)


# ============================================================
# 3. FUNCIÓN PRINCIPAL
# ============================================================

def ejecutar_optimizador(datos_front):

    """
    Ejecuta el algoritmo evolutivo para generar un horario.

    Recibe:

        datos_front:
            Diccionario con:

            - grupos
            - materias
            - laboratorios
            - aulas_teoricas
            - dias
            - bloques_tiempo

    Devuelve:

        Diccionario JSON con:

            - mensaje
            - fitness_final
            - parametros
            - horario
    """


    # ========================================================
    # 4. OBTENER DATOS
    # ========================================================

    grupos = datos_front.get(
        "grupos",
        []
    )

    materias = datos_front.get(
        "materias",
        {}
    )

    laboratorios = datos_front.get(
        "laboratorios",
        []
    )

    aulas_teoricas = datos_front.get(
        "aulas_teoricas",
        []
    )

    dias = datos_front.get(
        "dias",
        []
    )

    bloques_tiempo = datos_front.get(
        "bloques_tiempo",
        []
    )


    # ========================================================
    # 5. VALIDACIONES BÁSICAS
    # ========================================================

    if not grupos:

        raise ValueError(
            "No se recibieron grupos."
        )


    if not materias:

        raise ValueError(
            "No se recibieron materias."
        )


    if not dias:

        raise ValueError(
            "No se recibieron días."
        )


    if not bloques_tiempo:

        raise ValueError(
            "No se recibieron bloques de tiempo."
        )


    if not aulas_teoricas and not laboratorios:

        raise ValueError(
            "No existen espacios disponibles."
        )


    # ========================================================
    # 6. MOSTRAR INFORMACIÓN DE DIAGNÓSTICO
    # ========================================================

    print("\n")
    print("==============================================")
    print("       MOTOR EVOLUTIVO")
    print("==============================================")

    print("Grupos recibidos:")

    for grupo in grupos:

        print(
            "  ",
            grupo,
            "-> cuatrimestre:",
            obtener_cuatrimestre_grupo(grupo)
        )


    print("\nMaterias recibidas:")

    for codigo, detalles in materias.items():

        print(
            "  ",
            codigo,
            "-> cuatrimestre:",
            detalles.get("cuatrimestre"),
            "| horas:",
            detalles.get("horas"),
            "| profesor:",
            detalles.get("profesor")
        )


    print("\n==============================================")
    print("       ASIGNACIÓN DE MATERIAS")
    print("==============================================")


    # ========================================================
    # 7. FUNCIÓN PARA GENERAR HORARIO ALEATORIO
    # ========================================================

    def generar_horario_aleatorio():

        horario_completo = []


        # ----------------------------------------------------
        # Recorrer grupos
        # ----------------------------------------------------

        for grupo in grupos:

            cuatrimestre_grupo = (
                obtener_cuatrimestre_grupo(
                    grupo
                )
            )


            # Si no podemos determinar el cuatrimestre,
            # no podemos asignarle materias.

            if cuatrimestre_grupo is None:

                print(
                    "⚠️ Grupo ignorado:",
                    grupo,
                    "- no se pudo determinar el cuatrimestre."
                )

                continue


            print(
                "Grupo",
                grupo,
                "-> cuatrimestre",
                cuatrimestre_grupo
            )


            materias_grupo = []


            # ------------------------------------------------
            # Buscar materias del mismo cuatrimestre
            # ------------------------------------------------

            for codigo_materia, detalles in materias.items():

                cuatrimestre_materia = detalles.get(
                    "cuatrimestre"
                )


                if cuatrimestre_materia == cuatrimestre_grupo:

                    materias_grupo.append(
                        codigo_materia
                    )


            print(
                "   Materias encontradas:",
                materias_grupo
            )


            # ------------------------------------------------
            # Si no tiene materias
            # ------------------------------------------------

            if not materias_grupo:

                print(
                    "   ⚠️ No hay materias para el grupo",
                    grupo
                )

                continue


            # ------------------------------------------------
            # Crear clases
            # ------------------------------------------------

            for codigo_materia in materias_grupo:

                detalles = materias.get(
                    codigo_materia,
                    {}
                )


                nombre_materia = detalles.get(
                    "nombre",
                    codigo_materia
                )


                horas = int(
                    detalles.get(
                        "horas",
                        0
                    )
                )


                requiere_lab = bool(
                    detalles.get(
                        "requiere_lab",
                        False
                    )
                )


                profesor = detalles.get(
                    "profesor",
                    "Sin profesor"
                )


                # ------------------------------------------------
                # Determinar espacios
                # ------------------------------------------------

                if requiere_lab:

                    espacios_disponibles = (
                        laboratorios
                    )

                else:

                    espacios_disponibles = (
                        aulas_teoricas
                    )


                # ------------------------------------------------
                # Si no existe el espacio requerido,
                # utilizar cualquier espacio disponible.
                # ------------------------------------------------

                if not espacios_disponibles:

                    espacios_disponibles = (
                        laboratorios
                        if laboratorios
                        else aulas_teoricas
                    )


                # ------------------------------------------------
                # Seguridad adicional
                # ------------------------------------------------

                if not espacios_disponibles:

                    raise ValueError(
                        f"No existen espacios disponibles "
                        f"para la materia {codigo_materia}."
                    )


                # ------------------------------------------------
                # Crear una clase por cada hora semanal
                # ------------------------------------------------

                for _ in range(horas):

                    gen_clase = {

                        "grupo": grupo,

                        "materia_codigo": (
                            codigo_materia
                        ),

                        "materia": (
                            nombre_materia
                        ),

                        "profesor": (
                            profesor
                        ),

                        "dia": random.choice(
                            dias
                        ),

                        "bloque": random.choice(
                            bloques_tiempo
                        ),

                        "espacio": random.choice(
                            espacios_disponibles
                        )
                    }


                    horario_completo.append(
                        gen_clase
                    )


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


            # No penalizamos "Sin profesor" como si fuera
            # el mismo profesor real.

            if profesor != "Sin profesor":

                if llave_profesor in registro_profesores:

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
        # 5. ESPACIOS CORRECTOS
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

                # Materia de laboratorio debe estar
                # en laboratorio.

                if espacio not in laboratorios:

                    penalizaciones += 200

            else:

                # Materia teórica debe estar
                # en aula teórica.

                if espacio not in aulas_teoricas:

                    penalizaciones += 200


        return (
            penalizaciones,
        )


    # ========================================================
    # 9. MUTACIÓN
    # ========================================================

    def mutar_horario(individuo):

        if not individuo:

            return (
                individuo,
            )


        # ----------------------------------------------------
        # Elegir una clase
        # ----------------------------------------------------

        indice = random.randrange(
            len(individuo)
        )


        gen = individuo[indice]


        # ----------------------------------------------------
        # Cambiar día
        # ----------------------------------------------------

        gen["dia"] = random.choice(
            dias
        )


        # ----------------------------------------------------
        # Cambiar bloque
        # ----------------------------------------------------

        gen["bloque"] = random.choice(
            bloques_tiempo
        )


        # ----------------------------------------------------
        # Cambiar espacio
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


        return (
            individuo,
        )


    # ========================================================
    # 10. CRUZA SEGURA
    # ========================================================

    def cruzar_horarios(
        individuo1,
        individuo2
    ):

        """
        Cruza dos horarios utilizando
        dos puntos.

        Se realizan copias profundas para
        evitar compartir diccionarios.
        """

        hijo1 = copy.deepcopy(
            individuo1
        )

        hijo2 = copy.deepcopy(
            individuo2
        )


        # ----------------------------------------------------
        # Si no hay suficientes elementos,
        # no realizar cruza.
        # ----------------------------------------------------

        if (
            len(hijo1) < 2
            or
            len(hijo2) < 2
        ):

            return (
                hijo1,
                hijo2
            )


        # ----------------------------------------------------
        # Los dos individuos deben tener el mismo tamaño
        # para realizar la cruza correctamente.
        # ----------------------------------------------------

        longitud = min(
            len(hijo1),
            len(hijo2)
        )


        if longitud < 2:

            return (
                hijo1,
                hijo2
            )


        punto1 = random.randint(
            1,
            longitud - 1
        )


        punto2 = random.randint(
            1,
            longitud - 1
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


        # ----------------------------------------------------
        # Invalidar fitness
        # ----------------------------------------------------

        if hijo1.fitness.valid:

            del hijo1.fitness.values


        if hijo2.fitness.valid:

            del hijo2.fitness.values


        return (
            hijo1,
            hijo2
        )


    # ========================================================
    # 11. REGISTRO DEL TOOLBOX
    # ========================================================

    toolbox = base.Toolbox()


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
        )
        /
        len(valores)

        if valores

        else 0
    )


    # ========================================================
    # 15. EJECUTAR ALGORITMO EVOLUTIVO
    # ========================================================

    print("\n")
    print("==============================================")
    print("       INICIANDO ALGORITMO EVOLUTIVO")
    print("==============================================")

    print(
        "Población:",
        TAMANO_POBLACION
    )

    print(
        "Generaciones:",
        GENERACIONES
    )

    print(
        "Probabilidad de cruza:",
        PROB_CRUZA
    )

    print(
        "Probabilidad de mutación:",
        PROB_MUTACION
    )

    print(
        "=============================================="
    )


    poblacion_final, registro_log = (
        algorithms.eaSimple(
            poblacion,
            toolbox,
            cxpb=PROB_CRUZA,
            mutpb=PROB_MUTACION,
            ngen=GENERACIONES,
            stats=estadisticas,
            verbose=False
        )
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

    fitness_final = (
        mejor_horario.fitness.values[0]
    )


    # ========================================================
    # 18. LIMPIAR HORARIO PARA JSON
    # ========================================================

    horario_limpio = []


    for gen in mejor_horario:

        horario_limpio.append({

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

        })


    # ========================================================
    # 19. DIAGNÓSTICO FINAL
    # ========================================================

    print("\n")
    print("==============================================")
    print("       RESULTADO DEL ALGORITMO")
    print("==============================================")

    print(
        "Clases generadas:",
        len(horario_limpio)
    )

    print(
        "Fitness final:",
        fitness_final
    )


    if horario_limpio:

        print("\nPrimeras 5 clases:")

        for clase in horario_limpio[:5]:

            print(
                "  ",
                clase
            )

    else:

        print(
            "⚠️ EL ALGORITMO NO GENERÓ CLASES."
        )


    print(
        "=============================================="
    )


    # ========================================================
    # 20. RESULTADO FINAL
    # ========================================================

    return {

        "mensaje":
            "Simulación completada con éxito",

        "fitness_final":
            fitness_final,

        "parametros": {

            "tamano_poblacion":
                TAMANO_POBLACION,

            "prob_cruza":
                PROB_CRUZA,

            "prob_mutacion":
                PROB_MUTACION,

            "generaciones":
                GENERACIONES
        },

        "horario":
            horario_limpio
    }