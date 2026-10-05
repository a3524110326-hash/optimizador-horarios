# ==========================================
# CATÁLOGOS DE PRUEBA PARA EL MOTOR EVOLUTIVO
# ==========================================

# 1. ESPACIOS FÍSICOS DISPONIBLES
# 4 aulas con 40 asientos y 2 laboratorios con 36 equipos
aulas_teoricas = ["Aula_1", "Aula_2", "Aula_3", "Aula_4"]
laboratorios = ["Lab_1", "Lab_2"]

# 2. GRUPOS A PROGRAMAR
grupos = ["1A", "1B", "1C", "1D", "4A", "4B", "4C"]

# 3. ESTRUCTURA DEL TIEMPO (Lunes a Viernes)
# Son 8 bloques en total, omitiendo el receso de 09:30 a 10:00
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
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

# 4. MATERIAS, HORAS Y PROFESORES ASIGNADOS
materias = {
    # PRIMER CUATRIMESTRE
    "FSC": {"nombre": "Física", "horas": 6, "requiere_lab": False, "profesor": "Mtro. Juan Carlos De Los Santos Barbosa"},
    "FUP": {"nombre": "Fundamentos de Programación", "horas": 2, "requiere_lab": True, "profesor": "Dr. Julio César Alfaro Herrera"},
    "FUR": {"nombre": "Fundamentos de Redes", "horas": 2, "requiere_lab": True, "profesor": "Dra. Rosario Vargas Flores"},
    "FUM": {"nombre": "Fundamentos Matemáticos", "horas": 7, "requiere_lab": False, "profesor": "Mtro. Alfonso Noguerón Soto"},
    "DHV": {"nombre": "Desarrollo Humano y Valores", "horas": 4, "requiere_lab": False, "profesor": "Mtro. Erik Roque Mendoza"},
    "CHD": {"nombre": "Comunicación y Habilidades Digitales", "horas": 5, "requiere_lab": True, "profesor": "Mtro. Luis Roberto Bravo Torrescano"},
    "IN1": {"nombre": "Inglés I", "horas": 5, "requiere_lab": False, "profesor": "Mtra. Adriana Patricia Quizamán Olguín"},
    
    # CUARTO CUATRIMESTRE
    "AND": {"nombre": "Análisis y diseño de software", "horas": 3, "requiere_lab": False, "profesor": "Dra. Rosario Vargas Flores"},
    "CÁV": {"nombre": "Cálculo de varias variables", "horas": 5, "requiere_lab": False, "profesor": "Mtro. José Alberto Castelán De La Rosa"},
    "DEA": {"nombre": "Desarrollo de aplicaciones Móviles", "horas": 4, "requiere_lab": True, "profesor": "Dr. Héctor Bernardo Ortega Gines"},
    "ESD": {"nombre": "Estructura de datos", "horas": 3, "requiere_lab": True, "profesor": "Dra. Yedid Curloca Varela"},
    "APW": {"nombre": "Aplicaciones Web", "horas": 4, "requiere_lab": True, "profesor": "Dra. Yedid Curloca Varela"},
    "IN4": {"nombre": "Inglés IV", "horas": 5, "requiere_lab": False, "profesor": "Mtra. Adriana Patricia Quizamán Olguín"},
    "ÉTP": {"nombre": "Ética profesional", "horas": 5, "requiere_lab": False, "profesor": "Mtro. Erik Roque Mendoza"}
}