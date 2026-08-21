from fastapi import FastAPI

from app.core.config import settings
from app.routers import courses, health

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health.router)
app.include_router(courses.router)
