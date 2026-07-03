# Clase 10 - Middleware, CORS y manejo global de errores

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Carrera:** Analista Programador / Ingenieria en Informatica  
**Semestre:** 2do  
**Unidad:** IV  
**Duracion:** 2 horas presenciales + 2 horas asincronicas  
**Fecha:** Semana 14

---

## 2. Estructura conceptual

```
┌─────────────────────────────────────────────────────────┐
│                 REQUEST (cliente)                        │
│                         │                                │
│  ┌──────────────────────▼──────────────────────┐       │
│  │         Capa 0: LIFESPAN (startup)          │       │
│  │         (cargar BD, conectar servicios)      │       │
│  └──────────────────────┬──────────────────────┘       │
│                         │                                │
│  ┌──────────────────────▼──────────────────────┐       │
│  │         Capa 1: MIDDLEWARE 1 (logging)       │       │
│  │  "Registra: alguien entro por la puerta"     │       │
│  └──────────────────────┬──────────────────────┘       │
│                         │                                │
│  ┌──────────────────────▼──────────────────────┐       │
│  │         Capa 2: MIDDLEWARE 2 (CORS)          │       │
│  │  "Revisa: este invitado tiene pase?"         │       │
│  └──────────────────────┬──────────────────────┘       │
│                         │                                │
│  ┌──────────────────────▼──────────────────────┐       │
│  │         Capa 3: EXCEPTION HANDLER            │       │
│  │  "Si algo falla, responde con orden"         │       │
│  └──────────────────────┬──────────────────────┘       │
│                         │                                │
│  ┌──────────────────────▼──────────────────────┐       │
│  │         Capa 4: ROUTER + SERVICE + DB        │       │
│  │         (tu logica de negocio)               │       │
│  └──────────────────────┬──────────────────────┘       │
│                         │                                │
│  ┌──────────────────────▼──────────────────────┐       │
│  │         Capa 5: MIDDLEWARE 1 (post)         │       │
│  │  "Agrega header X-Process-Time"             │       │
│  └──────────────────────┬──────────────────────┘       │
│                         │                                │
│                 RESPONSE (cliente)                       │
└─────────────────────────────────────────────────────────┘
```

## 3. Objetivos

Al finalizar esta clase, el estudiante sera capaz de:

- Explicar que es un middleware y como se inserta en el ciclo request-response
- Configurar CORS correctamente para permitir conexiones desde un frontend
- Sobrescribir los manejadores de errores por defecto de FastAPI (`HTTPException`, `RequestValidationError`)
- Crear sus propias excepciones personalizadas con codigos HTTP especificos
- Implementar un middleware personalizado para logging y medicion de tiempos
- Usar el patron `lifespan` para tareas de inicializacion y limpieza

---

## 4. Middleware

### 4.1. ¿Que es un middleware?

**En español simple:** Un middleware es un filtro por el que pasa TODA peticion antes de llegar a tu endpoint, y por el que vuelve a pasar la respuesta antes de enviarla al cliente. Sirve para hacer cosas "a todas las rutas por igual": logs, mediciones, CORS, autenticacion global, etc.

**Analogia — Filtros de agua en un edificio:**

Imagina un edificio de departamentos. El agua que llega a cada casa pasa por varios filtros antes de salir de la canilla:

1. **Filtro grueso** — retiene piedras, ramas (equivale a verificar que la request tenga formato valido)
2. **Filtro de carbon** — elimina cloro, mal olor (equivale a CORS, verificar origen)
3. **Filtro de sedimentos** — atrapa particulas finas (equivale a logging, registro de la visita)
4. **La canilla** — el agua ya filtrada sale lista para usar (equivale a tu endpoint devolviendo datos)

Cada filtro recibe el agua, hace algo, y la pasa al siguiente. Asi funciona el middleware en FastAPI.

```
Request  →  [Middleware 1]  →  [Middleware 2]  →  [Endpoint]  →  [Middleware 2]  →  [Middleware 1]  →  Response
             (logging)         (CORS)                              (CORS post)        (logging post)
```

### 4.2. Sintaxis basica de un middleware

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

**Desglose linea por linea:**

