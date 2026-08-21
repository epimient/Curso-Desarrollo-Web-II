# Ejemplo guiado - API de cursos por capas en FastAPI

## Objetivo

Construir una API pequena para administrar cursos academicos separando responsabilidades en capas.

Al finalizar este ejemplo, tendras una API funcional con:
- `main.py` (punto de entrada)
- `routers/` (rutas)
- `schemas/` (validacion)
- `services/` (logica de negocio)

---

## Paso 1. Crear estructura del proyecto

Primero, creamos la carpeta del proyecto y el entorno virtual.

```bash
mkdir api-cursos
cd api-cursos
python -m venv .venv
```

**Explicacion:** Creamos una carpeta llamada `api-cursos` y dentro un entorno virtual `.venv` para aislar las dependencias.

Activar entorno:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install fastapi uvicorn
```

**Explicacion:** `fastapi` es el framework. `uvicorn` es el servidor que ejecutara nuestra API.

Crear estructura de carpetas:

```bash
mkdir -p app/routers app/schemas app/services
touch app/__init__.py
touch app/routers/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
```

**Explicacion:**
- `mkdir -p` crea todas las carpetas de una sola vez.
- Los archivos `__init__.py` le dicen a Python que estas carpetas son "paquetes" (modulos que pueden importarse entre si).
- Sin estos archivos, `from app.routers import cursos` no funcionaria.

**Estructura resultante:**
```
api-cursos/
  .venv/
  app/
    __init__.py
    main.py          (lo crearemos en el Paso 5)
    routers/
      __init__.py
      cursos.py      (lo crearemos en el Paso 4)
    schemas/
      __init__.py
      curso.py       (lo crearemos en el Paso 2)
    services/
      __init__.py
      curso_service.py  (lo crearemos en el Paso 3)
```

---

## Paso 2. Crear schema (validacion de datos)

> **¿Que es un schema?** Es un modelo que define "que forma deben tener los datos". Como un formulario con campos obligatorios, tipos de datos y restricciones.

Archivo: `app/schemas/curso.py`

```python
from pydantic import BaseModel, Field


class CursoCreate(BaseModel):
    """Modelo para los datos que el cliente ENVIA al crear un curso."""
    nombre: str = Field(
        min_length=3,        # El nombre debe tener al menos 3 caracteres
        max_length=80,       # Y como maximo 80
    )
    creditos: int = Field(
        ge=1,                # Mayor o igual a 1 (greater or equal)
        le=6,                # Menor o igual a 6 (less or equal)
    )


class CursoResponse(BaseModel):
    """Modelo para los datos que el servidor DEVUELVE como respuesta."""
    id: int
    nombre: str
    creditos: int
    activo: bool             # El servidor asigna True por defecto
```

### Explicacion:

| Elemento | Significado |
|---|---|
| `BaseModel` | Clase base de Pydantic para crear modelos de datos |
| `Field(...)` | Agrega validaciones adicionales a un campo |
| `min_length=3` | Valida que el texto tenga minimo 3 caracteres |
| `ge=1` | Valida que el numero sea >= 1 (greater or equal) |
| `CursoCreate` | Se usa cuando el cliente QUIERE CREAR un curso |
| `CursoResponse` | Se usa cuando el servidor RESPONDE con datos del curso |

**Decision importante:** Separar `CursoCreate` de `CursoResponse` permite que:
- El cliente solo envie `nombre` y `creditos`.
- El servidor devuelva `id`, `nombre`, `creditos` y `activo`.
- Si en el futuro agregamos un campo interno (ej: `creado_por`), lo incluimos solo en `CursoResponse`, no en `CursoCreate`.

---

## Paso 3. Crear service (logica de negocio)

> **¿Que es un service?** Es donde viven las "reglas del negocio". Por ejemplo: "no se puede crear un curso con nombre duplicado". El service decide si la operacion es valida y la ejecuta.

Archivo: `app/services/curso_service.py`

```python
from fastapi import HTTPException
from app.schemas.curso import CursoCreate

# "Base de datos" en memoria (lista de cursos)
_cursos = []
_next_id = 1


def listar_cursos():
    """Devuelve todos los cursos almacenados."""
    return _cursos


def crear_curso(curso: CursoCreate):
    """
    Crea un nuevo curso.
    
    Reglas de negocio:
    - No se puede crear un curso con nombre duplicado.
    """
    global _next_id

    # Revisa si ya existe un curso con el mismo nombre
    # (compara en minusculas para evitar "Web II" vs "web ii")
    existe = any(
        item["nombre"].lower() == curso.nombre.lower()
        for item in _cursos
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un curso con ese nombre"
        )

    # Crea el diccionario del nuevo curso
    nuevo = {
        "id": _next_id,
        "nombre": curso.nombre,
        "creditos": curso.creditos,
        "activo": True,
    }

    _cursos.append(nuevo)   # Guarda en la lista
    _next_id += 1            # Prepara el siguiente ID

    return nuevo
