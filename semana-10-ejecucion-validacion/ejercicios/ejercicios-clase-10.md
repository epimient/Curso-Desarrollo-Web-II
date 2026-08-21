## Ejercicio 0. Emparejar terminos

Une cada termino de la izquierda con su descripcion a la derecha:

| Termino | Descripcion |
|---|---|
| 1. `CORSMiddleware` | A. Funcion que conecta un middleware con el siguiente paso en la cadena |
| 2. `allow_origins` | B. Mecanismo de seguridad del navegador para origenes cruzados |
| 3. `call_next` | C. Lista de origenes que pueden acceder a la API |
| 4. `RequestValidationError` | D. Middleware de FastAPI que permite peticiones de origenes externos |
| 5. `lifespan` | E. Excepcion lanzada cuando falla la validacion de datos |
| 6. `@app.exception_handler()` | F. Patron para ejecutar codigo al iniciar y detener la app |
| 7. `CORS` | G. Excepcion base para errores HTTP |
| 8. `HTTPException` | H. Decorador que registra un manejador de errores personalizado |
| 9. `preflight` | I. Response header que muestra el tiempo de procesamiento |
| 10. `X-Process-Time` | J. Request OPTIONS que el navegador envia antes de una peticion "peligrosa" |

**Respuestas:** 1-D, 2-C, 3-A, 4-E, 5-F, 6-H, 7-B, 8-G, 9-J, 10-I

---

## Ejercicio 1. Configurar CORS para un frontend en produccion

Contexto: Tu API FastAPI se despliega en `https://api.misitio.com` y tu frontend React en `https://admin.misitio.com`.

**Tarea:** Escribe la configuracion de `CORSMiddleware` correcta.

**Requisitos:**
- Solo `https://admin.misitio.com` puede acceder
- Debe permitir credenciales (JWT)
- Debe permitir todos los metodos y headers
- Advertencia: NO usar `allow_origins=["*"]` con `allow_credentials=True`

**Solucion:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admin.misitio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Ejercicio 2. Personalizar errores 422

Contexto: En `app/errors/handlers.py` ya tienes un handler para `RequestValidationError`. Pero la jefa de carrera te pide que los mensajes de error sean en ESPANOL.

**Tarea:** Traduce los mensajes de error de validacion al espanol.

**Pista:** La libreria no traduce automaticamente. Debes crear un mapeo de `error["msg"]` a su version en espanol.

**Solucion:**
```python
TRADUCCIONES = {
    "field required": "campo obligatorio",
    "extra fields not permitted": "campos extras no permitidos",
    "value is not a valid integer": "no es un numero entero valido",
    "ensure this value has at most 80 characters": "maximo 80 caracteres",
    "ensure this value has at least 3 characters": "minimo 3 caracteres",
}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errores = []
    for error in exc.errors():
        campo = " -> ".join(str(loc) for loc in error["loc"])
        msg = TRADUCCIONES.get(error["msg"], error["msg"])
        errores.append(f"{campo}: {msg}")

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

---

## Ejercicio 3. Middleware que cuente requests por endpoint

Contexto: Tu equipo de operaciones quiere saber cuantas requests recibe cada endpoint.

**Tarea:** Escribe un middleware que mantenga un contador de requests por cada ruta y lo imprima en consola cada 10 requests.

**Requisitos:**
- Usar `@app.middleware("http")`
- Almacenar contadores en un diccionario global
- Cada 10 requests a un mismo endpoint, imprimir `"⚠️ /courses/ lleva 10 requests"`

**Pista:** Usa `request.url.path` como clave del diccionario.

**Solucion:**
```python
from collections import defaultdict

contadores = defaultdict(int)

@app.middleware("http")
async def contar_requests(request: Request, call_next):
    path = request.url.path
    contadores[path] += 1
    if contadores[path] % 10 == 0:
        print(f"⚠️ {path} lleva {contadores[path]} requests")
    response = await call_next(request)
    return response
```

---

## Ejercicio 4. Debug — Corrige los errores

Cada fragmento tiene uno o mas errores. Identificalos y corregelos.

### Fragmento A
```python
@app.middleware("http")
async def mi_middleware(request: Request, call_next):
    print("Antes")
    # falta llamar a call_next
    print("Despues")
```

**Error:** No llama a `await call_next(request)`. El cliente se queda colgado.

**Correccion:**
```python
@app.middleware("http")
async def mi_middleware(request: Request, call_next):
    print("Antes")
    response = await call_next(request)
    print("Despues")
    return response
```

### Fragmento B
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
)
```

**Error:** `allow_origins=["*"]` no puede usarse con `allow_credentials=True`. El navegador lo rechaza.

**Correccion:** Usar origenes explicitos o no usar `allow_credentials=True`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
)
```

### Fragmento C
```python
@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: Request):
    return {"error": True, "mensaje": str(exc)}
```

**Error 1:** El segundo parametro debe ser `exc: RequestValidationError`, no `exc: Request`.
**Error 2:** Los handlers deben devolver una `JSONResponse`, no un `dict`.

**Correccion:**
```python
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": True, "mensaje": str(exc)}
    )
```

### Fragmento D
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando...")

app = FastAPI(lifespan=lifespan)
```

**Error:** Falta `yield` en el lifespan. Sin `yield`, la app nunca termina de iniciarse o se queda congelada.

**Correccion:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando...")
    yield
    print("Apagando...")
```

### Fragmento E
```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost"],
)
```

**Contexto:** Abres `http://127.0.0.1:8000/docs` en el navegador y al ejecutar cualquier endpoint recibes `400 Bad Request: Invalid Host Header`.

**Error:** `allowed_hosts` incluye `"localhost"` pero no `"127.0.0.1"`. El host header es `127.0.0.1`.

**Correccion:**
```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"],
)
```

---

## Ejercicio 5. Desafio extra: Middleware de rate limit simple

**Contexto:** Quieres evitar que un mismo cliente abuse de tu API. Implementa un rate limit simple en memoria.

**Requisitos:**
- Limitar a 5 requests por minuto por direccion IP
- Usar `request.client.host` para obtener la IP
- Si supera el limite, devolver `429 Too Many Requests`
- Almacenar timestamps en un `defaultdict(list)`
- Limpiar timestamps viejos (> 60 segundos) en cada request

**Solucion:**
```python
from collections import defaultdict
import time
from fastapi import HTTPException, status

RATE_LIMIT = 5
WINDOW_SECONDS = 60
requests_por_ip = defaultdict(list)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    ahora = time.time()

    # Limpiar timestamps viejos
    requests_por_ip[ip] = [
        ts for ts in requests_por_ip[ip]
        if ahora - ts < WINDOW_SECONDS
    ]

    if len(requests_por_ip[ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": True,
                "codigo": 429,
                "mensaje": "Demasiadas solicitudes. Intenta en 60 segundos.",
            },
        )

    requests_por_ip[ip].append(ahora)
    response = await call_next(request)
    return response
```

**Nota:** Este rate limit funciona en memoria. Si reinicias el servidor, los contadores se reinician. En produccion se usa Redis para persistir los contadores entre reinicios.
