import random
from deap import base, creator, tools, algorithms
import datos_prueba as dp

# ==========================================
# 1. CONFIGURACIÓN BASE DE DEAP
# ==========================================
if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

if not hasattr(creator, "Individuo"):
    creator.create("Individuo", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# ==========================================
# 2. FÁBRICA DE GENES (EL GENERADOR ALEATORIO)
# ==========================================
def generar_horario_aleatorio():
    horario_completo = []
    
    for grupo in dp.grupos:
        prefijo = grupo[0] # "1" o "4"
        
        for codigo_materia, detalles in dp.materias.items():
            if (prefijo == "1" and codigo_materia in ["AND", "CÁV", "DEA", "ESD", "APW", "IN4", "ÉTP"]) or \
               (prefijo == "4" and codigo_materia in ["FSC", "FUP", "FUR", "FUM", "DHV", "CHD", "IN1"]):
                continue 

            for _ in range(detalles["horas"]):
                if detalles["requiere_lab"]:
                    espacio_asignado = random.choice(dp.laboratorios)
                else:
                    espacio_asignado = random.choice(dp.aulas_teoricas)
                
                gen_clase = {
                    "grupo": grupo,
                    "materia": detalles["nombre"],
                    "profesor": detalles["profesor"],
                    "dia": random.choice(dp.dias),
                    "bloque": random.choice(dp.bloques_tiempo),
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
        
        # 1. Evaluar choque de espacios
        if llave_aula in registro_aulas:
            penalizaciones += 10 
        else:
            registro_aulas.add(llave_aula)
            
        # 2. Evaluar choque de profesores
        if llave_profe in registro_profes:
            penalizaciones += 10
        else:
            registro_profes.add(llave_profe)
            
        # 3. Evaluar empalme de clases para los alumnos
        if llave_grupo in registro_grupos:
            penalizaciones += 10
        else:
            registro_grupos.add(llave_grupo)
            
    return (penalizaciones,)

# ==========================================
# 4. OPERADOR DE MUTACIÓN PERSONALIZADO
# ==========================================
def mutar_horario(individuo):
    # 1. Elegimos el índice de un gen (clase) al azar de todo el horario
    indice_al_azar = random.randrange(len(individuo))
    
    # 2. Le asignamos un nuevo día y un nuevo bloque de tiempo al azar
    individuo[indice_al_azar]["dia"] = random.choice(dp.dias)
    individuo[indice_al_azar]["bloque"] = random.choice(dp.bloques_tiempo)
    
    # DEAP siempre exige devolver una tupla
    return (individuo,)

# ==========================================
# 5. REGISTRO EN EL TOOLBOX DE DEAP
# ==========================================
toolbox.register("individuo", tools.initIterate, creator.Individuo, generar_horario_aleatorio)
toolbox.register("poblacion", tools.initRepeat, list, toolbox.individuo)
toolbox.register("evaluate", evaluar_horario)

# Agregamos las 3 herramientas de evolución faltantes
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutar_horario)

# ==========================================
# 6. EL MOTOR EVOLUTIVO (EJECUCIÓN PRINCIPAL)
# ==========================================
if __name__ == "__main__":
    # 1. Parámetros controlados desde el frontend
    TAMANO_POBLACION = 300
    PROB_CRUZA = 0.85
    PROB_MUTACION = 0.15
    GENERACIONES = 500

    # 2. Generar el caos inicial
    poblacion = toolbox.poblacion(n=TAMANO_POBLACION)

    # 3. Objeto para guardar estadísticas (nos mostrará cómo baja el fitness)
    estadisticas = tools.Statistics(lambda ind: ind.fitness.values)
    estadisticas.register("Min", min) # Solo nos importa ver el choque mínimo
    estadisticas.register("Max", max)

    print("=========================================================")
    print("INICIANDO TORNEO EVOLUTIVO...")
    print("=========================================================")

    # 4. Iniciar el algoritmo de cruza, mutación y selección automática
    poblacion_final, registro_log = algorithms.eaSimple(
        poblacion, 
        toolbox, 
        cxpb=PROB_CRUZA, 
        mutpb=PROB_MUTACION, 
        ngen=GENERACIONES, 
        stats=estadisticas, 
        verbose=True # Para ver el progreso en consola
    )

    # 5. Rescatar al ganador absoluto
    mejor_horario = tools.selBest(poblacion_final, 1)[0]
    
    print("\n=========================================================")
    print("EVOLUCIÓN TERMINADA")
    print(f"Mejor puntaje de Fitness logrado: {mejor_horario.fitness.values[0]}")
    print("=========================================================")

    # Auditoría de colisiones
    print("\n🔍 ANALIZANDO LOS CHOQUES RESTANTES:")
    registro_aulas = set()
    registro_profes = set()
    registro_grupos = set()
    
    for gen in mejor_horario:
        llave_aula = (gen["espacio"], gen["dia"], gen["bloque"])
        llave_profe = (gen["profesor"], gen["dia"], gen["bloque"])
        llave_grupo = (gen["grupo"], gen["dia"], gen["bloque"])
        
        if llave_aula in registro_aulas:
            print(f"⚠️ Choque de AULA: {gen['espacio']} doblemente ocupada el {gen['dia']} a las {gen['bloque']}")
        else:
            registro_aulas.add(llave_aula)
            
        if llave_profe in registro_profes:
            print(f"⚠️ Choque de PROFESOR: {gen['profesor']} doblemente asignado el {gen['dia']} a las {gen['bloque']}")
        else:
            registro_profes.add(llave_profe)
            
        if llave_grupo in registro_grupos:
            print(f"⚠️ Choque de GRUPO: {gen['grupo']} empalmado el {gen['dia']} a las {gen['bloque']}")
        else:
            registro_grupos.add(llave_grupo)