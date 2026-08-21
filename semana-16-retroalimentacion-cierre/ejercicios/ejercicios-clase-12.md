# Ejercicios — Clase 12

> **Nota para el estudiante:** Desplegar tu API es el paso final. No importa si algo falla en el primer intento — cada error es una oportunidad de aprender como funciona la infraestructura web real.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las siguientes frases con las palabras del recuadro:

> **Palabras:** Render | Supabase | PostgreSQL | variables de entorno | pydantic-settings | fastapi run

1. _________ es la plataforma cloud donde desplegamos el web service de nuestra API.
2. _________ es la plataforma que nos proporciona una base de datos PostgreSQL gratis que no expira.
3. _________ es el comando correcto para iniciar la aplicacion en produccion en Render.
4. La libreria _________ permite que la configuracion se lea desde variables de entorno y archivos `.env`.
5. En produccion, usamos _________ en lugar de SQLite para soportar multiples conexiones simultaneas.
6. La _____________ permite cambiar la configuracion (BD, secretos, CORS) sin modificar el codigo fuente.

---

## Ejercicio 1. Migrar configuracion a variables de entorno

Tu equipo heredo un proyecto FastAPI con la configuracion hardcodeada:

```python
class Settings:
    app_name = "MiApp"
    database_url = "sqlite:///./data.db"
    secret_key = "admin123"
    admin_email = "admin@miapp.com"
```

**Tarea:** Reescribe esta clase usando `pydantic-settings` con variables de entorno:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ...
    model_config = SettingsConfigDict(env_file=".env")
```

Requisitos:
- `app_name` con default `"MiApp"`
- `database_url` con default `"sqlite:///./data.db"` y que funcione con PostgreSQL
- `secret_key` SIN default (obligatorio definirla en entorno)
- `admin_email` con default `"admin@miapp.com"`
- `debug` con default `False`, tipo `bool`

**Pista:** Para `secret_key` sin default, simplemente no le asignes un valor: `secret_key: str`

---

## Ejercicio 2. Configurar Render para produccion

Tu API funciona localmente con SQLite. Ahora debes desplegarla en Render.

**Tarea:** Escribe los valores correctos para crear un Web Service en Render:

| Campo | Valor |
|---|---|
| **Runtime** | ? |
| **Build Command** | ? |
| **Start Command** | ? |
| **Plan** | ? |

**Preguntas:**
1. ¿Que archivo debe existir en tu repositorio para que Render instale las dependencias?
2. ¿Render necesita un Dockerfile? ¿Por que si o por que no?
3. ¿Que comando usa Render para iniciar tu API?

---

## Ejercicio 3. Depurar error de despliegue

Desplegaste tu API en Render pero al abrir `https://tu-api.onrender.com/docs` ves:

```
Internal Server Error
```

Revisas los logs de Render y encuentras:

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file
```

**Preguntas:**
1. ¿Por que SQLite falla en Render?
2. ¿Que cambio debes hacer en las variables de entorno de Render?
3. ¿Que servicio debes crear para solucionarlo?
4. **Escribe el comando** para obtener la URL de conexion correcta.

---

## Ejercicio 4. Configurar CORS para produccion

Tu API funciona en `https://api-academica.onrender.com`. Tu frontend en React esta en `https://frontend-app.onrender.com`.

**Tarea:** Escribe los valores correctos para las variables de entorno de produccion:

| Variable | Valor |
|---|---|
| `CORS_ORIGINS` | ? |
| `ALLOWED_HOSTS` | ? |
| `ENVIRONMENT` | ? |

**Pregunta adicional:** ¿Que pasaria si no configuras `ALLOWED_HOSTS` correctamente?

---

## Desafio extra (opcional)

**Objetivo:** Configurar un dominio personalizado para tu API en Render.

Render free tier no permite dominios personalizados directamente, pero puedes usar **Cloudflare DNS** para enmascarar la URL:

1. Compra un dominio (ej: `tuapi.com`) o usa un dominio gratis de Freenom
2. Configura Cloudflare como DNS
3. Crea un registro CNAME apuntando a `tu-api.onrender.com`
4. Configura SSL/TLS en Cloudflare (Flexible o Full)
5. Prueba que `https://api.tuapi.com/health/` funcione

**Meta:** Tu API responde desde un dominio personalizado con HTTPS.
