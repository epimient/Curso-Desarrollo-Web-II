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
10. [Type Hints en Python](#10--type-hints-en-python)
11. [CRUD completo](#11--crud-completo)

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

### Analogía 1: La placa en la puerta

Piensa en `__init__.py` como una **placa en la puerta** de una oficina:

- Con la placa: "Esta oficina existe, puedes entrar"
- Sin la placa: "No sé qué es este lugar"

### Analogía 2: El edificio de oficinas

Cada **carpeta** es un **edificio**. Cada **archivo `.py`** es una **oficina**. Los `__init__.py` son las **placas en la entrada**.

```
Un visitante quiere llegar a la oficina "equipo.py"
dentro del edificio "schemas".

Con placa:   from app.schemas.equipo import EquipoCreate   ✅
Sin placa:   from app.schemas.equipo import EquipoCreate   ❌ "no existe ese edificio"
```

La placa no hace nada útil por sí sola — solo dice **"este edificio existe y se puede visitar"**.

### Analogía 3: La agenda telefónica

Python quiere **llamar por teléfono** a un archivo:

```
from app.schemas.equipo import EquipoCreate

Python marca:  "app" → "schemas" → "equipo"
                │         │          └── contesto yo (el archivo)
                │         └── ¿existe? → necesita AGENDA __init__.py
                └── ¿existe? → necesita AGENDA __init__.py
```

`__init__.py` es la **agenda telefónica** de Python: sin el número, la llamada no conecta.

### Resumen en 3 frases

> **1.** `__init__.py` le dice a Python: "esta carpeta es un paquete, puedes importar sus archivos".
>
> **2.** El archivo **existe pero está vacío** — puedes abrirlo y no verás nada.
>
> **3.** Si una carpeta con código Python **no lo tiene**, los imports fallan con `ModuleNotFoundError`.

### Truco para recordar

> **"Carpeta que se importa → necesita placa. Carpeta que no se importa → no le pongas placa."**

Regla práctica:
- Contiene `.py` que otro archivo importa → **sí** `__init__.py`
- Contiene solo HTML, textos, imágenes o PDFs → **no**

### ¿Los tengo que crear yo?

**Sí.** Tú como programador **debes crearlos**. Son archivos vacíos — no tienen código — pero **deben existir**.

Cómof crearlos:

```bash
# Linux / macOS
touch app/__init__.py
touch app/routers/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
```

Windows:

```bash
type nul > app\__init__.py
type nul > app\routers\__init__.py
type nul > app\schemas\__init__.py
type nul > app\services\__init__.py
```

### ¿Todas las carpetas de la API necesitan uno?

**No.** Solo las que contienen archivos `.py` que se **importan desde otro lugar**.

| ¿Contiene `.py` que se importa? | ¿Necesita `__init__.py`? |
|----------------------------------|--------------------------|
| `app/schemas/` | Sí — `equipo.py` se importa como `app.schemas.equipo` |
| `app/services/` | Sí — `equipo_service.py` se importa como `app.services.equipo_service` |
| `app/routers/` | Sí — `equipos.py` se importa como `app.routers.equipos` |
| `html/` | No — solo tiene `index.html`, no se importa Python |
| `ejemplo-guiado/` | No — solo tiene archivos `.md` y subcarpetas de código |

Si mañana creas `app/models/` para base de datos → **sí**, necesitas `__init__.py`.
Si creas `app/docs/` para documentación markdown → **no**, no lo necesitas.

### Pregunta de confirmación

> *¿Dónde NO hace falta `__init__.py`?*
>
> A) `app/schemas/`
> B) `app/html/` ← **Correcta**: no hay Python importable
> C) `app/services/`
> D) `app/routers/`

**Regla de oro:** Si no lo sabes con certeza, revísalo: si la carpeta tiene `.py` que otros archivos importan → créalo.

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

#### Los tres puntos `...`: ¿qué significan?

Los tres puntos `...` (Ellipsis) significan: **"este campo es obligatorio"**.

```python
nombre: str = Field(..., min_length=3, max_length=80)
#              ^^^
#            "NO hay valor por defecto, el cliente DEBE enviarlo"
```

| Sintaxis | Significado |
|----------|-------------|
| `Field(...)` | **Obligatorio** — el cliente debe enviarlo, no tiene valor por defecto |
| `Field("Valor")` | Opcional — si no lo envían, usa "Valor" |
| `Field(0)` | Opcional — si no lo envían, usa 0 |
| `nombre: str` (sin Field) | También es obligatorio (el `...` es implícito) |

**Analogía:** Es como un formulario de registro:

