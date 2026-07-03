# Ejemplo guiado - Refactor a persistencia con SQLAlchemy

## Objetivo

Partir del proyecto modular de la Clase 05 y refactorizarlo para que los datos persistan en SQLite en lugar de listas en memoria.

---

## Requisitos

- Proyecto modular de la Clase 05 funcionando.
- Python 3.10+.
- `pip install sqlalchemy`

---

## Paso 1. Agregar dependencia

En `requirements.txt`:

```
fastapi[standard]
sqlalchemy
```

```bash
pip install -r requirements.txt
```

---

## Paso 2. Crear `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Que hace cada parte:**

| Componente | Rol |
|---|---|
| `engine` | El puente entre Python y la BD. Se conecta al archivo `cursos.db` |
| `SessionLocal` | Fabrica de sesiones. Cada llamada crea una conexion nueva |
| `Base` | Clase padre de todos los modelos. SQLAlchemy la usa para saber que tablas crear |
| `get_db()` | Generador que crea, entrega y cierra una sesion. FastAPI la inyecta con `Depends()` |

---

## Paso 3. Agregar `DATABASE_URL` en config

En `app/core/config.py`, agrega el campo `database_url`:

```python
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"


settings = Settings()
```

> **Explicacion:** `sqlite:///./cursos.db` crea un archivo llamado `cursos.db` en la raiz del proyecto. Ese archivo ES la base de datos. Puedes abrirlo con cualquier visor SQLite (DB Browser, DBeaver, etc.).

---

## Paso 4. Crear modelo SQLAlchemy

Crea la carpeta `app/models/` con su `__init__.py`:

```python
"""Modelos SQLAlchemy de la aplicacion."""
```

Luego `app/models/course.py`:

```python
from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    credits = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
```

**Comparacion con el schema Pydantic:**

| Concepto | Pydantic (`CourseCreate`) | SQLAlchemy (`Course`) |
|---|---|---|
| Proposito | Validar datos de entrada/salida (JSON) | Mapear la tabla de la BD |
| Define | Contrato con el cliente | Estructura de la tabla |
| `id` | Lo recibe del servicio | Se genera automaticamente |
| `active` | No existe (lo pone el sistema) | Existe en la tabla |

---

## Paso 5. Actualizar schema Pydantic

En `app/schemas/course.py`, agrega `from_attributes=True`:

```python
from pydantic import BaseModel, Field, ConfigDict


class CourseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    credits: int = Field(ge=1, le=6)


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    credits: int
    active: bool
```

> **Por que es necesario:** Sin `from_attributes=True`, Pydantic solo puede crear `CourseResponse` desde un diccionario (`dict`) o JSON. Con esta opcion, tambien puede crearlo desde un objeto SQLAlchemy (`Course`).

---

## Paso 6. Refactorizar `course_service.py`

Reemplaza el contenido de `app/services/course_service.py`:

```python
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.course import Course
from app.schemas.course import CourseCreate


def list_courses(db: Session) -> list[Course]:
    return db.query(Course).all()


def get_course(course_id: int, db: Session) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def create_course(course_data: CourseCreate, db: Session) -> Course:
    exists = db.query(Course).filter(
        Course.name.ilike(course_data.name)
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Course already exists")

    course = Course(
        name=course_data.name,
        credits=course_data.credits,
        active=True,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
```

**Lo que cambio:**

| Funcion | Antes (lista) | Ahora (BD) |
|---|---|---|
| `list_courses()` | `return _courses` | `return db.query(Course).all()` |
| `get_course(id)` | `for course in _courses: if ...` | `db.query(Course).filter(...).first()` |
| `create_course(...)` | `global _next_id`, `_courses.append(...)` | `Course(...)`, `db.add()`, `db.commit()` |

---

## Paso 7. Actualizar routers con `Depends(get_db)`

