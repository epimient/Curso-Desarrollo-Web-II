# Ejemplo guiado - Refactor a proyecto modular FastAPI

## Objetivo

Transformar un proyecto basico de FastAPI (como el de la Clase 04) en una estructura modular con:

- `core/config.py`
- `routers/health.py`
- `routers/courses.py`
- `schemas/course.py`
- `services/course_service.py`

---

## Paso 1. Crear estructura de carpetas

```bash
mkdir -p app/core app/routers app/schemas app/services
touch app/__init__.py
touch app/core/__init__.py
touch app/routers/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
```

**Explicacion:** `mkdir -p` crea toda la jerarquia de carpetas de una vez. `touch` crea los `__init__.py` — archivos vacios que le indican a Python "esta carpeta es un paquete desde el cual se puede importar".

**Resultado esperado:**
```text
app/
  __init__.py
  main.py          ← heredado de Clase 04
  core/
    __init__.py
    config.py
  routers/
    __init__.py
    health.py
    courses.py
  schemas/
    __init__.py
    course.py
  services/
    __init__.py
    course_service.py
```

---

## Paso 2. Crear configuracion centralizada

Archivo: `app/core/config.py`

```python
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"


settings = Settings()
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `from pydantic import BaseModel` | Importa la clase base para crear modelos de datos con validacion |
| `class Settings(BaseModel):` | Define una clase que hereda de `BaseModel` — sera nuestro objeto de configuracion |
| `app_name: str = "API academica"` | Campo de tipo `str` con valor por defecto |
| `app_version: str = "0.1.0"` | Campo para la version del proyecto |
| `environment: str = "development"` | Entorno: `development`, `staging`, `production` |
| `settings = Settings()` | **Crea la instancia** — un objeto `settings` listo para usar en otros archivos |

---

## Paso 3. Crear schemas de curso

Archivo: `app/schemas/course.py`

```python
from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    credits: int = Field(ge=1, le=6)


class CourseResponse(BaseModel):
    id: int
    name: str
    credits: int
    active: bool
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `from pydantic import BaseModel, Field` | Importa `BaseModel` y `Field` para validaciones extra |
| `class CourseCreate(BaseModel):` | Define el schema de **entrada** — datos que el cliente debe enviar |
| `name: str = Field(min_length=3, max_length=80)` | `name` debe ser texto de entre 3 y 80 caracteres |
| `credits: int = Field(ge=1, le=6)` | `credits` debe ser entero entre 1 y 6 (`ge=greater or equal`, `le=less or equal`) |
| `class CourseResponse(BaseModel):` | Define el schema de **salida** — datos que la API devuelve |
| `id: int` | El ID generado por el sistema (el cliente NO lo envia, el sistema lo asigna) |
| `active: bool` | Estado del curso (el cliente NO lo envia, el sistema lo pone en `True` por defecto) |

> **Dato clave:** `CourseCreate` tiene solo 2 campos (name, credits). `CourseResponse` tiene 4 (id, name, credits, active). Esto es intencional: el cliente no deberia poder definir el `id` ni el estado `active`.

---

## Paso 4. Crear servicio de cursos

Archivo: `app/services/course_service.py`

```python
from fastapi import HTTPException

from app.schemas.course import CourseCreate

_courses = [
    {"id": 1, "name": "Desarrollo Web II", "credits": 3, "active": True},
]
_next_id = 2


def list_courses() -> list[dict]:
    return _courses


def get_course(course_id: int) -> dict:
    for course in _courses:
        if course["id"] == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")


def create_course(course_data: CourseCreate) -> dict:
    global _next_id

    exists = any(
        course["name"].lower() == course_data.name.lower()
        for course in _courses
    )

    if exists:
        raise HTTPException(status_code=400, detail="Course already exists")

    course = {
        "id": _next_id,
        "name": course_data.name,
        "credits": course_data.credits,
        "active": True,
    }
    _courses.append(course)
    _next_id += 1
    return course
```

**Desglose:**

| Linea(s) | Que hace |
|---|---|
| `_courses = [...]` | Lista **privada** (convencion: el `_` indica "no tocar desde fuera") que almacena los cursos en memoria |
| `_next_id = 2` | Contador para asignar IDs automaticamente. Empieza en 2 porque ya hay un curso con id=1 |
| `def list_courses() -> list[dict]:` | Retorna TODA la lista de cursos sin filtrar |
| `def get_course(course_id: int) -> dict:` | Busca un curso por su `id`. Si no lo encuentra, lanza error 404 |
| `for course in _courses:` | Itera sobre la lista buscando coincidencia |
| `if course["id"] == course_id:` | Compara el id de cada curso con el solicitado |
| `raise HTTPException(status_code=404, ...)` | Si no encuentra, lanza una excepcion que FastAPI convierte en respuesta HTTP 404 |
| `def create_course(course_data: CourseCreate) -> dict:` | Recibe datos **ya validados** por Pydantic |
| `global _next_id` | **Importante:** le decimos a Python que `_next_id` no es una variable local, sino la global definida fuera de la funcion |
| `exists = any(...)` | Revisa si algun curso tiene el mismo nombre (case insensitive) |
| `course_data.name.lower()` | Convierte el nombre ingresado a minusculas para comparar sin importar mayusculas |
| `raise HTTPException(status_code=400, ...)` | Si el curso ya existe, error 400 (Bad Request) |
| `_courses.append(course)` | Agrega el nuevo curso a la lista |
| `_next_id += 1` | Incrementa el contador para el proximo curso |

---

## Paso 5. Crear router de salud

Archivo: `app/routers/health.py`

