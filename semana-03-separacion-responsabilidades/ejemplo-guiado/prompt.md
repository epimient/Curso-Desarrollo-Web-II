Quiero que construyas un proyecto mínimo educativo con FastAPI para estudiantes universitarios que están aprendiendo arquitectura por capas.

El objetivo principal NO es hacer una aplicación compleja. El objetivo es que el código sea sencillo, claro, explicable línea por línea y que muestre correctamente la separación entre:

* `main.py`
* routers
* schemas
* services

Por ahora NO usar base de datos, Supabase, SQLAlchemy, autenticación ni repositorios. Los datos deben guardarse temporalmente en una lista de Python en memoria.

# Proyecto

Construye una API llamada:

`API de Equipos de Laboratorio`

La API debe permitir inicialmente solamente:

```text
GET  /equipos
POST /equipos
```

El recurso `Equipo` debe tener:

```text
id
nombre
categoria
disponible
```

Ejemplo de respuesta:

```json
{
  "id": 1,
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador",
  "disponible": true
}
```

El cliente NO debe enviar:

```text
id
disponible
```

Esos valores deben ser asignados automáticamente por el servidor.

# Estructura obligatoria

Crea exactamente esta estructura:

```text
proyecto/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── equipos.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── equipo.py
│   │
│   └── services/
│       ├── __init__.py
│       └── equipo_service.py
│
├── requirements.txt
└── README.md
```

NO agregues todavía:

```text
models/
database/
repositories/
core/
auth/
```

La idea es trabajar con arquitectura progresiva.

# 1. Schema

Archivo:

```text
app/schemas/equipo.py
```

Usa Pydantic.

Debe existir:

```python
class EquipoCreate(BaseModel):
```

con:

```text
nombre: str
categoria: str
```

Validaciones:

* `nombre`: mínimo 3 caracteres y máximo 80.
* `categoria`: mínimo 3 caracteres y máximo 50.

Debe existir también:

```python
class EquipoResponse(BaseModel):
```

con:

```text
id: int
nombre: str
categoria: str
disponible: bool
```

El propósito es enseñar claramente la diferencia entre:

```text
datos que entran
vs
datos que salen
```

# 2. Service

Archivo:

```text
app/services/equipo_service.py
```

Debe existir una lista en memoria:

```python
_equipos = []
```

y un contador de IDs:

```python
_next_id = 1
```

Crear las funciones:

```python
listar_equipos()
crear_equipo(equipo)
```

## listar_equipos()

Debe devolver todos los equipos almacenados.

## crear_equipo()

Debe:

1. recibir un objeto `EquipoCreate`;
2. verificar que no exista otro equipo con el mismo nombre;
3. comparar los nombres ignorando mayúsculas/minúsculas;
4. si existe un equipo con el mismo nombre, lanzar:

```python
HTTPException(
    status_code=400,
    detail="Ya existe un equipo con ese nombre"
)
```

5. crear un nuevo diccionario con:

```text
id
nombre
categoria
disponible=True
```

6. guardar el equipo en `_equipos`;
7. incrementar `_next_id`;
8. devolver el equipo creado.

Para verificar duplicados se puede utilizar `any()`.

El código debe ser sencillo y legible. Evita abstracciones innecesarias.

# 3. Router

Archivo:

```text
app/routers/equipos.py
```

Usa:

```python
APIRouter
```

Configura:

```python
prefix="/equipos"
tags=["Equipos"]
```

Crea:

```text
GET /equipos/
```

Debe:

* llamar a `listar_equipos()`;
* devolver una lista de `EquipoResponse`.

Usar:

```python
response_model=list[EquipoResponse]
```

Crea:

```text
POST /equipos/
```

Debe:

* recibir `EquipoCreate`;
* llamar a `crear_equipo()`;
* devolver `EquipoResponse`;
* responder con HTTP 201.

Usar:

```python
status_code=status.HTTP_201_CREATED
```

El router debe ser delgado.

