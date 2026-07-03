# Clase 05 - Estructura profesional de un proyecto FastAPI

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 5  
**Unidad:** Unidad 2 - Uso de un Framework Especifico  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA1: Comprender los conceptos fundamentales del patron MVC y los frameworks de desarrollo de software mediante la identificacion de sus componentes y su interaccion.
- RA3: Desarrollar habilidades para la creacion y manejo de rutas y controladores dentro del framework mediante la implementacion de logica de negocio en controladores o equivalentes pedagogicos.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

Esta clase busca que el estudiante transforme una API minima en un proyecto organizado, modular y preparado para crecer. En la Clase 04 se creo una aplicacion basica con endpoints en `main.py`. Esa estructura sirve para iniciar, pero no es suficiente cuando el proyecto incorpora mas recursos, validaciones, reglas de negocio, configuracion, pruebas, seguridad y persistencia.

La meta es comprender como dividir responsabilidades en carpetas y modulos:

- `main.py` como punto de entrada.
- `routers/` para rutas agrupadas por recurso.
- `schemas/` para contratos de entrada y salida.
- `services/` para logica de negocio.
- `core/` para configuracion general.
- `tests/` como destino natural de pruebas.

La clase no pretende imponer una unica estructura universal. Pretende formar criterio. En FastAPI hay libertad, y la libertad sin estructura a veces se parece demasiado a una carpeta llamada `varios_final_final_ahora_si`.

## 3. Pregunta orientadora

**Como organizamos un proyecto FastAPI para que pueda crecer sin volverse inmantenible?**

Esta pregunta conecta con MVC, separacion de responsabilidades y buenas practicas de desarrollo profesional.

---

> **En español simple:** Pasar de tener TODO en `main.py` a tener carpetas separadas es como pasar de vivir en un estudio de 20m² donde cocinas, duermes y trabajas en el mismo espacio, a un departamento con cocina, sala y cuarto separados. Todo funciona igual, pero es mas facil encontrar las cosas, trabajar con alguien mas y ampliarlo sin romperlo.

---

## 4. Por que estructurar un proyecto

Una estructura profesional ayuda a:

- ubicar rapidamente archivos;
- separar responsabilidades;
- facilitar trabajo en equipo;
- reducir conflictos de edicion;
- mejorar pruebas;
- permitir crecimiento progresivo;
- preparar persistencia, seguridad y despliegue;
- evitar que `main.py` se convierta en pergamino infinito.

Un proyecto pequeno puede vivir con un solo archivo. Un proyecto de curso, con varias semanas de evolucion, necesita algo mas ordenado.

## 5. Estructura propuesta para el curso

Estructura base:

```text
app/
  __init__.py
  main.py
  core/
    __init__.py
    config.py
  routers/
    __init__.py
    health.py
    courses.py
  schemas/
    __init__.py
    course.py
  services/
    __init__.py
    course_service.py
requirements.txt
README.md
```

Esta estructura es suficiente para empezar a construir de forma modular sin caer en arquitectura excesiva.

> **Analogia del edificio de oficinas:** Imagina que tu API es un edificio.
> - **`main.py`** es la recepcionista que te da la bienvenida y te dirige al piso correcto.
> - **`routers/`** son los pisos del edificio. Piso 1 = Salud, Piso 2 = Cursos, Piso 3 = Usuarios.
> - **`services/`** son las oficinas internas donde realmente se hace el trabajo (cocina, contabilidad, operaciones).
> - **`schemas/`** son los formularios que llenas para pedir algo (solicitud de curso, reporte de notas).
> - **`core/`** es el manual del edificio: datos estaticos como nombre, version, reglas generales.
>
> Sin esta organizacion, todo estaria amontonado en la recepcion. Literalmente la sala de espera seria tambien la cocina, la contabilidad y el bano.

## 6. Responsabilidades por carpeta

### 6.1 `app/main.py`

Es el punto de entrada de la API. Debe encargarse de:

