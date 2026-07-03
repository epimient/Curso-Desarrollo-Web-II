import time
import logging
from fastapi import Request

logger = logging.getLogger("api.middleware")


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        inicio = time.perf_counter()
        metodo = request.method
        path = request.url.path

        logger.info(f"-> {metodo} {path}")

        response = await call_next(request)

        duracion = time.perf_counter() - inicio
        status = response.status_code
        logger.info(f"<- {metodo} {path} -> {status} ({duracion:.4f}s)")

        response.headers["X-Process-Time"] = f"{duracion:.4f}"
        return response