```

### Explicacion linea por linea:

| Codigo | Que hace |
|---|---|
| `_cursos = []` | Lista vacia que funciona como "base de datos temporal". El guion bajo indica que es privada. |
| `_next_id = 1` | Contador para asignar IDs unicos a cada curso. |
| `def listar_cursos():` | Funcion simple: devuelve la lista completa. |
| `def crear_curso(curso: CursoCreate):` | Recibe un objeto ya validado por Pydantic. |
| `global _next_id` | Permite modificar la variable `_next_id` dentro de la funcion. Sin esto, Python crearia una copia local. |
| `any(...)` | `any()` devuelve `True` si ALGUN elemento de la lista cumple la condicion. |
| `item["nombre"].lower() == curso.nombre.lower()` | Compara nombres en minusculas para evitar duplicados por diferencias de mayusculas. |
| `raise HTTPException(...)` | Lanza un error HTTP controlado. FastAPI lo convierte automaticamente en una respuesta JSON con codigo 400. |
| `nuevo = { ... }` | Crea un diccionario con los datos del nuevo curso. |
| `_cursos.append(nuevo)` | Agrega el curso a la lista. |
| `_next_id += 1` | Incrementa el contador. Sin esto, todos los cursos tendrian ID = 1. |

> **Decision importante:** La regla de nombre duplicado vive en el servicio, no en el router. El router no deberia cargar con toda la logica del negocio como protagonista sobreexplotado de shonen.

---

## Paso 4. Crear router (punto de entrada HTTP)

> **¿Que es un router?** Agrupa rutas relacionadas. Aqui decimos: "todos los endpoints que empiezan con `/cursos` se manejan aqui".

Archivo: `app/routers/cursos.py`

```python
from fastapi import APIRouter, status

from app.schemas.curso import CursoCreate, CursoResponse
from app.services.curso_service import crear_curso, listar_cursos

# Crea un router con prefijo /cursos
router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("/", response_model=list[CursoResponse])
def obtener_cursos():
    """GET /cursos - Devuelve la lista de todos los cursos."""
    return listar_cursos()