- crear la instancia de `FastAPI`;
- registrar routers;
- configurar metadatos generales;
- registrar middleware cuando corresponda;
- mantener limpia la composicion principal de la aplicacion.

Ejemplo:

```python
from fastapi import FastAPI

from app.core.config import settings
from app.routers import courses, health

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health.router)
app.include_router(courses.router)
```

**Desglose linea por linea:**

| Linea | Que hace |
|---|---|
| `from fastapi import FastAPI` | Importa la clase `FastAPI` del framework |
| `from app.core.config import settings` | Trae la configuracion desde `app/core/config.py` |
| `from app.routers import courses, health` | Importa los modulos `courses` y `health` de la carpeta `routers/` |
| `app = FastAPI(...)` | Crea la **instancia** de FastAPI con nombre y version |
| `title=settings.app_name` | Toma el nombre desde la configuracion centralizada |
| `version=settings.app_version` | Toma la version desde la configuracion centralizada |
| `app.include_router(health.router)` | **Registra** el router de salud para que FastAPI reconozca sus rutas |
| `app.include_router(courses.router)` | **Registra** el router de cursos para que FastAPI reconozca sus rutas |

> **Pregunta frecuente:** `main.py` no deberia contener toda la logica de negocio. Si empieza a medir mas que el syllabus, hay que intervenir.

### 6.2 `app/core/`

> **En español simple:** `core/` es como la placa de identificacion de la API. Guarda datos que no cambian seguido: el nombre del proyecto, la version, si estamos en desarrollo o produccion.

Contiene configuracion general y elementos transversales.

Ejemplos:

- nombre de la aplicacion;
- version;
- entorno;
- configuracion de CORS;
- variables de entorno;
- parametros de seguridad.

Para esta clase se usara una configuracion simple:

```python
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"


settings = Settings()
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `class Settings(BaseModel):` | Define una clase que hereda de `BaseModel` (Pydantic) |
| `app_name: str = "..."` | Campo con tipo `str` y valor por defecto |
| `settings = Settings()` | Crea una **instancia unica** de la configuracion lista para usar |

Mas adelante, esta configuracion puede evolucionar hacia variables de entorno con `pydantic-settings`.

### 6.3 `app/routers/`

> **En español simple:** Un router es un archivo que agrupa endpoints relacionados. Es como tener un archivador para cada departamento: uno para salud, otro para cursos, otro para usuarios.

Contiene rutas agrupadas por recurso o modulo.

Ejemplos:

- `health.py` para estado de la API;
- `courses.py` para cursos;
- `users.py` para usuarios;
- `auth.py` para autenticacion.

Un router debe:

- declarar rutas;
- recibir parametros;
- definir modelos de respuesta;
- invocar servicios;
- devolver resultados.

No debe convertirse en deposito de reglas de negocio.

> **Asi NO ❌ vs Asi SI ✅**
>
> **Router gordo (MAL):**
> ```python
> @router.post("/")
> def create_course(course: dict):
>     # validaciones, busquedas, reglas, persistencia...
>     if not course.get("name"):
>         return {"error": "name required"}
>     if len(course["name"]) < 3:
>         return {"error": "name too short"}
>     # 30 lineas mas de logica...
> ```
>
> **Router delgado (BIEN):**
> ```python
> @router.post("/", response_model=CourseResponse)
> def create_course_endpoint(course: CourseCreate):
>     return create_course(course)
> ```
> El router solo **coordina**. El servicio **decide**.

### 6.4 `app/schemas/`

> **En español simple:** Los schemas son los formularios de tu API. `CourseCreate` es el formulario de inscripcion (que datos necesitas para crear un curso). `CourseResponse` es el carnet que te llevas (que datos devuelve la API).

Contiene modelos Pydantic para contratos de datos.

Tipos frecuentes:

- `CourseCreate`: datos para crear.
- `CourseUpdate`: datos para actualizar.
- `CourseResponse`: datos que se devuelven.

**Analogia:** Imagina que pides una pizza.
- **CourseCreate** = el formulario que llenas ("pizza mediana, extra queso, sin cebolla").
- **CourseResponse** = el ticket que recibes ("Pizza mediana, Queso extra, SIN Cebolla — $12.500").

El formulario de pedido (Create) y el ticket de confirmacion (Response) NO son el mismo papel, aunque contengan datos parecidos.

Separar schemas evita errores como devolver informacion sensible o exigir campos que solo deberian existir internamente.

### 6.5 `app/services/`

> **En español simple:** El servicio es el cocinero. El router es el mesero. El mesero te toma la orden (router recibe la peticion), se la pasa al cocinero (service procesa la logica), y el cocinero devuelve el plato terminado (service retorna el resultado) que el mesero te entrega (router responde al cliente).

Contiene logica de negocio.

Responsabilidades:

- aplicar reglas;
- coordinar operaciones;
- gestionar almacenamiento temporal o repositorios;
- lanzar errores controlados;
- facilitar pruebas.

Ejemplo:

```python
def create_course(course: CourseCreate) -> CourseResponse:
    if course_name_exists(course.name):
        raise HTTPException(status_code=400, detail="Course already exists")
    ...
