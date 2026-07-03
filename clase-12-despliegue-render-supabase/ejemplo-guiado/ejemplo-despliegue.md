# Ejemplo guiado — Desplegar API FastAPI en Render + Supabase

## Objetivo

Llevar tu API academica a produccion usando Render (web service) y Supabase (base de datos PostgreSQL).

Al final de este ejemplo, tendras tu API corriendo en internet con una URL publica.

---

## Paso 0. Requisitos previos

Antes de empezar, asegurate de tener:

- [ ] Cuenta en [GitHub](https://github.com)
- [ ] Cuenta en [Render](https://render.com) (conectar con GitHub)
- [ ] Cuenta en [Supabase](https://supabase.com)
- [ ] Tu proyecto funcionando con tests pasando

---

## Paso 1. Configurar variables de entorno con pydantic-settings

### 1.1 Instalar la libreria

```bash
pip install pydantic-settings psycopg2-binary
```

**Explicacion:** `pydantic-settings` permite que `Settings` lea automaticamente variables de entorno y archivos `.env`. `psycopg2-binary` es el conector de Python a PostgreSQL.

### 1.2 Actualizar config.py

Reemplaza el contenido de `app/core/config.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    allowed_hosts: list[str] = [
        "localhost",
        "127.0.0.1",
    ]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
```

**Explicacion linea por linea:**

| Linea | Que cambia |
|---|---|
| `from pydantic_settings import...` | Nueva importacion |
| `model_config = SettingsConfigDict(env_file=".env")` | Lee variables desde `.env` y del entorno del sistema |
| `secret_key: str = "changeme"` | Default seguro: obliga a cambiarlo en produccion |

### 1.3 Crear .env (para desarrollo)

```bash
# .env — NO subir a Git
DATABASE_URL=sqlite:///./cursos.db
SECRET_KEY=miclave_secreta_local
ENVIRONMENT=development
```

### 1.4 Crear .env.example (para compartir)

```bash
# .env.example — SI subir a Git (sin valores reales)
DATABASE_URL=sqlite:///./cursos.db
SECRET_KEY=changeme
ENVIRONMENT=development
```

---

## Paso 2. Actualizar database.py

Elimina el `connect_args` especifico de SQLite para que funcione con cualquier base de datos:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
```

**Explicacion:** El unico cambio es que eliminamos `connect_args={"check_same_thread": False}` que solo funcionaba con SQLite. Ahora `create_engine(settings.database_url)` funciona con cualquier motor soportado por SQLAlchemy.

---

## Paso 3. Crear proyecto en Supabase

1. Ve a [supabase.com](https://supabase.com) e inicia sesion
2. Haz clic en **New project**
3. Configura:

| Campo | Valor |
|---|---|
| Name | `api-academica-db` |
| Database Password | Genera una segura (la necesitaras) |
| Region | La mas cercana a ti |
| Pricing Plan | Free |

4. Espera ~2 minutos mientras se crea la base de datos
5. Ve a **Project Settings → Database → Connection string**

Veras algo como:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxxx.supabase.co:5432/postgres
```

6. Reemplaza `[YOUR-PASSWORD]` con la contraseña que creaste en el paso 3
7. Guarda esta URL — la necesitaras en Render

> **Importante:** La contraseña debe estar codificada en URL si tiene caracteres especiales (ej: `%40` para `@`, `%21` para `!`).

---

## Paso 4. Subir el codigo a GitHub

```bash
# Desde la raiz de tu proyecto:
echo "*.db" >> .gitignore
echo ".env" >> .gitignore
echo "__pycache__" >> .gitignore

git init
git add .
git commit -m "Configurar variables de entorno y produccion"
git remote add origin https://github.com/tu-usuario/api-academica.git
git push -u origin main
```

---

## Paso 5. Desplegar en Render

### 5.1 Conectar GitHub

1. Ve a [render.com](https://render.com) e inicia sesion
2. Haz clic en **New + → Web Service**
3. Conecta tu repositorio de GitHub (busca `api-academica`)
4. Haz clic en **Connect**

### 5.2 Configurar el servicio

| Campo | Valor |
|---|---|
| **Name** | `api-academica` |
| **Region** | `Frankfurt` o la mas cercana |
| **Runtime** | `Python 3` |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `fastapi run app/main.py --port 10000` |
| **Plan** | Free |

> **Nota:** `fastapi run` usa `uvicorn` internamente con configuracion optimizada para produccion. Render ejecuta `pip install` automaticamente — no necesitas Docker.

### 5.3 Agregar variables de entorno

Haz clic en **Advanced** y luego en **Add Environment Variable**:

| Key | Value |
|---|---|
| `DATABASE_URL` | `postgresql://postgres:password@db.xxx.supabase.co:5432/postgres` |
| `SECRET_KEY` | (`openssl rand -hex 32` en terminal, pega el resultado) |
| `ENVIRONMENT` | `production` |
| `CORS_ORIGINS` | `["https://api-academica.onrender.com"]` |
| `ALLOWED_HOSTS` | `[".onrender.com"]` |

### 5.4 Crear y esperar

Haz clic en **Create Web Service**. Render:
1. Clona tu repositorio
2. Instala dependencias con `pip install -r requirements.txt`
3. Inicia la aplicacion con `fastapi run`
4. Verifica que responde

El proceso toma ~3 minutos. Veras los logs en vivo en el dashboard.

---

## Paso 6. Verificar el despliegue

Una vez que el status cambie a **Live**:

```bash
# Probar health check
curl https://api-academica.onrender.com/health/
# → {"status": "ok"}

# Probar documentacion (abre en el navegador)
open https://api-academica.onrender.com/docs
```

**Prueba completa desde Swagger UI:**
1. Abre `https://api-academica.onrender.com/docs`
2. Registra un usuario: `POST /users/register`
3. Haz login: `POST /token`
4. Usa el boton **Authorize** para pegar el token
5. Crea un curso: `POST /courses/`
6. Lista cursos: `GET /courses/`

> **Nota:** La primera request puede tardar ~30 segundos (cold start del free tier). Las siguientes seran rapidas mientras el servicio este activo.

---

## Paso 7. (Opcional) Render Blueprint

Crea `render.yaml` en la raiz de tu proyecto para definir la infraestructura como codigo:

```yaml
services:
  - type: web
    name: api-academica
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: fastapi run app/main.py --port 10000
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        sync: false
      - key: ENVIRONMENT
        value: production
      - key: CORS_ORIGINS
        sync: false
      - key: ALLOWED_HOSTS
        sync: false
```

Con `render.yaml`, Render configura el servicio automaticamente. Solo necesitas llenar las variables de entorno marcadas como `sync: false` desde el dashboard.

---

## Paso 8. (Opcional) GitHub Actions CI

Crea `.github/workflows/ci.yml` para ejecutar tests automaticamente:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pip install pytest httpx pytest-cov
      - run: pytest
```

Cada vez que hagas push, GitHub ejecuta los tests. Si fallan, Render no despliega (porque el push no llega a `main` si usas pull requests).

---

## Resumen: lo que lograste

| Paso | Que hiciste |
|---|---|
| 1 | pydantic-settings + variables de entorno |
| 2 | database.py agnostico (SQLite/PostgreSQL) |
| 3 | Crear base de datos PostgreSQL en Supabase |
| 4 | Subir a GitHub |
| 5 | Crear Web Service en Render con env vars |
| 6 | Verificar API corriendo en internet ✅ |
| 7 | (Opcional) Render Blueprint |
| 8 | (Opcional) GitHub Actions CI |

Tu API ahora vive en `https://api-academica.onrender.com`. Cualquier persona con internet puede usarla. Bienvenido a produccion.
