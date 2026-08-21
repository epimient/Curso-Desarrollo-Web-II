# AGENTS.md — Curso Desarrollo Web II (FastAPI)

## Naturaleza

Este repo es un **curso de 17 semanas de FastAPI** (1 pre-requisito + 16 regulares), no una aplicacion unica.  
Cada `semana-XX-*/` contiene su propio `clase-XX.md`, `ejemplo-guiado/` (proyecto FastAPI funcional), `ejercicios/`, `dudas/`, `html/` (slides) y `README.md`.

## Sin build step

El sitio de aterrizaje (SPA estatica, GitHub Pages) es **100% estatico**. Sin bundler:
```bash
python -m http.server 8000   # y abrir http://localhost:8000
```

## Hash routing (facil de errar)

- Toda navegacion usa `#/clase-XX/slides` o `#/clase-XX/docs`.
- URL completa: `https://epimient.github.io/Curso-Desarrollo-Web-II/#/clase-07/docs`
- Boton "Volver" -> `navStack` (hash anterior).
- Los slides son HTML en `semana-XX/html/`, renderizados en `<iframe>`.
- El markdown (`clase-XX.md`) se renderiza client-side con `marked.min.js` + `highlight.min.js` (CDN, atom-one-dark).

## Pagina de aterrizaje

- `index.html` — skeleton, 59 lineas, refs externas con `defer` + `rel="stylesheet"`
- `landing.css` — Tokio Nights, glassmorphism
- `landing.js` — SPA: navegacion, routing, renderizado
- `data.js` — UNITS (16 semanas) + RESOURCES
- `engine/` — `slides.css`, `slides.js` (flechas/swipe), `swagger-anatomia.md`

## Estructura del curso (17 semanas)

### Pre-requisito (Semana 0)
- Semana 00: Introduccion a Python, APIs y FastAPI

### Unidad 1 — Fundamentos MVC y Frameworks (Semanas 1-5)
- Semana 01: Introduccion al curso (HTTP, REST, Swagger)
- Semana 02: Concepto, componentes e interaccion del MVC
- Semana 03: Separacion de responsabilidades
- Semana 04: Frameworks web: conceptos, ventajas y limitaciones
- Semana 05: **Parcial 1**

### Unidad 2 — FastAPI Fundamentals (Semanas 6-11)
- Semana 06: Seleccion de un framework especifico (FastAPI)
- Semana 07: Instalacion y configuracion
- Semana 08: Estructura y organizacion de proyecto
- Semana 09: Creacion y configuracion de app basica (Pydantic)
- Semana 10: Ejecucion y validacion (JWT, middleware, CORS)
- Semana 11: **Parcial 2**

### Unidad 3 — FastAPI Intermedio (Semanas 12-15)
- Semana 12: Creacion y manejo de rutas (APIRouter)
- Semana 13: Routers, logica de negocio y SQLAlchemy
- Semana 14: Motores de plantillas y testing (pytest)
- Semana 15: **Parcial 3**

### Unidad 4 — Cierre (Semana 16)
- Semana 16: Retroalimentacion y despliegue (Render + Supabase)

## Variables CSS Tokio Nights

```css
--bg-base: #1a1b2e;  --bg-panel: #24283b;
--cyan: #7dcfff;     --blue: #7aa2f7;
--green: #9ece6a;    --red: #f7768e;
--orange: #ff9e64;   --purple: #9d7cd8;
```

## Stack Python (codigo de ejemplo)

- **Framework:** FastAPI (`fastapi[standard]`)
- **ORM:** SQLAlchemy
- **Auth:** `passlib[bcrypt]` + `python-jose[cryptography]` (JWT)
- **Settings:** `pydantic-settings`
- **DB:** SQLite en desarrollo, PostgreSQL (via `psycopg2-binary`) en produccion
- **Testing:** `TestClient` de FastAPI, BD SQLite en test, `conftest.py` con `override_get_db()`
- **Tests:** `pytest app/tests/`

### Dependencias tipicas (`requirements.txt`)

```
fastapi[standard]
sqlalchemy
passlib[bcrypt]
bcrypt==4.0.1
python-jose[cryptography]
pydantic-settings
psycopg2-binary
```

## Despliegue (Render — sin Docker)

- Build: `pip install -r requirements.txt`
- Start: `fastapi run app/main.py --port 10000`
- **No Docker, no Dockerfile, no .dockerignore**

## Git

- Rama: `master`
- Origen: `https://github.com/epimient/Curso-Desarrollo-Web-II.git`
- `.gitignore`: `__pycache__/`, `*.py[cod]`, `*.db`, `venv/`, `.env`, `.coverage`, `.pytest_cache/`, `.vscode/`, `.idea/`
