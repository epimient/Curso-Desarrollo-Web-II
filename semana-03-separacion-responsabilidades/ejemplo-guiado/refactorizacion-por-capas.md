# Ejemplo guiado — De monolito a capas: refactorizacion de una API de estudiantes

## Objetivo

Partir de una API funcional donde **todo vive en un solo archivo** y refactorizarla paso a paso hasta lograr una arquitectura con separacion de responsabilidades.

Al finalizar este ejemplo tendras:
- Un "antes" (monolito) y un "despues" (capas) que puedes comparar lado a lado.
- CRUD completo: Crear, Listar, Obtener por ID, Actualizar y Eliminar.
- Una comprension practica de **por que** se separa, no solo **como**.

> **Requisito previo:** haber completado el ejemplo guiado de la Semana 02 (API de cursos por capas).

---

## Paso 1. El monolito — todo junto

Crea un proyecto nuevo:

```bash
mkdir api-estudiantes
cd api-estudiantes
python -m venv .venv
```

Activa el entorno:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

Instala dependencias:

```bash
pip install fastapi uvicorn
```

Ahora crea un unico archivo `main.py` con todo adentro:

```python
# main.py — EL MONOLITO (asi NO se deberia mantener)
from fastapi import FastAPI, HTTPException

app = FastAPI(title="API Estudiantes — Monolito")

# "Base de datos" en memoria
_estudiantes = []
_next_id = 1


@app.get("/estudiantes")
def listar():
    return _estudiantes


@app.get("/estudiantes/{estudiante_id}")
def obtener(estudiante_id: int):
    for e in _estudiantes:
        if e["id"] == estudiante_id:
            return e
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")


@app.post("/estudiantes", status_code=201)
def crear(nombre: str, email: str, semestre: int):
    global _next_id

    # Validacion manual
    if not nombre or len(nombre) < 2:
        raise HTTPException(status_code=400, detail="Nombre muy corto")
    if semestre < 1 or semestre > 10:
        raise HTTPException(status_code=400, detail="Semestre invalido")
    if any(e["email"] == email for e in _estudiantes):
        raise HTTPException(status_code=400, detail="Email duplicado")

    nuevo = {
        "id": _next_id,
        "nombre": nombre,
        "email": email,
        "semestre": semestre,
        "activo": True,
    }
    _estudiantes.append(nuevo)
    _next_id += 1
    return nuevo


@app.put("/estudiantes/{estudiante_id}")
def actualizar(estudiante_id: int, nombre: str, email: str, semestre: int):
    for e in _estudiantes:
        if e["id"] == estudiante_id:
            if semestre < 1 or semestre > 10:
                raise HTTPException(status_code=400, detail="Semestre invalido")
            e["nombre"] = nombre
            e["email"] = email
            e["semestre"] = semestre
            return e
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")


@app.delete("/estudiantes/{estudiante_id}", status_code=204)
def eliminar(estudiante_id: int):
    global _estudiantes
    original = len(_estudiantes)
    _estudiantes = [e for e in _estudiantes if e["id"] != estudiante_id]
    if len(_estudiantes) == original:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
```

Ejecuta:

```bash
uvicorn main:app --reload
```

Abre http://127.0.0.1:8000/docs y prueba los endpoints. **Funcionan**, pero...

### Problemas del monolito

| Problema | Consecuencia |
|---|---|
| Validacion manual con `if` | Hay que repetir reglas en cada endpoint |
| Logica de negocio en los endpoints | No se puede reutilizar (ej: en un script de carga masiva) |
| Sin schemas | No hay documentacion automatica de los datos esperados |
| Todo en un archivo | Buscar un bug es buscar en 70+ lineas mezcladas |
| Sin separacion de capas | Cambiar una regla puede romper un endpoint |

> **Pregunta para reflexionar:** Si necesitas agregar un campo `carrera` al estudiante, ¿cuantos lugares del archivo tienes que tocar? Respuesta: al menos 3 (crear, actualizar, y la estructura del diccionario). Con capas separadas, solo tocaras el schema y el servicio.

