# Dudas frecuentes - Clase 08

> Aqui encontraras las preguntas mas comunes sobre relaciones entre modelos con SQLAlchemy.

---

## 1. ¿Que es una clave foranea (ForeignKey)?

**Respuesta corta:** Es una columna que almacena el ID de otra tabla, creando un vinculo entre ambas.

**Respuesta larga:** `ForeignKey("courses.id")` en la columna `course_id` de `Enrollment` significa "esto solo puede contener valores que existan en la columna `id` de la tabla `courses`". Si intentas guardar un `course_id=999` y no existe un curso con ese ID, la BD lanza `IntegrityError`.

**Tipos de FK:**
- **Simple:** un solo campo apunta a otra tabla.
- **Compuesta:** dos o mas campos juntos apuntan a otra tabla (avanzado).

**Analogia:** Es como el numero de cedula en un pais. Tu tienes una cedula (PK en la tabla de ciudadanos). Cualquier formulario que pida tu cedula (FK) solo puede poner numeros que realmente existan.

---

## 2. ¿Que es `relationship()` y en que se diferencia de ForeignKey?

**Respuesta corta:** `ForeignKey` es el vinculo fisico en la BD. `relationship()` es un atajo Python para navegar ese vinculo sin escribir JOINs.

**Respuesta larga:**

| Caracteristica | `ForeignKey` | `relationship()` |
|---|---|---|
| Donde existe | En la BD (la tabla) | En Python (el modelo) |
| Que hace | Restringe valores invalidos | Permite navegar entre objetos |
| Ejemplo | `course_id = Column(ForeignKey("courses.id"))` | `course = relationship("Course")` |
| Lo necesitas? | Siempre, para crear el vinculo | Opcional, para facilitar el acceso |

**Sin `relationship()`:**
```python
# Tienes el ID, pero necesitas hacer otra query para obtener el objeto
course = db.query(Course).filter(Course.id == enrollment.course_id).first()
```

**Con `relationship()`:**
```python
# Un solo atributo te da el objeto completo
course = enrollment.course
```

---

## 3. ¿Que es `back_populates`?

**Respuesta corta:** Conecta dos `relationship()` para que sepan que son el mismo vinculo visto desde lados opuestos.

**Respuesta larga:** Cuando tienes una relacion bidireccional (Course ↔ Enrollment ↔ Student), necesitas que ambos lados sepan que estan conectados:

```python
class Course(Base):
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    course = relationship("Course", back_populates="enrollments")
```

**Sin `back_populates`:**
```python
course.enrollments  # funciona
enrollment.course   # devuelve None — no sabe que esta conectado
```

**Con `back_populates`:**
```python
course.enrollments  # funciona
enrollment.course   # funciona
```

**Analogia:** `back_populates` es como dos espejos enfrentados. Cada uno refleja al otro. Cuando agregas una inscripcion a un curso, ambos lados lo saben.

---

## 4. ¿Que diferencia hay entre `back_populates` y `backref`?

**Respuesta corta:** `backref` es la forma antigua y automatica. `back_populates` es la forma explicita y recomendada.

**Respuesta larga:**

```python
# Forma ANTIGUA (backref) — SQLAlchemy crea el otro lado automaticamente:
class Course(Base):
    enrollments = relationship("Enrollment", backref="course")

# Forma ACTUAL (back_populates) — debes declarar ambos lados explicitamente:
class Course(Base):
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    course = relationship("Course", back_populates="enrollments")
```

**¿Cual usar?** `back_populates` — es mas explicito, facil de depurar y recomendado por la documentacion actual.

---

## 5. ¿Que es lazy loading y eager loading?

**Respuesta corta:** Lazy = carga las relaciones solo cuando las necesitas. Eager = las carga automaticamente con la query principal.

**Respuesta larga:**

### Lazy loading (por defecto)

```python
course = db.query(Course).first()
# Aqui NO se ha consultado enrollments

for enrollment in course.enrollments:
    # Aqui se ejecuta: SELECT * FROM enrollments WHERE course_id = ?
    print(enrollment.student.name)
    # Y aqui otra: SELECT * FROM students WHERE id = ?
```

**Problema:** Si tienes 100 cursos con 10 estudiantes cada uno, haces 1 + 100 + 1000 = 1101 queries.

### Eager loading

```python
from sqlalchemy.orm import selectinload

course = db.query(Course).options(
    selectinload(Course.enrollments).selectinload(Enrollment.student)
).first()
# Solo 3 queries:
# 1. SELECT * FROM courses
# 2. SELECT * FROM enrollments WHERE course_id IN (...)
# 3. SELECT * FROM students WHERE id IN (...)
```

**Analogia:** Lazy loading es como ir al super y comprar solo lo que necesitas en cada visita (muchos viajes). Eager loading es hacer una sola compra grande con todo lo que necesitas.

---

## 6. ¿Que hace `selectinload()` y `joinedload()`?

**Respuesta corta:** Ambos cargan relaciones automaticamente (eager loading), pero usan estrategias SQL distintas.

**Respuesta larga:**

| Funcion | Como lo hace | Mejor para |
|---|---|---|
| `selectinload()` | Hace una segunda consulta con `WHERE id IN (...)` | Relaciones grandes, muchos registros |
| `joinedload()` | Hace un `LEFT JOIN` en la misma consulta | Relaciones pequenas, pocos registros |

