from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    return {"status": "ok"}


@router.get("/version")
def version():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
