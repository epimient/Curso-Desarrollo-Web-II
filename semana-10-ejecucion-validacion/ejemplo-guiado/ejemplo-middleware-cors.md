# Ejemplo guiado: Middleware, CORS y manejo global de errores

## Contexto

Partimos del proyecto con autenticacion JWT de la clase 09 (`proyecto-con-auth`) y le agregamos:

1. **CORS** — para que un frontend (React, Vue, etc.) pueda consumir la API
2. **Middleware personalizado** — para logging y medicion de tiempos
3. **Manejo global de errores** — para respuestas limpias y consistentes
4. **Lifespan** — para inicializacion ordenada
5. **TrustedHostMiddleware** — para seguridad basica

---

## Paso 1: Estructura final del proyecto

```
proyecto-con-middleware-cors/          ← nueva carpeta
├── requirements.txt                   ← mismo que clase 09
└── app/
    ├── __init__.py
    ├── main.py                        ← MODIFICADO
    │
    ├── core/
    │   ├── __init__.py
    │   └── config.py                  ← MODIFICADO (+cors, +allowed_hosts)
    │
    ├── database.py                    ← igual
    │
    ├── middleware/                    ← NUEVA carpeta
    │   ├── __init__.py
    │   └── logging.py                 ← NUEVO
    │
    ├── errors/                        ← NUEVA carpeta
    │   ├── __init__.py
    │   ├── exceptions.py              ← NUEVO (excepciones personalizadas)
    │   └── handlers.py                ← NUEVO (exception_handlers)
    │
    ├── auth/   (igual)
    ├── models/ (igual)
    ├── schemas/(igual)
    ├── services/(igual)
    └── routers/(igual)
```

---

## Paso 2: `app/core/config.py` — Agregar configuracion de CORS

**Antes (clase 09):**
```python
class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"
    secret_key: str = "supersecretkey1234567890"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
```

**Despues:**
```python
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"
    secret_key: str = "supersecretkey1234567890"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]
    allowed_hosts: list[str] = [
        "localhost",
        "127.0.0.1",
    ]


settings = Settings()
```

**Desglose de lo nuevo:**

| Linea | Que hace |
|---|---|
| `cors_origins: list[str] = [...]` | Lista de origenes permitidos por CORS |
| `allowed_hosts: list[str] = [...]` | Lista de hosts validos (TrustedHostMiddleware) |
| Los valores son los tipicos en desarrollo | En produccion se leen de variables de entorno |

---

## Paso 3: `app/middleware/logging.py` — Middleware personalizado

```python
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

        logger.info(f"→ {metodo} {path}")

        response = await call_next(request)

        duracion = time.perf_counter() - inicio
        status = response.status_code
        logger.info(f"← {metodo} {path} → {status} ({duracion:.4f}s)")

        response.headers["X-Process-Time"] = f"{duracion:.4f}"
        return response
```

**Desglose linea por linea:**

| Linea | Que hace |
|---|---|
| `class LoggingMiddleware:` | Middleware basado en clase (se usa con `add_middleware`) |
| `def __init__(self, app):` | Recibe la aplicacion/siguiente middleware |
| `async def __call__(self, request, call_next):` | Se ejecuta en cada request |
| `logger.info(f"→ {metodo} {path}")` | Log de entrada: "→ GET /courses" |
| `response = await call_next(request)` | Pasa al siguiente eslabon de la cadena |
| `logger.info(f"← {metodo} {path} → {status}")` | Log de salida: "← GET /courses → 200 (0.0234s)" |
| `response.headers["X-Process-Time"] = ...` | Agrega header con tiempo de respuesta |

**¿Por que clase y no funcion?**

`add_middleware()` funciona con clases que siguen el patron ASGI. Las funciones con `@app.middleware("http")` tambien funcionan, pero `add_middleware()` es mas compatible con middlewares de terceros y permite inyectar configuracion en `__init__`.

---

