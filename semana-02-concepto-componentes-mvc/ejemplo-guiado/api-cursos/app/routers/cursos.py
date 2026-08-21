from fastapi import APIRouter, status

from app.schemas.curso import CursoCreate, CursoResponse
from app.services.curso_service import crear_curso, listar_cursos

router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("/", response_model=list[CursoResponse])
def obtener_cursos():
    return listar_cursos()


@router.post(
    "/",
    response_model=CursoResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_curso(curso: CursoCreate):
    return crear_curso(curso)
