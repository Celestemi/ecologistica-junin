from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="EcoLogística Huancayo",
    version="1.0.0",
    description="Sistema de gestión y optimización sostenible de rutas."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# MODELOS
# =========================

class Vehiculo(BaseModel):
    placa: str
    modelo: str
    combustible: str
    capacidad_kg: float
    rendimiento: float
    factor_co2: float
    estado: str = "Activo"


class Pedido(BaseModel):
    cliente: str
    distrito: str
    peso_kg: float
    hora_inicio: str
    hora_fin: str
    estado: str = "Pendiente"


# =========================
# DATOS TEMPORALES
# =========================

vehiculos: List[Vehiculo] = [
    Vehiculo(
        placa="ABC-123",
        modelo="Furgón",
        combustible="GNV",
        capacidad_kg=1000,
        rendimiento=12.5,
        factor_co2=2.75
    )
]

pedidos: List[Pedido] = [
    Pedido(
        cliente="Cliente Huancayo",
        distrito="Huancayo",
        peso_kg=50,
        hora_inicio="09:00",
        hora_fin="12:00"
    )
]


# =========================
# INICIO
# =========================

@app.get("/")
def inicio():
    return {
        "sistema": "EcoLogística Huancayo",
        "estado": "operativo",
        "version": "1.0.0"
    }


# =========================
# VEHÍCULOS - CRUD
# =========================

@app.get("/api/vehiculos")
def listar_vehiculos():
    return vehiculos


@app.post("/api/vehiculos")
def registrar_vehiculo(vehiculo: Vehiculo):
    if any(v.placa == vehiculo.placa for v in vehiculos):
        raise HTTPException(
            status_code=400,
            detail="La placa ya está registrada"
        )

    vehiculos.append(vehiculo)
    return {
        "mensaje": "Vehículo registrado correctamente",
        "vehiculo": vehiculo
    }


@app.put("/api/vehiculos/{placa}")
def actualizar_vehiculo(placa: str, vehiculo: Vehiculo):
    for i, actual in enumerate(vehiculos):
        if actual.placa == placa:
            vehiculos[i] = vehiculo
            return {
                "mensaje": "Vehículo actualizado correctamente",
                "vehiculo": vehiculo
            }

    raise HTTPException(
        status_code=404,
        detail="Vehículo no encontrado"
    )


@app.delete("/api/vehiculos/{placa}")
def eliminar_vehiculo(placa: str):
    for i, vehiculo in enumerate(vehiculos):
        if vehiculo.placa == placa:
            vehiculos.pop(i)
            return {
                "mensaje": "Vehículo eliminado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Vehículo no encontrado"
    )


# =========================
# PEDIDOS - CRUD
# =========================

@app.get("/api/pedidos")
def listar_pedidos():
    return pedidos


@app.post("/api/pedidos")
def registrar_pedido(pedido: Pedido):
    pedidos.append(pedido)

    return {
        "mensaje": "Pedido registrado correctamente",
        "pedido": pedido
    }


@app.delete("/api/pedidos/{indice}")
def eliminar_pedido(indice: int):
    if indice < 0 or indice >= len(pedidos):
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    pedidos.pop(indice)

    return {
        "mensaje": "Pedido eliminado correctamente"
    }


# =========================
# RUTAS
# =========================

@app.get("/api/rutas")
def obtener_rutas():
    return {
        "estado": "pendiente",
        "algoritmo": "VRPTW + Green VRP",
        "mensaje": "El motor de optimización será implementado en la siguiente iteración."
    }
