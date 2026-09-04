# API de Equipos de Laboratorio

> Proyecto mínimo educativo de **arquitectura por capas** con FastAPI

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Objetivo

Enseñar cómo se **separa la lógica** en una API REST usando FastAPI:

```
Recibir petición  →  Validar datos  →  Ejecutar lógica  →  Responder
     Router              Schema            Service           HTTP
```

Sin bases de datos, sin autenticación, sin complicaciones. Solo código claro y explicado.

---

## Estructura del proyecto

```
proyecto/
├── app/
│   ├── __init__.py              # Marca "app" como paquete Python
│   ├── main.py                  # Punto de entrada — crea la app FastAPI
│   │
│   ├── routers/
│   │   ├── __init__.py          # Marca "routers" como paquete
│   │   └── equipos.py           # Endpoints: GET y POST /equipos
│   │
│   ├── schemas/
│   │   ├── __init__.py          # Marca "schemas" como paquete
│   │   └── equipo.py            # Modelos Pydantic: EquipoCreate, EquipoResponse
│   │
│   └── services/
│       ├── __init__.py          # Marca "services" como paquete
│       └── equipo_service.py    # Lógica de negocio: listar, crear, validar duplicados
│
├── requirements.txt             # Dependencias: fastapi, uvicorn
└── README.md                    # Este archivo
```

---

## Capas de la arquitectura

### 1. Schema (`schemas/equipo.py`)

Define **qué datos entran** y **qué datos salen**. No contiene lógica.

```python
# Datos que el cliente ENVÍA al crear un equipo
class EquipoCreate(BaseModel):
    nombre: str       # Mínimo 3, máximo 80 caracteres
    categoria: str    # Mínimo 3, máximo 50 caracteres

# Datos que el servidor DEVUELVE
class EquipoResponse(BaseModel):
    id: int
    nombre: str
    categoria: str
    disponible: bool
```

### 2. Service (`services/equipo_service.py`)

Contiene **toda la lógica de negocio**. No sabe nada de HTTP.

```python
_equipos: list[dict] = []    # Lista en memoria (simula una BD)
_next_id = 1                  # Contador de IDs

def listar_equipos() -> list[dict]:
    return _equipos

def crear_equipo(equipo: EquipoCreate) -> dict:
    # 1. Verificar que no exista otro con el mismo nombre
    # 2. Crear diccionario con id, nombre, categoria, disponible=True
    # 3. Guardar en la lista
    # 4. Devolver el equipo creado
```

### 3. Router (`routers/equipos.py`)

**Recibe peticiones HTTP** y las delega al service. No tiene lógica de negocio.

```python
router = APIRouter(prefix="/equipos", tags=["Equipos"])

@router.get("/", response_model=list[EquipoResponse])
def get_equipos():
    return listar_equipos()          # Solo llama al service

@router.post("/", response_model=EquipoResponse, status_code=201)
def post_equipo(equipo: EquipoCreate):
    return crear_equipo(equipo)      # Solo llama al service
```

### 4. Main (`main.py`)

Punto de entrada. Crea la app y registra los routers.

```python
app = FastAPI(title="API de Equipos", version="1.0.0")
app.include_router(equipos_router)
```

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/epimient/Curso-Desarrollo-Web-II.git
cd Curso-Desarrollo-Web-II/semana-03-separacion-responsabilidades/ejemplo-guiado/proyecto

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución

```bash
uvicorn app.main:app --reload
```

Abrir en el navegador:

| URL | Descripción |
|-----|-------------|
| http://127.0.0.1:8000/docs | Swagger UI (probar endpoints) |
| http://127.0.0.1:8000/redoc | ReDoc (documentación formal) |

---

## Endpoints

### `GET /equipos/`

Devuelve todos los equipos almacenados.

**Respuesta 200:**

```json
[
  {
    "id": 1,
    "nombre": "Arduino UNO",
    "categoria": "Microcontrolador",
    "disponible": true
  }
]
```

### `POST /equipos/`

Crea un nuevo equipo.

**Request body:**

```json
{
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador"
}
```

**Respuesta 201:**

```json
{
  "id": 1,
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador",
  "disponible": true
}
```

**Errores posibles:**

| Código | Causa |
|--------|-------|
| 422 | Datos inválidos (nombre < 3 chars, categoría < 3 chars) |
| 400 | Ya existe un equipo con ese nombre (ignora mayúsculas) |

---

## Flujo de una petición

```
┌──────────┐     ┌────────┐     ┌────────┐     ┌─────────┐     ┌──────────┐
│ Cliente  │────▶│ Router │────▶│ Schema │────▶│ Service │────▶│ Memoria  │
│ (curl)   │◀────│        │◀────│        │◀────│         │◀────│ (lista)  │
└──────────┘     └────────┘     └────────┘     └─────────┘     └──────────┘
```

1. **Cliente** envía `POST /equipos/` con JSON
2. **Router** recibe la petición y pasa el body al service
3. **Schema** valida que `nombre` tenga ≥3 caracteres y `categoria` ≥3
4. **Service** verifica duplicados, asigna `id` y `disponible=True`
5. **Memoria** guarda el diccionario en `_equipos`
6. **Router** devuelve `EquipoResponse` con HTTP 201

---

## Dependencias

```
fastapi    — Framework web asíncrono
uvicorn    — Servidor ASGI para desarrollo
```

Sin SQLAlchemy, sin Docker, sin JWT, sin frontend. Solo lo mínimo.

---

## Archivos `__init__.py`

Los archivos `__init__.py` están **vacíos**. Su único propósito es decirle a Python:

> "Esta carpeta es un paquete — se puede importar desde aquí."

Sin `__init__.py`, ejecuciones `from app.schemas.equipo import ...` fallarían.

---

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web |
| [Pydantic](https://docs.pydantic.dev/) | Validación de datos |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [Python 3.10+](https://www.python.org/) | Lenguaje |

---

## Licencia

Proyecto educativo — uso libre para fines académicos.

---

**Desarrollado para el curso de Desarrollo Web II — Ing. Eduardo Pimienta**