---

## Paso 2. Crear la estructura por capas

Detén el servidor (`Ctrl+C`) y crea la estructura:

```bash
mkdir -p app/routers app/schemas app/services
touch app/__init__.py
touch app/routers/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
```

**Estructura resultante:**

```
api-estudiantes/
  main.py               ← el monolito (lo conservamos como referencia)
  app/
    __init__.py
    main.py              ← nuevo punto de entrada (Paso 6)
    routers/
      __init__.py
      estudiantes.py     ← Paso 5
    schemas/
      __init__.py
      estudiante.py      ← Paso 3
    services/
      __init__.py
      estudiante_service.py  ← Paso 4
```

---

## Paso 3. Extraer schemas (capa de validacion)

> **¿Que estamos sacando del monolito?** Toda la validacion manual (`if not nombre`, `if semestre < 1`). Pydantic la hara automaticamente.

Archivo: `app/schemas/estudiante.py`

```python
from pydantic import BaseModel, Field, EmailStr


class EstudianteCreate(BaseModel):
    """Datos que el cliente envia para CREAR un estudiante."""
    nombre: str = Field(
        min_length=2,
        max_length=100,
        examples=["Maria Garcia"],
    )
    email: str = Field(
        min_length=5,
        max_length=120,
        examples=["maria@universidad.edu"],
    )
    semestre: int = Field(
        ge=1,
        le=10,
        examples=[3],
    )


class EstudianteUpdate(BaseModel):
    """Datos que el cliente envia para ACTUALIZAR un estudiante."""
    nombre: str = Field(
        min_length=2,
        max_length=100,
        examples=["Maria Garcia Lopez"],
    )
    email: str = Field(
        min_length=5,
        max_length=120,
        examples=["maria.garcia@universidad.edu"],
    )
    semestre: int = Field(
        ge=1,
        le=10,
        examples=[4],
    )


class EstudianteResponse(BaseModel):
    """Datos que el servidor DEVUELVE como respuesta."""
    id: int
    nombre: str
    email: str
    semestre: int
    activo: bool
```

### ¿Que ganamos?

| Antes (monolito) | Despues (schema) |
|---|---|
| `if not nombre or len(nombre) < 2:` | `nombre: str = Field(min_length=2)` |
| `if semestre < 1 or semestre > 10:` | `semestre: int = Field(ge=1, le=10)` |
| Validacion repetida en POST y PUT | Una sola definicion reutilizable |
| Sin documentacion de los datos | Swagger documenta automaticamente los campos |
| Errores manuales con `HTTPException` | Errores automaticos 422 con detalles por campo |

> **Decision de diseño:** Creamos `EstudianteCreate` y `EstudianteUpdate` como schemas separados. Hoy son iguales, pero en el futuro `EstudianteUpdate` podria tener campos opcionales (`Optional[str]`) para actualizaciones parciales. Prepararse para el cambio es parte de separar responsabilidades.

---

## Paso 4. Extraer servicio (capa de logica de negocio)

> **¿Que estamos sacando del monolito?** Las reglas: "no se puede crear con email duplicado", "buscar por ID", "eliminar de la lista". Todo lo que NO es recibir/responder HTTP.

Archivo: `app/services/estudiante_service.py`

