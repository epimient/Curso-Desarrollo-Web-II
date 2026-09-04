from fastapi import APIRouter, status

from app.schemas.equipo import EquipoCreate, EquipoResponse
from app.services.equipo_service import crear_equipo, listar_equipos

router = APIRouter(prefix="/equipos", tags=["Equipos"])


@router.get("/", response_model=list[EquipoResponse])
def get_equipos():
    return listar_equipos()


@router.post("/", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
def post_equipo(equipo: EquipoCreate):
    return crear_equipo(equipo)
