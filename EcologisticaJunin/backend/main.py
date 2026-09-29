from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="EcoLogística Huancayo API",
    version="1.0.0",
    description="API para la optimización sostenible de rutas de última milla."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "proyecto": "EcoLogística Huancayo",
        "mensaje": "API funcionando correctamente",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "servicio": "backend"
    }


@app.get("/api/rutas")
def rutas():
    return {
        "rutas": [],
        "mensaje": "Módulo de optimización pendiente de implementación."
    }