NO pongas lógica de negocio dentro de las funciones de ruta.

Las funciones de ruta deberían limitarse básicamente a:

```python
return listar_equipos()
```

y:

```python
return crear_equipo(equipo)
```

# 4. main.py

Archivo:

```text
app/main.py
```

Debe crear:

```python
app = FastAPI(...)
```

Usar:

```text
title="API de Equipos"
description="Ejemplo básico de arquitectura por capas con FastAPI"
version="1.0.0"
```

Importar el router de equipos y registrarlo con:

```python
app.include_router(...)
```

No agregues lógica de negocio en `main.py`.

# 5. requirements.txt

Debe contener únicamente las dependencias realmente necesarias para ejecutar el proyecto.

Como mínimo:

```text
fastapi
uvicorn
```

No agregues dependencias innecesarias.

# 6. README.md

Crea un README sencillo y educativo.

Debe explicar:

## Objetivo

Que este proyecto enseña arquitectura básica con FastAPI usando:

```text
Router
Schema
Service
```

## Estructura de carpetas

Explicar brevemente qué responsabilidad tiene:

```text
main.py
routers/
schemas/
services/
```

## Instalación

Explicar cómo crear un entorno virtual:

```bash
python -m venv venv
```

Activación Linux/macOS:

```bash
source venv/bin/activate
```

Activación Windows:

```bash
venv\Scripts\activate
```

Instalación:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

## Swagger

Indicar:

```text
http://127.0.0.1:8000/docs
```

# 7. Ejemplos para probar

Documenta en el README estas pruebas.

## GET inicial

```text
GET /equipos/
```

Debe devolver:

```json
[]
```

## Crear equipo

```text
POST /equipos/
```

Body:

```json
{
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador"
}
```

Respuesta esperada:

```json
{
  "id": 1,
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador",
  "disponible": true
}
```

## Crear segundo equipo

```json
{
  "nombre": "Sensor DHT22",
  "categoria": "Sensor"
}
```

Después:

```text
GET /equipos/
```

debe devolver ambos equipos.

## Error Pydantic

Probar:

```json
{
  "nombre": "X",
  "categoria": "A"
}
```

Debe producir error de validación.

## Error de negocio

Intentar crear nuevamente:

```json
{
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador"
}
```

Debe producir:

```text
HTTP 400
```

con:

```json
{
  "detail": "Ya existe un equipo con ese nombre"
}
```

# 8. Restricciones importantes

No agregues:

* base de datos;
* Supabase;
* SQLAlchemy;
* SQLModel;
* autenticación;
* JWT;
* repositorios;
* Docker;
* frontend;
* tests avanzados;
* patrones adicionales;
* clases service innecesarias;
* async si no aporta nada al ejemplo;
* configuración compleja.

No conviertas el proyecto en una arquitectura empresarial.

El objetivo es que un estudiante principiante pueda explicar absolutamente cada línea.

# 9. Criterios de calidad

El proyecto debe:

* ejecutar correctamente;
* permitir probar todos los endpoints desde `/docs`;
* tener imports correctos;
* respetar la estructura indicada;
* tener funciones cortas;
* tener nombres claros;
* separar validación estructural y lógica de negocio;
* evitar código duplicado;
* evitar sobreingeniería.

Antes de terminar:

1. revisa todos los imports;
2. ejecuta la aplicación;
3. verifica `GET /equipos/`;
4. verifica `POST /equipos/`;
5. verifica error por datos inválidos;
6. verifica error por nombre duplicado;
7. confirma que Swagger funciona en `/docs`.

Finalmente muestra:

1. árbol de carpetas;
2. contenido completo de cada archivo;
3. instrucciones de ejecución;
4. breve explicación del flujo:

```text
Cliente
  ↓
Router
  ↓
Schema Pydantic
  ↓
Service
  ↓
Lista en memoria
  ↓
Response
  ↓
Cliente
```

No agregues características adicionales sin que sean solicitadas.
