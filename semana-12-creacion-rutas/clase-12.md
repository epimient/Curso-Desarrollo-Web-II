# Clase 12 - Creacion y manejo de rutas

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 12  
**Unidad:** Unidad 3 - FastAPI Intermedio  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA4: Crear y configurar endpoints de una aplicacion web mediante la implementacion de rutas, controladores y manejo de solicitudes HTTP.
- RA5: Implementar la logica de negocio de una aplicacion web mediante el uso de patrones de diseno y buenas practicas de desarrollo.

## 2. Proposito de la clase

Esta clase busca que el estudiante domine la creacion y organizacion de rutas en FastAPI usando `APIRouter`. En la clase anterior vimos la estructura del proyecto y los conceptos基本. Ahora toca construir: crear endpoints que reciban peticiones, validen datos y retornen respuestas correctas.

El objetivo es que el estudiante pueda crear una API organizada con multiples rutas, usando path parameters, query parameters y HTTP methods de forma correcta.

## 3. Pregunta orientadora

**Como organizar las rutas de una API para que sea mantenible y escalable?**

Esta pregunta conecta con el problema real de tener todas las rutas en un solo archivo y querer escalar la API sin que se vuelva un caos.

## 4. APIRouter: organizacion de rutas

> **En espanol simple:** `APIRouter` es como una carpeta de archivos. En lugar de tener todas las rutas en un solo archivo, las organizas por categorias: una carpeta para cursos, otra para usuarios, otra para autenticacion.

En FastAPI, `APIRouter` permite dividir las rutas en modulos separados:

```python
# app/routers/courses.py
from fastapi import APIRouter

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/")
def list_courses():
    return [{"id": 1, "name": "FastAPI"}]

@router.get("/{course_id}")
def get_course(course_id: int):
    return {"id": course_id, "name": "FastAPI"}
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import courses

app = FastAPI()
app.include_router(courses.router)
```

**Beneficios:**
- Cada modulo tiene sus propias rutas
- Facil de encontrar y mantener
- Reutilizable entre proyectos
- Tags automaticos para Swagger

## 5. Path Parameters (parametros de ruta)

> **En espanol simple:** son datos que van directo en la URL. Como `/courses/5` - el `5` es un path parameter.

```python
@router.get("/{course_id}")
def get_course(course_id: int):
    # course_id es un entero que viene de la URL
    return {"id": course_id, "name": "FastAPI"}
```

**Reglas:**
- Se definen con `{nombre}`
- Se convierten al tipo indicado (int, str, float, etc.)
- Son obligatorios

## 6. Query Parameters (parametros de consulta)

> **En espanol simple:** son datos que van despues del `?` en la URL. Como `/courses?page=1&limit=10`.

```python
from typing import Optional

@router.get("/")
def list_courses(page: int = 1, limit: int = 10, search: Optional[str] = None):
    # page, limit y search son query parameters
    # Son opcionales si tienen valor por defecto
    return {"page": page, "limit": limit, "search": search}
```

**Reglas:**
- Se definen como argumentos de funcion con valores por defecto
- Son opcionales si tienen valor por defecto
- Sin valor por defecto = obligatorio

## 7. HTTP Methods

| Metodo | Uso | Ejemplo |
|--------|-----|---------|
| `GET` | Obtener datos | `GET /courses` |
| `POST` | Crear recurso | `POST /courses` |
| `PUT` | Actualizar recurso completo | `PUT /courses/5` |
| `PATCH` | Actualizar parcialmente | `PATCH /courses/5` |
| `DELETE` | Eliminar recurso | `DELETE /courses/5` |

```python
@router.get("/")
def list_courses():
    return []

@router.post("/", status_code=201)
def create_course(course: CourseCreate):
    return {"id": 1, **course.model_dump()}

@router.put("/{course_id}")
def update_course(course_id: int, course: CourseCreate):
    return {"id": course_id, **course.model_dump()}

@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: int):
    return None
```

## 8. Status Codes importantes

| Codigo | Significado | Uso |
|--------|-------------|-----|
| `200` | OK | GET exitoso, PUT exitoso |
| `201` | Created | POST exitoso |
| `204` | No Content | DELETE exitoso |
| `400` | Bad Request | Datos invalidos |
| `404` | Not Found | Recurso no encontrado |
| `422` | Unprocessable Entity | Error de validacion Pydantic |

## 9. Ejemplo completo: API de cursos

```python
# app/routers/courses.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.course import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["courses"])

# Base de datos simulada
courses_db = []
next_id = 1

@router.get("/", response_model=list[CourseResponse])
def list_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None
):
    results = courses_db
    if search:
        results = [c for c in results if search.lower() in c["name"].lower()]
    start = (page - 1) * limit
    return results[start:start + limit]

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int):
    course = next((c for c in courses_db if c["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course

@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate):
    global next_id
    new_course = {"id": next_id, **course.model_dump()}
    courses_db.append(new_course)
    next_id += 1
    return new_course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseCreate):
    existing = next((c for c in courses_db if c["id"] == course_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    existing.update(course.model_dump())
    return existing

@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: int):
    global courses_db
    courses_db = [c for c in courses_db if c["id"] != course_id]
    return None
```

## 10. En espanol simple: resumen

> Las rutas son como las "direcciones" de tu API. Cada ruta dice: "cuando alguien pida esto, haz esto otro". APIRouter te permite organizar esas direcciones por carpetas, como organizar archivos en un escritorio.

## 11. Ejercicio guiado

### Ejercicio 0: Verificacion rapida

```bash
python --version
pip --version
```

### Ejercicio 1: Crear router de usuarios

Crea un router para gestionar usuarios con las siguientes rutas:
- `GET /users/` - listar usuarios
- `GET /users/{user_id}` - obtener usuario por ID
- `POST /users/` - crear usuario
- `PUT /users/{user_id}` - actualizar usuario
- `DELETE /users/{user_id}` - eliminar usuario

### Ejercicio 2: Agregar paginacion

Modifica el endpoint `GET /users/` para incluir paginacion con query parameters:
- `page` (default: 1)
- `limit` (default: 10, max: 100)

### Ejercicio 3: Agregar busqueda

Agrega un query parameter `search` que filtre usuarios por nombre.

## 12. Preguntas frecuentes

**P: Cuantos routers puedo crear?**
R: Tantos como necesites. Cada recurso principal (cursos, usuarios, etc.) puede tener su propio router.

**P: Que pasa si dos routers tienen la misma ruta?**
R: FastAPI usa el ultimo router registrado. Evita duplicar rutas.

**P: Puedes anidar routers?**
R: FastAPI no soporta anidamiento directo, pero puedes usar prefijos para simularlo.

**P: Como pruebo las rutas?**
R: Usa Swagger UI (`/docs`) o herramientas como Postman/Thunder Client.

## 13. Material de estudio

- Clase 08: Estructura y organizacion de proyecto
- Clase 09: App basica con Pydantic
- Documentacion oficial: https://fastapi.tiangolo.com/tutorial/bigger-applications/