En `app/routers/courses.py`:

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseCreate, CourseResponse
from app.services.course_service import create_course, get_course, list_courses

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[CourseResponse])
def read_courses(db: Session = Depends(get_db)):
    return list_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def read_course(course_id: int, db: Session = Depends(get_db)):
    return get_course(course_id, db)


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    return create_course(course_data, db)
```

**Que cambio:** Cada endpoint ahora recibe `db: Session = Depends(get_db)` y se lo pasa al servicio correspondiente.

---

## Paso 8. Actualizar `main.py` — crear tablas al iniciar

```python
from fastapi import FastAPI

from app.core.config import settings
from app.database import engine, Base
from app.routers import courses, health

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(health.router)
app.include_router(courses.router)
```

**Que hace `create_all()`:**
- La primera vez: crea la tabla `courses` en `cursos.db`
- Las siguientes veces: detecta que ya existe y no hace nada
- Si agregas un nuevo modelo, crea su tabla automaticamente

---

## Paso 9. Ejecutar y probar

```bash
uvicorn app.main:app --reload
```

**Pruebas:**

| Accion | Comando | Respuesta esperada |
|---|---|---|
| Listar cursos | `GET /courses` | `[]` (tabla vacia) |
| Crear curso | `POST /courses` con `{"name": "Fisica", "credits": 4}` | Status 201 |
| Listar de nuevo | `GET /courses` | 1 curso (Fisica) |
| **Reiniciar servidor** | Ctrl+C, luego `uvicorn ...` | — |
| Listar despues de reinicio | `GET /courses` | **1 curso** (Fisica) — ¡persistio! |

> **Antes (Clase 05):** al reiniciar, el curso creado desaparecia.
> **Ahora (Clase 07):** el curso sigue ahi porque se guardo en `cursos.db`.

---

## Paso 10. Verificar el archivo `.db`

Al ejecutar, veras que aparece un archivo nuevo:

```bash
ls -la cursos.db
```

Puedes explorarlo con:

```bash
sqlite3 cursos.db ".tables"
sqlite3 cursos.db "SELECT * FROM courses;"
```

---

## Paso 11. ¿Que pasaria si...?

**Escenario 1:** Olvido `from_attributes=True`
```python
# ❌ FALTA: CourseResponse no tiene from_attributes
# Al hacer GET /courses → error interno 500
```
**Solucion:** Agrega `model_config = ConfigDict(from_attributes=True)`.

**Escenario 2:** Olvido `db.commit()`
```python
db.add(course)
# ❌ FALTA: db.commit()
# El curso "se crea" (status 201) pero al reiniciar NO existe
```
**Solucion:** Siempre llama `db.commit()` despues de `db.add()`.

**Escenario 3:** Olvido `Depends(get_db)` en el router
```python
# ❌ FALTA: db: Session = Depends(get_db)
def read_courses(db):  # db no se inyecta
```
**Solucion:** El parametro debe ser `db: Session = Depends(get_db)`.

**Escenario 4:** Dos personas ejecutan el mismo proyecto
- Cada una tiene su propio `cursos.db`
- Si usaran PostgreSQL, compartirian la misma BD

---

## Resumen de archivos modificados/nuevos

| Archivo | Estado | Cambio |
|---|---|---|
| `requirements.txt` | Modificado | + `sqlalchemy` |
| `app/database.py` | **NUEVO** | engine, SessionLocal, Base, get_db |
| `app/core/config.py` | Modificado | + `database_url` |
| `app/models/__init__.py` | **NUEVO** | Docstring del paquete |
| `app/models/course.py` | **NUEVO** | Clase Course (SQLAlchemy) |
| `app/schemas/course.py` | Modificado | + `from_attributes=True` |
| `app/services/course_service.py` | Refactor | Lista → consultas BD |
| `app/routers/courses.py` | Modificado | + `Depends(get_db)` |
| `app/main.py` | Modificado | + `@app.on_event("startup")` |

---

## Cierre

La API ahora persiste datos. El archivo `cursos.db` contiene la informacion y sobrevive a reinicios. En la siguiente clase se profundizara en relaciones entre modelos (claves foraneas) y consultas mas complejas.
