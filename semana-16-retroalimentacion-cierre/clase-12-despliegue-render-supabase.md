# Clase 12 - Despliegue en Render + Supabase

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II
**Enfoque del curso:** FastAPI como framework principal para el desarrollo de aplicaciones web y APIs modernas.
**Semana:** 12
**Unidad:** Unidad 4 - Calidad y despliegue
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.
**Resultado de aprendizaje asociado:**
- RA5: Desplegar aplicaciones FastAPI en entornos de produccion utilizando variables de entorno, PostgreSQL en la nube y plataformas cloud como Render y Supabase.

## 2. Proposito de la clase

Tienes una API funcional con tests automatizados. Pero solo existe en tu computadora. Nadie mas puede usarla. Para que tu API sea util, debe estar disponible 24/7 en internet.

En esta clase aprenderas a:
- Usar variables de entorno para configurar produccion vs desarrollo
- Migrar de SQLite a PostgreSQL con Supabase (gratis, no expira)
- Desplegar en Render usando su runtime Python nativo
- Conectar tu API con una base de datos en la nube

## 3. ¿Que significa desplegar una API?

> **En espanol simple:** Desplegar es poner tu API en un servidor que este encendido 24/7 para que cualquiera pueda usarla desde internet.

### 3.1 Desarrollo vs Produccion

| Aspecto | Desarrollo | Produccion |
|---|---|---|
| ¿Donde corre? | Tu computadora | Un servidor en la nube |
| ¿Quien accede? | Solo tu | Cualquiera con internet |
| Base de datos | SQLite (archivo local) | PostgreSQL (en la nube) |
| URL | `http://localhost:8000` | `https://tu-api.onrender.com` |
| Configuracion | Hardcodeada | Variables de entorno |
| ¿Esta 24/7? | Solo cuando ejecutas `fastapi dev` | Siempre |

### 3.2 Stack de produccion que usaremos

```
Navegador / App
       │
       ▼
  Render.com ─── Web Service
       │
       ▼
  Supabase ───── PostgreSQL
```

- **Render** aloja el web service (el runtime Python con tu API)
- **Supabase** aloja la base de datos PostgreSQL

Render se encarga de todo: clona tu repo de GitHub, instala dependencias con `pip`, e inicia tu API con `fastapi run`. No necesitas Docker ni configurar un servidor manualmente.

## 4. Stack tecnologico para produccion

### 4.1 Render

Render es una plataforma cloud que permite desplegar aplicaciones web gratis. Soporta Python, Node.js, Go, Rust, etc.

| Caracteristica | Free Tier |
|---|---|
| RAM | 512 MB |
| CPU | 0.1 vCPU |
| Tiempo activo | Sporadic (se apaga tras 15 min de inactividad) |
| SSL | Automatico (HTTPS) |
| Dominio | `tu-app.onrender.com` |
| Costo | $0 |

> **Nota:** El free tier Render apaga el servicio tras 15 minutos sin uso. Cuando alguien accede, tarda ~30 segundos en encenderse (cold start). Es normal. Para produccion real se necesita plan pago ($7/mes).

### 4.2 Supabase (base de datos)

Supabase es una plataforma que ofrece PostgreSQL gratis. A diferencia de Render Postgres, la base de datos **nunca expira**.

| Caracteristica | Free Tier |
|---|---|
| Almacenamiento | 500 MB |
| Conexiones simultaneas | 10 |
| SSL | Incluido |
| Tiempo de vida | Ilimitado (no expira) |
| Costo | $0 |

### 4.3 El runtime Python de Render

Render tiene soporte nativo para Python. Cuando seleccionas `Runtime: Python 3`, Render:

1. Clona tu repositorio de GitHub
2. Crea un entorno virtual
3. Ejecuta `pip install -r requirements.txt`
4. Ejecuta `fastapi run app/main.py --port 10000`

No necesitas Docker. No necesitas configurar un servidor web. Render maneja todo automaticamente.

