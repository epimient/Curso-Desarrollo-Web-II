# Preguntas Frecuentes — Clase 13: Proyecto Integrador

## 1. ¿Por qué usar Enum en lugar de string para el status?

**Pregunta:** En el modelo Enrollment usamos `Enum` para el status. ¿Por qué no usar un string simple?

**Respuesta:** `Enum` evita errores tipográficos y datos inválidos. Si usas string, podrías guardar `"enroled"`, `"completd"`, etc. Con `Enum`, solo los valores definidos son válidos. Además, Swagger UI muestra las opciones como un dropdown, no como un campo de texto libre.

---

## 2. ¿Cómo manejar la migración de la base de datos?

**Pregunta:** Ya tengo datos en SQLite. Si agrego la tabla `enrollments`, ¿pierdo los datos existentes?

**Respuesta:** SQLAlchemy con `Base.metadata.create_all()` solo crea tablas que **no existen**. Tus tablas `users` y `courses` existentes no se modifican. La tabla `enrollments` se crea nueva. No pierdes datos.

Si necesitas cambios destructivos (renombrar columnas, cambiar tipos), necesitas Alembic (migraciones).

---

## 3. ¿Por qué mis tests no encuentran la tabla enrollments?

**Pregunta:** Ejecuto pytest y me sale `sqlalchemy.exc.ProgrammingError: (sqlite3.OperationalError) no such table: enrollments`.

**Respuesta:** Asegúrate de que:

1. El modelo `Enrollment` está importado en algún lado (idealmente en `app/models/__init__.py`)
2. El conftest.py importa `app.models` para que SQLAlchemy registre todas las tablas
3. La base de datos de test se crea antes de cada test

En `conftest.py`:

```python
from app.models import Enrollment  # ← obligatorio para registrar la tabla
```

---

## 4. ¿Cómo asegurar que un estudiante no se inscribe dos veces?

**Pregunta:** Implementé el check de duplicados pero aún puedo inscribir al mismo estudiante en el mismo curso.

**Respuesta:** Revisa que tu consulta filtre correctamente:

```python
existing = db.query(Enrollment).filter(
    Enrollment.student_id == data.student_id,
    Enrollment.course_id == data.course_id,
    Enrollment.status != EnrollmentStatus.cancelled,
).first()
```

El filtro `status != cancelled` permite reinscribir si la matrícula anterior fue cancelada. Si quieres evitar reinscripción total (incluso después de cancelada), quita ese filtro.

---

## 5. PUT vs PATCH — ¿cuál usar?

**Pregunta:** ¿Cuándo uso PUT y cuándo PATCH?

**Respuesta:**

| PUT | PATCH |
|-----|-------|
| Reemplaza el recurso completo | Actualización parcial |
| Envías **todos** los campos | Envías **solo** los campos a cambiar |
| Si omitas un campo, se pone en `null` | Si omites un campo, no se modifica |
| Idempotente (misma llamada = mismo resultado) | Puede no ser idempotente |

**Regla general:** Usa PUT para `CourseUpdate` (todos los campos) y PATCH para `EnrollmentUpdate` (solo nota o solo status).

---

## 6. ¿Cómo probar la paginación en Swagger?

**Pregunta:** Swagger no tiene campo para `page` y `per_page`.

**Respuesta:** Swagger UI muestra los query parameters automáticamente si los declaras como parámetros de la función:

```python
@router.get("/")
def list_courses(page: int = 1, per_page: int = 10, ...):
```

Aparecerán en Swagger como campos de texto en la sección "Parameters". Si no aparecen, verifica que tu función tenga type hints (`int`).
