from fastapi import FastAPI

from app.core.config import settings
from app.database import engine, Base
from app.routers import courses, health

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(health.router)
app.include_router(courses.router)