> **Comparacion:** Si Docker es una caja de mudanzas donde empaquetas todo, el runtime Python de Render es como un camion de mudanzas que ya viene preparado. Solo le dices que llevas (requirements.txt) y donde dejarlo (start command).

## 5. Variables de entorno — "Configuracion que cambia segun el ambiente"

> **En espanol simple:** En desarrollo usas SQLite y `localhost`. En produccion usas PostgreSQL y `onrender.com`. Las variables de entorno te permiten cambiar la configuracion sin modificar el codigo.

### 5.1 El problema con la configuracion actual

```python
# app/core/config.py — ANTES
class Settings(BaseModel):
    database_url: str = "sqlite:///./cursos.db"  # Hardcodeado
    secret_key: str = "supersecretkey1234567890"  # Hardcodeado
    environment: str = "development"
```

Esto funciona en desarrollo, pero en produccion:
- La base de datos no es SQLite, es PostgreSQL
- La `secret_key` no debe estar en el codigo fuente
- Los CORS origins deben apuntar al dominio real

### 5.2 La solucion: pydantic-settings

```python
# app/core/config.py — DESPUES
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./cursos.db"  # Default: desarrollo
    secret_key: str = "changeme"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

`pydantic-settings` lee automaticamente:
1. Las variables de entorno del sistema (prioridad mas alta)
2. El archivo `.env` si existe
3. Los valores default definidos en la clase

### 5.3 El archivo .env

```bash
# .env — NO se sube a Git (esta en .gitignore)
DATABASE_URL=sqlite:///./cursos.db
SECRET_KEY=mi_clave_secreta_local
ENVIRONMENT=development
```

En produccion, Render configura estas variables desde el dashboard — no necesitas un archivo `.env`.

## 6. PostgreSQL con Supabase — "La BD que vive en la nube"

> **En espanol simple:** SQLite guarda los datos en un archivo local. Si escalas tu API a 2 servidores, cada uno tendria su propio archivo, y los datos no se sincronizarian. PostgreSQL es una base de datos cliente-servidor: muchos servidores pueden conectarse a la misma BD.

### 6.1 ¿Por que PostgreSQL y no SQLite?

| Aspecto | SQLite | PostgreSQL |
|---|---|---|
| Tipo | Archivo local | Cliente-servidor |
| Escalabilidad | 1 proceso | Multiples conexiones simultaneas |
| Velocidad escritura | Lenta en concurrencia | Rapida con muchas conexiones |
| Instalacion | No requiere | Requiere servidor (Supabase lo provee) |
| Ideal para | Desarrollo, prototipos | Produccion, equipos |

### 6.2 Nuestra database.py ahora es agnostica

```python
from sqlalchemy import create_engine
from app.core.config import settings

engine = create_engine(settings.database_url)
# Si DATABASE_URL = "sqlite:///./cursos.db"  → SQLite
# Si DATABASE_URL = "postgresql://user:pass@host:5432/db"  → PostgreSQL
```

No necesitas cambiar el codigo. Solo cambia el valor de `DATABASE_URL` segun el ambiente.

> **Analogia:** Es como un cargador universal. El enchufe (la URL) cambia segun el pais (desarrollo/produccion), pero el cable (tu codigo) es el mismo.

## 7. Render: despliegue directo sin Docker

Render puede ejecutar tu API directamente con su runtime Python. No necesitas Dockerfile ni contenedores.

### 7.1 Como funciona

Cuando creas un Web Service en Render con `Runtime: Python 3`:

| Paso | Que hace Render |
|---|---|
| 1. Clona | Tu repositorio de GitHub |
| 2. Construye | `pip install -r requirements.txt` |
| 3. Inicia | `fastapi run app/main.py --port 10000` |
| 4. Verifica | Health check para confirmar que responde |
| 5. Publica | Asigna una URL `https://tu-app.onrender.com` |

### 7.2 ¿Que necesitas en tu proyecto?

