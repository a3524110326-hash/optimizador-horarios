from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. IMPORTAMOS TU ARCHIVO DE INTELIGENCIA ARTIFICIAL
from algoritmo import motor_evolutivo

app = FastAPI(title="API Optimizador de Horarios TSU")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def estado_servidor():
    return {"estatus": "En línea", "mensaje": "API del Optimizador lista"}

# 2. CONECTAMOS EL ENDPOINT CON EL MOTOR
# Al pedir "datos_front: dict", FastAPI automáticamente lee el JSON que manda la web
@app.post("/api/generar-horario")
def arrancar_simulacion(datos_front: dict):
    
    # Le inyectamos los datos dinámicos a tu algoritmo y esperamos a que termine
    resultado_ia = motor_evolutivo.ejecutar_optimizador(datos_front)
    
    # Devolvemos el diccionario con el fitness final y el horario ganador a las pantallas
    return resultado_ia