| Linea | Que hace |
|---|---|
| `@app.middleware("http")` | Registra la funcion como middleware para peticiones HTTP |
| `async def add_process_time_header(...)` | La funcion recibe `request` y `call_next` (el siguiente paso en la cadena) |
| `start_time = time.perf_counter()` | Toma el tiempo ANTES de procesar la request |
| `response = await call_next(request)` | Pasa la request al siguiente middleware (o al endpoint) y espera la respuesta |
| `process_time = ...` | Calcula cuanto tardo la request completa |
| `response.headers[...] = ...` | Agrega un header CUSTOM a la respuesta |
| `return response` | Devuelve la respuesta al paso anterior |

### 4.3. `call_next` — el eslabon que conecta

**En español simple:** `call_next` es el "pase de la pelota". Sin el, la request nunca llega al endpoint y el cliente se queda esperando para siempre.

```
Middleware A recibe request
    → hace algo (logging)
    → await call_next(request)   ← pasa la pelota
        → Middleware B
            → await call_next(request)
                → ENDPOINT
            ← recibe response
        ← devuelve response
    ← hace algo post-procesamiento (tiempo)
    → return response
```

**Asi NO ❌ vs Asi SI ✅:**

```python
# ❌ MAL: nunca llama a call_next
@app.middleware("http")
async def bad_middleware(request: Request, call_next):
    print("Request recibida")
    # Falta await call_next(request) — la request queda colgada

# ✅ BIEN: siempre pasa la pelota
@app.middleware("http")
async def good_middleware(request: Request, call_next):
    print("Request recibida")
    response = await call_next(request)
    return response
```

### 4.4. `app.add_middleware()` — para middlewares basados en clases

Algunos middlewares vienen como clases (como `CORSMiddleware`, `TrustedHostMiddleware`). Se registran con `app.add_middleware()`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Diferencia entre `@app.middleware("http")` y `app.add_middleware()`:**

| Aspecto | `@app.middleware("http")` | `app.add_middleware()` |
|---|---|---|
| Tipo | Funcion | Clase ASGI |
| Uso tipico | Logging, metricas, headers | CORS, TrustedHost, GZip |
| Control fino | Total (accedes a request y response) | Limitado a lo que expone la clase |
| Async por defecto | Si | Depende de la implementacion |

---

## 5. CORS (Cross-Origin Resource Sharing)

### 5.1. ¿Que es CORS y por que existe?

**En español simple:** CORS es un mecanismo de seguridad del navegador. Cuando tu frontend (ej: React en `localhost:5173`) intenta hablar con tu backend (FastAPI en `localhost:8000`), el navegador dice: "Son origenes diferentes, esto esta prohibido a menos que el backend lo autorice explicitamente".

**Analogia — El bar con lista de invitados:**

Imagina un bar privado (tu backend). Tiene un seguridad en la puerta (el navegador). Cuando alguien llega, el seguridad revisa:

1. **Same-Origin:** Si la persona viene de adentro del bar (mismo origen), pasa sin problema.
2. **Cross-Origin:** Si la persona viene de la calle (otro origen), el seguridad pregunta al gerente: "¿Dejamos entrar a alguien de esta direccion?".

El gerente (tu backend) responde con headers CORS:
- `Access-Control-Allow-Origin`: "Si, deja pasar a `http://localhost:5173`"
- `Access-Control-Allow-Methods`: "Pueden entrar con GET, POST, PUT, DELETE"
- `Access-Control-Allow-Headers`: "Pueden traer estos objetos (headers)"

Si el gerente no responde o dice que no, el seguridad bloquea la entrada y el frontend recibe un error en la consola.

```
Frontend (React)                    Backend (FastAPI)
    │                                     │
    │  GET /courses                       │
    │────────────────────────────────────>│
    │                                     │
    │  ← BLOQUEADO ❌                     │
    │  (No Access-Control-Allow-Origin)    │
    │                                     │
    │  ──── Despues de configurar CORS ────│
    │                                     │
    │  GET /courses                       │
    │────────────────────────────────────>│
    │                                     │
    │  ← Access-Control-Allow-Origin: *   │
    │  ← (datos) ✅                       │
```

### 5.2. Configuracion de CORSMiddleware

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",      # React dev
    "http://localhost:3000",      # Next.js dev
    "http://127.0.0.1:5173",
    "https://miapp.com",          # Produccion
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Parametros de CORSMiddleware:**