```
proyecto/
├── app/
│   ├── main.py          # Tu aplicacion FastAPI
│   ├── database.py       # Sin connect_args de SQLite
│   └── core/
│       └── config.py     # Usando pydantic-settings
├── requirements.txt      # Todas las dependencias
├── .env.example          # Opcional: ejemplo de configuracion
└── render.yaml           # Opcional: infraestructura como codigo
```

No necesitas:
- ❌ Dockerfile
- ❌ .dockerignore
- ❌ Docker instalado localmente
- ❌ Nginx ni reverse proxy

### 7.3 Beneficios de este enfoque

| Aspecto | Con Docker | Sin Docker (Render Runtime) |
|---|---|---|
| Complejidad | Mayor (aprender Docker) | Menor (solo Python) |
| Archivos extra | Dockerfile, .dockerignore | Ninguno |
| Consistencia | Maxima | Alta (Render usa Python 3 estable) |
| Control | Total (SO, version exacta) | Suficiente (Python 3.x) |
| Velocidad de deploy | Lento (build imagen) | Rapido (pip install) |

> **¿Cuando usar Docker?** Si tu proyecto necesita una version especifica de Python, herramientas del sistema, o multiples servicios, Docker es mejor. Para este curso, el runtime de Render es suficiente y mas simple.

## 8. Desplegar en Render + Supabase — Paso a paso

### 8.1 Crear proyecto en Supabase