```python
from fastapi import HTTPException

from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate

# "Base de datos" en memoria
_estudiantes: list[dict] = []
_next_id: int = 1


def listar_estudiantes() -> list[dict]:
    """Devuelve todos los estudiantes."""
    return _estudiantes


def obtener_estudiante(estudiante_id: int) -> dict:
    """Busca un estudiante por ID. Lanza 404 si no existe."""
    for e in _estudiantes:
        if e["id"] == estudiante_id:
            return e
    raise HTTPException(
        status_code=404,
        detail=f"Estudiante con id {estudiante_id} no encontrado",
    )


def crear_estudiante(datos: EstudianteCreate) -> dict:
    """
    Crea un nuevo estudiante.

    Regla de negocio: no se permite email duplicado.
    """
    global _next_id

    # Regla de negocio: email unico
    email_existe = any(
        e["email"].lower() == datos.email.lower()
        for e in _estudiantes
    )
    if email_existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un estudiante con ese email",
        )

    nuevo = {
        "id": _next_id,
        "nombre": datos.nombre,
        "email": datos.email,
        "semestre": datos.semestre,
        "activo": True,
    }
    _estudiantes.append(nuevo)
    _next_id += 1
    return nuevo


def actualizar_estudiante(estudiante_id: int, datos: EstudianteUpdate) -> dict:
    """
    Actualiza un estudiante existente.

    Regla de negocio: el nuevo email no debe pertenecer a otro estudiante.
    """
    estudiante = obtener_estudiante(estudiante_id)  # reutiliza la busqueda

    # Verifica que el nuevo email no pertenezca a OTRO estudiante
    for e in _estudiantes:
        if e["id"] != estudiante_id and e["email"].lower() == datos.email.lower():
            raise HTTPException(
                status_code=400,
                detail="Ese email ya pertenece a otro estudiante",
            )

    estudiante["nombre"] = datos.nombre
    estudiante["email"] = datos.email
    estudiante["semestre"] = datos.semestre
    return estudiante


def eliminar_estudiante(estudiante_id: int) -> None:
    """Elimina un estudiante por ID. Lanza 404 si no existe."""
    global _estudiantes

    original = len(_estudiantes)
    _estudiantes = [e for e in _estudiantes if e["id"] != estudiante_id]

    if len(_estudiantes) == original:
        raise HTTPException(
            status_code=404,
            detail=f"Estudiante con id {estudiante_id} no encontrado",
        )
```

### ¿Que ganamos?

| Aspecto | Beneficio |
|---|---|
| **Reutilizacion** | `obtener_estudiante()` se usa en GET por ID y en PUT (buscar antes de actualizar) |
| **Reglas centralizadas** | "email unico" vive en un solo lugar, no en cada endpoint |
| **Testeable** | Puedes probar `crear_estudiante()` sin simular HTTP |
| **Independiente** | Si manana usas una BD real, solo cambias este archivo |

> **Nota importante:** `obtener_estudiante()` se reutiliza dentro de `actualizar_estudiante()`. En el monolito, la busqueda por ID estaba copiada en dos endpoints. Esa duplicacion es exactamente el tipo de problema que la separacion de responsabilidades resuelve.

---

## Paso 5. Extraer router (capa de presentacion)

> **¿Que estamos sacando del monolito?** Solo las rutas HTTP. El router recibe, delega al servicio y responde. Nada mas.

Archivo: `app/routers/estudiantes.py`

```python
from fastapi import APIRouter, status

from app.schemas.estudiante import (
    EstudianteCreate,
    EstudianteResponse,
    EstudianteUpdate,
)
from app.services import estudiante_service

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/", response_model=list[EstudianteResponse])
def listar():
    """GET /estudiantes — Devuelve todos los estudiantes."""
    return estudiante_service.listar_estudiantes()


@router.get("/{estudiante_id}", response_model=EstudianteResponse)
def obtener(estudiante_id: int):
    """GET /estudiantes/{id} — Devuelve un estudiante por su ID."""
    return estudiante_service.obtener_estudiante(estudiante_id)


@router.post(
    "/",
    response_model=EstudianteResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(estudiante: EstudianteCreate):
    """POST /estudiantes — Crea un nuevo estudiante."""
    return estudiante_service.crear_estudiante(estudiante)


@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar(estudiante_id: int, estudiante: EstudianteUpdate):
    """PUT /estudiantes/{id} — Actualiza un estudiante existente."""
    return estudiante_service.actualizar_estudiante(estudiante_id, estudiante)


@router.delete(
    "/{estudiante_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(estudiante_id: int):
    """DELETE /estudiantes/{id} — Elimina un estudiante."""
    estudiante_service.eliminar_estudiante(estudiante_id)
```

### Explicacion:

| Elemento | Significado |
|---|---|
| `prefix="/estudiantes"` | Todas las rutas empiezan con `/estudiantes` |
| `tags=["Estudiantes"]` | Agrupa los endpoints en Swagger |
| `response_model=EstudianteResponse` | Documenta y valida la respuesta automaticamente |
| `status_code=201` | Indica "recurso creado" en POST |
| `status_code=204` | Indica "sin contenido" en DELETE |

> **Observa como cada funcion del router tiene maximo 2 lineas de codigo.** Recibe datos, delega al servicio, y devuelve. Si un router tiene 20+ lineas en una sola funcion, probablemente esta haciendo trabajo del servicio.

---

## Paso 6. Crear el punto de entrada

Archivo: `app/main.py`

```python
from fastapi import FastAPI

from app.routers import estudiantes

app = FastAPI(
    title="API Estudiantes",
    description="Ejemplo de refactorizacion: de monolito a capas separadas — Semana 03",
    version="0.1.0",
)

app.include_router(estudiantes.router)
```

---

## Paso 7. Ejecutar y probar

Asegurate de estar en la carpeta `api-estudiantes/` y ejecuta:

```bash
uvicorn app.main:app --reload
```

> **Nota:** Ya NO usamos `uvicorn main:app` (el monolito). Ahora usamos `uvicorn app.main:app` (la version refactorizada).

Abre http://127.0.0.1:8000/docs

### 7.1 Crear un estudiante (POST)

En Swagger, haz clic en `POST /estudiantes` > "Try it out" y envia:

```json
{
  "nombre": "Maria Garcia",
  "email": "maria@universidad.edu",
  "semestre": 3
}
```

**Respuesta esperada (201 Created):**

```json
{
  "id": 1,
  "nombre": "Maria Garcia",
  "email": "maria@universidad.edu",
  "semestre": 3,
  "activo": true
}
```

### 7.2 Listar estudiantes (GET)

`GET /estudiantes` > "Try it out" > "Execute"

**Respuesta esperada (200 OK):**

```json
[
  {
    "id": 1,
    "nombre": "Maria Garcia",
    "email": "maria@universidad.edu",
    "semestre": 3,
    "activo": true
  }
]
```

### 7.3 Obtener por ID (GET)

`GET /estudiantes/1` > "Try it out" > "Execute"

**Respuesta esperada (200 OK):**

```json
{
  "id": 1,
  "nombre": "Maria Garcia",
  "email": "maria@universidad.edu",
  "semestre": 3,
  "activo": true
}
```

### 7.4 Probar validacion (schema)

Intenta crear con datos invalidos:

```json
{
  "nombre": "A",
  "email": "x",
  "semestre": 15
}
```

