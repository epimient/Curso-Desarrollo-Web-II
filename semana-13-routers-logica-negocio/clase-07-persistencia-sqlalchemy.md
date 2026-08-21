# Clase 07 - Persistencia de datos con SQLAlchemy

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 7  
**Unidad:** Unidad 2 - Uso de un Framework Especifico  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA3: Desarrollar habilidades para la creacion y manejo de rutas y controladores dentro del framework mediante la implementacion de logica de negocio en controladores o equivalentes pedagogicos.
- RA4: Aplicar principios de diseno de APIs RESTful en la construccion de servicios web mediante la implementacion de endpoints que cumplan con los estandares de la arquitectura REST.
- RA5: Implementar operaciones CRUD utilizando un sistema de persistencia de datos en el desarrollo de aplicaciones web.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

Hasta ahora los datos de la API han vivido en listas en memoria (`_courses = [...]`). Cada vez que el servidor se reinicia, los datos desaparecen. Es como escribir en una pizarra: funcional para la clase, inutil para un proyecto real.

En esta clase se introduce **SQLAlchemy**, el ORM (Object-Relational Mapper) mas usado de Python, para reemplazar la memoria volatil por una base de datos SQLite persistente. Los estudiantes aprenderan a:

- configurar la conexion a una base de datos desde FastAPI;
- definir modelos SQLAlchemy que representan tablas;
- usar sesiones de base de datos inyectadas con `Depends()`;
- reemplazar las operaciones en memoria por consultas reales a la BD;
- ejecutar migraciones con Alembic.

## 3. Pregunta orientadora

**Como hacemos que los datos de nuestra API sobrevivan al reinicio del servidor?**

---

> **En español simple:** Hasta ahora los datos viven en listas de Python. Cuando apagas el servidor, las listas se borran. Con SQLAlchemy, los datos viven en un archivo `.db` en tu computadora. Apagas, prendes, los datos siguen ahi. Como pasar de escribir en una pizarra a escribir en un cuaderno.

---

## 4. Conceptos previos requeridos

- Estructura modular del proyecto (Clase 05).
- Schemas Pydantic con `BaseModel` y `Field()` (Clase 06).
- Funcionamiento de inyeccion de dependencias con `Depends()` (Clase 05 - ya se usa implicitamente).
- Conocimientos basicos de SQL (SELECT, INSERT, WHERE, JOIN).

## 5. El problema: datos volatiles

Proyecto actual en `app/services/course_service.py`:

```python
_courses = [
    {"id": 1, "name": "Desarrollo Web II", "credits": 3, "active": True},
]
_next_id = 2

def list_courses() -> list[dict]:
    return _courses

def create_course(course_data: CourseCreate) -> dict:
    global _next_id
    # ...valida, crea, agrega a _courses...
```

**Problemas:**
- Al reiniciar, `_courses` vuelve a tener solo el curso inicial.
- Dos personas no pueden compartir los datos.
- No hay forma de consultar datos historicos.

## 6. Que es SQLAlchemy

SQLAlchemy es un **ORM** (Object-Relational Mapper). Esto significa que te permite trabajar con la base de datos usando objetos de Python en lugar de escribir SQL directamente.

| Concepto SQL | Concepto SQLAlchemy |
|---|---|
| Tabla | Clase Python |
| Fila | Instancia de la clase |
| Columna | Atributo de la clase |
| `SELECT * FROM courses` | `db.query(Course).all()` |
| `INSERT INTO courses VALUES ...` | `db.add(course)` + `db.commit()` |
| `WHERE id = 1` | `.filter(Course.id == 1)` |

> **Analogia:** SQLAlchemy es un traductor. Tu le hablas en Python ("dame todos los cursos"), el traduce a SQL ("SELECT * FROM courses"), ejecuta la consulta, y te devuelve objetos Python. Tu nunca escribes SQL directamente.

## 7. Instalacion

Agrega al `requirements.txt`:

```
fastapi[standard]
sqlalchemy
```

```bash
pip install -r requirements.txt
```

## 8. Estructura nueva del proyecto