```
Nombre:   ____________   ← Campo vacío = "..." = el usuario DEBE llenarlo
```

vs.

```
Estado civil: [Soltero]   ← Valor por defecto = el usuario puede dejarlo así
```

**¿Qué pasa si el cliente no envía `nombre`?**

Pydantic devuelve error 422:

```json
{"detail": [{"loc": ["body", "nombre"], "msg": "Field required", ...}]}
```

> **Dato extra:** En Python puro, `...` es el valor `Ellipsis`. Pero en Pydantic se usa **únicamente** como marcador de "aquí va el valor del cliente, yo no pongo default".

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

### ¿Por qué `any()` y no un `if`?

#### ¿De dónde sale la `e`?

La `e` **la inventas tú** — es la variable del bucle:

```python
for e in _equipos:     # "para cada e (equipo) dentro de la lista"
```

Es igual que en `for i in range(10)` donde la `i` la pones tú. Aquí la `e` representa **cada diccionario** de la lista `_equipos`:

```python
_equipos = [
    {"id": 1, "nombre": "Arduino UNO",    "categoria": "Microcontrolador", "disponible": True},
    {"id": 2, "nombre": "Sensor DHT22",  "categoria": "Sensor",           "disponible": True},
]
```

Por eso se accede con `e["nombre"]` (como a un diccionario), no con `e.nombre`.

#### ¿Qué es `any()`?

Una **función nativa** de Python — siempre existe, no necesitas importarla.

Recibe una lista de valores booleanos y devuelve:

| Si tiene... | Devuelve |
|-------------|----------|
| Todos `False` | `False` |
| **Al menos un** `True` | `True` |

```python
any([False, False, False])  # → False
any([False, True, False])   # → True
```

#### ¿Qué es la estructura `... for e in _equipos`?

Es una **expresión generadora**: construye una lista de `True`/`False` sobre la marcha.

Paso a paso con 2 equipos en `_equipos`:

```python
# Turno 1:  e = {"nombre": "Arduino UNO", ...}
#           "arduino uno" == "arduino uno"   → True

# Turno 2:  e = {"nombre": "Sensor DHT22", ...}
#           "sensor dht22" == "arduino uno"  → False

# any([True, False]) → True  → existe = True  → error 400
```

Si **ninguno** fuera igual (turno 1 = False, turno 2 = False):

```python
any([False, False]) → False → no hay duplicado → se crea el equipo
```

#### ¿Por qué `any()` y no un `for` + `if`?

Las dos formas son **equivalentes**. Mira la diferencia:

**Versión A — con `any()` (la que usamos):**

```python
existe = any(
    e["nombre"].lower() == equipo.nombre.lower() for e in _equipos
)
if existe:
    raise HTTPException(400, "Ya existe un equipo con ese nombre")
```

**Versión B — con bucle `for` + `if` (también funciona):**

```python
existe = False
for e in _equipos:
    if e["nombre"].lower() == equipo.nombre.lower():
        existe = True
        break              # ← hay que recordar "parar"
if existe:
    raise HTTPException(400, "Ya existe un equipo con ese nombre")
```

| Criterio | `any()` | `for` + `if` |
|----------|---------|--------------|
| Líneas de código | 1 | 5 |
| Intención | Dice "¿existe alguno?" directamente | Repites la lógica manual |
| Error de novato | Menos probable | Fácil olvidar `break` |
| Estilo | Elegante pero más abstracto | Más explícito pero verboso |

> **Conclusión:** `any()` es como preguntar *"¿hay alguno igual?"* en una sola línea. El bucle `for` + `if` es como revisar **uno por uno** y apuntar en una libreta. Funcionan igual, pero `any()` es más legible una vez que entiendes la sintaxis.

**Resumen:** la `e` la inventas tú (variable del bucle), `any()` es una función nativa de Python, y la estructura `for e in _equipos` es un generador que construye `True`/`False` por cada equipo y luego `any()` revisa si hubo al menos un `True`.

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

### ¿De dónde viene el parámetro `equipo`?

Cuando un cliente hace `POST /equipos/` con este JSON:

```json
{
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador"
}
```

FastAPI hace **automáticamente** esto por ti:

```python
# 1. Recibe el texto JSON de la red
# 2. Lo convierte a objeto EquipoCreate validando con Pydantic
equipo = EquipoCreate(nombre="Arduino UNO", categoria="Microcontrolador")

# 3. Y lo mete en tu función
post_equipo(equipo=equipo)
```

Tu función **NO recibe texto**. Recibe un objeto con atributos:

