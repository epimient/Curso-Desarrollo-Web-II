import time
import logging
from fastapi import Request

logger = logging.getLogger("api.middleware")


async def log_requests(request: Request, call_next):
    inicio = time.perf_counter()
    metodo = request.method
    path = request.url.path

    logger.info("-> %s %s", metodo, path)

    response = await call_next(request)

    duracion = time.perf_counter() - inicio
    status = response.status_code
    logger.info("<- %s %s -> %s (%.4fs)", metodo, path, status, duracion)

    response.headers["X-Process-Time"] = f"{duracion:.4f}"
    return response