| Parametro | Que controla | Ejemplo |
|---|---|---|
| `allow_origins` | Que origenes pueden acceder | `["http://localhost:5173"]` o `["*"]` |
| `allow_credentials` | Si permite cookies/auth headers | `True` si usas JWT con `Authorization` |
| `allow_methods` | Que metodos HTTP permite | `["*"]` o `["GET", "POST"]` |
| `allow_headers` | Que headers custom permite | `["*"]` o `["Authorization", "Content-Type"]` |
| `expose_headers` | Headers que el frontend puede leer | `["X-Process-Time"]` |

### 5.3. CORS en produccion vs desarrollo

| Entorno | `allow_origins` | `allow_credentials` |
|---|---|---|
| Desarrollo | `["*"]` o lista de origenes locales | `True` |
| Produccion | Lista exacta de dominios permitidos | `True` si hay auth |

**En español simple:** En desarrollo puedes abrir la puerta a todo el mundo (`["*"]`), pero en produccion solo debes dejar pasar a los origenes que conoces y confias.

### 5.4. Preflight request (OPTIONS)

**En español simple:** Antes de enviar una request "peligrosa" (con headers custom, con DELETE, etc.), el navegador hace una preguntita timida con metodo OPTIONS para asegurarse de que el backend acepta ese tipo de request.

```
Frontend                           Backend
   │                                   │
   │  OPTIONS /courses                 │  ← PREFLIGHT (solo navegador)
   │  Access-Control-Request-Method: DELETE
   │──────────────────────────────────>│
   │                                   │
   │  ← 200 OK                         │
   │  Access-Control-Allow-Origin: *   │
   │  Access-Control-Allow-Methods: DELETE
   │                                   │
   │  DELETE /courses/1                │  ← REQUEST REAL
   │──────────────────────────────────>│
   │                                   │
   │  ← 200 {"detail": "Deleted"}      │
```

FastAPI + CORSMiddleware maneja el preflight automaticamente. No necesitas hacer nada extra.

---

## 6. Manejo global de errores

### 6.1. ¿Por que centralizar errores?

**En español simple:** Sin handlers personalizados, FastAPI devuelve errores 422 con un JSON enorme y confuso. Centralizar te permite dar respuestas limpias, consistentes y utiles.

**Analogia — La central de alarmas del edificio:**

Sin handler personalizado, cuando algo falla:

```
¡ALARMA! ¡ALARMA! ¡ERROR!
{ "detail": [ { "loc": ["body", "name"], "msg": "field required", "type": "value_error.missing" } ] }
```

El usuario ve un texto de robot que no entiende.

Con handler personalizado:

```
❌ Dato invalido: El campo 'name' es obligatorio
```

El usuario entiende exactamente que paso y que hacer.

### 6.2. Personalizar `HTTPException`

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(
    request: Request, exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "codigo": exc.status_code,
            "mensaje": exc.detail,
        },
    )
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `@app.exception_handler(HTTPException)` | Registra el handler para todas las `HTTPException` |
| `exc: HTTPException` | Recibe la excepcion que se lanzo |
| `JSONResponse(...)` | Devuelve un JSON con formato propio (no el de FastAPI) |
| `"mensaje": exc.detail` | Toma el mensaje original (`detail`) y lo pone en un campo `mensaje` |

**Resultado:**
```json
// Antes (default)
{ "detail": "Course not found" }

// Despues (personalizado)
{ "error": true, "codigo": 404, "mensaje": "Course not found" }
```

### 6.3. Personalizar `RequestValidationError` (errores 422)

```python
from fastapi.exceptions import RequestValidationError

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
```

**En español simple:** Sin este handler, un error 422 devuelve un JSON lleno de `loc`, `msg`, `type` que asusta a los estudiantes. Con el handler, devolvemos algo como:

```json
{
  "error": true,
  "codigo": 422,
  "mensaje": "Datos invalidos",
  "detalles": [
    "body -> name: field required",
    "body -> credits: input should be a valid integer"
  ]
}
```

### 6.4. Crear excepciones personalizadas

```python
# errors/exceptions.py
from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, recurso: str, id: int):
        super().__init__(
            status_code=404,
            detail=f"{recurso} con id {id} no encontrado"
        )


class ForbiddenException(HTTPException):
    def __init__(self, mensaje: str = "No tienes permisos"):
        super().__init__(status_code=403, detail=mensaje)


class BusinessRuleException(HTTPException):
    def __init__(self, mensaje: str):
        super().__init__(status_code=400, detail=mensaje)
```

