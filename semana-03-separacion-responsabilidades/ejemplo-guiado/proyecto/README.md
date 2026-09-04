# API de Equipos de Laboratorio

Proyecto mínimo educativo que enseña **arquitectura por capas** con FastAPI.

## Objetivo

Demostrar la separación entre:

- **Router** → recibe peticiones HTTP
- **Schema** → valida y estructura datos con Pydantic
- **Service** → contiene la lógica de negocio

## Estructura

```
proyecto/
├── app/
│   ├── main.py              # Punto de entrada, crea la app
│   ├── routers/
│   │   └── equipos.py       # Endpoints HTTP (delgado)
│   ├── schemas/
│   │   └── equipo.py        # Modelos Pydantic (validación)
│   └── services/
│       └── equipo_service.py # Lógica de negocio
├── requirements.txt
└── README.md
```

## Instalación

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

Abrir http://127.0.0.1:8000/docs para Swagger.

## Pruebas en Swagger

### GET inicial

```
GET /equipos/
```

Respuesta: `[]`

### Crear equipo

```
POST /equipos/
```

Body:

```json
{
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador"
}
```

Respuesta:

```json
{
  "id": 1,
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador",
  "disponible": true
}
```

### Crear segundo equipo

```json
{
  "nombre": "Sensor DHT22",
  "categoria": "Sensor"
}
```

### Error por datos inválidos

```json
{
  "nombre": "X",
  "categoria": "A"
}
```

Error 422: validación de Pydantic (mínimo 3 caracteres).

### Error por nombre duplicado

Crear nuevamente "Arduino UNO":

```json
{
  "nombre": "Arduino UNO",
  "categoria": "Microcontrolador"
}
```

Error 400: `{"detail": "Ya existe un equipo con ese nombre"}`

## Flujo

```
Cliente
  ↓
Router (recibe HTTP)
  ↓
Schema Pydantic (valida datos)
  ↓
Service (lógica de negocio)
  ↓
Lista en memoria
  ↓
Response
  ↓
Cliente
```
