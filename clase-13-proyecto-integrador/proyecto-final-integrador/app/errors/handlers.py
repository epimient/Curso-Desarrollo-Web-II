import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

logger = logging.getLogger("api.errors")


def register_error_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "codigo": exc.status_code,
                "mensaje": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errores = []
        for error in exc.errors():
            campo = " -> ".join(str(loc) for loc in error["loc"])
            errores.append(f"{campo}: {error['msg']}")

        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "codigo": 422,
                "mensaje": "Datos invalidos",
                "detalles": errores,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"Error interno: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "codigo": 500,
                "mensaje": "Error interno del servidor",
            },
        )