@router.post(
    "/",
    response_model=CursoResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_curso(curso: CursoCreate):
    """POST /cursos - Crea un nuevo curso (con validacion)."""
    return crear_curso(curso)
```

### Explicacion:

| Elemento | Significado |
|---|---|
| `APIRouter` | Clase para agrupar rutas. |
| `prefix="/cursos"` | Todas las rutas aqui empiezan con `/cursos`. Asi, `@router.get("/")` responde en `GET /cursos`. |
| `tags=["Cursos"]` | Agrupa los endpoints en la documentacion de Swagger. |
| `response_model=list[CursoResponse]` | Declara que la respuesta sera una lista de objetos `CursoResponse`. FastAPI usa esto para documentacion y validacion. |
| `status_code=201` | Codigo HTTP para "recurso creado exitosamente". |

> **Nota:** El router no contiene logica de negocio. Solo recibe, delega al servicio y responde. Si el router hiciera todo, seria un "controlador obeso".

---

## Paso 5. Crear aplicacion principal (main.py)

> **¿Que hace main.py?** Es el punto de entrada. Crea la aplicacion FastAPI y registra los routers.

Archivo: `app/main.py`

```python
from fastapi import FastAPI
from app.routers import cursos

app = FastAPI(
    title="API Academica",
    description="API de ejemplo con arquitectura por capas para Desarrollo Web II",
    version="0.1.0",
)

# Registra el router de cursos
app.include_router(cursos.router)
```

### Explicacion:

| Linea | Que hace |
|---|---|
| `from fastapi import FastAPI` | Importa la clase principal de FastAPI. |
| `from app.routers import cursos` | Importa el router que acabamos de crear. |
| `app = FastAPI(title="...", description="...", version="...")` | Crea la aplicacion con metadatos que aparecen en la documentacion. |
| `app.include_router(cursos.router)` | "Registra" el router. Sin esta linea, las rutas no existirian. FastAPI no descubrira los routers solos. |

> **Decision importante:** `main.py` registra componentes. No contiene toda la aplicacion. Si el proyecto crece, `main.py` seguira siendo pequeno y legible.

---

## Paso 6. Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

**Explicacion:**
- `app.main` significa "el archivo `app/main.py`".
- `:app` significa "la variable `app` dentro de ese archivo".
- `--reload` reinicia automaticamente el servidor cuando detecta cambios en el codigo (util mientras desarrollas).

Abre tu navegador y visita:
```text
http://127.0.0.1:8000/docs
```

Deberias ver la interfaz de **Swagger UI** con la documentacion automatica de tu API.

> **¿Que es Swagger UI?** Es una pagina web que se genera automaticamente a partir de tu codigo FastAPI. Muestra todos los endpoints, permite probarlos, y documenta los modelos de datos. Sin escribir una sola linea de documentacion, ya tienes una interfaz para probar tu API.

---

## Paso 7. Probar los endpoints

### Crear un curso (POST)

Desde Swagger UI, haz clic en `POST /cursos` > "Try it out" y envia:

```json
{
  "nombre": "Desarrollo Web II",
  "creditos": 3
}
```

**Respuesta esperada (201 Created):**

```json
{
  "id": 1,
  "nombre": "Desarrollo Web II",
  "creditos": 3,
  "activo": true
}
```

### Listar cursos (GET)

Haz clic en `GET /cursos` > "Try it out" > "Execute".

**Respuesta esperada (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Desarrollo Web II",
    "creditos": 3,
    "activo": true
  }
]
```

### Probar validacion (intentar crear curso invalido)

Intenta crear un curso con:
```json
{
  "nombre": "AB",
  "creditos": 10
}
```

**Respuesta esperada (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "nombre"],
      "msg": "String should have at least 3 characters",
      "input": "AB"
    },
    {
      "type": "less_than_equal",
      "loc": ["body", "creditos"],
      "msg": "Input should be less than or equal to 6",
      "input": 10
    }
  ]
}
```

> **¿Que paso aqui?** Pydantic rechazo los datos porque `"AB"` tiene solo 2 caracteres (minimo 3) y `10` supera el maximo de 6 creditos. Fastavid devolvio un error 422 con los detalles de cada campo invalido. **No escribimos una sola linea de validacion manual.**

### Probar regla de negocio (duplicados)

Crea "Desarrollo Web II" dos veces. La segunda vez debe responder:

```json
{
  "detail": "Ya existe un curso con ese nombre"
}
```

> Esta validacion NO la hace Pydantic. La hace el servicio (`curso_service.py`). Es una regla de negocio, no una validacion de formato.

---

## Paso 8. Errores comunes y como resolverlos

| Error | Posible causa | Solucion |
|---|---|---|
| `ModuleNotFoundError: No module named 'fastapi'` | No instalaste fastapi | `pip install fastapi uvicorn` |
| `ModuleNotFoundError: No module named 'app'` | Ejecutaste desde la carpeta equivocada | Ejecuta `uvicorn app.main:app --reload` desde `api-cursos/` |
| `ImportError: ...` | Falta `__init__.py` en alguna carpeta | Crea los archivos `__init__.py` vacios |
| La API no responde | El servidor no se ejecuta | Verifica que `uvicorn` este corriendo y el puerto sea 8000 |
| `422 Unprocessable Entity` | Los datos enviados no cumplen las validaciones | Revisa los requisitos de cada campo (min_length, ge, le) |
| Error 405 Method Not Allowed | Usaste un metodo HTTP incorrecto | Ej: enviaste GET a un endpoint que solo acepta POST |

---

## Paso 9. Discusion final

Responde estas preguntas para verificar tu comprension:

1. **¿Que archivo cumple el papel mas parecido al controlador en MVC?**
   - Respuesta: El router (`app/routers/cursos.py`), porque recibe solicitudes, coordina y responde.

2. **¿Que archivo representa la validacion de entrada (como el "modelo" de MVC)?**
   - Respuesta: El schema (`app/schemas/curso.py`), porque define la estructura y reglas de los datos.

3. **¿Donde vive la regla de negocio "no duplicados"?**
   - Respuesta: En el servicio (`app/services/curso_service.py`), separado del router y del schema.

4. **¿Que pasaria si se agrega base de datos?**
   - Respuesta: Solo cambiaria el servicio. Los routers y schemas no necesitarian modificarse.

5. **¿Que ventajas tiene esta estructura frente a poner todo en `main.py`?**
   - Respuesta: Es mas facil de entender, mantener, probar y escalar. Cada archivo tiene una responsabilidad clara.

---

## Resumen de conceptos aplicados

| Concepto | Como se aplico |
|---|---|
| **Arquitectura por capas** | Separamos main, routers, schemas, services |
| **Validacion Pydantic** | `Field(min_length=3, ge=1)` valida automaticamente |
| **Reglas de negocio** | `crear_curso()` verifica duplicados en el servicio |
| **Separacion de responsabilidades** | Cada archivo hace una cosa y la hace bien |
| **Documentacion automatica** | Swagger UI en `/docs` sin escribir una linea |
| **OpenAPI** | FastAPI genera el esquema OpenAPI automaticamente |

---

## Cierre

Este ejemplo muestra una arquitectura pequena pero ordenada. En clases posteriores se agregaran persistencia (base de datos real), pruebas (con TestClient), seguridad (autenticacion, CORS) y middleware.

Lo importante es que la estructura ya permite crecer sin convertir el proyecto en una criatura pegada con cinta.

**Tu primera API esta funcionando. Bien hecho.**
