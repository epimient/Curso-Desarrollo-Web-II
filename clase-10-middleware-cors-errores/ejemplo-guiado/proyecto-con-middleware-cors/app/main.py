from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from app.core.config import settings
from app.database import engine, Base
from app.errors.handlers import register_error_handlers
from app.middleware.logging import LoggingMiddleware
from app.routers import courses, health, auth

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("Iniciando API academica con middleware y CORS...")
    Base.metadata.create_all(bind=engine)
    yield
    # SHUTDOWN
    print("API detenida.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# Middleware de seguridad: solo hosts permitidos
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts,
)

# Middleware CORS: permite conexiones desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware personalizado: logging y tiempo de respuesta
app.add_middleware(LoggingMiddleware)

# Handlers de errores personalizados
register_error_handlers(app)

# Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(courses.router)
