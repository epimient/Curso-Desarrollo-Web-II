# Clase 03 - Separacion de responsabilidades y organizacion de aplicaciones web mediante MVC

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 3  
**Unidad:** Unidad 1 - Introduccion a MVC y Frameworks  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA1: Comprender los conceptos fundamentales del patron MVC y los frameworks de desarrollo de software mediante la identificacion de sus componentes y su interaccion.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

Esta clase busca que el estudiante entienda la separacion de responsabilidades como el corazon del patron MVC. No se trata de memorizar carpetas, sino de comprender **por que** cada pieza del codigo debe vivir en un lugar determinado y **que pasa** cuando no lo hace.

El problema real no es "donde pongo este archivo". El problema es: si ponemos toda la logica en un solo archivo, cualquier cambio pequeño puede romper cosas que no tenian que ver con ese cambio. La separacion de responsabilidades es la solucion a ese problema.

## 3. Pregunta orientadora

**Que pasa cuando no separamos responsabilidades y como lo resolvemos?**

Esta pregunta conecta directamente con la experiencia de tener un archivo gigante donde todo esta mezclado y cualquier cambio se siente como desarmar una bomba.

## 4. Que es la separacion de responsabilidades

> **En espanol simple:** la separacion de responsabilidades significa que cada parte del codigo tiene un trabajo y solo un trabajo. Como en un equipo de futbol: el portero no juega de delantero, el mediocampista no defiende la portería.

El Principio de Separacion de Responsabilidades (SRP - Single Responsibility Principle) dice que una clase, modulo o funcion debe tener **una sola razon para cambiar**.

**Analogia:** Imagina una mochila de escuela. Si metes todo junto (libros, lonchera, tablet, botella de agua, cuadernos), cuando necesitas la tablet tienes que revolver todo. Pero si tienes compartimentos separados, cada cosa tiene su lugar y la encuentras rapido.

En programacion pasa igual: si la logica de base de datos, la logica de negocio y la presentacion estan en el mismo archivo, cuando cambias algo de una, puedes romper las otras.

## 5. Las tres capas de una aplicacion web

Toda aplicacion web tiene tres responsabilidades fundamentales:

| Capa | Responsabilidad | Ejemplo en FastAPI |
|------|-----------------|-------------------|
| **Presentacion** | Mostrar informacion al usuario | JSON response, HTML, Swagger |
| **Logica de negocio** | Procesar reglas y decisiones | Validaciones, calculos, reglas |
| **Datos** | Almacenar y recuperar informacion | SQLAlchemy, SQLite, PostgreSQL |

**Analogia del restaurante (versión extendida):**

| Capa | Restaurante | FastAPI |
|------|-------------|---------|
| Presentacion | El plato y la carta | Respuesta JSON, status codes |
| Logica de negocio | El chef y las recetas | Funciones de servicio, validaciones |
| Datos | El almacen y la despensa | Base de datos, sesiones SQLAlchemy |

## 6. Ejemplo: aplicacion SIN separacion

```python
# TODO EN UN SOLO ARCHIVO -asi NO-
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
engine = create_engine("sqlite:///./test.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    credits = Column(Integer)

Base.metadata.create_all(bind=engine)

@app.get("/courses")
def get_courses():
    db = SessionLocal()
    courses = db.query(Course).all()
    return [{"id": c.id, "name": c.name, "credits": c.credits} for c in courses]

@app.post("/courses")
def create_course(name: str, credits: int):
    db = SessionLocal()
    course = Course(name=name, credits=credits)
    db.add(course)
    db.commit()
    return {"id": course.id, "name": course.name}
```

**Problemas:**
- La definicion del modelo esta mezclada con la logica de la app
- La sesion de BD se crea en cada endpoint (ineficiente)
- No hay validacion de datos
- Si cambias la BD, tienes que tocar los endpoints
- Si cambias el formato de respuesta, tienes que tocar la logica de negocio

