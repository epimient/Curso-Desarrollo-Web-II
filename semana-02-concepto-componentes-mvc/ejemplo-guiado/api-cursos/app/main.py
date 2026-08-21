from fastapi import FastAPI

from app.routers import cursos

app = FastAPI(
    title="API Academica",
    description="Ejemplo por capas para Desarrollo Web II",
    version="0.1.0",
)

app.include_router(cursos.router)
