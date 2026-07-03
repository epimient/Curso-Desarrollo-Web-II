# Ejemplo guiado — Proyecto Integrador

**Objetivo:** Extender el proyecto base de la Clase 12 (`proyecto-con-despliegue`) para agregar matrículas (enrollments), paginación, PUT en cursos, y pruebas.

---

## Paso 1: Copiar el proyecto base

```bash
cp -r ../clase-12-despliegue-render-supabase/proyecto-con-despliegue proyecto-final-integrador
cd proyecto-final-integrador
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Paso 2: Crear el modelo Enrollment

`app/models/enrollment.py`:

```python
from sqlalchemy import Column, Integer, Float, ForeignKey, String, Enum as SAEnum
from app.database import Base
import enum

class EnrollmentStatus(str, enum.Enum):
    enrolled = "enrolled"
    completed = "completed"
    cancelled = "cancelled"

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    grade = Column(Float, nullable=True)
    status = Column(SAEnum(EnrollmentStatus), default=EnrollmentStatus.enrolled)
```

Registrar en `app/models/__init__.py`:

```python
from app.models.course import Course
from app.models.user import User
from app.models.enrollment import Enrollment  # ← nuevo
```

## Paso 3: Crear schemas para Enrollment

`app/schemas/enrollment.py`:

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.enrollment import EnrollmentStatus

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentUpdate(BaseModel):
    grade: Optional[float] = None
    status: Optional[EnrollmentStatus] = None

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade: Optional[float] = None
    status: EnrollmentStatus

    model_config = {"from_attributes": True}
```

Registrar en `app/schemas/__init__.py`:

```python
from app.schemas.course import CourseCreate, CourseResponse
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, TokenData
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
```

## Paso 4: Servicio de Enrollment

`app/services/enrollment_service.py`:

```python
from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from app.errors.exceptions import NotFoundException, BusinessRuleException

class EnrollmentService:

    @staticmethod
    def create(db: Session, data: EnrollmentCreate) -> Enrollment:
        existing = db.query(Enrollment).filter(
            Enrollment.student_id == data.student_id,
            Enrollment.course_id == data.course_id,
            Enrollment.status != EnrollmentStatus.cancelled,
        ).first()
        if existing:
            raise BusinessRuleException("El estudiante ya está inscrito en este curso")
        enrollment = Enrollment(**data.model_dump())
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    @staticmethod
    def get_all(db: Session, student_id: int | None = None, course_id: int | None = None) -> list[Enrollment]:
        query = db.query(Enrollment)
        if student_id:
            query = query.filter(Enrollment.student_id == student_id)
        if course_id:
            query = query.filter(Enrollment.course_id == course_id)
        return query.all()

    @staticmethod
    def get_by_id(db: Session, enrollment_id: int) -> Enrollment:
        enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            raise NotFoundException("Matrícula no encontrada")
        return enrollment

    @staticmethod
    def update(db: Session, enrollment_id: int, data: EnrollmentUpdate) -> Enrollment:
        enrollment = EnrollmentService.get_by_id(db, enrollment_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(enrollment, key, value)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    @staticmethod
    def delete(db: Session, enrollment_id: int) -> None:
        enrollment = EnrollmentService.get_by_id(db, enrollment_id)
        db.delete(enrollment)
        db.commit()
```

Registrar en `app/services/__init__.py`:

```python
from app.services.course_service import CourseService
from app.services.user_service import UserService
from app.services.enrollment_service import EnrollmentService
```

## Paso 5: Router de Enrollment

`app/routers/enrollments.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
from app.services.enrollment_service import EnrollmentService
from app.auth.dependencies import get_current_user, require_admin
from app.models.user import User

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentResponse, status_code=201)
def create_enrollment(data: EnrollmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return EnrollmentService.create(db, data)

@router.get("/", response_model=list[EnrollmentResponse])
def list_enrollments(student_id: int | None = None, course_id: int | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return EnrollmentService.get_all(db, student_id, course_id)

@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return EnrollmentService.get_by_id(db, enrollment_id)

@router.patch("/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(enrollment_id: int, data: EnrollmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return EnrollmentService.update(db, enrollment_id, data)

@router.delete("/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    EnrollmentService.delete(db, enrollment_id)
```