```

Los servicios permiten que los routers sean delgados. Router delgado, servicio claro, proyecto menos enredado.

## 7. Endpoints de salud y version

Un proyecto profesional suele incluir endpoints simples para verificar estado.

> **En español simple:** Los endpoints de salud son como el "check engine" del auto. Cuando la API esta en produccion, el equipo de operaciones necesita saber si el sistema esta vivo y que version esta corriendo.

### 7.1 Health check

```http
GET /health
```

Respuesta:

```json
{
  "status": "ok"
}
```

Sirve para confirmar que la API esta viva.

### 7.2 Version

```http
GET /health/version
```

Respuesta:

```json
{
  "name": "API academica",
  "version": "0.1.0",
  "environment": "development"
}
```

Sirve para diagnostico, despliegue y soporte.

## 8. Rutas por recurso: ejemplo con cursos

Recurso: `Course`

Campos:

- `id`
- `name`
- `credits`
- `active`

Endpoints iniciales:

```http
GET /courses
POST /courses
GET /courses/{course_id}
```

La ruta `GET /courses` lista cursos.  
La ruta `POST /courses` crea un curso.  
La ruta `GET /courses/{course_id}` consulta un curso por identificador.

**Tabla de flujo completo para cada endpoint:**

| Endpoint | Que hace | Router donde vive | Schema que valida | Servicio que ejecuta |
|---|---|---|---|---|
| `GET /courses` | Lista todos los cursos | `routers/courses.py` | `CourseResponse` (salida) | `course_service.list_courses()` |
| `POST /courses` | Crea un curso nuevo | `routers/courses.py` | `CourseCreate` (entrada) | `course_service.create_course()` |
| `GET /courses/{id}` | Busca un curso por ID | `routers/courses.py` | `CourseResponse` (salida) | `course_service.get_course()` |

**Diagrama visual del flujo:**

```
Cliente (navegador / Swagger UI)
    │
    ▼
main.py ──recibe la peticion──
    │                         │
    ▼                         ▼
routers/courses.py     routers/health.py
    │                         │
    ▼                         ▼
services/               core/config.py
course_service.py       (datos estaticos)
    │
    ▼
schemas/course.py
(validacion ent/sal)
    │
    ▼
