# Ejemplo guiado - Relaciones entre modelos con SQLAlchemy

## Objetivo

Partiendo del proyecto con BD de la Clase 07, agregar los modelos `Student` y `Enrollment` con claves foraneas y relaciones, y crear endpoints que crucen datos entre tablas.

---

## Requisitos

- Proyecto de Clase 07 funcionando (proyecto-con-bd).
- `pip install sqlalchemy` (ya deberia estar).

---

## Paso 1. Agregar modelo Student

Crea `app/models/student.py`:

```python
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)

    enrollments = relationship("Enrollment", back_populates="student")
```

**Nuevo respecto a Clase 07:** La linea `enrollments = relationship(...)` — permite hacer `student.enrollments` para obtener todas las inscripciones de un estudiante.

---

## Paso 2. Agregar modelo Enrollment

Crea `app/models/enrollment.py`:

```python
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.now)
    grade = Column(Float, nullable=True)

    course = relationship("Course", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")
```

**Desglose de las FK:**

```python
course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
#                │              │                      │
#         tipo entero   "apunta a la tabla        no puede ser nulo
#                        courses, columna id"
```

---

## Paso 3. Agregar `relationship()` en Course

Modifica `app/models/course.py` — agrega la linea con `relationship()`:

```python
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    credits = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

    enrollments = relationship("Enrollment", back_populates="course")
```

**Unico cambio:** la ultima linea. Sin esto, `course.enrollments` no existiria.

---

## Paso 4. Crear schemas para las relaciones

`app/schemas/student.py`:

```python
from pydantic import BaseModel, Field, ConfigDict


class StudentCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5, max_length=100)


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    active: bool
```

`app/schemas/enrollment.py`:

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EnrollmentCreate(BaseModel):
    course_id: int
    student_id: int


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    student_id: int
    enrolled_at: datetime
    grade: float | None = None
```

`app/schemas/course.py` — agregar schema anidado:

```python
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.student import StudentResponse


class CourseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    credits: int = Field(ge=1, le=6)


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    credits: int
    active: bool


class CourseWithStudentsResponse(CourseResponse):
    students: list[StudentResponse] = []
```

**Desglose de `CourseWithStudentsResponse`:**

| Linea | Que hace |
|---|---|
| `class CourseWithStudentsResponse(CourseResponse):` | Hereda todos los campos de `CourseResponse` (id, name, credits, active) |
| `students: list[StudentResponse] = []` | Agrega un campo nuevo: una lista de objetos `StudentResponse` |

Este schema se usa en `GET /courses/{id}/students` para devolver el curso con sus estudiantes adentro.

---

## Paso 5. Crear servicios

`app/services/student_service.py`:

```python
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.student import Student
from app.schemas.student import StudentCreate


def list_students(db: Session) -> list[Student]:
    return db.query(Student).all()


def get_student(student_id: int, db: Session) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


def create_student(student_data: StudentCreate, db: Session) -> Student:
    student = Student(name=student_data.name, email=student_data.email)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
```

`app/services/enrollment_service.py`:

```python
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException

from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.student import Student


