# Optimizador de Horarios - TSU Desarrollo de Software

Sistema diseñado para la Universidad Tecnológica de Tehuacán que automatiza la generación de horarios escolares utilizando algoritmos evolutivos. El sistema busca la distribución óptima de clases respetando las restricciones de profesores, aulas, materias y bloques de tiempo.

**Equipo:**
* Juan Manuel Romero Reyes
* Eduardo Miguel Cruz Barragan
* Karen Rojas Diego
* Juan Daniel Perez Palacios
* Bryan Hernandez Muñoz

---

## Arquitectura del Proyecto
* **Frontend:** React + Vite (Desplegado en Vercel)
* **Backend:** FastAPI + Python (Desplegado en Render)
* **Base de Datos:** Supabase (PostgreSQL)
* **Motor Evolutivo:** DEAP

---

## Créditos y Licencias

### Herramientas y Librerías Principales
Este proyecto fue construido integrando tecnologías de código abierto y servicios de infraestructura en la nube:
* **Frontend:** [React](https://reactjs.org/) y [Vite](https://vitejs.dev/) (Licencia MIT).
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) y Python (Licencia MIT / PSF).
* **Motor Evolutivo:** [DEAP](https://github.com/DEAP/deap) - Distributed Evolutionary Algorithms in Python (Licencia LGPL).
* **Base de Datos:** [Supabase](https://supabase.com/) (PostgreSQL).
* **Infraestructura (Hosting):** Vercel (Frontend) y Render (Backend).

### Fuentes de Datos
* **Catálogos de la Institución:** La información correspondiente a profesores, materias, aulas y bloques de horario es gestionada dinámicamente por los usuarios a través de la plataforma para modelar la jornada operativa real de la universidad. No se importaron datasets externos ni conjuntos de datos preentrenados.

### Declaración de Uso de Inteligencia Artificial (Transparencia)
Durante el ciclo de desarrollo de este proyecto, se emplearon herramientas de Inteligencia Artificial generativa bajo un enfoque de programación asistida. A continuación, se delimita la autoría técnica:

**Secciones estructuradas con asistencia de IA:**
* Generación del código base (*boilerplate*) y configuración inicial del entorno de Vite y FastAPI.
* Esqueletos de conexión para el cliente de Supabase y validación de variables de entorno.
* Propuestas de lógica matemática para las funciones de cruza y mutación dentro del algoritmo genético.
* Refactorización estructural del algoritmo genético (DEAP) para transicionar de un script estático a una función dinámica empaquetada, permitiendo la inyección de datos vía JSON.
* Construcción del *endpoint* POST en FastAPI para el "Gran Ensamble", enlazando el motor evolutivo con las peticiones web del cliente.
* Asistencia en *debugging* de errores de consola (resolución de rutas de importación en Python, comandos de entorno virtual y dependencias), así como guías de configuración de directorios raíz para el despliegue en Vercel y Render.

**Secciones diseñadas, modificadas e implementadas por el equipo:**
* Diseño arquitectónico del sistema Full Stack y separación estructurada de los entornos (Frontend/Backend).
* Diseño del modelo relacional en la base de datos y establecimiento de las reglas de negocio estrictas (ej. módulos de clase de 50 minutos).
* Ajuste fino (*fine-tuning*) de los parámetros del motor evolutivo (población, generaciones, pesos de aptitud) para garantizar que los resultados cumplan con las restricciones físicas de la escuela.
* Construcción de la interfaz gráfica (UI/UX), enlace de los *endpoints* con el cliente web y orquestación del flujo completo para la generación asíncrona de los horarios.