## Paso 6: Registrar en main.py

`app/main.py`:

```python
from app.routers.courses import router as courses_router
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.enrollments import router as enrollments_router  # ← nuevo

# En la función create_app o después de crear la app:
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(courses_router)
app.include_router(enrollments_router)  # ← nuevo
```

## Paso 7: Paginación en GET /courses/

Actualizar `app/routers/courses.py`:

```python
from math import ceil

@router.get("/", response_model=dict)
def list_courses(
    name: str | None = None,
    credits: int | None = None,
    active: bool | None = None,
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db),
):
    courses = CourseService.get_all(db, name=name, credits=credits, active=active)
    total = len(courses)
    start = (page - 1) * per_page
    end = start + per_page
    page_courses = courses[start:end]
    return {
        "items": page_courses,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": ceil(total / per_page) if total > 0 else 0,
    }
```

Actualizar `app/services/course_service.py`:

```python
@staticmethod
def get_all(db: Session, name: str | None = None, credits: int | None = None, active: bool | None = None) -> list[Course]:
    query = db.query(Course)
    if name:
        query = query.filter(Course.name.ilike(f"%{name}%"))
    if credits is not None:
        query = query.filter(Course.credits == credits)
    if active is not None:
        query = query.filter(Course.active == active)
    return query.all()
```

## Paso 8: PUT /courses/{id}

Agregar a `app/schemas/course.py`:

```python
class CourseUpdate(BaseModel):
    name: Optional[str] = None
    credits: Optional[int] = None
    active: Optional[bool] = None
```

Agregar a `app/services/course_service.py`:

```python
@staticmethod
def update(db: Session, course_id: int, data: CourseUpdate) -> Course:
    course = CourseService.get_by_id(db, course_id)
    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing = db.query(Course).filter(Course.name == update_data["name"], Course.id != course_id).first()
        if existing:
            raise BusinessRuleException("Ya existe un curso con ese nombre")
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course
```

Agregar a `app/routers/courses.py`:

```python
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, data: CourseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CourseService.update(db, course_id, data)
```

---

## Paso 9: Escribir tests

`app/tests/test_enrollments.py`:

```python
import pytest
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.schemas.enrollment import EnrollmentCreate

def test_create_enrollment(client, token, created_course):
    response = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course.id,
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["student_id"] == 1
    assert data["status"] == "enrolled"

def test_duplicate_enrollment_fails(client, token, created_course):
    client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course.id,
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course.id,
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

def test_list_enrollments(client, token, created_course):
    client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course.id,
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/enrollments/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_enrollment_by_id(client, token, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course.id,
    }, headers={"Authorization": f"Bearer {token}"})
    eid = create_resp.json()["id"]
    response = client.get(f"/enrollments/{eid}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_update_enrollment_grade(client, token, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course.id,
    }, headers={"Authorization": f"Bearer {token}"})
    eid = create_resp.json()["id"]
    response = client.patch(f"/enrollments/{eid}", json={"grade": 95.5}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["grade"] == 95.5

def test_delete_enrollment_as_admin(client, admin_headers, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course.id,
    }, headers=admin_headers)
    eid = create_resp.json()["id"]
    response = client.delete(f"/enrollments/{eid}", headers=admin_headers)
    assert response.status_code == 204

def test_delete_enrollment_as_student_fails(client, token, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course.id,
    }, headers={"Authorization": f"Bearer {token}"})
    eid = create_resp.json()["id"]
    response = client.delete(f"/enrollments/{eid}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
```

Actualizar conftest.py para incluir fixtures nuevas si hiciera falta.

---

## Paso 10: Verificar todo

```bash
# Tests
pytest -v

# Coverage
pytest --cov=app --cov-report=term-missing

# Swagger: abrir http://localhost:8000/docs
fastapi dev app/main.py

# Verificar que todo funciona
fastapi dev app/main.py
```

---

## Paso 11: Desplegar en Render

1. Subir a GitHub
2. Configurar DATABASE_URL con PostgreSQL de Supabase
3. Render detecta el push y despliega automáticamente
4. Verificar: `curl https://tu-app.onrender.com/health/`
