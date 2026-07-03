# Clase 08 - Relaciones entre modelos con SQLAlchemy

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 8  
**Unidad:** Unidad 2 - Uso de un Framework Especifico  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA4: Aplicar principios de diseno de APIs RESTful en la construccion de servicios web mediante la implementacion de endpoints que cumplan con los estandares de la arquitectura REST.
- RA5: Implementar operaciones CRUD utilizando un sistema de persistencia de datos en el desarrollo de aplicaciones web.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

En la Clase 07 aprendiste a conectar tu API a una base de datos y hacer CRUD basico sobre una tabla (`courses`). Pero las aplicaciones reales no viven con una sola tabla aislada. Un sistema de cursos necesita:

- saber qué estudiantes estan inscritos en cada curso;
- saber en qué cursos esta cada estudiante;
- poder consultar "dame todos los estudiantes con nota > 4.0 en Desarrollo Web II".

Para eso necesitas **relaciones entre tablas**. Esta clase te ensena a definirlas, navegarlas y consultarlas con SQLAlchemy.

## 3. Pregunta orientadora

**Como conectamos tablas entre si para responder preguntas que cruzan datos?**

---

> **En español simple:** Hoy cada tabla vive sola (Course, Student). Necesitamos un puente entre ellas. La clave foranea es ese puente, y `relationship()` es el auto que la cruza sin que escribas JOINs.

---

## 4. Conceptos previos requeridos

- Modelo SQLAlchemy basico (Clase 07).
- CRUD con `db.query()`, `db.add()`, `db.commit()`.
- Inyeccion de sesion con `Depends(get_db)`.
- Schemas Pydantic con `from_attributes=True`.
- Concepto basico de clave primaria y tabla.

## 5. El problema: tablas aisladas

En Clase 07 tienes:

```python
class Course(Base):      # Tabla courses
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    credits = Column(Integer)
    active = Column(Boolean)

class Student(Base):     # Tabla students
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
```

Pero **no hay forma** de responder:
- `GET /courses/1/students` → "¿que estudiantes cursan Desarrollo Web II?"
- `GET /students/1/courses` → "¿en que cursos esta Ana?"

Las tablas existen, pero no estan conectadas.

> **Analogia:** Es como tener la lista de estudiantes en una hoja y la de cursos en otra, sin ningun numero de expediente que las vincule. Sabes que existen, pero no quien esta en que.

## 6. La solucion: clave foranea + relationship

Se necesitan DOS cosas:

1. **`ForeignKey`** — una columna en una tabla que apunta a la PK de otra (el puente fisico en la BD).
2. **`relationship()`** — un atributo Python que permite navegar entre objetos sin escribir JOINs (el mapa mental).

| Concepto | Analogia |
|---|---|
| `ForeignKey` | El numero de seguro social que vincula a una persona con su expediente medico |
| `relationship()` | La ficha que dice "esta persona tiene estos expedientes" sin buscar uno por uno |

---

## 7. Modelo Enrollment (tabla puente)

Entre Course y Student hay una relacion **Many-to-Many**: un curso tiene muchos estudiantes, un estudiante puede estar en muchos cursos. En BD relacional, eso necesita una **tabla intermedia**.

La creamos con `Enrollment`:

```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
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

**Desglose:**

| Linea | Que hace |
|---|---|
| `course_id = Column(Integer, ForeignKey("courses.id"))` | Columna que almacena el ID del curso. `ForeignKey("courses.id")` le dice a la BD: "esto solo puede contener IDs que existan en la tabla courses" |
| `student_id = Column(Integer, ForeignKey("students.id"))` | Igual, pero para el estudiante |
| `course = relationship("Course", back_populates="enrollments")` | Atributo Python. `enrollment.course` devuelve el objeto `Course` completo (no solo el ID) |
| `student = relationship("Student", back_populates="enrollments")` | `enrollment.student` devuelve el objeto `Student` |
| `grade = Column(Float, nullable=True)` | Nota opcional. `nullable=True` significa que puede ser `NULL` (sin nota aun) |

> **En español simple:** `ForeignKey` es el candado fisico en la BD que impide IDs invalidos. `relationship()` es la llave Python que te deja hacer `enrollment.course.name` en lugar de tener que hacer otra query con el `course_id`.

---

## 8. Agregar `relationship()` en Course y Student

El modelo Course necesita un `relationship()` que apunte de vuelta a Enrollment:

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

    # NUEVO: relacion inversa
    enrollments = relationship("Enrollment", back_populates="course")
```

Y el modelo Student:

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

    # NUEVO: relacion inversa
    enrollments = relationship("Enrollment", back_populates="student")
```

**Que logramos con esto:**

```python
# Antes: teniamos IDs sueltos
enrollment.course_id  # → 1 (solo un numero)