## Paso 4: `app/errors/exceptions.py` — Excepciones personalizadas

```python
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
```

**Desglose:**

| Clase | Codigo HTTP | Uso tipico |
|---|---|---|
| `NotFoundException` | 404 | Curso, usuario o recurso no encontrado |
| `ForbiddenException` | 403 | Usuario sin permisos (no es admin, no es dueno) |
| `BusinessRuleException` | 400 | Regla de negocio violada (curso ya existe, cupo lleno) |

---

## Paso 5: `app/errors/handlers.py` — Manejadores de errores

```python
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
```

**Desglose de `validation_exception_handler`:**

```python
for error in exc.errors():
    campo = " -> ".join(str(loc) for loc in error["loc"])
    errores.append(f"{campo}: {error['msg']}")
```

| Parte | Que hace |
|---|---|
| `exc.errors()` | Devuelve lista de errores de validacion (cada uno con `loc`, `msg`, `type`) |
| `error["loc"]` | Es una lista como `["body", "name"]` o `["query", "course_id"]` |
| `" -> ".join(...)` | Convierte `["body", "name"]` en `"body -> name"` |
| `error["msg"]` | Mensaje del error: `"field required"`, `"ensure this value has at most 80 characters"` |
| Resultado final | `"body -> name: field required"` — mucho mas legible que el default |

**¿Por que una funcion `register_error_handlers(app)`?**

Porque los handlers necesitan acceso a la instancia `app`, y es mas ordenado tener toda la configuracion de errores en un solo archivo en lugar de en `main.py`.

---