```python
# selectinload: dos queries separadas
course = db.query(Course).options(
    selectinload(Course.enrollments)
).first()
# Query 1: SELECT * FROM courses
# Query 2: SELECT * FROM enrollments WHERE course_id IN (1, 2, 3)

# joinedload: un solo JOIN
course = db.query(Course).options(
    joinedload(Course.enrollments)
).first()
# Query: SELECT courses.*, enrollments.* FROM courses LEFT JOIN enrollments
```

**Recomendacion:** Usa `selectinload()` por defecto. Usa `joinedload()` solo cuando sepas que la relacion es 1:1 o muy pequena.

---

## 7. ¿Que es una tabla intermedia (association table)?

**Respuesta corta:** Una tabla que conecta dos tablas en una relacion Many-to-Many.

**Respuesta larga:** Cuando un Course puede tener muchos Students y un Student puede estar en muchos Courses, no puedes poner la FK en ninguna de las dos (porque necesitarias muchas FK). En su lugar, creas una tercera tabla:

```text
courses ──┐                ┌── students
          │                │
          └── enrollments ──┘
```

Cada fila en `enrollments` vincula UN course con UN student. Muchas filas = muchas relaciones.

**Analogia:** Es como el registro de asistencia. No pones la lista de cursos en la libreta del estudiante (no cabrian), ni la lista de estudiantes en el curso (no cabrian). Tienes una hoja aparte donde cada linea dice "estudiante X asistio al curso Y".

---

## 8. ¿Que es un cascade delete?

**Respuesta corta:** Una regla que dice "si eliminas el padre, elimina tambien los hijos".

**Respuesta larga:**

```python
class Enrollment(Base):
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
```

**Comportamiento:**
- Sin `CASCADE`: intentar eliminar un curso con inscripciones da `IntegrityError`.
- Con `CASCADE`: eliminas el curso, y SQLite elimina automaticamente todas sus inscripciones.

**Opciones de `ondelete`:**

| Opcion | Que hace |
|---|---|
| `NO ACTION` | (default) No hace nada. La BD puede o no rechazar segun configuracion |
| `RESTRICT` | Rechaza la eliminacion si hay hijos |
| `CASCADE` | Elimina los hijos automaticamente |
| `SET NULL` | Pone la FK en `NULL` en los hijos |

---

## 9. ¿Como hago una consulta Many-to-Many con SQLAlchemy?

**Respuesta corta:** Navegas a traves de la tabla intermedia usando `relationship()`.

**Respuesta larga:**

```python
# Obtener estudiantes de un curso:
course = db.query(Course).filter(Course.id == 1).first()
students = [e.student for e in course.enrollments]

# Obtener cursos de un estudiante:
student = db.query(Student).filter(Student.id == 1).first()
courses = [e.course for e in student.enrollments]

# Query directa con filtro:
results = (
    db.query(Student)
    .join(Enrollment)
    .join(Course)
    .filter(Course.name == "Fisica")
    .all()
)
```

---

## 10. ¿Que es el problema N+1 queries?

**Respuesta corta:** Hacer 1 query para obtener N registros + N queries para obtener sus relaciones.

**Respuesta larga:**

```python
courses = db.query(Course).all()  # 1 query → N cursos

for course in courses:
    print(course.enrollments)  # N queries adicionales (una por curso)
```

Si tienes 100 cursos, son 1 + 100 = 101 queries. Con 3 niveles de relacion, podrian ser miles.

**Solucion:** Usa `selectinload()` para cargar todo en 2-3 queries totales.

**Analogia:** Es como llamar a 100 personas por telefono para preguntarles su direccion (lazy) en lugar de pedir una lista con todas las direcciones de una vez (eager).

---

## 11. ¿Cuando debo usar `relationship()` vs hacer la query manual?

**Respuesta corta:** Usa `relationship()` para navegacion simple (obtener estudiantes de un curso). Usa query manual con JOIN para consultas complejas (promedio de notas por curso).

**Respuesta larga:**

```python
# CASO 1: Navegacion simple → relationship()
students = [e.student for e in course.enrollments]

# CASO 2: Consulta con agregacion → JOIN manual
results = (
    db.query(Course.name, func.avg(Enrollment.grade))
    .join(Enrollment)
    .group_by(Course.id)
    .all()
)
```

**Regla practica:**
- Si solo necesitas los objetos relacionados: `relationship()`.
- Si necesitas filtrar, ordenar o agregar datos: JOIN manual.

---

## 12. ¿Como evito el error `DetachedInstanceError` con relaciones?

**Respuesta corta:** Carga las relaciones con eager loading (`selectinload()`) antes de que la sesion se cierre.

**Respuesta larga:**

```python
# ❌ FALLARA: lazy loading despues de cerrar sesion
@router.get("/courses/{id}/students")
def get_students(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    # Aqui db aun esta abierta, pero...
    return course  # FastAPI convierte a JSON DESPUES de que db se cierra
    # course.enrollments se intenta cargar cuando la sesion ya no existe

# ✅ FUNCIONA: eager loading dentro de la sesion
@router.get("/courses/{id}/students")
def get_students(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).options(
        selectinload(Course.enrollments).selectinload(Enrollment.student)
    ).filter(Course.id == course_id).first()
    return course
```