```python
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    return {"status": "ok"}


@router.get("/version")
def version():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `from fastapi import APIRouter` | Importa `APIRouter` — un "mini-FastAPI" para agrupar rutas |
| `router = APIRouter(prefix="/health", tags=["Health"])` | Crea un router donde todas las rutas empezaran con `/health` y apareceran bajo la etiqueta "Health" en `/docs` |
| `@router.get("/")` | Escucha en `GET /health` (porque el `prefix` es `/health`) |
| `@router.get("/version")` | Escucha en `GET /health/version` |
| `settings.app_name` | Toma el nombre desde la configuracion centralizada |

---

## Paso 6. Crear router de cursos

Archivo: `app/routers/courses.py`

```python
from fastapi import APIRouter, status

from app.schemas.course import CourseCreate, CourseResponse
from app.services.course_service import create_course, get_course, list_courses

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[CourseResponse])
def read_courses():
    return list_courses()


@router.get("/{course_id}", response_model=CourseResponse)
def read_course(course_id: int):
    return get_course(course_id)


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_course(course_data: CourseCreate):
    return create_course(course_data)
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `router = APIRouter(prefix="/courses", tags=["Courses"])` | Crea router con prefijo `/courses` y etiqueta "Courses" |
| `@router.get("/", response_model=list[CourseResponse])` | `GET /courses` y declara que la respuesta sera una **lista** de `CourseResponse` |
| `def read_courses(): return list_courses()` | Router delgado: solo llama al servicio y devuelve |
| `@router.get("/{course_id}", response_model=CourseResponse)` | `GET /courses/1` con parametro de ruta entero |
| `def read_course(course_id: int):` | FastAPI convierte automaticamente `course_id` a `int` |
| `@router.post("/", response_model=CourseResponse, status_code=201)` | `POST /courses`, retorna status 201 (Created) |
| `course_data: CourseCreate` | FastAPI valida automaticamente el body contra el schema `CourseCreate` |
| `return create_course(course_data)` | Router delgado: pasa los datos validados al servicio |

---

## Paso 7. Actualizar `main.py`

Archivo: `app/main.py`

```python
from fastapi import FastAPI

from app.core.config import settings
from app.routers import courses, health

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health.router)
app.include_router(courses.router)
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `from app.routers import courses, health` | Importa los modulos enteros (NO los routers directamente) |
| `app.include_router(health.router)` | "Conecta" el router de salud a la aplicacion. Sin esto, `/health` no existiria |
| `app.include_router(courses.router)` | "Conecta" el router de cursos a la aplicacion |

> **Error tipico:** Olvidar `app.include_router(...)`. Si un endpoint no aparece en `/docs`, probablemente es por esto.

---

## Paso 8. Ejecutar

```bash
uvicorn app.main:app --reload
```

Probar:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
http://127.0.0.1:8000/health/version
http://127.0.0.1:8000/courses
```

---

## Paso 9. ¿Que pasaria si...?

**Escenario 1: Olvidaste `__init__.py` en alguna carpeta**
```text
ModuleNotFoundError: No module named 'app.routers'
```
La carpeta `routers/` existe pero no tiene `__init__.py`. Python no la reconoce como paquete.
**Solucion:** `touch app/routers/__init__.py`

**Escenario 2: Olvidaste `app.include_router(courses.router)`**
```text
/docs no muestra los endpoints de cursos
```
FastAPI no tiene forma de saber que existe el router de cursos.
**Solucion:** Agrega `app.include_router(courses.router)` en `main.py`

**Escenario 3: Intentas hacer `POST /courses` sin enviar body**
```text
422 Unprocessable Entity
```
FastAPI espera un JSON con `name` y `credits`.
**Solucion:** Envia el body correcto:
```json
{"name": "Nuevo Curso", "credits": 4}
```

**Escenario 4: Intentas hacer `POST /courses` con nombre menor a 3 caracteres**
```text
422 con mensaje: "String should have at least 3 characters"
```
Pydantic valida el `min_length=3` del schema.
**Solucion:** Usa un nombre de al menos 3 caracteres.

**Escenario 5: Intentas crear un curso con el mismo nombre de uno existente**
```text
400 Bad Request: "Course already exists"
```
El servicio `create_course` revisa duplicados antes de crear.
**Solucion:** Usa un nombre diferente.

---

## Paso 10. Analisis final

Responde estas preguntas para verificar tu comprension:

1. **¿Que archivo registra los routers?**
   - `app/main.py`, con `app.include_router(...)`.

2. **¿Que archivo contiene la configuracion general?**
   - `app/core/config.py`, con la clase `Settings`.

3. **¿Donde esta la validacion de datos?**
   - En `app/schemas/course.py`, con `Field(min_length=3, ...)`.

4. **¿Donde esta la logica de negocio?**
   - En `app/services/course_service.py`, con funciones como `create_course()`.

5. **¿Que ventaja tiene esta estructura frente al proyecto de la Clase 04?**
   - Separacion de responsabilidades, facil de extender, facil de probar, facil de trabajar en equipo.

---

## Resumen: que contiene cada archivo

| Archivo | Que contiene |
|---|---|
| `app/main.py` | Instancia de FastAPI + registro de routers |
| `app/core/config.py` | Clase `Settings` con nombre, version, entorno |
| `app/routers/health.py` | Endpoints `GET /health` y `GET /health/version` |
| `app/routers/courses.py` | Endpoints CRUD de cursos |
| `app/schemas/course.py` | `CourseCreate` (entrada) y `CourseResponse` (salida) |
| `app/services/course_service.py` | Logica: listar, buscar, crear cursos |

---

## Cierre

Este refactor deja la API preparada para crecer. En la siguiente clase se profundizara en validacion, modelos de datos y documentacion automatica con Pydantic.