**Uso en servicios:**
```python
# Antes: raise HTTPException(status_code=404, detail="Course not found")
# Despues:
raise NotFoundException("Course", course_id)
```

**En español simple:** Crear tus propias excepciones es como tener botones personalizados en lugar de escribir la direccion cada vez. `NotFoundException` ya sabe que es 404 y que mensaje poner.

### 6.5. Handler generico para errores no capturados (500)

```python
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "codigo": 500,
            "mensaje": "Error interno del servidor",
        },
    )
```

**Advertencia:** En produccion, este handler NO debe mostrar el mensaje real del error (podria exponer informacion sensible). Solo debe devolver un mensaje generico y loguear el error real.

```python
import logging
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no esperado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "codigo": 500,
            "mensaje": "Error interno del servidor",
            # NO incluyas exc.__str__() en produccion
        },
    )
```

### 6.6. Orden de evaluacion de handlers

FastAPI busca el handler mas especifico primero:

1. `NotFoundException` (tu subclase) → handler para `NotFoundException` si existe
2. `HTTPException` → handler para `HTTPException`
3. `RequestValidationError` → handler para `RequestValidationError`
4. `Exception` → handler generico (captura todo lo demas)

```
try:
    # tu codigo
except NotFoundException as e:    ← 1. Handler especifico
    ...
except HTTPException as e:         ← 2. Handler general HTTP
    ...
except RequestValidationError as e: ← 3. Handler validacion
    ...
except Exception as e:              ← 4. Handler generico
    ...
```

---

## 7. Lifespan (startup / shutdown)

### 7.1. ¿Que es lifespan?

**En español simple:** El lifespan define que pasa cuando la aplicacion ARRANCA y cuando se APAGA. Sirve para conectar la base de datos, cargar configuracion, o liberar recursos.

**Analogia — Abrir y cerrar el edificio:**

- **Startup:** Llegas al edificio por la manana, abres las puertas, enciendes las luces, conectas la calefaccion.
- **Shutdown:** Al final del dia, apagas todo, cierras las puertas, revisas que no haya nada encendido.

### 7.2. Sintaxis con `asynccontextmanager`

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──
    print("🚀 Iniciando aplicacion...")
    # Conectar BD, cargar config, etc.
    yield
    # ── SHUTDOWN ──
    print("🛑 Apagando aplicacion...")
    # Cerrar conexiones, liberar recursos

app = FastAPI(lifespan=lifespan)
```

### 7.3. Lifespan con logging y BD

```python
from contextlib import asynccontextmanager
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("Iniciando API academica...")
    Base.metadata.create_all(bind=engine)
    yield
    # SHUTDOWN
    print("API detenida. Conexiones cerradas.")
```

**Asi NO ❌ vs Asi SI ✅:**

```python
# ❌ ANTES (eventos deprecados)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
def shutdown():
    pass

# ✅ AHORA (lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
```
```

### 7.4. ¿Cuando usar lifespan?

| Situacion | Lifespan | `@app.on_event` |
|---|---|---|
| Crear tablas de BD | ✅ (recomendado) | ⚠️ (deprecado) |
| Conectar a Redis / cola | ✅ | ⚠️ |
| Cargar modelo ML en memoria | ✅ | ⚠️ |
| Cerrar pool de conexiones | ✅ | ⚠️ |
| Inicializar cliente HTTP | ✅ | ⚠️ |

---

## 8. Middleware built-in en FastAPI

FastAPI incluye algunos middlewares listos para usar:

### 8.1. `TrustedHostMiddleware`

