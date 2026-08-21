# Ejercicios - Clase 07

> **Nota:** El ejercicio 0 es de calentamiento. Los ejercicios 1-5 construyen progresivamente sobre el refactor a BD.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las frases con las palabras del recuadro:

> **Palabras:** ENGINE | SESSION | COMMIT | QUERY | FILTER | ADD | REFRESH | DEPENDS

1. El _________ es el puente entre Python y la base de datos.
2. `SessionLocal()` crea una _________ nueva para cada request.
3. Sin _________, los cambios en la BD no se guardan.
4. `db.`_________(Course).all() equivale a `SELECT * FROM courses`.
5. `.`_________(Course.id == 1) equivale a `WHERE id = 1`.
6. `db.`_________(course) prepara un INSERT de un objeto.
7. `db.`_________(course) vuelve a leer el objeto de la BD para obtener el id generado.
8. `db: Session =` _________`(get_db)` inyecta la sesion en el endpoint.

---

## Ejercicio 1. Escribir `database.py`

Sin mirar el ejemplo guiado, escribe el contenido completo de `app/database.py` que debe incluir:

1. `create_engine` con `settings.database_url`
2. `SessionLocal` usando `sessionmaker`
3. Clase `Base` usando `DeclarativeBase`
4. Funcion `get_db()` que crea, entrega y cierra una sesion

---

## Ejercicio 2. Definir modelo Student

Crea `app/models/student.py` con la clase `Student` que tenga:

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | Integer | primary_key, index |
| `name` | String(100) | not null |
| `email` | String(100) | not null |
| `active` | Boolean | default=True |

**Ademas:** Crea el schema Pydantic `StudentResponse` con `from_attributes=True` en `app/schemas/student.py`.

---

## Ejercicio 3. Refactor: migrar modulo users a BD

Partiendo del modulo `users` que creaste en el desafio de Clase 05, refactoriza `app/services/user_service.py` para que use la BD en lugar de una lista en memoria.

Debes:

1. Crear el modelo `User` en `app/models/user.py`
2. Crear el schema `UserResponse` con `from_attributes=True`
3. Refactorizar `user_service.py` para usar `db.query()`, `db.add()`, `db.commit()`
4. Actualizar `routers/users.py` para usar `Depends(get_db)`

**Verificacion desde Swagger UI:**

1. Abre `http://localhost:8000/docs`
2. Busca el grupo correspondiente al recurso (ej: Users)
3. Haz clic en `POST /users/` → "Try it out"
4. En el campo Request body, ingresa:
   ```json
   {"name": "Ana", "email": "ana@mail.com"}
   ```
5. Haz clic en "Execute" → debe devolver 201 Created con los datos del usuario
6. Haz clic en `GET /users/` → "Try it out" → "Execute"
   → Debe mostrar el usuario creado
7. Reinicia el servidor (`Ctrl+C` y `uvicorn` de nuevo)
8. Repite el paso 6 → el usuario debe seguir existiendo

---

## Ejercicio 4. Depurar errores

Para cada error, identifica la causa y escribe la solucion:

**Error A:**
```text
sqlite3.OperationalError: no such table: courses
```

**Preguntas:**
- ¿Que falta en `main.py`?
- ¿Que linea solucionaria esto?

**Error B:**
```text
AttributeError: 'dict' object has no attribute 'name'
```

**Contexto:** El servicio devuelve `course` como diccionario en lugar de objeto SQLAlchemy.

**Preguntas:**
- ¿Que tipo de objeto deberia devolver `db.query().first()`?
- ¿Por que el codigo esta devolviendo un dict?

**Error C:**
```python
# Codigo:
course = Course(name="Fisica", credits=4, active=True)
db.add(course)
return course
# Al reiniciar, el curso NO existe
```

**Pregunta:**
- ¿Que linea falta entre `db.add(course)` y `return course`?

**Error D:**
```text
sqlite3.IntegrityError: NOT NULL constraint failed: courses.name
```

**Pregunta:**
- ¿Por que ocurre este error si el schema Pydantic valida que `name` no este vacio?
- (Pista: la validacion Pydantic ocurre en el router, no en el servicio)

---

## Ejercicio 5. Consultas con filtros

Dado el modelo `Course`, escribe las funciones en `course_service.py` para:

```python
def get_active_courses(db: Session) -> list[Course]:
    """Retorna solo cursos con active=True"""
    # tu codigo aqui


def search_courses_by_name(query: str, db: Session) -> list[Course]:
    """Retorna cursos cuyo nombre contenga 'query' (busqueda parcial, case insensitive)"""
    # Pista: usa .ilike(f"%{query}%")


def count_courses(db: Session) -> int:
    """Retorna la cantidad total de cursos"""
    # Pista: usa db.query().count()


def update_course_active(course_id: int, active: bool, db: Session) -> Course:
    """Actualiza el estado active de un curso y lo retorna"""
    # Pista: busca el curso, modifica el atributo, haz commit, refresh
```

---

## Desafio extra (opcional)

Crea un modelo `Enrollment` que relacione `Course` con `Student`:

```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.now)
    grade = Column(Integer, nullable=True)  # nota opcional
```

**Luego crea:**

1. `app/schemas/enrollment.py` con `EnrollmentCreate` (course_id, student_id) y `EnrollmentResponse`
2. `app/routers/enrollments.py` con `POST /enrollments` y `GET /enrollments`
3. Registrar el router en `main.py`

**Verificacion:**

```bash
# Crear estudiante
POST /students {"name": "Ana", "email": "ana@mail.com"}
# Crear curso
POST /courses {"name": "Fisica", "credits": 4}
# Inscribir estudiante
POST /enrollments {"course_id": 1, "student_id": 1}
# Listar inscripciones
GET /enrollments
```