```
app/
  __init__.py
  main.py
  database.py              ← NUEVO
  core/
    __init__.py
    config.py              ← + DATABASE_URL
  models/                  ← NUEVO (carpeta)
    __init__.py
    course.py              ← NUEVO (modelo SQLAlchemy)
  routers/
    __init__.py
    health.py
    courses.py             ← + Depends(get_db)
  schemas/
    __init__.py
    course.py              ← + from_attributes=True
  services/
    __init__.py
    course_service.py      ← REFACTOR (usa BD en vez de lista)
```

---

## 9. Paso a paso: de la lista a la base de datos

### 9.1 `app/database.py` — Configuracion de la BD

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

**Desglose:**

| Linea | Que hace |
|---|---|
| `create_engine(settings.database_url)` | Crea el "puente" entre Python y la BD. El `database_url` dice que BD y donde esta |
| `connect_args={"check_same_thread": False}` | Necesario para SQLite. Permite que FastAPI (multihilo) acceda desde varios hilos |
| `SessionLocal = sessionmaker(...)` | Fabrica de sesiones. Cada vez que la llamas, obtienes una conexion nueva |
| `autocommit=False` | Los cambios no se guardan automaticamente. Tu decides cuando hacer `commit()` |
| `class Base(DeclarativeBase)` | Clase base para todos los modelos SQLAlchemy. Todos heredan de aqui |
| `def get_db():` | Generador que crea una sesion, la entrega (`yield`), y la cierra al terminar |
| `db = SessionLocal()` | Crea una sesion nueva |
| `yield db` | Entrega la sesion al endpoint que la necesita |
| `finally: db.close()` | Cuando el endpoint termina, cierra la sesion |

### 9.2 `app/core/config.py` — Agregar DATABASE_URL

```python
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"


settings = Settings()
```

> **En español simple:** `sqlite:///./cursos.db` significa "crea un archivo llamado `cursos.db` en la carpeta actual del proyecto". Ese archivo ES la base de datos.

### 9.3 `app/models/course.py` — Modelo SQLAlchemy

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

**Desglose:**

| Linea | Que hace |
|---|---|
| `class Course(Base):` | Define un modelo que hereda de `Base`. Cada modelo = una tabla |
| `__tablename__ = "courses"` | Nombre de la tabla en la BD |
| `id = Column(Integer, primary_key=True)` | Columna `id`, entero, clave primaria (autoincremental por defecto) |
| `name = Column(String(80), nullable=False)` | Columna `name`, texto hasta 80 caracteres, no puede ser nulo |
| `credits = Column(Integer, nullable=False)` | Columna `credits`, entero, no nulo |
| `active = Column(Boolean, default=True)` | Columna `active`, booleano, por defecto `True` |

### 9.4 `app/schemas/course.py` — Agregar `from_attributes=True`

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

> **En español simple:** `from_attributes=True` le dice a Pydantic "puedes leer los datos desde un objeto SQLAlchemy, no solo desde un diccionario". Sin esto, `CourseResponse.model_validate(course_sqlalchemy)` fallaria.

### 9.5 `app/main.py` — Crear tablas al iniciar

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

**Desglose:**

| Linea | Que hace |
|---|---|
| `@app.on_event("startup")` | Decorador: ejecuta esta funcion CUANDO el servidor arranca |
| `Base.metadata.create_all(bind=engine)` | Crea TODAS las tablas definidas en modelos que heredan de `Base`. Si ya existen, no las duplica |

> **Analogia:** `create_all()` es como "al llegar a la oficina, asegurate de que los muebles esten armados". Si ya estan armados, no los armas de nuevo.

### 9.6 `app/services/course_service.py` — Refactor a BD

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

**Desglose de cada funcion:**

| Funcion | Antes (lista) | Despues (BD) |
|---|---|---|
| `list_courses` | `return _courses` | `return db.query(Course).all()` |
| `get_course` | Buscar en lista con `for` | `db.query(Course).filter(Course.id == id).first()` |
| `create_course` | Append a lista + `global _next_id` | `db.add()`, `db.commit()`, `db.refresh()` |

**Desglose SQLAlchemy:**

