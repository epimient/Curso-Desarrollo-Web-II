# Proyecto base - Clase 04

API minima construida con FastAPI para la Clase 04 de Desarrollo Web II.

## Requisitos

- Python 3.10 o superior.
- Entorno virtual recomendado.

## Instalacion

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecucion

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `GET /`
- `GET /estado`
- `GET /saludo/{nombre}`
- `GET /cursos`
- `GET /cursos?activo=false`

## Documentacion

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
