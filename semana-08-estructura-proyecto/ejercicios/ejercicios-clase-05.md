# Ejercicios - Clase 05

> **Nota:** El ejercicio 0 es de calentamiento para asegurarnos de que los conceptos basicos estan claros antes de empezar a codificar.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las frases con las palabras del recuadro:

> **Palabras:** ROUTER | SCHEMA | SERVICE | CORE | MAIN.PY | INCLUDE_ROUTER | APIRouter | INIT

1. El archivo _________ es el punto de entrada de la aplicacion FastAPI.
2. _________ es la funcion que conecta un router a la aplicacion.
3. La carpeta _________ contiene la configuracion general (nombre, version, entorno).
4. Un _________ es un "mini-FastAPI" que agrupa endpoints relacionados.
5. La carpeta _________ contiene los modelos Pydantic para validar entrada y salida.
6. La carpeta _________ contiene la logica de negocio (reglas, validaciones, operaciones).
7. La clase _________ se usa para crear un grupo de rutas con un prefijo comun.
8. Cada carpeta dentro de `app/` debe tener un archivo `___`.py para que Python la reconozca como paquete.

---

## Ejercicio 1. Clasificar archivos

Indique en que carpeta ubicaria cada archivo o responsabilidad:

| Archivo o responsabilidad | Carpeta sugerida |
|---|---|
| Configuracion de nombre y version de la app | |
| Endpoints de cursos | |
| Modelo Pydantic `CourseCreate` | |
| Funcion que valida si un curso ya existe | |
| Endpoint `/health` | |
| Conexion futura a base de datos | |

> **Pista:** Revisa la seccion 5 de la clase. Las carpetas disponibles son: `core/`, `routers/`, `schemas/`, `services/`.

---

## Ejercicio 2. Refactor de `main.py`

Parta del proyecto de la Clase 04 (donde todos los endpoints estaban en `main.py`).

Debe crear los siguientes archivos vacios con la estructura correcta:

- `app/core/config.py`
- `app/routers/health.py`
- `app/routers/courses.py`
- `app/schemas/course.py`
- `app/services/course_service.py`

Luego registre los routers en `main.py` usando:

```python
app.include_router(health.router)
app.include_router(courses.router)
```

**Verificacion:** Al ejecutar `uvicorn app.main:app --reload` y abrir `/docs`, deben aparecer todos los endpoints.

---

## Ejercicio 3. Endpoint de salud

Cree un endpoint en `app/routers/health.py`:

```http
GET /health
```

Respuesta esperada:

```json
{
  "status": "ok"
}
```

> **Pista:** Usa `APIRouter(prefix="/health", tags=["Health"])`.

---

## Ejercicio 4. Endpoint de version

Agregue al mismo `app/routers/health.py`:

```http
GET /health/version
```

Respuesta esperada:

```json
{
  "name": "API academica",
  "version": "0.1.0",
  "environment": "development"
}
```

> **Pista:** Importa `settings` desde `app.core.config` para obtener `app_name`, `app_version` y `environment`.

---

## Ejercicio 5. Router de cursos

Implemente en `app/routers/courses.py`:

```http
GET /courses          → lista todos los cursos
POST /courses         → crea un curso (status 201)
GET /courses/{id}     → busca curso por ID
```

Use:

- **Schemas:** `CourseCreate` (entrada) y `CourseResponse` (salida) en `app/schemas/course.py`
- **Servicios:** `list_courses()`, `get_course()`, `create_course()` en `app/services/course_service.py`
- **Datos:** lista en memoria con un curso inicial

**Pruebas esperadas:**

| Accion | URL | Respuesta esperada |
|---|---|---|
| Listar cursos | `GET /courses` | Lista con al menos 1 curso |
| Crear curso | `POST /courses` con `{"name": "Nuevo", "credits": 4}` | Status 201, curso creado con `id=2` |
| Buscar id=1 | `GET /courses/1` | Curso con `name="Desarrollo Web II"` |
| Buscar id=999 | `GET /courses/999` | Status 404 |

---

## Ejercicio 6. README tecnico

Actualice el README del proyecto con:

- descripcion del proyecto;
- estructura de carpetas (puedes usar tree o un bloque de texto);
- instrucciones de instalacion y ejecucion;
- lista de endpoints;
- decisiones de arquitectura (por que separar en routers, schemas, services).

**Formato sugerido:**

```markdown
# [Nombre del proyecto]

## Descripcion
...

## Estructura
...
```

---

## Ejercicio 7. Reflexion

Responda:

**¿Que problema aparece si cada integrante del equipo agrega endpoints directamente en `main.py` sin organizar routers?**

Incluya al menos dos consecuencias tecnicas y una consecuencia para el trabajo en equipo.

**Pistas:**
- Piensa en conflictos de Git (merge conflicts).
- Piensa en la legibilidad del codigo.
- Piensa en como probar un endpoint sin romper otro.

---

## Desafio extra (opcional)

Crea un nuevo modulo completo: **`users`**.

Debes crear:

1. `app/schemas/user.py` — `UserCreate` (name, email) y `UserResponse` (id, name, email, active)
2. `app/services/user_service.py` — funciones `list_users()`, `get_user()`, `create_user()`
3. `app/routers/users.py` — endpoints `GET /users`, `POST /users`, `GET /users/{user_id}`
4. Registrar el router en `main.py`

**Verificacion:** `GET /users` debe retornar una lista vacia (aun no hay usuarios creados).
