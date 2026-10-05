from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Optimizador de Horarios TSU")

# Permisos para que el Frontend se pueda comunicar con este Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de prueba para saber si el servidor está vivo
@app.get("/")
def estado_servidor():
    return {"estatus": "En línea", "mensaje": "API del Optimizador lista"}

# Endpoint principal que conectaremos con el motor evolutivo
@app.post("/api/generar-horario")
def arrancar_simulacion():
    # Aquí vamos a importar el motor_evolutivo después
    return {
        "mensaje": "Endpoint listo para recibir datos del front y pasarlos a la IA",
        "fitness_final": 0,
        "horario": []
    }