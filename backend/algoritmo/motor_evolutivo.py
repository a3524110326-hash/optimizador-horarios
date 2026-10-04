import random
from deap import base, creator, tools
import datos_prueba as dp

# ==========================================
# 1. CONFIGURACIÓN BASE DE DEAP
# ==========================================
# Definimos el objetivo: Minimizar los choques de horario (peso negativo)
if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# Definimos al Individuo: Una lista de genes que usará nuestro FitnessMin
if not hasattr(creator, "Individuo"):
    creator.create("Individuo", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# ==========================================
# 2. FÁBRICA DE GENES (EL GENERADOR ALEATORIO)
# ==========================================
def generar_horario_aleatorio():
    """
    Construye 1 individuo (un horario completo para toda la escuela).
    Itera sobre los grupos, revisa qué materias necesitan y asigna horas al azar.
    """
    horario_completo = []
    
    for grupo in dp.grupos:
        # Determinar si el grupo es de 1ro o 4to cuatrimestre para filtrar materias
        prefijo = grupo[0] # "1" o "4"
        
        for codigo_materia, detalles in dp.materias.items():
            # Regla de negocio: Si la materia es de 4to, no se la damos a los de 1ro, y viceversa.
            # (Asumimos por lógica de negocio que las de 1ro no aplican a 4to, ajusta si es necesario)
            if (prefijo == "1" and codigo_materia in ["AND", "CÁV", "DEA", "ESD", "APW", "IN4", "ÉTP"]) or \
               (prefijo == "4" and codigo_materia in ["FSC", "FUP", "FUR", "FUM", "DHV", "CHD", "IN1"]):
                continue 

            # Generar tantos "Genes" (clases) como horas exija la materia
            for _ in range(detalles["horas"]):
                # Seleccionar espacio dependiente de si requiere laboratorio o no
                if detalles["requiere_lab"]:
                    espacio_asignado = random.choice(dp.laboratorios)
                else:
                    espacio_asignado = random.choice(dp.aulas_teoricas)
                
                # Crear el Gen (Una clase individual)
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
# 3. REGISTRO EN EL TOOLBOX DE DEAP
# ==========================================
# Le enseñamos a DEAP cómo crear 1 individuo usando nuestra función
toolbox.register("individuo", tools.initIterate, creator.Individuo, generar_horario_aleatorio)

# Le enseñamos a DEAP cómo crear una población (una lista de N individuos)
toolbox.register("poblacion", tools.initRepeat, list, toolbox.individuo)

# ==========================================
# BLOQUE DE PRUEBA (SOLO PARA EL GENETISTA)
# ==========================================
if __name__ == "__main__":
    # Generamos una población inicial de 3 horarios distintos
    poblacion_inicial = toolbox.poblacion(n=3)
    
    print(f"Se generaron {len(poblacion_inicial)} horarios aleatorios.")
    print("---------------------------------------------------------")
    print("Muestra de los primeros 3 genes (clases) del HORARIO 1:")
    
    horario_1 = poblacion_inicial[0]
    for i in range(3):
        print(horario_1[i])