1. Ve a [supabase.com](https://supabase.com) y crea una cuenta gratis
2. Haz clic en "New project"
3. Completa:
   - **Name:** `api-academica-db`
   - **Database Password:** Genera una segura (guardala)
   - **Region:** La mas cercana a tus usuarios
4. Espera ~2 minutos a que se cree el proyecto
5. Ve a **Project Settings → Database → Connection string**
6. Copia la **URI** (empieza con `postgresql://...`)
7. **Importante:** Reemplaza `[YOUR-PASSWORD]` con la contraseña que creaste

### 8.2 Subir tu codigo a GitHub

```bash
# En la raiz de tu proyecto:
git init
git add .
git commit -m "Primer commit: API academica lista para produccion"
git remote add origin https://github.com/tu-usuario/api-academica.git
git push -u origin main
```

### 8.3 Crear Web Service en Render

1. Ve a [render.com](https://render.com) y crea una cuenta (conecta GitHub)
2. Haz clic en **New + → Web Service**
3. Conecta tu repositorio de GitHub
4. Configura:

| Campo | Valor |
|---|---|
| **Name** | `api-academica` |
| **Region** | La mas cercana |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `fastapi run app/main.py --port 10000` |
| **Plan** | Free |

5. En la seccion **Environment Variables**, agrega:

| Key | Value |
|---|---|
| `DATABASE_URL` | `postgresql://...` (la URI de Supabase con tu password) |
| `SECRET_KEY` | Un token seguro (ej: `openssl rand -hex 32`) |
| `ENVIRONMENT` | `production` |
| `CORS_ORIGINS` | `["https://tu-app.onrender.com"]` |
| `ALLOWED_HOSTS` | `[".onrender.com"]` |

6. Haz clic en **Create Web Service**

Render construye, instala dependencias, y despliega tu API. En ~3 minutos tendras tu API corriendo en `https://api-academica.onrender.com`.

### 8.4 Verificar el despliegue

```bash
curl https://api-academica.onrender.com/health/
# → {"status": "ok"}

curl https://api-academica.onrender.com/docs
# → Swagger UI (desde internet!)
```

## 9. Migrar datos de SQLite a PostgreSQL (opcional)

Si ya tenias datos en SQLite y quieres migrarlos a PostgreSQL:

```bash
# 1. Exportar SQLite a SQL
sqlite3 cursos.db .dump > dump.sql

# 2. Ajustar el dump para PostgreSQL (cambiar tipos, eliminar AUTOINCREMENT, etc.)

# 3. Importar en Supabase (desde el SQL Editor de Supabase)
# O usando psql:
psql "$DATABASE_URL" < dump.sql
```

**Alternativa mas simple:** Como usamos `Base.metadata.create_all()` en el lifespan, al desplegar las tablas se crean automaticamente en PostgreSQL. Solo necesitas registrar los usuarios de nuevo.

## 10. CI/CD — Despliegues automaticos

> **En espanol simple:** Cada vez que haces `git push`, Render detecta el cambio, reconstruye y despliega la nueva version automaticamente. No necesitas hacer nada manual.

Render se conecta a GitHub y escucha cambios en la rama `main`. Cuando detecta un nuevo commit:
1. Clona el repositorio
2. Ejecuta `pip install -r requirements.txt`
3. Inicia el servidor con `fastapi run`
4. Verifica que responde correctamente (health check)
5. Redirige el trafico a la nueva version

### 10.1 GitHub Actions (CI opcional)

Puedes agregar un workflow de CI que ejecute los tests ANTES de hacer merge:

```yaml
# .github/workflows/ci.yml
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
      - run: pytest
```

## 11. Buenas practicas de produccion

### 11.1 Secretos NUNCA en el codigo

| Mal | Bien |
|---|---|
| `secret_key = "123456"` en config.py | `SECRET_KEY` en variables de entorno |
| `database_url` hardcodeado | `DATABASE_URL` desde env |
| `.env` subido a Git | `.env` en `.gitignore` |

### 11.2 CORS en produccion

```python
# En desarrollo: permite localhost
# En produccion: permite solo tu dominio
cors_origins = [
    "https://mi-frontend.onrender.com",
    "https://www.mi-dominio.com",
]
```

### 11.3 TrustedHostMiddleware

```python
allowed_hosts = [
    "api-academica.onrender.com",
    ".onrender.com",  # Permite cualquier subdominio de onrender.com
]
```

### 11.4 Logging

En produccion, considera usar `structlog` o `python-json-logger` para que los logs sean parseables por herramientas como Datadog o Grafana.

## 12. Render Blueprint (opcional)

Render permite definir la infraestructura como codigo usando `render.yaml`:

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
```

Al incluir este archivo en tu repositorio, Render configura el servicio automaticamente. Solo necesitas agregar los valores de `DATABASE_URL` y `SECRET_KEY` manualmente en el dashboard.

## 13. Checklist de implementacion

- [ ] Instalar `pydantic-settings` y `psycopg2-binary`
- [ ] Actualizar `config.py` para usar `pydantic-settings` con `SettingsConfigDict(env_file=".env")`
- [ ] Actualizar `database.py` para usar solo `settings.database_url` (sin `connect_args` de SQLite)
- [ ] Crear `.env.example` con valores de desarrollo
- [ ] Crear `render.yaml` con configuracion basica
- [ ] Crear proyecto en Supabase y obtener `DATABASE_URL`
- [ ] Subir a GitHub
- [ ] Crear Web Service en Render desde el dashboard (Runtime: Python 3)
- [ ] Configurar variables de entorno en Render (DATABASE_URL, SECRET_KEY, etc.)
- [ ] Verificar que `https://tu-api.onrender.com/docs` funciona

## 14. Cierre conceptual

Tu API ya no vive solo en tu computadora. Vive en internet, disponible 24/7, con una base de datos profesional PostgreSQL.

### Conceptos clave

| Concepto | Resumen |
|---|---|
| pydantic-settings | Lee configuracion desde variables de entorno y .env |
| Render | Plataforma cloud que aloja tu web service gratis con runtime Python nativo |
| Supabase | PostgreSQL gratis en la nube que no expira |
| CI/CD | Despliegues automaticos con cada `git push` |
| Variables de entorno | Configuracion que cambia segun el ambiente sin modificar codigo |

### Proxima clase
**Proyecto integrador** — Repaso general, refinamiento y presentacion del proyecto final del curso.