```python
def post_equipo(equipo: EquipoCreate):
    equipo.nombre      # "Arduino UNO"     (accede como objeto)
    equipo.categoria   # "Microcontrolador"
    return crear_equipo(equipo)
```

**Analogía:** Tu función es un **chef**:

```
Cliente hace pedido → JSON crudo (una hoja de papel)
FastAPI es el mesero → lee el pedido, valida que "esté bien escrito"
Tu función es el chef → recibe EL PEDIDO YA ORDENADO (objeto EquipoCreate)
```

El chef no lee el papel crudo — el mesero (FastAPI) ya lo interpretó y lo sirvió ordenado.

### Tipos de parámetros: de dónde viene cada uno

```python
def post_equipo(
    equipo: EquipoCreate,      # ← Body JSON (cuerpo de la petición)
    categoria: str,            # ← Query param (?categoria=Sensor)
    equipo_id: int             # ← Path param (/equipos/5)
):
```

| Tipo del parámetro | De dónde viene | Ejemplo |
|--------------------|----------------|---------|
| Modelo Pydantic (`EquipoCreate`) | **Body** (cuerpo del JSON) | POST con JSON |
| `str`, `int`, `bool` simple | **Query** (después de `?`) | `?categoria=Sensor` |
| Coincide con ruta `{equipo_id}` | **Path** (en la URL) | `/equipos/5` |

### La firma es un contrato de validación

Con `equipo: EquipoCreate` le estás diciendo a FastAPI:

> "El body de esta petición debe validarse y convertirse al modelo `EquipoCreate`"

La conexión entre los archivos:

```
routers/equipos.py              schemas/equipo.py
┌───────────────────────────┐  ┌──────────────────────────┐
│ equipo: EquipoCreate       │──▶│ class EquipoCreate:      │
│                           │  │   nombre: str (3-80)     │
└───────────────────────────┘  │   categoria: str (3-50)  │
   "usa este modelo"           └──────────────────────────┘
   (importado arriba)          "aquí están las reglas"
                               (aquí está la definición)
```

La **firma de tu función es un CONTRATO**: "Para llamar a `post_equipo`, el body debe cumplir las reglas de `EquipoCreate`."

### ¿Por qué parece que se valida dos veces?

Ves `EquipoCreate` en el router **y** en el service:

```python
# router — ¿valida?
def post_equipo(equipo: EquipoCreate):    # ← AQUÍ se valida (1 vez)

# service — ¿valida?
def crear_equipo(equipo: EquipoCreate):   # ← NO valida, es documentación
```

**En realidad solo se valida UNA vez**, en el router.

| Capa | ¿Valida? | Por qué lo parece |
|------|----------|-------------------|
| Router (`equipo: EquipoCreate`) | **SÍ** — aquí se corre la validación | Es donde FastAPI construye el objeto |
| Service (`equipo: EquipoCreate`) | **NO** — solo type hint | Es solo documentación para el programador |

**Analogía:** El router es el **guardia de seguridad** de la entrada:

```
Router (guardia):  "Muéstrame tu identificación" → Pydantic la revisa
Service (técnico): "Este es el visitante ya aprobado" → trabaja con confianza
```

El service **no revisa nada** porque asume que el guardia ya lo hizo. El `EquipoCreate` que escribe en la firma es solo el **uniforme** que muestra: "yo trabajo con visitantes aprobados".

**Punto clave:** Nunca llamas tú a esa función. FastAPI la llama solo cuando llega una petición `POST /equipos/`, y **si el JSON tiene datos inválidos, tu función ni siquiera se ejecuta** — Pydantic lanza error 422 antes.

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

## 10 · Type Hints en Python

### ¿Qué es un type hint?

Un type hint es una **anotación de tipo** que le dice al programador (y a herramientas como PyCharm, VS Code o mypy) qué tipo de dato se espera en una variable, parámetro o función.

```python
nombre: str = "Arduino UNO"          # ← "nombre es un string"
edad: int = 25                       # ← "edad es un entero"
activo: bool = True                  # ← "activo es un booleano"
equipos: list[dict] = []             # ← "equipos es una lista de diccionarios"
```

### Ejemplos en nuestro proyecto

```python
# Parámetro: "equipo debe ser un objeto EquipoCreate"
def crear_equipo(equipo: EquipoCreate) -> dict:
    ...

# Return: "esta función devuelve una lista de diccionarios"
def listar_equipos() -> list[dict]:
    return _equipos

# Variable: "es una lista de diccionarios"
_equipos: list[dict] = []
```

### La diferencia clave: type hint ≠ validación

