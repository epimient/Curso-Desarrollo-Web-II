# Dudas frecuentes — Clase 12

> Aqui encontraras las preguntas que los estudiantes suelen hacer (pero a veces da verguenza preguntar). Todas son validas.

---

## 1. ¿Necesito Docker para desplegar en Render?

**Respuesta corta:** No. Render despliega tu API sin Docker usando su runtime Python nativo.

**Respuesta larga:** Cuando configuras Render con `Runtime: Python 3`, `Build Command: pip install -r requirements.txt` y `Start Command: fastapi run app/main.py --port 10000`, Render:
1. Clona tu repositorio
2. Crea un entorno virtual
3. Instala las dependencias con pip
4. Inicia tu API con fastapi run

No necesitas Dockerfile, .dockerignore, ni tener Docker instalado. Render se encarga de todo.

**¿Cuando usarias Docker?** Si tu proyecto necesita una version especifica de Python (ej: 3.11.9), herramientas del sistema operativo, o multiples servicios que deben coordinarse. Para proyectos academicos y la mayoria de APIs profesionales, el runtime Python de Render es suficiente.

---

## 2. ¿SQLite sirve para produccion?

**Respuesta corta:** No, a menos que tu app tenga un solo usuario.

**Respuesta larga:** SQLite tiene limitaciones graves en produccion:
- **Escritura concurrente:** solo un proceso puede escribir a la vez. Si tienes 2 replicas de tu API, se corrompe.
- **Escalabilidad:** no soporta multiples conexiones simultaneas de forma eficiente.
- **Persistencia:** en Render free tier, el filesystem es efimero. Si el servicio se reinicia, pierdes los datos.

SQLite es perfecto para desarrollo y prototipos. PostgreSQL es el estandar para produccion.

---

## 3. ¿Cuanto cuesta Render + Supabase?

**Respuesta corta:** $0 para proyectos educativos y hobby.

**Respuesta larga:**

| Servicio | Free Tier | Limitaciones |
|---|---|---|
| Render Web Service | Gratis | Se apaga tras 15 min de inactividad, 512MB RAM |
| Supabase PostgreSQL | Gratis | 500MB, 10 conexiones, nunca expira |

Para un proyecto academico o prototipo, es completamente gratis. Para produccion real:
- Render: $7/mes (plan Starter, sin cold start)
- Supabase: $25/mes (plan Pro, 8GB, 100 conexiones)

---

## 4. ¿Por que mi API tarda 30 segundos en responder la primera vez?

**Respuesta corta:** Cold start del free tier de Render.

**Respuesta larga:** Render free tier apaga el servicio despues de 15 minutos sin actividad. Cuando alguien hace una request, Render enciende el servicio de nuevo. Ese proceso (cold start) toma ~30 segundos.

**No es un bug de tu codigo.** Es el comportamiento normal del free tier. Los planes pagos de Render mantienen el servicio siempre activo.

Para mitigarlo:
- Usa un servicio como [cron-job.org](https://cron-job.org) para hacer una request cada 10 minutos (keep alive)
- O actualiza a un plan pago ($7/mes)

---

## 5. ¿Como manejo migraciones de base de datos?

**Respuesta corta:** Con `Base.metadata.create_all()` para empezar. Despues, usa Alembic.

**Respuesta larga:** Por ahora, nuestra app crea las tablas automaticamente en el startup (lifespan). Esto funciona bien mientras el equipo es pequeno.

Para proyectos profesionales, necesitas **Alembic** (el migrador oficial de SQLAlchemy):

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

Alembic te permite:
- Versionar cambios en el esquema de BD
- Aplicar migraciones de forma segura (con rollback)
- Trabajar en equipo sin pisar cambios

---

## 6. ¿Render o Railway?

**Respuesta corta:** Los dos son muy similares. Render es un poco mas popular.

**Respuesta larga:**

| Aspecto | Render | Railway |
|---|---|---|
| Free tier | 512MB RAM, cold start | 512MB RAM, cold start |
| PostgreSQL | No gratis (expira a 30 dias) | No incluido |
| Facilidad de uso | Muy facil | Muy facil |
| GitHub integration | Nativa | Nativa |
| Custom domains | Solo plan pago | Solo plan pago |
| Popularidad | Mas popular | Creciente |

**Veredicto:** Para este curso elegimos Render por su integracion nativa con GitHub y su comunidad mas grande. Railway es una alternativa excelente si prefieres su interfaz.
