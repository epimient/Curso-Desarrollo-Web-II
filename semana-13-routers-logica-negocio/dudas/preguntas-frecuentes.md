# Dudas frecuentes - Clase 07

> Aqui encontraras las preguntas mas comunes sobre SQLAlchemy y persistencia de datos en FastAPI.

---

## 1. ¿Que es un ORM?

**Respuesta corta:** Un ORM te permite trabajar con la base de datos usando objetos de Python en lugar de escribir SQL.

**Respuesta larga:** ORM = Object-Relational Mapper. Traduce entre dos mundos:

| Mundo SQL | Mundo ORM (Python) |
|---|---|
| Tabla `courses` | Clase `Course` |
| Fila con id=1, name="Fisica" | `course = Course(name="Fisica")` |
| `SELECT * FROM courses` | `db.query(Course).all()` |
| `INSERT INTO courses VALUES (...)` | `db.add(course)` + `db.commit()` |

Tu escribes Python, SQLAlchemy escribe SQL por ti.

**Analogia:** Un ORM es como un traductor simultaneo. Tu hablas en Python, el le habla a la BD en SQL, y te devuelve la respuesta en Python. Tu nunca necesitas aprender SQL (aunque ayuda saberlo).

---

## 2. ¿SQLAlchemy reemplaza a SQL?

**Respuesta corta:** No, lo abstrae. SQL sigue ejecutandose, pero tu no lo escribes.

**Respuesta larga:** SQLAlchemy NO elimina SQL. Lo genera automaticamente. Cuando haces `db.query(Course).filter(Course.id == 1).first()`, SQLAlchemy genera y ejecuta:

```sql
SELECT courses.id, courses.name, courses.credits, courses.active
FROM courses
WHERE courses.id = 1
```

Saber SQL te ayuda a entender que esta pasando "bajo el capo", pero no es necesario para usar SQLAlchemy.

---

## 3. ¿Que es una sesion (`Session`) y por que necesito una por request?

**Respuesta corta:** Una sesion es una conversacion con la BD. Cada request obtiene su propia sesion.

**Respuesta larga:** `Session` es el objeto que usas para hacer queries y guardar cambios. Es como un "bloc de notas" donde anotas las operaciones pendientes. Cuando haces `db.commit()`, todas las operaciones se ejecutan a la vez.

**Cada request necesita su propia sesion porque:**
- Si dos requests compartieran la misma sesion, sus cambios se mezclarian.
- Si un request falla, solo cierra su sesion sin afectar a otros.
- Facilita el manejo de errores (cada sesion se cierra individualmente).

**Analogia:** Es como el ticket de turno en un banco. Cada cliente recibe su propio numero. Cuando le toca, es atentido. Cuando termina, su ticket ya no sirve.

---

## 4. ¿Que es `Depends(get_db)` y como funciona?

**Respuesta corta:** Es la forma en que FastAPI inyecta la sesion de BD en un endpoint.

**Respuesta larga:** `Depends()` le dice a FastAPI: "antes de ejecutar este endpoint, ejecuta `get_db()` y pasame el resultado". El flujo es:

1. Llega una request a `GET /courses`
2. FastAPI ve `db: Session = Depends(get_db)`
3. FastAPI ejecuta `get_db()`:
   - Abre una sesion (`SessionLocal()`)
   - Entrega la sesion con `yield db`
4. FastAPI pasa `db` al endpoint
5. El endpoint ejecuta su logica con `db`
6. El endpoint termina, FastAPI continua en `get_db()`
7. Se ejecuta `finally: db.close()` → sesion cerrada

---

## 5. ¿Que hace `from_attributes=True` en Pydantic?

**Respuesta corta:** Permite crear un Pydantic model desde un objeto SQLAlchemy, no solo desde un diccionario.

**Respuesta larga:** Por defecto, Pydantic solo puede crear instancias desde diccionarios:

```python
# Esto funciona siempre:
course = CourseResponse(**{"id": 1, "name": "Fisica", "credits": 4, "active": True})

# Sin from_attributes, esto FALLA:
course_sqlalchemy = Course(id=1, name="Fisica", credits=4, active=True)
course = CourseResponse.model_validate(course_sqlalchemy)
# → Error: Input should be a valid dictionary

# Con from_attributes=True, esto FUNCIONA:
course = CourseResponse.model_validate(course_sqlalchemy)
```

**Analogia:** `from_attributes=True` es como decirle a Pydantic "puedes leer los datos de un objeto con atributos (course.name), no solo de un diccionario ({"name": ...})".

---

## 6. ¿Cuando usar `db.commit()` vs `db.flush()`?

**Respuesta corta:** `commit()` guarda permanentemente. `flush()` envia a la BD pero permite deshacer.

**Respuesta larga:**

| Operacion | Que hace |
|---|---|
| `db.add(course)` | Agrega a la sesion (aun no se envia nada a la BD) |
| `db.flush()` | Envia el INSERT a la BD, pero NO confirma. Se puede deshacer con `rollback()` |
| `db.commit()` | Envia y CONFIRMA. Los cambios son permanentes |
| `db.rollback()` | Deshace todos los cambios desde el ultimo `commit()` |

