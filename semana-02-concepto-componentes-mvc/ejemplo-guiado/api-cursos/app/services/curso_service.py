from fastapi import HTTPException

from app.schemas.curso import CursoCreate

_cursos = []
_next_id = 1


def listar_cursos():
    return _cursos


def crear_curso(curso: CursoCreate):
    global _next_id

    existe = any(item["nombre"].lower() == curso.nombre.lower() for item in _cursos)

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un curso con ese nombre",
        )

    nuevo = {
        "id": _next_id,
        "nombre": curso.nombre,
        "creditos": curso.creditos,
        "activo": True,
    }

    _cursos.append(nuevo)
    _next_id += 1

    return nuevo
