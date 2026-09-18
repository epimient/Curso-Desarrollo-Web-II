from fastapi import FastAPI
from app.routers import pqrs

# Metadatos del sistema para enriquecer la documentación Swagger UI / OpenAPI
tags_metadata = [
    {
        "name": "General",
        "description": "Endpoints generales de verificación del servicio.",
    },
    {
        "name": "PQRS - Peticiones, Quejas, Reclamos y Sugerencias",
        "description": "Gestión del ciclo de vida de peticiones de los ciudadanos (radicación, consulta y actualización de estado).",
    },
]

app = FastAPI(
    title="API de PQRS - Sistema de Atención al Ciudadano",
    description="""
## Ejemplo Guiado - Semana 06: Selección de Framework (FastAPI)

Esta API demuestra por qué **FastAPI** es la opción seleccionada para el curso:
* **Validación de Datos en Runtime:** Pydantic valida automáticamente los esquemas de entrada.
* **Documentación Interactiva Automática:** Swagger UI (`/docs`) y ReDoc (`/redoc`) sin configuraciones adicionales.
* **Altos Estándares HTTP:** Uso correcto de verbos (POST, GET, PATCH), parámetros tipados y códigos de estado (201, 404, 422).
* **Organización Modular:** Estructura limpia basada en `routers` y `schemas`.
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir el enrutador modular de PQRS con el prefijo v1
app.include_router(pqrs.router, prefix="/api/v1")


@app.get(
    "/",
    tags=["General"],
    summary="Mensaje de bienvenida e información de navegación"
)
def root():
    return {
        "mensaje": "Bienvenido a la API de PQRS - Semana 06 (FastAPI)",
        "documentacion_swagger": "http://localhost:8000/docs",
        "documentacion_redoc": "http://localhost:8000/redoc",
        "endpoints_principales": {
            "radicar_pqrs": "POST /api/v1/pqrs/",
            "listar_pqrs": "GET /api/v1/pqrs/",
            "estadisticas": "GET /api/v1/pqrs/estadisticas/resumen",
            "consultar_radicado": "GET /api/v1/pqrs/{codigo_radicado}"
        }
    }


@app.get(
    "/health",
    tags=["General"],
    summary="Verificación de estado de la aplicación"
)
def health_check():
    return {
        "estado": "OK",
        "framework": "FastAPI",
        "semana": 6,
        "mensaje": "Servicio de PQRS funcionando correctamente"
    }