Permite solo requests que vengan de hosts especificos (protege contra host header injection):

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.miapp.com"],
)
```

### 8.2. `GZipMiddleware`

Comprime las respuestas con GZip si el navegador lo soporta:

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 8.3. `HTTPSRedirectMiddleware`

Redirige automaticamente HTTP a HTTPS:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

### 8.4. Orden de los middlewares

**Importante:** El orden en que agregas los middlewares importa. El primer middleware agregado es el que recibe la request primero.

```python
# Orden recomendado:
app.add_middleware(TrustedHostMiddleware, ...)  # 1. Seguridad
app.add_middleware(HTTPSRedirectMiddleware, ...) # 2. Redireccion
app.add_middleware(CORSMiddleware, ...)          # 3. CORS
app.add_middleware(GZipMiddleware, ...)          # 4. Compresion
# @app.middleware("http") personalizados        # 5. Custom (ultimos)
```

---

## 9. Ejemplo integrador

A continuacion, el contenido minimo de `main.py` con todo lo visto:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.database import engine, Base
from app.errors.handlers import (
    register_error_handlers,
)
from app.middleware.logging import LoggingMiddleware
from app.routers import courses, health, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    Base.metadata.create_all(bind=engine)
    yield
    # SHUTDOWN
    # (podrias cerrar conexiones aqui)


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

# ── MIDDLEWARE PERSONALIZADO ──
app.add_middleware(LoggingMiddleware)

# ── ERROR HANDLERS ──
register_error_handlers(app)

# ── ROUTERS ──
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(courses.router)
```

> **Nota:** El detalle completo de cada archivo esta en el ejemplo guiado.

---

## 10. ¿Que NO vimos?

| Tema | Por que no lo vimos |
|---|---|
| Middleware de rate limiting | Excede el alcance; requiere Redis o almacenamiento externo |
| Middleware de autenticacion global | Ya lo vimos con `Depends()` y `get_current_user` |
| Sub-applicaciones (mount) | Caso avanzado de microservicios |
| Middleware ASGI puro | Requiere conocimientos de ASGI, no necesario para el curso |
| CORS con credentials y wildcard | No se puede usar `allow_origins=["*"]` con `allow_credentials=True` |
| Logging estructurado (JSON) | Se puede agregar con `python-json-logger`, no es esencial |

---

## 11. Troubleshooting

| Error | Causa probable | Solucion |
|---|---|---|
| `CORS: No 'Access-Control-Allow-Origin' header` | Falta CORSMiddleware o `allow_origins` incorrecto | Agregar `app.add_middleware(CORSMiddleware, ...)` |
| `CORS: Method DELETE not allowed` | `allow_methods` no incluye DELETE | Usar `allow_methods=["*"]` |
| `422 Unprocessable Entity` con JSON feo | No hay handler personalizado para `RequestValidationError` | Agregar `@app.exception_handler(RequestValidationError)` |
| Mi middleware personalizado no se ejecuta | El middleware no llama a `call_next` | Verificar que haces `await call_next(request)` |
| `HTTPException` se ve distinto a lo que defini | Otro handler esta interceptando antes | Verificar orden de middlewares y handlers |
| La app no arranca: `TypeError: lifespan() missing` | El parametro `lifespan` no se paso a `FastAPI()` | Verificar `app = FastAPI(lifespan=lifespan)` |
| `TrustedHostMiddleware` bloquea localhost | `allowed_hosts` no incluye `"localhost"` | Agregar `"localhost"` a la lista |
| Error 500 no muestra mi JSON personalizado | El handler de `Exception` no esta registrado | Agregar `@app.exception_handler(Exception)` |

### Checklist de troubleshooting

- [ ] ¿El middleware llama a `await call_next(request)`?
- [ ] `allow_origins` ¿tiene el origen exacto del frontend (con puerto)?
- [ ] Si uso `allow_credentials=True`, ¿`allow_origins` NO es `["*"]`?
- [ ] ¿Los exception handlers estan registrados ANTES de incluir los routers?
- [ ] ¿El handler de `RequestValidationError` importa de `fastapi.exceptions`?
- [ ] ¿Lifespan usa `asynccontextmanager` y `yield` en el lugar correcto?

---

## 12. Trabajo independiente

1. **Leer:** Documentacion oficial de FastAPI sobre middleware y CORS
2. **Hacer:** Los ejercicios de la clase
3. **Investigar:** ¿Que es `python-json-logger`? ¿Como se integra con FastAPI?
4. **Preparar:** Revisar el codigo de `proyecto-con-auth` de la clase 9 para la prueba parcial

---

## 13. Bibliografia

- FastAPI - Middleware: https://fastapi.tiangolo.com/tutorial/middleware/
- FastAPI - CORS: https://fastapi.tiangolo.com/tutorial/cors/
- FastAPI - Handling Errors: https://fastapi.tiangolo.com/tutorial/handling-errors/
- FastAPI - Lifespan: https://fastapi.tiangolo.com/advanced/events/