| Linea | Que hace |
|---|---|
| `db.query(Course)` | "Prepara una consulta SELECT en la tabla courses" |
| `.filter(Course.id == course_id)` | "Agrega WHERE id = ?" |
| `.first()` | "Ejecuta y devuelve el primer resultado (o None)" |
| `.all()` | "Ejecuta y devuelve TODOS los resultados como lista" |
| `.filter(Course.name.ilike(...))` | "WHERE name LIKE ? ignorando mayusculas" |
| `Course(name=..., credits=...)` | Crea una instancia del modelo (aun no guardada) |
| `db.add(course)` | "Agrega este objeto a la sesion para ser insertado" |
| `db.commit()` | "Ejecuta el INSERT en la BD" |
| `db.refresh(course)` | "Vuelve a leer el objeto de la BD (para obtener el `id` generado)" |

### 9.7 `app/routers/courses.py` — Inyectar `db` con `Depends()`

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

**Desglose de `Depends(get_db)`:**

```python
def read_courses(db: Session = Depends(get_db)):
    # 1. FastAPI ve "db: Session = Depends(get_db)"
    # 2. Llama a get_db() → abre sesion → yield db
    # 3. Pasa db a esta funcion
    # 4. Cuando la funcion termina, sigue ejecutando get_db()
    # 5. finally: db.close() → cierra la sesion
    return list_courses(db)
```

> **Analogia:** `Depends(get_db)` es como pedir un ticket de turno en el banco. Cada request recibe su propio ticket (sesion). Cuando termina, devuelve el ticket. No compartes ticket con nadie.

---

## 10. Flujo completo de una peticion

```
Cliente: POST /courses {"name": "Fisica", "credits": 4}
    │
    ▼
main.py recibe la peticion
    │
    ▼
FastAPI detecta db: Session = Depends(get_db)
    │
    ▼
get_db() crea SessionLocal() → yield db
    │
    ▼
courses.py: add_course(course_data, db)
    │
    ▼
course_service: create_course(course_data, db)
    ├── db.query(Course).filter(name.ilike(...)).first()  → ¿existe?
    ├── Course(name="Fisica", credits=4, active=True)     → crea objeto
    ├── db.add(course)                                     → prepara INSERT
    ├── db.commit()                                        → ejecuta INSERT
    ├── db.refresh(course)                                 → lee id generado
    └── return course                                      → devuelve objeto
    │
    ▼
Pydantic convierte Course (SQLA) → CourseResponse (JSON)
    │
    ▼
Respuesta: 201 Created {"id": 2, "name": "Fisica", ...}
    │
    ▼
get_db() → finally: db.close()
```

---

## 11. SQLite vs PostgreSQL

| Caracteristica | SQLite | PostgreSQL |
|---|---|---|
| Tipo | Base de datos embebida (archivo) | Servidor independiente |
| Instalacion | No requiere (viene con Python) | Requiere instalacion |
| Uso | Desarrollo, pruebas, proyectos pequenos | Produccion, datos compartidos |
| URL | `sqlite:///./archivo.db` | `postgresql://user:pass@host/db` |
| Multiusuario | Limitado | Excelente |

Para este curso usamos SQLite. Cuando despliegues a produccion, cambias UNA linea en `config.py`:

```python
database_url: str = "postgresql://user:pass@localhost:5432/mi_db"
```

---

## 12. Alembic — Migraciones (introduccion)

> **En español simple:** Cuando cambias la estructura de una tabla (agregar columna, cambiar tipo), necesitas actualizar la BD. Alembic es como "Git para la base de datos": registra cada cambio y permite aplicarlo o deshacerlo.

```bash
pip install alembic
alembic init alembic
```

Luego en `alembic/env.py` configuras la URL de la BD y los modelos:

```python
from app.database import Base
target_metadata = Base.metadata
```

Cuando agregues una columna a `Course`:

```bash
alembic revision --autogenerate -m "add description column"
alembic upgrade head
```

Esto genera y ejecuta el SQL necesario para modificar la tabla sin perder datos.

---

## 13. Errores comunes y troubleshooting

### 13.1 `sqlite3.OperationalError: no such table: courses`

**Causa:** La tabla no se ha creado. `create_all()` no se ejecuto.

**Solucion:** Verifica que `main.py` tenga `@app.on_event("startup")` con `Base.metadata.create_all(bind=engine)`. O ejecuta manualmente:

```python
from app.database import engine, Base
from app.models.course import Course
Base.metadata.create_all(bind=engine)
```

