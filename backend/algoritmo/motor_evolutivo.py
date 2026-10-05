import random
from deap import base, creator, tools, algorithms

# ==========================================
# 1. CONFIGURACIÓN BASE DE DEAP (Se queda global)
# ==========================================
if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

if not hasattr(creator, "Individuo"):
    creator.create("Individuo", list, fitness=creator.FitnessMin)

# ==========================================
# FUNCIÓN PRINCIPAL EXPORTABLE A FASTAPI
# ==========================================
def ejecutar_optimizador(datos_front):
    """
    Esta función recibe los datos dinámicos desde el frontend, 
    corre la evolución y devuelve el mejor horario encontrado.
    """
    # 1. Desempaquetamos los datos dinámicos
    grupos = datos_front.get("grupos", [])
    materias = datos_front.get("materias", {})
    laboratorios = datos_front.get("laboratorios", [])
    aulas_teoricas = datos_front.get("aulas_teoricas", [])
    dias = datos_front.get("dias", [])
    bloques_tiempo = datos_front.get("bloques_tiempo", [])
    
    # IMPORTANTE: Creamos la caja de herramientas DENTRO de la función 
    # para que cada petición web tenga un entorno limpio y no se mezclen.
    toolbox = base.Toolbox()

    # ==========================================
    # 2. FÁBRICA DE GENES (EL GENERADOR ALEATORIO)
    # ==========================================
    def generar_horario_aleatorio():
        horario_completo = []
        
        for grupo in grupos:
            prefijo = grupo[0] # "1" o "4"
            
            for codigo_materia, detalles in materias.items():
                if (prefijo == "1" and codigo_materia in ["AND", "CÁV", "DEA", "ESD", "APW", "IN4", "ÉTP"]) or \
                   (prefijo == "4" and codigo_materia in ["FSC", "FUP", "FUR", "FUM", "DHV", "CHD", "IN1"]):
                    continue 

                for _ in range(detalles["horas"]):
                    if detalles["requiere_lab"]:
                        espacio_asignado = random.choice(laboratorios)
                    else:
                        espacio_asignado = random.choice(aulas_teoricas)
                    
                    gen_clase = {
                        "grupo": grupo,
                        "materia": detalles["nombre"],
                        "profesor": detalles["profesor"],
                        "dia": random.choice(dias),
                        "bloque": random.choice(bloques_tiempo),
                        "espacio": espacio_asignado
                    }
                    horario_completo.append(gen_clase)
                    
        return horario_completo

    # ==========================================
    # 3. FUNCIÓN DE FITNESS (EL JUEZ DE COLISIONES)
    # ==========================================
    def evaluar_horario(individuo):
        penalizaciones = 0
        registro_aulas = set()
        registro_profes = set()
        registro_grupos = set()
        
        for gen in individuo:
            llave_aula = (gen["espacio"], gen["dia"], gen["bloque"])
            llave_profe = (gen["profesor"], gen["dia"], gen["bloque"])
            llave_grupo = (gen["grupo"], gen["dia"], gen["bloque"])
            
            if llave_aula in registro_aulas:
                penalizaciones += 10 
            else:
                registro_aulas.add(llave_aula)
                
            if llave_profe in registro_profes:
                penalizaciones += 10
            else:
                registro_profes.add(llave_profe)
                
            if llave_grupo in registro_grupos:
                penalizaciones += 10
            else:
                registro_grupos.add(llave_grupo)
                
        return (penalizaciones,)

    # ==========================================
    # 4. OPERADOR DE MUTACIÓN PERSONALIZADO
    # ==========================================
    def mutar_horario(individuo):
        indice_al_azar = random.randrange(len(individuo))
        individuo[indice_al_azar]["dia"] = random.choice(dias)
        individuo[indice_al_azar]["bloque"] = random.choice(bloques_tiempo)
        return (individuo,)

    # ==========================================
    # 5. REGISTRO EN EL TOOLBOX DE DEAP
    # ==========================================
    toolbox.register("individuo", tools.initIterate, creator.Individuo, generar_horario_aleatorio)
    toolbox.register("poblacion", tools.initRepeat, list, toolbox.individuo)
    toolbox.register("evaluate", evaluar_horario)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutar_horario)

    # ==========================================
    # 6. EL MOTOR EVOLUTIVO (EJECUCIÓN PRINCIPAL)
    # ==========================================
    # Extraemos parámetros del frontend (con valores por defecto si no los envían)
    TAMANO_POBLACION = datos_front.get("tamano_poblacion", 300)
    PROB_CRUZA = datos_front.get("prob_cruza", 0.85)
    PROB_MUTACION = datos_front.get("prob_mutacion", 0.15)
    GENERACIONES = datos_front.get("generaciones", 500)

    poblacion = toolbox.poblacion(n=TAMANO_POBLACION)

    estadisticas = tools.Statistics(lambda ind: ind.fitness.values)
    estadisticas.register("Min", min)

    # Apagamos el verbose=False para que FastAPI no se trabe imprimiendo 500 líneas en consola cada vez
    poblacion_final, registro_log = algorithms.eaSimple(
        poblacion, 
        toolbox, 
        cxpb=PROB_CRUZA, 
        mutpb=PROB_MUTACION, 
        ngen=GENERACIONES, 
        stats=estadisticas, 
        verbose=False 
    )

    # 7. Rescatar al ganador absoluto y empaquetarlo para enviarlo como JSON
    mejor_horario = tools.selBest(poblacion_final, 1)[0]
    
    return {
        "mensaje": "Simulación completada con éxito",
        "fitness_final": mejor_horario.fitness.values[0],
        # Convertimos el genotipo complejo de DEAP a una lista limpia de diccionarios
        "horario": [dict(gen) for gen in mejor_horario] 
    }