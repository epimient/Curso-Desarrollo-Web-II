from fastapi import HTTPException

from app.schemas.equipo import EquipoCreate

_equipos: list[dict] = []
_next_id = 1


def listar_equipos() -> list[dict]:
    return _equipos


def crear_equipo(equipo: EquipoCreate) -> dict:
    global _next_id

    existe = any(
        e["nombre"].lower() == equipo.nombre.lower() for e in _equipos
    )
    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un equipo con ese nombre",
        )

    nuevo = {
        "id": _next_id,
        "nombre": equipo.nombre,
        "categoria": equipo.categoria,
        "disponible": True,
    }
    _equipos.append(nuevo)
    _next_id += 1

    return nuevo