**Regla practica:** Usa SIEMPRE `db.commit()`. `flush()` es para casos avanzados (cuando necesitas el `id` generado antes de hacer otro INSERT, pero aun no quieres confirmar).

---

## 7. ¿Que es `DetachedInstanceError`?

**Respuesta corta:** Ocurre cuando intentas usar un objeto SQLAlchemy DESPUES de que la sesion que lo creo se cerro.

**Respuesta larga:**

```python
def get_course(course_id: int, db: Session) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    # db esta activa aqui
    return course
    # Cuando el endpoint termina, db.close() se ejecuta

# Fuera del endpoint:
course = get_course(1, db)
print(course.name)  # ❌ DetachedInstanceError si la sesion ya se cerro
```

**Solucion:** Convierte el objeto SQLAlchemy a Pydantic MIENTRAS la sesion esta abierta:

```python
# En el router:
return get_course(course_id, db)
# FastAPI convierte automaticamente a CourseResponse (con from_attributes)
# Esto ocurre ANTES de que db.close() se ejecute
```

---

## 8. ¿Que es `IntegrityError`?

**Respuesta corta:** Ocurre cuando intentas violar una regla de la BD (ej: duplicado, campo nulo prohibido).

**Respuesta larga:** Ejemplos comunes:

| Causa | Ejemplo |
|---|---|
| `NOT NULL` | Guardar un `Course` sin `name` |
| `UNIQUE` | Dos cursos con el mismo valor en una columna que deberia ser unica |
| `FOREIGN KEY` | Crear un `Enrollment` con `course_id=999` cuando ese curso no existe |

**Solucion:** Revisa el mensaje de error. Te dice exactamente que restriccion se violo:

```text
sqlite3.IntegrityError: NOT NULL constraint failed: courses.name
               ↑                                    ↑
         tipo de error                       columna afectada
```

---

## 9. ¿SQLite vs PostgreSQL — cual elijo?

**Respuesta corta:** SQLite para desarrollo, PostgreSQL para produccion.

**Respuesta larga:**

| Aspecto | SQLite | PostgreSQL |
|---|---|---|
| ¿Que es? | Un archivo `.db` | Un servidor |
| Instalacion | No requiere nada | `apt install postgresql` |
| URL tipica | `sqlite:///./data.db` | `postgresql://user:pass@localhost/db` |
| Velocidad | Rapida para un usuario | Optimizada para muchos usuarios |
| Concurrente | Limitado | Excelente |
| ¿Para que usarlo? | Desarrollo, pruebas, prototipos | Produccion, equipos, escalar |

**Cambiar de SQLite a PostgreSQL:** Solo cambias UNA linea en `config.py`:

```python
database_url: str = "postgresql://usuario:password@localhost:5432/mi_db"
```

---

## 10. ¿Que es Alembic y para que sirve?

**Respuesta corta:** Es una herramienta para gestionar cambios en la estructura de la BD (migraciones).

**Respuesta larga:** Cuando tu proyecto evoluciona, a veces necesitas cambiar las tablas:

- Agregar una columna (`description`)
- Cambiar un tipo (`name` de 80 a 200 caracteres)
- Agregar una tabla nueva (`enrollments`)

Alembic genera automaticamente el SQL necesario y lo ejecuta sin perder datos.

```bash
# Inicializar Alembic (solo una vez):
alembic init alembic

# Detectar cambios en los modelos y generar migracion:
alembic revision --autogenerate -m "add description to courses"

# Aplicar la migracion:
alembic upgrade head
```

**Analogia:** Alembic es como Git para tu base de datos. Cada migracion es un commit. Puedes ir hacia adelante (`upgrade`) o atras (`downgrade`).

---

## 11. ¿Cada request abre una conexion nueva a la BD?

**Respuesta corta:** No exactamente. SQLAlchemy usa un pool de conexiones.

**Respuesta larga:** Cuando haces `SessionLocal()`, SQLAlchemy no abre una conexion nueva cada vez. Mantiene un **pool** de conexiones reutilizables.

```text
Request 1 → toma conexion del pool → la usa → la devuelve al pool
Request 2 → toma conexion del pool → la usa → la devuelve al pool
Request 3 → toma conexion del pool → la usa → la devuelve al pool
```

Si todas las conexiones del pool estan ocupadas, la request espera a que una se libere. Esto es eficiente y evita saturar la BD.

---

## 12. ¿Por que mi modelo SQLAlchemy no tiene `id` despues de crearlo?

**Respuesta corta:** Porque el `id` lo genera la BD al hacer `commit()`. Necesitas `refresh()` para obtenerlo.

**Respuesta larga:**

```python
course = Course(name="Fisica", credits=4)
print(course.id)   # None — aun no se guardo

db.add(course)
print(course.id)   # None — aun no se ejecuto el INSERT

db.commit()
print(course.id)   # None — el INSERT se ejecuto, pero el objeto aun no se actualizo

db.refresh(course)
print(course.id)   # 1 — ahora el objeto refleja lo que hay en la BD
```

**Flujo correcto siempre:**
```python
db.add(course)
db.commit()
db.refresh(course)
return course
```
