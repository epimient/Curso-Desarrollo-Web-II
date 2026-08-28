from fastapi import FastAPI

from app.routers import estudiantes

app = FastAPI(
    title="API Estudiantes",
    description="Ejemplo de refactorizacion: de monolito a capas separadas — Semana 03",
    version="0.1.0",
)

app.include_router(estudiantes.router)