**Respuesta esperada (422 Unprocessable Entity):**

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "nombre"],
      "msg": "String should have at least 2 characters"
    },
    {
      "type": "string_too_short",
      "loc": ["body", "email"],
      "msg": "String should have at least 5 characters"
    },
    {
      "type": "less_than_equal",
      "loc": ["body", "semestre"],
      "msg": "Input should be less than or equal to 10"
    }
  ]
}
```

> Pydantic valido los tres campos automaticamente. En el monolito, solo validabamos nombre y semestre manualmente. El email no tenia validacion.

### 7.5 Probar regla de negocio (email duplicado)

Crea otro estudiante con el mismo email:

```json
{
  "nombre": "Carlos Lopez",
  "email": "maria@universidad.edu",
  "semestre": 5
}
```

**Respuesta esperada (400 Bad Request):**

```json
{
  "detail": "Ya existe un estudiante con ese email"
}
```

### 7.6 Actualizar (PUT)

`PUT /estudiantes/1`:

```json
{
  "nombre": "Maria Garcia Lopez",
  "email": "maria.garcia@universidad.edu",
  "semestre": 4
}
```

**Respuesta esperada (200 OK):**

```json
{
  "id": 1,
  "nombre": "Maria Garcia Lopez",
  "email": "maria.garcia@universidad.edu",
  "semestre": 4,
  "activo": true
}
```

### 7.7 Eliminar (DELETE)

`DELETE /estudiantes/1`

**Respuesta esperada:** `204 No Content` (sin cuerpo).

### 7.8 Probar 404

`GET /estudiantes/999`

**Respuesta esperada (404 Not Found):**

```json
{
  "detail": "Estudiante con id 999 no encontrado"
}
```

---

## Paso 8. Comparacion final — monolito vs capas

| Aspecto | Monolito (`main.py`) | Capas (app/) |
|---|---|---|
| **Archivos** | 1 archivo (~70 lineas) | 5 archivos (~30 lineas cada uno) |
| **Validacion** | Manual con `if` | Automatica con Pydantic |
| **Reglas de negocio** | Dentro de los endpoints | En el servicio (reutilizable) |
| **Documentacion** | Minima | Swagger completo con ejemplos |
| **Buscar un bug** | Hay que leer todo el archivo | Sabes exactamente en que archivo buscar |
| **Agregar un campo** | Tocar 3+ lugares del mismo archivo | Tocar schema + servicio (separados) |
| **Reutilizar logica** | No es posible | Puedes llamar al servicio desde otro contexto |
| **Probar una regla** | Necesitas simular HTTP | Puedes probar la funcion directamente |

---

## Paso 9. Errores comunes

| Error | Causa probable | Solucion |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` | Ejecutas desde la carpeta incorrecta | Ejecuta desde `api-estudiantes/` |
| `ImportError: cannot import name 'EstudianteCreate'` | Falta `__init__.py` en `schemas/` | Crea el archivo vacio |
| `422 Unprocessable Entity` al crear | Datos no cumplen las reglas del schema | Revisa min_length, ge, le |
| `400 Bad Request` al crear | Email duplicado (regla de negocio) | Usa un email diferente |
| `404 Not Found` | El ID no existe | Verifica con GET /estudiantes |

---

## Paso 10. Preguntas de reflexion

1. **¿Que archivo tocarias si necesitas agregar el campo `carrera` al estudiante?**
   - `app/schemas/estudiante.py` (agregar el campo en Create, Update y Response)
   - `app/services/estudiante_service.py` (incluirlo en el diccionario `nuevo`)
   - El router NO cambia. Esa es la gracia de separar responsabilidades.

2. **¿Donde iria la regla "un estudiante no puede estar en semestre 10 si no ha aprobado proyecto de grado"?**
   - En el servicio (`estudiante_service.py`), porque es una regla de negocio.
   - El schema solo valida formato (rango 1-10). El servicio valida logica.

3. **¿Que pasaria si mañana conectas una base de datos real?**
   - Solo cambiaria `estudiante_service.py` (las listas se reemplazan por queries SQLAlchemy).
   - Los routers y schemas quedan intactos.
   - Eso es exactamente lo que haremos en la Semana 13.

4. **¿Por que el router `eliminar()` no hace `return`?**
   - Porque el status 204 No Content no lleva cuerpo en la respuesta. Solo confirma que se elimino.

---

## Resumen de conceptos aplicados

| Concepto | Como se aplico |
|---|---|
| **Separacion de responsabilidades** | Cada archivo tiene UNA responsabilidad clara |
| **Refactorizacion** | Partir de codigo funcional y reorganizarlo sin cambiar el comportamiento |
| **Validacion con Pydantic** | Schemas con `Field()` reemplazan validacion manual |
| **Reutilizacion** | `obtener_estudiante()` se usa en GET y PUT |
| **CRUD completo** | Create, Read (list + by ID), Update, Delete |
| **Documentacion automatica** | Swagger muestra schemas, ejemplos y status codes |

---

## Cierre

La separacion de responsabilidades no es sobre crear carpetas bonitas. Es sobre **saber donde buscar cuando algo falla** y poder **cambiar una cosa sin romper otra**.

El monolito funciona. Pero cuando el proyecto crece, funcionar no es suficiente: necesitas que sea **mantenible**.

**Tu primera refactorizacion esta completa. Bien hecho.**