### 13.2 `DetachedInstanceError`

```text
DetachedInstanceError: Instance <Course at 0x...> is not bound to a Session
```

**Causa:** Intentas acceder a un objeto SQLAlchemy DESPUES de que la sesion se cerro.

**Solucion:** Asegurate de que `CourseResponse` tenga `from_attributes=True`. El objeto debe convertirse a schema MIENTRAS la sesion esta abierta.

### 13.3 `IntegrityError: NOT NULL constraint failed`

**Causa:** Intentaste guardar un registro con un campo `nullable=False` sin valor.

**Solucion:** Verifica que todos los campos obligatorios tengan valor antes de `db.commit()`.

### 13.4 El endpoint funciona pero no guarda los datos

**Causa:** Olvidaste `db.commit()`.

**Solucion:** Siempre llama a `db.commit()` despues de `db.add()`. Sin commit, los cambios solo existen en memoria.

```python
db.add(course)
db.commit()      # ← Sin esto, no se guarda
db.refresh(course)
```

### 13.5 Error `sqlite3.ProgrammingError: Cannot operate on a closed database`

**Causa:** La sesion se cerro antes de tiempo.

**Solucion:** Verifica que `get_db()` use `try/finally` para cerrar la sesion solo cuando el endpoint termino.

---

## 14. Actividad central de clase

Refactorizar el proyecto modular de la Clase 05 para que use SQLAlchemy en lugar de listas en memoria.

**Pasos:**
1. Agregar `sqlalchemy` a `requirements.txt` e instalar.
2. Crear `app/database.py` con engine, SessionLocal, Base y get_db.
3. Crear `app/models/` con `course.py` (modelo SQLAlchemy).
4. Agregar `from_attributes=True` a `CourseResponse`.
5. Refactorizar `course_service.py`: reemplazar lista por consultas a la BD.
6. Actualizar `routers/courses.py`: agregar `Depends(get_db)`.
7. Agregar `@app.on_event("startup")` en `main.py`.
8. Probar: crear curso, reiniciar servidor, verificar que persiste.

## 15. Producto de clase — Checklist de verificacion

- [ ] `requirements.txt` incluye `sqlalchemy`
- [ ] `app/database.py` existe con engine, SessionLocal, Base, get_db
- [ ] `app/models/course.py` existe con clase `Course`
- [ ] `CourseResponse` tiene `model_config = ConfigDict(from_attributes=True)`
- [ ] `course_service.py` usa `db.query()`, `db.add()`, `db.commit()`, `db.refresh()`
- [ ] Los servicios reciben `db: Session` como parametro
- [ ] Los routers usan `db: Session = Depends(get_db)` y pasan `db` al servicio
- [ ] `main.py` tiene `@app.on_event("startup")` con `create_all()`
- [ ] Al crear un curso y reiniciar el servidor, el curso sigue existiendo
- [ ] `GET /courses` retorna los cursos persistidos

---

## 16. Cierre conceptual

Reemplazar la lista en memoria por una base de datos es el salto de "prototipo" a "aplicacion real". La estructura del proyecto (routers, services, schemas) no cambio. Solo cambio la implementacion de los services. Esa es la ventaja de la arquitectura modular: puedes cambiar como guardas los datos sin tocar los routers ni los schemas.

---

## 17. Trabajo independiente

Para la siguiente clase, los estudiantes deben:

1. Completar el refactor a BD del proyecto integrador.
2. Agregar un modelo SQLAlchemy `Student` con campos: id, name, email, active.
3. Agregar un modelo `Enrollment` con `course_id` y `student_id` (claves foraneas).
4. Refactorizar el modulo `users` (del desafio de Clase 05) para que use BD.
5. Ejecutar `alembic init` y crear una migracion inicial.

---

## 18. Bibliografia y referencias utiles

- SQLAlchemy. (s. f.). *ORM Quick Start*. https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- FastAPI. (s. f.). *SQL (Relational) Databases*. https://fastapi.tiangolo.com/tutorial/sql-databases/
- Alembic. (s. f.). *Tutorial*. https://alembic.sqlalchemy.org/en/latest/tutorial.html
- Python Software Foundation. (s. f.). *sqlite3*. https://docs.python.org/3/library/sqlite3.html
