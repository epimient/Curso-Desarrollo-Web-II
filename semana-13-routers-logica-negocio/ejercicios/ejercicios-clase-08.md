# Ejercicios - Clase 08

> **Nota:** El ejercicio 0 es de calentamiento. Los ejercicios 1-5 construyen sobre el ejemplo guiado de relaciones.

---

## Ejercicio 0. Emparejar terminos

Une cada termino de la izquierda con su descripcion a la derecha:

| Termino | Descripcion |
|---|---|
| 1. `ForeignKey` | A. Atributo Python para navegar entre objetos relacionados |
| 2. `relationship()` | B. Columna que apunta a la PK de otra tabla |
| 3. `back_populates` | C. Carga las relaciones automaticamente al hacer la query principal |
| 4. `selectinload()` | D. Conexion inversa entre dos `relationship()` |
| 5. Lazy loading | E. Elimina registros relacionados al eliminar el padre |
| 6. Cascade | F. Las relaciones se cargan solo cuando se accede a ellas |
| 7. Many-to-Many | G. Usa una tabla intermedia para conectar dos tablas |
| 8. `ondelete="CASCADE"` | H. Estrategia de eliminacion en cascada en la FK |

---

## Ejercicio 1. Definir modelo Enrollment

Sin mirar el ejemplo, escribe el modelo completo `Enrollment` que:

1. Tenga `id` como PK autoincremental
2. Tenga `course_id` como FK a `courses.id`
3. Tenga `student_id` como FK a `students.id`
4. Tenga `enrolled_at` con `default=datetime.now`
5. Tenga `grade` como `Float` opcional
6. Tenga `relationship()` a `Course` y `Student`

```python
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    # Escribe aqui el modelo completo
    ...
```

---

## Ejercicio 2. Navegar relaciones en shell

Dado el siguiente codigo, responde las preguntas:

```python
# Tenemos 3 cursos y 2 estudiantes con varias inscripciones
courses = db.query(Course).all()       # 3 cursos
students = db.query(Student).all()     # 2 estudiantes
enrollments = db.query(Enrollment).all()  # 4 inscripciones

# Pregunta 1: ¿Que devuelve courses[0].enrollments?
# Pregunta 2: ¿Que devuelve enrollments[0].student.name?
# Pregunta 3: ¿Como obtienes TODOS los estudiantes del segundo curso?
# Pregunta 4: ¿Como obtienes TODOS los cursos del primer estudiante?
```

**Escribe tu respuesta:**

```
Pregunta 1: _________________________________
Pregunta 2: _________________________________
Pregunta 3: _________________________________
Pregunta 4: _________________________________
```

---

## Ejercicio 3. Endpoint con relacion anidada

Crea un endpoint que devuelva un curso con todos sus estudiantes y sus notas:

```http
GET /courses/{course_id}/grades
```

**Respuesta esperada:**

```json
{
  "id": 1,
  "name": "Fisica",
  "credits": 4,
  "students": [
    {"student_name": "Ana", "grade": 4.5},
    {"student_name": "Luis", "grade": 3.8}
  ]
}
```

**Pista:** Necesitaras un schema nuevo `CourseGradesResponse` y usar el `Enrollment` para acceder tanto al `student.name` como al `grade`.

```python
class CourseGradesResponse(BaseModel):
    id: int
    name: str
    credits: int
    students: list[StudentGrade] = []


class StudentGrade(BaseModel):
    student_name: str
    grade: float | None = None
```

---

## Ejercicio 4. Depurar errores de relaciones

Identifica la causa y escribe la solucion para cada error:

**Error A:**
```python
# Modelos
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course")  # ❌ falta back_populates
```

**Pregunta:** ¿Que falla al hacer `enrollment.course.name`?

**Error B:**
```text
sqlite3.IntegrityError: FOREIGN KEY constraint failed
al hacer: db.commit() despues de db.add(enrollment)
```

**Pregunta:** ¿Cuales son las dos causas posibles?

**Error C:**
```python
# En un endpoint:
course = db.query(Course).filter(Course.id == 1).first()
db.close()
return course.enrollments  # ❌ Error en ejecucion
```

**Pregunta:** ¿Que tipo de error ocurre y por que?

---

## Ejercicio 5. Consulta con filtro sobre relacion

Implementa una funcion que retorne los estudiantes de un curso que tengan nota mayor o igual a un valor:

```python
def get_students_with_grade(
    course_id: int, min_grade: float, db: Session
) -> list[dict]:
    """
    Retorna los estudiantes del curso cuyo grade >= min_grade.
    Cada elemento: {"student_name": str, "grade": float}
    """
    # Tu codigo aqui
```

**Pista:** Necesitas hacer una query sobre `Enrollment` con filtros en `course_id` y `grade`, y luego acceder a `enrollment.student.name`.

**Verificacion:**

| Datos | Resultado esperado |
|---|---|
| Curso 1 tiene Ana(4.5) y Luis(3.8) | `get_students_with_grade(1, 4.0)` → solo Ana |
| Curso 1 tiene Ana(4.5) y Luis(3.8) | `get_students_with_grade(1, 3.0)` → Ana y Luis |

---

## Desafio extra (opcional)

Crea un modelo `Review` para resenas de cursos por estudiantes:

```python
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 a 5
    comment = Column(String(500), nullable=True)
```

**Luego debes:**

1. Agregar `relationship()` en ambos lados (Course, Student).
2. Crear `app/schemas/review.py` con `ReviewCreate` y `ReviewResponse`.
3. Crear `app/routers/reviews.py` con:
   - `POST /reviews` (validar rating 1-5, verificar que el estudiante esta inscrito en el curso).
   - `GET /courses/{course_id}/reviews` (retorna resenas con nombre del estudiante).
4. Registrar el router en `main.py`.

**Verificacion:**

```bash
# Crear resena
POST /reviews {"course_id": 1, "student_id": 1, "rating": 5, "comment": "Excelente"}

# Listar resenas del curso
GET /courses/1/reviews
```
