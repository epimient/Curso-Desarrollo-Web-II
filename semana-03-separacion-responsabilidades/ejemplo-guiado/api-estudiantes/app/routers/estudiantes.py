from fastapi import APIRouter, status

from app.schemas.estudiante import (
    EstudianteCreate,
    EstudianteResponse,
    EstudianteUpdate,
)
from app.services import estudiante_service

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/", response_model=list[EstudianteResponse])
def listar():
    """GET /estudiantes — Devuelve todos los estudiantes."""
    return estudiante_service.listar_estudiantes()


@router.get("/{estudiante_id}", response_model=EstudianteResponse)
def obtener(estudiante_id: int):
    """GET /estudiantes/{id} — Devuelve un estudiante por su ID."""
    return estudiante_service.obtener_estudiante(estudiante_id)


@router.post(
    "/",
    response_model=EstudianteResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(estudiante: EstudianteCreate):
    """POST /estudiantes — Crea un nuevo estudiante."""
    return estudiante_service.crear_estudiante(estudiante)


@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar(estudiante_id: int, estudiante: EstudianteUpdate):
    """PUT /estudiantes/{id} — Actualiza un estudiante existente."""
    return estudiante_service.actualizar_estudiante(estudiante_id, estudiante)


@router.delete(
    "/{estudiante_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(estudiante_id: int):
    """DELETE /estudiantes/{id} — Elimina un estudiante."""
    estudiante_service.eliminar_estudiante(estudiante_id)