Respuesta JSON al cliente
```

## 9. Versionado de API

> **En español simple:** Versionar una API es como ponerle numeros a las recetas de cocina. La receta v1.0 es la original. Si la mejoras, sacas v1.1. Si cambias algo que rompe la receta anterior, sacas v2.0. Asi los clientes viejos siguen usando v1 mientras los nuevos usan v2.

El versionado permite evolucionar una API sin romper clientes existentes.

Dos estrategias comunes:

### 9.1 Version en la ruta

```text
/api/v1/courses
```

Ventaja: visible y facil de consumir.

### 9.2 Version en headers

```text
Accept: application/vnd.api.v1+json
```

Ventaja: ruta mas limpia, pero mayor complejidad.

Para este curso se recomienda version por ruta cuando el proyecto crezca:

```python
router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])
```

En esta clase puede mantenerse `/courses` para simplicidad, pero se explica el camino hacia `/api/v1`.

## 10. Buenas practicas iniciales

### 10.1 Nombres consistentes

> **En español simple:** Ponerle nombres claros a tus archivos y variables es como etiquetar las cajas cuando te mudas. "Cocina - platos" es mejor que "caja_3".

Usar nombres claros:

- `courses.py`, no `cosas.py`.
- `course_service.py`, no `funciones2.py`.
- `CourseCreate`, no `Datos`.

La computadora ejecuta cualquier cosa. Los humanos despues tienen que leerla. Seamos humanos decentes.

### 10.2 Routers delgados

El router coordina, el servicio decide.

Mal:

```python
@router.post("/")
def create_course(course: dict):
    # validaciones, busquedas, reglas, persistencia...
```

Mejor:

```python
@router.post("/", response_model=CourseResponse)
def create_course_endpoint(course: CourseCreate):
    return create_course(course)
```

### 10.3 Schemas diferenciados

No todo modelo sirve para todo.

- Entrada: lo que el cliente envia.
- Salida: lo que la API responde.
- Persistencia: lo que se guarda en base de datos.

### 10.4 README util

Un README profesional debe incluir:

- descripcion;
- requisitos;
- instalacion;
- ejecucion;
- endpoints principales;
- estructura del proyecto.

Un README que solo diga "proyecto de clase" es tecnicamente un archivo, pero espiritualmente una rendicion.

## 11. Actividad central de clase

### 11.1 Refactor del proyecto base

Partiendo del proyecto de la Clase 04, el estudiante debe:

1. Crear carpetas `core`, `routers`, `schemas` y `services`.
2. Mover endpoints de estado a `routers/health.py`.
3. Crear `schemas/course.py`.
4. Crear `services/course_service.py`.
5. Crear `routers/courses.py`.
6. Registrar routers en `main.py`.
7. Probar `/health`, `/health/version`, `/courses` y `/docs`.
8. Actualizar README.

### 11.2 Producto de clase — Checklist de verificacion

Al finalizar, tu proyecto debe cumplir esto:

- [ ] La carpeta `app/` contiene subcarpetas `core/`, `routers/`, `schemas/`, `services/`
- [ ] Cada subcarpeta tiene su archivo `__init__.py`
- [ ] `app/core/config.py` define `Settings` con `app_name`, `app_version`, `environment`
- [ ] `app/routers/health.py` tiene endpoint `GET /health` que retorna `{"status": "ok"}`
- [ ] `app/routers/health.py` tiene endpoint `GET /health/version` que retorna nombre, version, entorno
- [ ] `app/schemas/course.py` define `CourseCreate` y `CourseResponse`
- [ ] `app/services/course_service.py` tiene funciones `list_courses()`, `get_course()`, `create_course()`
- [ ] `app/routers/courses.py` tiene endpoints `GET /courses`, `POST /courses`, `GET /courses/{course_id}`
- [ ] `app/main.py` importa y registra ambos routers con `app.include_router()`
- [ ] `GET /courses` lista los cursos
- [ ] `POST /courses` crea un curso y retorna status 201
- [ ] `GET /courses/1` retorna el curso con id=1
- [ ] `GET /docs` muestra la documentacion con todos los endpoints
- [ ] El proyecto tiene `requirements.txt`
- [ ] El proyecto tiene `README.md` con descripcion, instalacion, ejecucion y endpoints

## 12. Errores comunes y troubleshooting

### 12.1 ModuleNotFoundError: No module named 'app'

```text
ModuleNotFoundError: No module named 'app'
```

**Causas posibles:**
- Ejecutaste `uvicorn` desde dentro de la carpeta `app/`
- Olvidaste crear `__init__.py` en la carpeta `app/`
- Escribiste mal el import

**Solucion:** Ejecuta `uvicorn` desde la **raiz** del proyecto (donde esta la carpeta `app/`), no desde adentro.

```bash
# ❌ MAL: estas dentro de app/
~/proyecto/app$ uvicorn app.main:app --reload