## Paso 6: `app/main.py` — Integrar todo

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from app.core.config import settings
from app.database import engine, Base
from app.errors.handlers import register_error_handlers
from app.middleware.logging import LoggingMiddleware
from app.routers import courses, health, auth

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──
    print("Iniciando API academica con middleware y CORS...")
    Base.metadata.create_all(bind=engine)
    yield
    # ── SHUTDOWN ──
    print("API detenida.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# ── MIDDLEWARES ──
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# ── ERROR HANDLERS ──
register_error_handlers(app)

# ── ROUTERS ──
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(courses.router)
```

**Desglose de los cambios respecto a clase 09:**

| Antes (clase 09) | Ahora (clase 10) | ¿Por que cambio? |
|---|---|---|
| `@app.on_event("startup")` | `lifespan` con `asynccontextmanager` | `on_event` esta deprecado en FastAPI |
| Sin CORS | `app.add_middleware(CORSMiddleware, ...)` | Necesario para frontend |
| Sin logging | `app.add_middleware(LoggingMiddleware)` | Para monitorear requests |
| Sin TrustedHost | `app.add_middleware(TrustedHostMiddleware, ...)` | Seguridad basica |
| `HTTPException` default | `register_error_handlers(app)` | Respuestas limpias y consistentes |

---

## Paso 7: Usar excepciones personalizadas en servicios

**Antes (clase 09) en `course_service.py`:**
```python
from fastapi import HTTPException

def get_course(course_id: int, db: Session) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
```

**Despues:**
```python
from app.errors.exceptions import NotFoundException, BusinessRuleException

def get_course(course_id: int, db: Session) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise NotFoundException("Course", course_id)
    return course

def create_course(course_data: CourseCreate, db: Session) -> Course:
    exists = db.query(Course).filter(
        Course.name.ilike(course_data.name)
    ).first()
    if exists:
        raise BusinessRuleException("El curso ya existe")
    # ... resto igual
```

**Beneficio:** El mensaje de error incluye automaticamente el ID del recurso buscado, y el codigo HTTP es parte de la excepcion, no del lugar donde se lanza.

---

## Paso 8: Probar el resultado

### 8.1. Iniciar servidor

```bash
cd proyecto-con-middleware-cors
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Veras en la terminal:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
Iniciando API academica con middleware y CORS...
INFO:     Application startup complete.
```

### 8.2. Probar CORS

Desde Swagger UI:

1. Abre `http://localhost:8000/docs`
2. Ejecuta cualquier endpoint (ej: `GET /courses/`)
3. Despues de "Execute", revisa la seccion **Response headers**
4. Deberias ver:

```
access-control-allow-origin: http://localhost:5173
access-control-allow-methods: *
access-control-allow-headers: *
access-control-allow-credentials: true
```

### 8.3. Probar logging en terminal

1. Desde Swagger UI, ejecuta `GET /courses/`
2. Mira la terminal donde corre `uvicorn`
3. Deberias ver:

```
2026-07-03 10:00:00 | api.middleware | INFO | → GET /courses/
2026-07-03 10:00:00 | api.middleware | INFO | ← GET /courses/ → 200 (0.0123s)
```

### 8.4. Probar header `X-Process-Time`

1. Desde Swagger UI, ejecuta `GET /health/`
2. Revisa la seccion **Response headers** debajo del body
3. Deberias ver:

```
x-process-time: 0.0089
```

### 8.5. Probar error personalizado 422

1. Desde Swagger UI, busca `POST /courses/`
2. Haz clic en **Authorize** 🔒, pega tu token como `Bearer <token>`
3. En el Request body, envia un JSON vacio: `{}`
4. "Execute"
5. Respuesta esperada:
```json
{
  "error": true,
  "codigo": 422,
  "mensaje": "Datos invalidos",
  "detalles": [
    "body -> name: field required",
    "body -> credits: field required"
  ]
}
```

---

## ¿Que pasaria si...?

### Escenario 1: Olvido configurar CORS

```
Frontend en React (localhost:5173)
    → GET http://localhost:8000/courses/
    ← BLOQUEADO por el navegador
    ← Error: "No 'Access-Control-Allow-Origin' header"
```

**Solucion:** Agregar `app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], ...)`

### Escenario 2: No registro el handler de `RequestValidationError`

```
POST /courses/ con body invalido
→ Respuesta default de FastAPI:
{
  "detail": [
    { "loc": ["body", "name"], "msg": "field required", "type": "value_error.missing" }
  ]
}
```

El estudiante ve un JSON confuso. Con el handler personalizado, ve un mensaje claro.

### Escenario 3: `TrustedHostMiddleware` bloquea localhost

```
Desde Swagger UI, ejecuta GET /courses/
→ 400 "Invalid Host Header"
```

**Solucion:** Agregar `"localhost"` y `"127.0.0.1"` a `settings.allowed_hosts`.

### Escenario 4: El middleware no llama a `call_next`

```python
@app.middleware("http")
async def broken_middleware(request: Request, call_next):
    logger.info("Request recibida")
    # FALTA: response = await call_next(request)
    # La request nunca llega al endpoint
```

El cliente se queda esperando para siempre hasta que el timeout del servidor lo corta. **Siempre llamar a `await call_next(request)`.**

---

## Resumen archivos nuevos/modificados

| Archivo | Estado | Lineas | Cambio principal |
|---|---|---|---|
| `app/main.py` | MODIFICADO | ~45 | +lifespan, +CORS, +TrustedHost, +LoggingMiddleware, +register_error_handlers |
| `app/core/config.py` | MODIFICADO | ~25 | +cors_origins, +allowed_hosts |
| `app/middleware/__init__.py` | NUEVO | 1 | Init del paquete |
| `app/middleware/logging.py` | NUEVO | 25 | LoggingMiddleware con medicion de tiempo |
| `app/errors/__init__.py` | NUEVO | 1 | Init del paquete |
| `app/errors/exceptions.py` | NUEVO | 20 | NotFoundException, ForbiddenException, BusinessRuleException |
| `app/errors/handlers.py` | NUEVO | 45 | register_error_handlers con HTTPException, 422, 500 |

**Total archivos en proyecto:** ~30 (hereda 24 de clase 09 + 6 nuevos/modificados)