# Ahora: navegamos al objeto completo
enrollment.course      # → <Course(id=1, name="Fisica")>
enrollment.course.name # → "Fisica"
enrollment.student.email # → "ana@mail.com"
```

> **En español simple:** `back_populates` es como la comunicacion de radio entre dos personas: "Curso, tus inscripciones estan en Enrollment". "Enrollment, tu curso esta en Course". Ambas clases se senalan mutuamente.

---

## 9. Flujo de datos con relaciones

Visualmente, asi se conectan las tablas:

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│   courses    │       │   enrollments    │       │   students   │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │←──┐   │ id (PK)          │   ┌──→│ id (PK)      │
│ name         │   └───│ course_id (FK)   │   │   │ name         │
│ credits      │       │ student_id (FK)  │───┘   │ email        │
│ active       │       │ enrolled_at      │       │ active       │
└──────────────┘       │ grade            │       └──────────────┘
                       └──────────────────┘
```

**Traduccion:** Cada fila en `enrollments` tiene un `course_id` que apunta a `courses.id` y un `student_id` que apunta a `students.id`. Una inscripcion = un estudiante en un curso.

---

## 10. Consultas con relaciones

### 10.1 Obtener estudiantes de un curso

```python
def get_students_by_course(course_id: int, db: Session) -> list[Student]:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # course.enrollments es una lista de Enrollment
    # Cada enrollment tiene .student → el objeto Student
    return [enrollment.student for enrollment in course.enrollments]
```

**Explicacion:**
1. Buscamos el curso por ID.
2. `course.enrollments` nos da TODAS las inscripciones de ese curso (SQLAlchemy ejecuta la query automaticamente).
3. De cada inscripcion, tomamos `.student` para obtener el estudiante.

**La query SQL que SQLAlchemy ejecuta detras:**

```sql
-- Paso 1: buscar el curso
SELECT * FROM courses WHERE id = 1;

-- Paso 2: buscar inscripciones (lazy loading, la primera vez que accedes a .enrollments)
SELECT * FROM enrollments WHERE course_id = 1;

-- Paso 3: buscar estudiantes (una query por enrollment, si no hay eager loading)
SELECT * FROM students WHERE id = ?;
```

### 10.2 Obtener cursos de un estudiante

```python
def get_courses_by_student(student_id: int, db: Session) -> list[Course]:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return [enrollment.course for enrollment in student.enrollments]
```

### 10.3 Crear inscripcion

```python
def create_enrollment(
    course_id: int, student_id: int, db: Session
) -> Enrollment:
    # Verificar que el curso existe
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Verificar que el estudiante existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Verificar que no este ya inscrito
    existing = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.student_id == student_id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Student already enrolled in this course"
        )

    enrollment = Enrollment(course_id=course_id, student_id=student_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment
```

---

## 11. Eager loading vs Lazy loading

> **En español simple:** Cuando cargas un curso, `course.enrollments` puede cargarse automaticamente (eager) o solo cuando lo necesitas (lazy). Como pedir la cuenta con todos los platos detallados (eager) vs pedir cada plato por separado (lazy).

### Lazy loading (por defecto)

```python
course = db.query(Course).first()
# En este momento, course.enrollments NO se ha consultado aun

# Solo cuando accedes a .enrollments se ejecuta la query:
for enrollment in course.enrollments:  # ← aqui se ejecuta SELECT WHERE course_id=?
    print(enrollment.student.name)     # ← aqui otra SELECT para cada student
```

**Problema:** Si tienes 100 estudiantes, haces 1 + 1 + 100 = 102 queries. Esto se llama **problema N+1**.

### Eager loading con `selectinload()`

```python
from sqlalchemy.orm import selectinload

course = db.query(Course).options(
    selectinload(Course.enrollments).selectinload(Enrollment.student)
).first()
# Ahora SOLO 3 queries:
# 1. SELECT * FROM courses
# 2. SELECT * FROM enrollments WHERE course_id IN (...)
# 3. SELECT * FROM students WHERE id IN (...)
```

**Regla practica:** En desarrollo usa lazy (es mas simple). Cuando veas lentitud, agrega `selectinload()`.

---

## 12. Cascading deletes

**Pregunta:** ¿Que pasa si elimino un curso que tiene inscripciones?

### Opcion A: Restrict (por defecto)

```sql
DELETE FROM courses WHERE id = 1;
-- ERROR: FOREIGN KEY constraint failed
-- No puedes eliminar un curso que tiene inscripciones
```

### Opcion B: Cascade

```python
class Enrollment(Base):
    __tablename__ = "enrollments"
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),  ←
        nullable=False,
    )
```

Con `ondelete="CASCADE"`, si eliminas el curso, se eliminan TODAS sus inscripciones automaticamente.

**Analogia:** Si cierras un curso (lo eliminas), las inscripciones tambien desaparecen. Los estudiantes no, solo su relacion con ese curso.