# ✅ BIEN: estas en la raiz del proyecto
~/proyecto$ uvicorn app.main:app --reload
```

### 12.2 ModuleNotFoundError especifico

```text
ModuleNotFoundError: No module named 'app.routers'
```

**Causa:** Falta el `__init__.py` en alguna carpeta intermedia.

**Solucion:** Verifica que cada carpeta dentro de `app/` tenga su `__init__.py`:

```bash
ls -la app/routers/__init__.py  # debe existir
ls -la app/schemas/__init__.py  # debe existir
ls -la app/services/__init__.py # debe existir
ls -la app/core/__init__.py     # debe existir
```

### 12.3 Endpoint no aparece en `/docs`

**Causa:** El router no fue registrado en `main.py`.

```python
# ❌ FALTA: nunca registraste el router de courses
app = FastAPI(...)
app.include_router(health.router)
# courses.router nunca se incluyo

# ✅ CORRECTO:
app = FastAPI(...)
app.include_router(health.router)
app.include_router(courses.router)
```

FastAPI no adivina routers escondidos. Todavia no tiene modo Jedi.

### 12.4 Circular import

**Que es:** Dos archivos que se importan mutuamente.

```python
# app/main.py
from app.routers import courses  # main importa courses
...

# app/routers/courses.py
from app.main import app  # courses importa main ← CIRCULAR!
```

**Por que pasa:** Porque quieres usar la variable `app` (la instancia de FastAPI) dentro de un router.

**Solucion:** Nunca importes `app` desde `main.py` hacia un router. Si necesitas acceder a la configuracion, importa `settings` desde `core/config.py`, no desde `main.py`.

```python
# ✅ CORRECTO: importa settings, no app
from app.core.config import settings
```

### 12.5 Error 422 al hacer POST

```text
POST /courses → 422 Unprocessable Entity
```

**Causa:** Enviaste datos que no cumplen con la validacion del schema.

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "String should have at least 3 characters"
    }
  ]
}
```

**Solucion:** Revisa que los datos cumplan con las reglas:
- `name`: entre 3 y 80 caracteres
- `credits`: entre 1 y 6

### 12.6 Error 405 Method Not Allowed

```text
POST /health → 405 Method Not Allowed
```

**Causa:** El endpoint `/health` solo acepta `GET`, no `POST`.

**Solucion:** Revisa el metodo HTTP que estas usando. Si no estas seguro, ve a `/docs` y prueba desde ahi.

## 13. Cierre conceptual

Al finalizar esta clase, el estudiante debe comprender que la estructura de carpetas no es decoracion. Es una herramienta para distribuir responsabilidades y preparar el crecimiento del proyecto.

La arquitectura propuesta no es final ni universal. Es una base didactica y practica para construir el proyecto integrador. En las siguientes clases se agregaran validaciones mas fuertes, modelos de datos, persistencia, pruebas, middleware y seguridad.

El objetivo no es tener muchas carpetas. El objetivo es que cada carpeta tenga una razon clara para existir.

## 14. Trabajo independiente

Para la siguiente clase, los estudiantes deben:

1. Completar el refactor modular.
2. Agregar un nuevo recurso inicial al proyecto integrador.
3. Documentar la estructura en el README.
4. Crear endpoints de salud y version.
5. Preparar schemas para el recurso principal del proyecto.

## 15. Bibliografia y referencias utiles

- FastAPI. (s. f.). *Bigger Applications - Multiple Files*. https://fastapi.tiangolo.com/tutorial/bigger-applications/
- FastAPI. (s. f.). *APIRouter*. https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
- FastAPI. (s. f.). *Response Model*. https://fastapi.tiangolo.com/tutorial/response-model/
- Pydantic. (s. f.). *Models*. https://docs.pydantic.dev/
- Python Packaging Authority. (s. f.). *Python Packaging User Guide*. https://packaging.python.org/