def create_enrollment(course_id: int, student_id: int, db: Session) -> Enrollment:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing = db.query(Enrollment).filter(
        and_(Enrollment.course_id == course_id, Enrollment.student_id == student_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    enrollment = Enrollment(course_id=course_id, student_id=student_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def get_students_by_course(course_id: int, db: Session) -> list[Student]:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return [enrollment.student for enrollment in course.enrollments]


def get_courses_by_student(student_id: int, db: Session) -> list[Course]:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return [enrollment.course for enrollment in student.enrollments]
```

---

## Paso 6. Crear routers

`app/routers/students.py`:

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student_service import create_student, get_student, list_students
from app.services.enrollment_service import get_courses_by_student
from app.schemas.course import CourseResponse

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=list[StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return list_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    return get_student(student_id, db)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def add_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    return create_student(student_data, db)


@router.get("/{student_id}/courses", response_model=list[CourseResponse])
def read_student_courses(student_id: int, db: Session = Depends(get_db)):
    return get_courses_by_student(student_id, db)
```

`app/routers/enrollments.py`:

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.services.enrollment_service import (
    create_enrollment,
)

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post(
    "/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_enrollment(
    enrollment_data: EnrollmentCreate, db: Session = Depends(get_db)
):
    return create_enrollment(
        enrollment_data.course_id, enrollment_data.student_id, db
    )
```

Y en `app/routers/courses.py`, agrega un endpoint nuevo:

```python
# ... (codigo existente) ...

from app.services.enrollment_service import get_students_by_course
from app.schemas.student import StudentResponse


@router.get("/{course_id}/students", response_model=list[StudentResponse])
def read_course_students(course_id: int, db: Session = Depends(get_db)):
    return get_students_by_course(course_id, db)
```

---

## Paso 7. Actualizar `main.py`

Registra los nuevos routers:

```python
from app.routers import courses, health, students, enrollments

app.include_router(health.router)
app.include_router(courses.router)
app.include_router(students.router)      # ← NUEVO
app.include_router(enrollments.router)   # ← NUEVO
```

---

## Paso 8. Crear tablas y probar

```bash
uvicorn app.main:app --reload
```

**Pruebas:**

| Accion | URL / Body | Resultado esperado |
|---|---|---|
| Crear estudiante | `POST /students` `{"name": "Ana", "email": "ana@mail.com"}` | Status 201 |
| Listar estudiantes | `GET /students` | 1 estudiante |
| Crear curso | `POST /courses` `{"name": "Fisica", "credits": 4}` | Status 201 |
| Inscribir | `POST /enrollments` `{"course_id": 1, "student_id": 1}` | Status 201 |
| Estudiantes del curso | `GET /courses/1/students` | `[{"id": 1, "name": "Ana", ...}]` |
| Cursos del estudiante | `GET /students/1/courses` | `[{"id": 1, "name": "Fisica", ...}]` |
| Inscribir duplicado | `POST /enrollments` mismo course_id y student_id | Status 400 |
| Inscribir en curso inexistente | `POST /enrollments` `{"course_id": 999, "student_id": 1}` | Status 404 |

---

## Paso 9. ¿Que pasaria si...?

**Escenario 1:** Olvido `back_populates` en un lado
```python
# Course tiene: enrollments = relationship("Enrollment", back_populates="course")
# Enrollment tiene: course = relationship("Course")  # ❌ falta back_populates
```
**Sintoma:** `course.enrollments` funciona, pero `enrollment.course` devuelve `None`.
**Solucion:** Agrega `back_populates="course"` en ambos lados.

**Escenario 2:** FK sin `nullable=False`
```python
course_id = Column(Integer, ForeignKey("courses.id"))  # ❌ falta nullable=False
```
**Sintoma:** Puedes crear inscripciones sin especificar curso.
**Solucion:** Siempre usa `nullable=False` en FK obligatorias.

**Escenario 3:** Crear inscripcion sin verificar existencia
```python
# ❌ MAL: no verificas si el curso/estudiante existe
enrollment = Enrollment(course_id=999, student_id=1)
db.add(enrollment)
db.commit()  # ← Explota aqui: IntegrityError
```
**Sintoma:** `IntegrityError: FOREIGN KEY constraint failed`.
**Solucion:** Siempre verifica existencia antes de crear.

**Escenario 4:** Acceder a `course.enrollments` fuera de la sesion
```python
course = db.query(Course).first()
db.close()
print(course.enrollments)  # ❌ DetachedInstanceError
```
**Solucion:** Usa `selectinload()` para cargar las relaciones mientras la sesion esta abierta.

---

## Resumen de archivos nuevos/modificados

| Archivo | Estado | Cambio |
|---|---|---|
| `app/models/student.py` | **NUEVO** | Modelo Student con relationship |
| `app/models/enrollment.py` | **NUEVO** | Modelo Enrollment con FK |
| `app/models/course.py` | Modificado | + `enrollments = relationship(...)` |
| `app/schemas/student.py` | **NUEVO** | StudentCreate + StudentResponse |
| `app/schemas/enrollment.py` | **NUEVO** | EnrollmentCreate + EnrollmentResponse |
| `app/schemas/course.py` | Modificado | + `CourseWithStudentsResponse` |
| `app/services/student_service.py` | **NUEVO** | CRUD de estudiantes |
| `app/services/enrollment_service.py` | **NUEVO** | Crear inscripcion + consultas cruzadas |
| `app/routers/students.py` | **NUEVO** | Endpoints de estudiantes |
| `app/routers/enrollments.py` | **NUEVO** | Endpoint de inscripcion |
| `app/routers/courses.py` | Modificado | + `GET /{id}/students` |
| `app/main.py` | Modificado | + routers de students y enrollments |

---

## Cierre

Ahora los datos estan conectados. Puedes responder preguntas que cruzan tablas sin escribir SQL manualmente. La relacion Many-to-Many via tabla intermedia es el patron mas comun en aplicaciones web: usuarios con roles, productos con categorias, estudiantes con cursos.