```python
def saludar(nombre: str):
    print(f"Hola {nombre}")

saludar(123)      # ← Funciona, Python no lanza error
saludar(True)     # ← Funciona también
```

**Python NO valida los type hints en tiempo de ejecución.** Son "adornos" — documentos para el programador.

| Anotación | ¿Qué hace Python en runtime? |
|-----------|------------------------------|
| `nombre: str` | Nada — solo recuerda el nombre para el editor |
| `def f(x: int) -> str:` | Nada — no verifica que x sea int ni que devuelvas str |

**¿Por qué existen entonces?**

1. **Documentación** — Sabes qué tipo de dato esperas sin leer todo el código
2. **Autocompletado** — El editor te sugiere `.nombre`, `.categoria`, etc.
3. **Legibilidad** — Otro programador entiende rápido qué hace la función
4. **Detección de errores** — Herramientas como `mypy` o `Pylance` detectan inconsistencias **antes** de ejecutar

### Type hints en Pydantic (sí validan)

Pydantic **sí usa** los type hints para validar:

```python
class EquipoCreate(BaseModel):
    nombre: str           # ← Pydantic SÍ valida: "nombre debe ser str"
    categoria: str        # ← Pydantic SÍ valida: "categoria debe ser str"
```

¿Por qué Pydantic sí y Python no? Porque Pydantic **reescribe el código** internamente: lee las anotaciones y genera código de validación automática.

### Conexión con el service

```python
# service
def crear_equipo(equipo: EquipoCreate) -> dict:
    ...
```

El `EquipoCreate` aquí **no valida**. Solo documenta: "esta función recibe objetos EquipoCreate". Por eso no hay "doble validación" — el service confía en que el router ya validó.

### Resumen

| Concepto | ¿Valida? | Para qué sirve |
|----------|----------|----------------|
| Type hints de Python (`nombre: str`) | No | Documentación, autocompletado, legibilidad |
| Pydantic (`class EquipoCreate(BaseModel)`) | Sí | Validación automática de datos |
| FastAPI + Pydantic (`equipo: EquipoCreate`) | Sí (solo en el router) | Convierte JSON a objeto validado |

> **Regla:** Los type hints son **para humanos y herramientas**. Pydantic es **para datos**. FastAPI usa Pydantic para que los type hints **sí validen** en el punto de entrada.

---

## 11 · CRUD completo

### ¿Qué es CRUD?

CRUD son las **4 operaciones básicas** que se pueden hacer con cualquier recurso:

| Operación | HTTP | Qué hace |
|-----------|------|----------|
| **C**reate | POST | Crear un equipo nuevo |
| **R**ead | GET | Leer equipos (lista o uno por ID) |
| **U**pdate | PUT | Actualizar un equipo existente |
| **D**elete | DELETE | Eliminar un equipo |

### Endpoints finales

| Método | Ruta | Función |
|--------|------|---------|
| `GET` | `/equipos/` | Listar todos |
| `GET` | `/equipos/{equipo_id}` | Obtener uno por ID |
| `POST` | `/equipos/` | Crear nuevo |
| `PUT` | `/equipos/{equipo_id}` | Actualizar |
| `DELETE` | `/equipos/{equipo_id}` | Eliminar |

### Nuevo concepto: Path Parameters

Cuando pones `{equipo_id}` en la ruta, FastAPI extrae ese valor y lo convierte al tipo que indiques en la función:

```python
@router.get("/{equipo_id}", response_model=EquipoResponse)
def get_equipo(equipo_id: int):       # ← FastAPI convierte el string "1" a int
    return obtener_equipo(equipo_id)   #    Si no es número → error 422
```

**Ruta:** `GET /equipos/1` → FastAPI ve `1` → lo pasa como `equipo_id: int = 1`

**Error:** `GET /equipos/abc` → FastAPI ve `abc` → no puede convertir a int → error 422

### Nuevo concepto: HTTP 404

Cuando el ID no existe en la lista, el service lanza un error 404:

```python
def obtener_equipo(equipo_id: int) -> dict:
    for e in _equipos:
        if e["id"] == equipo_id:
            return e
    raise HTTPException(           # ← Si el bucle termina sin encontrar
        status_code=404,           #    "Equipo no encontrado"
        detail="Equipo no encontrado",
    )
```

El 404 significa: **"El recurso no existe"**. Es diferente al 422 (datos inválidos) y al 400 (error de negocio).

### GET por ID — `obtener_equipo()`

```python
def obtener_equipo(equipo_id: int) -> dict:
    for e in _equipos:
        if e["id"] == equipo_id:
            return e
    raise HTTPException(404, "Equipo no encontrado")
```