---

## 13. Errores comunes y troubleshooting

### 13.1 `IntegrityError: FOREIGN KEY constraint failed`

```text
sqlite3.IntegrityError: FOREIGN KEY constraint failed
```

**Causa:** Intentaste crear un `Enrollment` con un `course_id` o `student_id` que no existe.

**Solucion:** Verifica que el curso y el estudiante existen antes de crear la inscripcion.

### 13.2 El `relationship()` no devuelve datos

**Causa:** Definiste `relationship()` en un modelo pero olvidaste el `back_populates` en el otro.

**Solucion:** Siempre usa `back_populates` en AMBOS lados de la relacion.

### 13.3 Error al hacer `db.refresh()` con relaciones

**Causa:** El modelo relacionado aun no esta en la BD.

**Solucion:** `refresh()` funciona sobre el objeto principal. Las relaciones cargadas con lazy loading pueden fallar si la sesion se cerro.

### 13.4 `DetachedInstanceError` con relaciones

```python
course = db.query(Course).first()
# ... la sesion se cierra
for enrollment in course.enrollments:  # ❌ DetachedInstanceError
```

**Solucion:** Usa eager loading (`selectinload()`) para cargar las relaciones MIENTRAS la sesion esta abierta.

### 13.5 Problema N+1

**Sintoma:** La API funciona pero es muy lenta al listar cursos con estudiantes.

**Causa:** Por cada curso, SQLAlchemy hace una query adicional para cargar `enrollments`.

**Solucion:** Agrega `selectinload()` en la query principal.

---

## 14. Actividad central de clase

Extender la API de cursos para incorporar estudiantes e inscripciones con relaciones.

**Pasos:**
1. Agregar modelo `Student` (si no existe).
2. Crear modelo `Enrollment` con FK a `courses` y `students`.
3. Agregar `relationship()` en los tres modelos.
4. Crear schema `EnrollmentResponse` con `from_attributes=True`.
5. Crear schema `CourseWithStudentsResponse` que incluya lista de estudiantes.
6. Endpoint `GET /courses/{id}/students` → estudiantes de un curso.
7. Endpoint `GET /students/{id}/courses` → cursos de un estudiante.
8. Endpoint `POST /enrollments` → inscribir estudiante en curso (con validaciones).

## 15. Producto de clase — Checklist de verificacion

- [ ] `app/models/enrollment.py` existe con FK a course y student
- [ ] `Course` tiene `enrollments = relationship("Enrollment", back_populates="course")`
- [ ] `Student` tiene `enrollments = relationship("Enrollment", back_populates="student")`
- [ ] `Enrollment` tiene `course = relationship(...)` y `student = relationship(...)`
- [ ] `CourseWithStudentsResponse` existe como schema anidado
- [ ] `GET /courses/{id}/students` retorna lista de estudiantes del curso
- [ ] `GET /students/{id}/courses` retorna lista de cursos del estudiante
- [ ] `POST /enrollments` valida que curso y estudiante existen
- [ ] `POST /enrollments` rechaza inscripcion duplicada (mismo estudiante en mismo curso)
- [ ] `GET /courses` sigue funcionando sin cambios (compatibilidad hacia atras)
- [ ] Crear estudiante, inscribirlo, reiniciar servidor, verificar persistencia
- [ ] El archivo `.db` se puede inspeccionar con `sqlite3`

---

## 16. Cierre conceptual

Las relaciones son lo que transforma tablas aisladas en un **modelo de datos**. Con FK + relationship puedes navegar entre objetos como si fueran atributos, sin escribir JOINs manualmente.

El salto de Clase 07 a Clase 08 es el salto de "tengo datos" a "mis datos estan conectados y puedo hacer preguntas que cruzan tablas".

---

## 17. Trabajo independiente

1. Agregar `Review` (resena) con FK a Course y Student, y campos `rating` (1-5) y `comment` (texto).
2. Endpoint `POST /reviews` para crear resena.
3. Endpoint `GET /courses/{id}/reviews` que retorna resenas del curso con nombre del estudiante.
4. Investigar la diferencia entre `selectinload()` y `joinedload()` (leer documentacion SQLAlchemy).
5. Agregar `ondelete="CASCADE"` en las FK de Enrollment y probar eliminar un curso.

---

## 18. Bibliografia y referencias utiles

- SQLAlchemy. (s. f.). *Relationship Configuration*. https://docs.sqlalchemy.org/en/20/orm/relationships.html
- SQLAlchemy. (s. f.). *Basic Relationship Patterns*. https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
- SQLAlchemy. (s. f.). *Loading Relationships*. https://docs.sqlalchemy.org/en/20/orm/loading_relationships.html
- FastAPI. (s. f.). *SQL (Relational) Databases*. https://fastapi.tiangolo.com/tutorial/sql-databases/
