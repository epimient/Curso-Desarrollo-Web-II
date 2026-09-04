# Guía completa: API de Equipos de Laboratorio

> Explicación paso a paso de cada archivo, cada función y cada concepto.
> Orientado a estudiantes que están aprendiendo arquitectura por capas.

---

## Tabla de contenidos

1. [¿Qué es la arquitectura por capas?](#1--qué-es-la-arquitectura-por-capas)
2. [Los archivos `__init__.py`](#2--los-archivos-initpy)
3. [Schema: validación con Pydantic](#3--schema-validación-con-pydantic)
4. [Service: lógica de negocio](#4--service-lógica-de-negocio)
5. [Router: endpoints HTTP](#5--router-endpoints-http)
6. [Main: punto de entrada](#6--main-punto-de-entrada)
7. [El flujo completo](#7--el-flujo-completo)
8. [Cómo ejecutar y probar](#8--cómo-ejecutar-y-probar)
9. [Errores comunes y cómo solucionarlos](#9--errores-comunes-y-cómo-solucionarlos)

---

## 1 · ¿Qué es la arquitectura por capas?

Imagina una **fábrica** donde cada trabajador hace **una sola cosa**:

| Trabajador | Qué hace |
|------------|----------|
| Recepcionista | Recibe el pedido del cliente |
| Validador | Revisa que el pedido esté bien escrito |
| Técnico | Ejecuta el trabajo |
| Almacén | Guarda o entrega el resultado |

En nuestro proyecto:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Router    │───▶│   Schema    │───▶│   Service   │───▶│   Memoria   │
│             │    │             │    │             │    │             │
│ Recibe HTTP │    │ Valida datos│    │ Lógica      │    │ Guarda datos│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**¿Por qué separar así?**

- Si mañana cambias la base de datos, solo tocas el **Service**
- Si cambias el formato de los datos, solo tocas el **Schema**
- Si agregas un nuevo endpoint, solo tocas el **Router**
- Cada archivo tiene **una responsabilidad**

---

## 2 · Los archivos `__init__.py`

### ¿Qué son?

Son archivos **completamente vacíos**. No tienen código. No hacen nada.

### ¿Para qué existen?

Python necesita saber qué carpetas son **paquetes** (grupos de archivos que se pueden importar).

```
app/
├── __init__.py          ← "app es un paquete"
├── main.py
├── routers/
│   ├── __init__.py      ← "routers es un paquete"
│   └── equipos.py
├── schemas/
│   ├── __init__.py      ← "schemas es un paquete"
│   └── equipo.py
└── services/
    ├── __init__.py      ← "services es un paquete"
    └── equipo_service.py
```

### ¿Qué pasa si no los creo?

Si borras `app/__init__.py` y ejecutas:

```python
from app.schemas.equipo import EquipoCreate
```

Python lanza:

```
ModuleNotFoundError: No module named 'app'
```

### Analogía

Piensa en `__init__.py` como una **placa en la puerta** de una oficina:

- Con la placa: "Esta oficina existe, puedes entrar"
- Sin la placa: "No sé qué es este lugar"

**Regla simple:** Si una carpeta contiene archivos `.py` que se importan, necesitas `__init__.py`.

---

## 3 · Schema: validación con Pydantic

### Archivo: `app/schemas/equipo.py`

### ¿Qué es Pydantic?

Pydantic es una librería que **valida automáticamente** los datos que entran y salen de tu API.

Si el cliente envía `{"nombre": "X"}` y tú dijiste que `nombre` debe tener mínimo 3 caracteres, Pydantic **rechaza la petición automáticamente** sin que tú escribas código de validación.

### Los dos schemas

#### `EquipoCreate` — datos que ENVÍA el cliente

```python
from pydantic import BaseModel, Field


class EquipoCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=80)
    categoria: str = Field(..., min_length=3, max_length=50)
```

| Elemento | Significado |
|----------|-------------|
| `BaseModel` | Clase base de Pydantic — todos los schemas la heredan |
| `str` | Tipo de dato: texto |
| `Field(...)` | Configuración del campo |
| `min_length=3` | Mínimo 3 caracteres |
| `max_length=80` | Máximo 80 caracteres |

**¿Qué pasa si el cliente envía `{"nombre": "AB"}`?**

Pydantic devuelve error 422 automáticamente:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "nombre"],
      "msg": "String should have at least 3 characters",
      "input": "AB",
      "ctx": {"min_length": 3}
    }
  ]
}
```

#### `EquipoResponse` — datos que DEVUELVE el servidor

```python
class EquipoResponse(BaseModel):
    id: int
    nombre: str
    categoria: str
    disponible: bool
```

Esta clase define **cómo se ve la respuesta**. El cliente recibe exactamente estos 4 campos — ni uno más, ni uno menos.

### ¿Por qué dos schemas separados?

| Schema | Propósito | Ejemplo |
|--------|-----------|---------|
| `EquipoCreate` | Lo que el cliente envía | `{"nombre": "Arduino", "categoria": "Micro"}` |
| `EquipoResponse` | Lo que el servidor devuelve | `{"id": 1, "nombre": "Arduino", "categoria": "Micro", "disponible": true}` |

El cliente **nunca** envía `id` ni `disponible` — esos los asigna el servidor.

### Errores de validación que Pydantic maneja solo

| Error | Causa |
|-------|-------|
| 422 | `nombre` tiene menos de 3 caracteres |
| 422 | `categoria` tiene menos de 3 caracteres |
| 422 | Falta el campo `nombre` |
| 422 | `nombre` no es texto (ej: envías un número) |

**Tú no escribes ninguna de estas validaciones.** Pydantic lo hace por ti.

---

## 4 · Service: lógica de negocio

### Archivo: `app/services/equipo_service.py`

### Código completo explicado

```python
from fastapi import HTTPException

from app.schemas.equipo import EquipoCreate
```

Importas `HTTPException` para lanzar errores HTTP y `EquipoCreate` para tipar los datos.

---

```python
_equipos: list[dict] = []
_next_id = 1
```

| Variable | Tipo | Propósito |
|----------|------|-----------|
| `_equipos` | Lista de diccionarios | Simula una base de datos en memoria |
| `_next_id` | Entero | Contador automático de IDs |

El guión bajo al inicio (`_equipos`) indica que es una variable **interna** — no se debe acceder directamente desde fuera.

---

```python
def listar_equipos() -> list[dict]:
    return _equipos
```

**Qué hace:** Devuelve todos los equipos guardados.

**Por qué es simple:** Solo returns la lista. No hay lógica. No hay filtros. Solo returns lo que hay.

---

```python
def crear_equipo(equipo: EquipoCreate) -> dict:
    global _next_id
```

**`global _next_id`** le dice a Python: "Quiero modificar la variable `_next_id` que está fuera de esta función". Sin esto, Python crearía una variable local y el contador nunca aumentaría.

---

```python
    existe = any(
        e["nombre"].lower() == equipo.nombre.lower() for e in _equipos
    )
    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un equipo con ese nombre",
        )
```

**Línea por línea:**

1. `any(...)` — Devuelve `True` si **al menos un** elemento cumple la condición
2. `e["nombre"].lower()` — Toma el nombre guardado y lo pasa a minúsculas
3. `equipo.nombre.lower()` — Toma el nombre enviado y lo pasa a minúsculas
4. Si son iguales → `True` → el equipo ya existe
5. `raise HTTPException(400, ...)` — Lanza error HTTP 400

**¿Por qué `.lower()`?**

Para que "Arduino UNO", "arduino uno" y "ARDUINO UNO" se consideren **iguales**. Sin esto, podrías crear duplicados con diferente capitalización.

---

```python
    nuevo = {
        "id": _next_id,
        "nombre": equipo.nombre,
        "categoria": equipo.categoria,
        "disponible": True,
    }
```

Crea un diccionario con:
- `id` = contador actual (1, 2, 3...)
- `nombre` = lo que envió el cliente
- `categoria` = lo que envió el cliente
- `disponible` = **siempre** `True` (el cliente no controla esto)

---

```python
    _equipos.append(nuevo)
    _next_id += 1

    return nuevo
```

1. Agrega el equipo a la lista
2. Incrementa el contador para el próximo equipo
3. Devuelve el equipo creado

---

## 5 · Router: endpoints HTTP

### Archivo: `app/routers/equipos.py`

### Código completo explicado

```python
from fastapi import APIRouter, status

from app.schemas.equipo import EquipoCreate, EquipoResponse
from app.services.equipo_service import crear_equipo, listar_equipos
```

Importas:
- `APIRouter` — para crear rutas agrupadas
- `status` — para usar códigos HTTP como `status.HTTP_201_CREATED`
- Los schemas y services que necesitas

---

```python
router = APIRouter(prefix="/equipos", tags=["Equipos"])
```

| Parámetro | Significado |
|-----------|-------------|
| `prefix="/equipos"` | Todas las rutas empiezan con `/equipos` |
| `tags=["Equipos"]` | En Swagger, se agrupan bajo "Equipos" |

Esto significa que:
- `@router.get("/")` se convierte en `GET /equipos/`
- `@router.post("/")` se convierte en `POST /equipos/`

---

```python
@router.get("/", response_model=list[EquipoResponse])
def get_equipos():
    return listar_equipos()
```

| Elemento | Significado |
|----------|-------------|
| `@router.get("/")` | Decorador: esta función responde a GET |
| `response_model=list[EquipoResponse]` | Swagger sabe que devuelve una lista de equipos |
| `return listar_equipos()` | **Solo llama al service** — no hay lógica aquí |

**¿Por qué `list[EquipoResponse]`?**

Le dice a Swagger: "La respuesta es una lista donde cada elemento tiene `id`, `nombre`, `categoria` y `disponible`".

---

```python
@router.post("/", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
def post_equipo(equipo: EquipoCreate):
    return crear_equipo(equipo)
```

| Elemento | Significado |
|----------|-------------|
| `@router.post("/")` | Decorador: responde a POST |
| `status_code=201` | HTTP 201 Created (éxito al crear) |
| `equipo: EquipoCreate` | FastAPI **valida automáticamente** el body con Pydantic |
| `return crear_equipo(equipo)` | Delega al service |

**¿Qué hace FastAPI automáticamente?**

1. Recibe el JSON del cliente
2. Lo convierte en un objeto `EquipoCreate`
3. Valida con Pydantic (min_length, max_length)
4. Si falla → error 422
5. Si pasa → llama a `crear_equipo(equipo)`

**El router es delgado.** No hay lógica de negocio. Solo recibe y delega.

---

## 6 · Main: punto de entrada

### Archivo: `app/main.py`

```python
from fastapi import FastAPI

from app.routers.equipos import router as equipos_router

app = FastAPI(
    title="API de Equipos",
    description="Ejemplo básico de arquitectura por capas con FastAPI",
    version="1.0.0",
)

app.include_router(equipos_router)
```

**Línea por línea:**

1. `from fastapi import FastAPI` — Importa la clase principal
2. `from app.routers.equipos import router as equipos_router` — Importa el router (con alias para claridad)
3. `app = FastAPI(...)` — Crea la aplicación con metadatos para Swagger
4. `app.include_router(equipos_router)` — Registra las rutas del router

**¿Qué hace `include_router`?**

Sin esta línea, los endpoints no existen. Es como decirle a FastAPI: "Oye, usa este grupo de rutas".

Si quisieras agregar otro módulo (ej: `usuarios`), harías:

```python
from app.routers.usuarios import router as usuarios_router
app.include_router(usuarios_router)
```

---

## 7 · El flujo completo

### Crear un equipo: `POST /equipos/`

```
Cliente envía:
{
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador"
}
        │
        ▼
┌─────────────────────────────────────────────────┐
│ 1. FASTAPI recibe la petición POST              │
│    Ruta: /equipos/                              │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│ 2. PYDANTIC valida el JSON                      │
│    ¿"nombre" tiene ≥3 caracteres?  ✓ SÍ         │
│    ¿"categoria" tiene ≥3 caracteres?  ✓ SÍ      │
│    ¿Faltan campos?  ✓ NO                        │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│ 3. ROUTER recibe EquipoCreate ya validado       │
│    Llama a: crear_equipo(equipo)                │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│ 4. SERVICE ejecuta lógica de negocio            │
│    a. ¿Existe otro "Arduino UNO"?  → NO         │
│    b. Crea diccionario:                         │
│       {id: 1, nombre: "Arduino UNO",            │
│        categoria: "Microcontrolador",            │
│        disponible: true}                        │
│    c. Guarda en _equipos                        │
│    d. _next_id = 2                              │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│ 5. ROUTER devuelve respuesta                    │
│    HTTP 201 Created                             │
│    Body: {"id":1, "nombre":"Arduino UNO", ...}  │
└─────────────────────────────────────────────────┘
        │
        ▼
Cliente recibe:
{
  "id": 1,
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador",
  "disponible": true
}
```

### Crear equipo duplicado: `POST /equipos/`

```
Cliente envía:
{"nombre": "Arduino UNO", "categoria": "Microcontrolador"}
        │
        ▼
Pydantic valida ✓
        │
        ▼
Service verifica: ¿Existe "arduino uno" en _equipos? → SÍ
        │
        ▼
Service lanza: HTTPException(400, "Ya existe un equipo con ese nombre")
        │
        ▼
Cliente recibe:
HTTP 400 Bad Request
{"detail": "Ya existe un equipo con ese nombre"}
```

### Datos inválidos: `POST /equipos/`

```
Cliente envía:
{"nombre": "X", "categoria": "A"}
        │
        ▼
Pydantic valida:
  - "nombre" tiene 1 carácter, necesita ≥3  ✗
  - "categoria" tiene 1 carácter, necesita ≥3  ✗
        │
        ▼
Pydantic lanza error 422 automáticamente
        │
        ▼
Cliente recibe:
HTTP 422 Unprocessable Entity
{"detail": [... errores de validación ...]}
```

---

## 8 · Cómo ejecutar y probar

### Paso 1: Instalar

```bash
cd proyecto/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 2: Ejecutar

```bash
uvicorn app.main:app --reload
```

### Paso 3: Abrir Swagger

Ve a: http://127.0.0.1:8000/docs

Verás la interfaz de Swagger con:
- `GET /equipos/` — en color verde
- `POST /equipos/` — en color azul

### Paso 4: Probar desde Swagger

1. Haz clic en `POST /equipos/`
2. Haz clic en "Try it out"
3. Escribe:
```json
{
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador"
}
```
4. Haz clic en "Execute"
5. Verás la respuesta 201

### Paso 5: Probar GET

1. Haz clic en `GET /equipos/`
2. Haz clic en "Try it out"
3. Haz clic en "Execute"
4. Verás la lista con el equipo creado

### Paso 6: Probar error de duplicado

1. Crea otro equipo con el mismo nombre "Arduino UNO"
2. Verás error 400

### Paso 7: Probar error de validación

1. Crea un equipo con `nombre: "AB"`
2. Verás error 422

---

## 9 · Errores comunes y cómo solucionarlos

### Error: `ModuleNotFoundError: No module named 'app'`

**Causa:** No estás ejecutando uvicorn desde la raíz del proyecto.

**Solución:**
```bash
cd proyecto/          # ← Asegúrate de estar aquí
uvicorn app.main:app --reload
```

### Error: `ImportError: cannot import name 'equipo_service'`

**Causa:** Falta `__init__.py` en la carpeta `services/`.

**Solución:** Crea el archivo vacío:
```bash
touch app/services/__init__.py
```

### Error: `422 Unprocessable Entity`

**Causa:** Los datos no cumplen las validaciones de Pydantic.

**Solución:** Revisa que:
- `nombre` tenga al menos 3 caracteres
- `categoria` tenga al menos 3 caracteres
- Los campos estén escritos correctamente

### Error: `400 Bad Request: Ya existe un equipo con ese nombre`

**Causa:** Estás intentando crear un equipo con un nombre que ya existe.

**Solución:** Usa un nombre diferente o verifica los equipos existentes con GET.

### Error: `NameError: name 'status' is not defined`

**Causa:** No importaste `status` de FastAPI.

**Solución:**
```python
from fastapi import APIRouter, status    # ← Agrega status
```

---

## Resumen

| Concepto | Archivo | Función |
|----------|---------|---------|
| Paquete | `__init__.py` | Marca carpetas como importables |
| Schema | `schemas/equipo.py` | Define y valida estructura de datos |
| Service | `services/equipo_service.py` | Contiene lógica de negocio |
| Router | `routers/equipos.py` | Recibe HTTP, delega al service |
| Main | `main.py` | Crea la app y registra routers |

### Flujo

```
Cliente → Router → Schema → Service → Memoria → Response → Cliente
```

### Regla de oro

> **El router nunca tiene lógica de negocio.**
> **El service nunca sabe de HTTP.**
> **El schema solo define estructura.**

---

**Guía creada para el curso de Desarrollo Web II — Ing. Eduardo Pimienta**
