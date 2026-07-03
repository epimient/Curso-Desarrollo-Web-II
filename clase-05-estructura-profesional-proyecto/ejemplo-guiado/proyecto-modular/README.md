# Proyecto modular - Clase 05

Proyecto FastAPI organizado por capas para Desarrollo Web II.

## Estructura

```text
app/
  main.py
  core/
    config.py
  routers/
    health.py
    courses.py
  schemas/
    course.py
  services/
    course_service.py
```

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

- `GET /health`
- `GET /health/version`
- `GET /courses`
- `GET /courses/{course_id}`
- `POST /courses`

## Documentacion

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
