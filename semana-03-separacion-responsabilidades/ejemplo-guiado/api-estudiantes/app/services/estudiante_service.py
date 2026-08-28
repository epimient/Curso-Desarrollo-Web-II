from fastapi import HTTPException

from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate

# "Base de datos" en memoria
_estudiantes: list[dict] = []
_next_id: int = 1


def listar_estudiantes() -> list[dict]:
    """Devuelve todos los estudiantes."""
    return _estudiantes


def obtener_estudiante(estudiante_id: int) -> dict:
    """Busca un estudiante por ID. Lanza 404 si no existe."""
    for e in _estudiantes:
        if e["id"] == estudiante_id:
            return e
    raise HTTPException(
        status_code=404,
        detail=f"Estudiante con id {estudiante_id} no encontrado",
    )


def crear_estudiante(datos: EstudianteCreate) -> dict:
    """
    Crea un nuevo estudiante.

    Regla de negocio: no se permite email duplicado.
    """
    global _next_id

    # Regla de negocio: email unico
    email_existe = any(
        e["email"].lower() == datos.email.lower()
        for e in _estudiantes
    )
    if email_existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un estudiante con ese email",
        )

    nuevo = {
        "id": _next_id,
        "nombre": datos.nombre,
        "email": datos.email,
        "semestre": datos.semestre,
        "activo": True,
    }
    _estudiantes.append(nuevo)
    _next_id += 1
    return nuevo


def actualizar_estudiante(estudiante_id: int, datos: EstudianteUpdate) -> dict:
    """
    Actualiza un estudiante existente.

    Regla de negocio: el nuevo email no debe pertenecer a otro estudiante.
    """
    estudiante = obtener_estudiante(estudiante_id)  # reutiliza la busqueda

    # Verifica que el nuevo email no pertenezca a OTRO estudiante
    for e in _estudiantes:
        if e["id"] != estudiante_id and e["email"].lower() == datos.email.lower():
            raise HTTPException(
                status_code=400,
                detail="Ese email ya pertenece a otro estudiante",
            )

    estudiante["nombre"] = datos.nombre
    estudiante["email"] = datos.email
    estudiante["semestre"] = datos.semestre
    return estudiante


def eliminar_estudiante(estudiante_id: int) -> None:
    """Elimina un estudiante por ID. Lanza 404 si no existe."""
    global _estudiantes

    original = len(_estudiantes)
    _estudiantes = [e for e in _estudiantes if e["id"] != estudiante_id]

    if len(_estudiantes) == original:
        raise HTTPException(
            status_code=404,
            detail=f"Estudiante con id {estudiante_id} no encontrado",
        )
