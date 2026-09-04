from fastapi import FastAPI

from app.routers.equipos import router as equipos_router

app = FastAPI(
    title="API de Equipos",
    description="Ejemplo básico de arquitectura por capas con FastAPI",
    version="1.0.0",
)

app.include_router(equipos_router)