**Qué hace:** Recorre la lista y devuelve el equipo cuyo `id` coincida. Si ninguno coincide, lanza 404.

**¿Por qué un `for` y no `any()`?** Porque aquí necesitamos **devolver el equipo entero**, no solo verificar si existe. `any()` solo dice True/False.

### PUT — `actualizar_equipo()`

```python
def actualizar_equipo(equipo_id: int, datos: EquipoCreate) -> dict:
    for i, e in enumerate(_equipos):
        if e["id"] == equipo_id:
            duplicado = any(
                e2["nombre"].lower() == datos.nombre.lower()
                and e2["id"] != equipo_id          # ← ¡Excluir el equipo actual!
                for e2 in _equipos
            )
            if duplicado:
                raise HTTPException(400, "Ya existe otro equipo con ese nombre")
            _equipos[i]["nombre"] = datos.nombre
            _equipos[i]["categoria"] = datos.categoria
            return _equipos[i]
    raise HTTPException(404, "Equipo no encontrado")
```

**Detalle importante:** La condición `and e2["id"] != equipo_id` **excluye el equipo que se está editando**. Sin esto, si intentas cambiar "Arduino UNO" a "Arduino UNO" (sin cambiar nada), el `any()` siempre encontraría una coincida y daría error.

**¿Qué es `enumerate()`?** Una función que devuelve **índice + valor** en cada vuelta:

```python
for i, e in enumerate(_equipos):
    # i = 0, 1, 2... (posición en la lista)
    # e = {"id": 1, "nombre": "Arduino UNO", ...} (el equipo)
```

Esto permite modificar `_equipos[i]` directamente.

### DELETE — `eliminar_equipo()`

```python
def eliminar_equipo(equipo_id: int) -> dict:
    for i, e in enumerate(_equipos):
        if e["id"] == equipo_id:
            return _equipos.pop(i)    # ← pop() quita y devuelve el elemento
    raise HTTPException(404, "Equipo no encontrado")
```

**¿Qué hace `pop(i)`?** Quita el elemento en la posición `i` de la lista **y lo devuelve**. La lista queda más corta y el cliente recibe el equipo eliminado.

### Router: CRUD completo

```python
@router.get("/{equipo_id}", response_model=EquipoResponse)
def get_equipo(equipo_id: int):
    return obtener_equipo(equipo_id)

@router.put("/{equipo_id}", response_model=EquipoResponse)
def put_equipo(equipo_id: int, equipo: EquipoCreate):
    return actualizar_equipo(equipo_id, equipo)

@router.delete("/{equipo_id}", response_model=EquipoResponse)
def delete_equipo(equipo_id: int):
    return eliminar_equipo(equipo_id)
```

**Nota:** El router sigue siendo delgado — solo llama al service. Toda la lógica está en `equipo_service.py`.

### Orden de los endpoints: importa

```python
@router.get("/")              # ← Lista (sin parámetro)
@router.get("/{equipo_id}")   # ← Uno por ID (con parámetro)
```

**¿Por qué el `/` primero?** Si `/equipos/{equipo_id}` estuviera primero, FastAPI intentaría interpretar "equipos" como un `equipo_id` y todo saldría mal.

**Regla:** Rutas fijas (`/`) siempre van **antes** que rutas con parámetros (`/{id}`).

### Resumen del CRUD

| Concepto | Qué introduce |
|----------|---------------|
| `{equipo_id}` | Path parameter — extrae el ID de la URL |
| `: int` | FastAPI convierte string a entero (error 422 si falla) |
| `HTTPException(404, ...)` | "El recurso no existe" |
| `enumerate()` | Índice + valor para modificar la lista |
| `.pop(i)` | Quitar y devolver un elemento |
| `and e2["id"] != equipo_id` | Excluir el equipo actual en PUT |
| **Orden de rutas** | Rutas fijas antes que rutas con parámetros |

---

## Resumen

| Concepto | Archivo | Función |
|----------|---------|---------|
| Paquete | `__init__.py` | Marca carpetas como importables |
| Schema | `schemas/equipo.py` | Define y valida estructura de datos |
| Service | `services/equipo_service.py` | Contiene lógica de negocio |
| Router | `routers/equipos.py` | Recibe HTTP, delega al service |
| Main | `main.py` | Crea la app y registra routers |
| Type Hints | En cualquier `.py` | Anotaciones de tipo para documentación y autocompletado |
| CRUD | Router + Service | Crear, leer, actualizar, eliminar |

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