## 7. Ejemplo: aplicacion CON separacion

### 7.1 Modelo (datos)

```python
# app/models/course.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
```

### 7.2 Schema (validacion)

```python
# app/schemas/course.py
from pydantic import BaseModel, Field

class CourseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    credits: int = Field(..., gt=0, le=10)

class CourseResponse(BaseModel):
    id: int
    name: str
    credits: int

    class Config:
        from_attributes = True
```

### 7.3 Servicio (logica de negocio)

```python
# app/services/course_service.py
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate

def get_courses(db: Session):
    return db.query(Course).all()

def create_course(db: Session, course_data: CourseCreate):
    course = Course(**course_data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
```

### 7.4 Ruta (presentacion)

```python
# app/routers/courses.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.course import CourseCreate, CourseResponse
from app.services import course_service

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return course_service.get_courses(db)

@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return course_service.create_course(db, course)
```

**Beneficios:**
- Cada archivo tiene UNA responsabilidad
- Cambiar la BD no afecta los endpoints
- Cambiar la respuesta no afecta la logica de negocio
- El codigo es mas facil de leer, probar y mantener

## 8. En espanol simple: por que importa

> Si tienes un archivo de 500 lineas donde todo esta junto, encontrar un bug es como buscar una aguja en un pajar. Si tienes archivos separados por responsabilidad, sabes exactamente donde buscar.

La separacion no es burocracia. Es organization para que tu codigo no se convierta en un nudo impossible de desenredar.

## 9. Ejercicio guiado

### Ejercicio 0: Verificacion rapida

Antes de empezar, verifica que tienes Python y pip:

```bash
python --version
pip --version
```

Si no los tienes, instala Python desde https://www.python.org/downloads/

### Ejercicio 1: Identificar responsabilidades

Dado el siguiente codigo, identifica las tres capas y propone separacion:

```python
from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/usuarios")
def get_usuarios():
    conn = sqlite3.connect("mi_base.db")
    cursor = conn.execute("SELECT * FROM usuarios")
    usuarios = [{"id": r[0], "nombre": r[1], "email": r[2]} for r in cursor.fetchall()]
    conn.close()
    return usuarios

@app.post("/usuarios")
def crear_usuario(nombre: str, email: str):
    conn = sqlite3.connect("mi_base.db")
    conn.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
    conn.commit()
    conn.close()
    return {"mensaje": f"Usuario {nombre} creado"}
```

**Solucion:**
- **Presentacion:** Las rutas `@app.get` y `@app.post`
- **Logica de negocio:** La transformacion de datos y validacion
- **Datos:** La conexion SQLite y las consultas SQL

### Ejercicio 2: Refactorizar

Toma el codigo del Ejercicio 1 y separalo en:
1. `models/usuario.py` - modelo de datos
2. `schemas/usuario.py` - schemas de validacion
3. `services/usuario_service.py` - logica de negocio
4. `routers/usuarios.py` - rutas/ENDpoints

## 10. Preguntas frecuentes

**P: MVC es obligatorio?**
R: No es obligatorio, pero es una buena practica. Sin separacion de responsabilidades, tu proyecto se vuelve dificil de mantener rapido.

**P: FastAPI es MVC?**
R: FastAPI no sigue MVC literalmente, pero sus routers, schemas y modelos cumplen funciones similares. La idea es la misma: separar responsabilidades.

**P: Cuantas capas debo crear?**
R: Para empezar, tres capas son suficientes: presentacion, logica de negocio y datos. Puedes agregar mas despues si es necesario.

**P: Que pasa si no separo?**
R: Tu codigo funcionara al principio, pero cuando crezca, sera dificil de mantener, probar y modificar. Es como construir una casa sin planos: funciona hasta que necesitas hacer un cambio.

## 11. Material de estudio

- Clase 02: MVC, patrones y FastAPI
- Ejemplo guiado: Arquitectura por capas
- Ejercicios: Separacion de responsabilidades
