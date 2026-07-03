from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, recurso: str, id: int):
        super().__init__(
            status_code=404,
            detail=f"{recurso} con id {id} no encontrado",
        )


class ForbiddenException(HTTPException):
    def __init__(self, mensaje: str = "No tienes permisos para esta accion"):
        super().__init__(status_code=403, detail=mensaje)


class BusinessRuleException(HTTPException):
    def __init__(self, mensaje: str):
        super().__init__(status_code=400, detail=mensaje)
