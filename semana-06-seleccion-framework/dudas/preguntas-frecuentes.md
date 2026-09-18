# Dudas frecuentes - Clase 06

> Aquí encontrarás las preguntas y aclaraciones que los estudiantes suelen hacer al seleccionar FastAPI como framework principal del curso y al comenzar a trabajar con dominios reales como PQRS. Si tienes una duda que no aparece aquí, ¡tráela a clase!

---

## 1. ¿Por qué elegimos FastAPI y no Django si Django es más conocido?

**Respuesta corta:** Porque el enfoque del curso es construir **APIs REST modernas, rápidas y tipadas**, no sitios monolíticos renderizados en servidor.

**Respuesta larga:** 
Django es un framework "con baterías incluidas" (trae panel de administración, ORM, sistema de usuarios y motor de plantillas HTML). Sin embargo:
- Para hacer APIs REST en Django necesitas una extensión pesada llamada *Django REST Framework (DRF)*.
- FastAPI fue construido desde el día 1 **exclusivamente para APIs REST**.
- FastAPI incluye validación de datos con Pydantic y documentación automática OpenAPI (`/docs`) nativamente, sin instalar paquetes adicionales.
- FastAPI ofrece un rendimiento sustancialmente superior gracias a `async/await` y Uvicorn.

---

## 2. ¿FastAPI reemplaza a Pydantic o trabajan juntos?

**Respuesta corta:** Trabajan juntos. Pydantic es la librería de validación que FastAPI usa por dentro.

**Respuesta larga:**
FastAPI no inventó su propio sistema de validación de datos. Utiliza **Pydantic** (una de las librerías de parseo y validación de tipos más veloces y populares de Python). 
- Cuando defines una clase que hereda de `BaseModel` (por ejemplo `PQRSCreate`), estás usando **Pydantic**.
- Cuando pones esa clase como argumento en un endpoint `@router.post("/")`, **FastAPI** toma esa clase y valida automáticamente los datos que vienen en la petición HTTP.

---

## 3. ¿Para qué sirve Swagger UI (`/docs`) en una API como la de PQRS?

**Respuesta corta:** Es una interfaz gráfica interactiva que te permite probar tu API directamente desde el navegador sin necesidad de usar Postman, Insomnia o llamadas con `curl`.

**Respuesta larga:**
En el desarrollo de software moderno, los desarrolladores backend deben compartir la API con el equipo frontend, clientes o aplicaciones móviles. 
- Swagger UI genera un portal web automático (`http://localhost:8000/docs`).
- Muestra todos los endpoints disponibles (`POST /api/v1/pqrs/`, `GET /api/v1/pqrs/`, etc.).
- Detalla los esquemas de datos esperados (tipos de campos, restricciones de longitud, valores permitidos).
- Permite hacer peticiones reales ("Try it out") y ver la respuesta JSON con su código de estado HTTP (ej. `201 Created` o `422 Unprocessable Entity`).

---

## 4. En el ejemplo de PQRS, ¿por qué validamos el correo de contacto solo si la PQRS no es anónima?

**Respuesta corta:** Por reglas de negocio y protección de privacidad del ciudadano.

**Respuesta larga:**
Una PQRS (Petición, Queja, Reclamo o Sugerencia) puede ser radicada de dos formas:
1. **Identificada:** El ciudadano proporciona su nombre y correo para recibir notificaciones sobre su trámite.
2. **Anónima:** El ciudadano decide reportar una falla o sugerencia sin revelar su identidad.

Mediante Pydantic, aplicamos un validador de campo (`@field_validator`):
```python
if not es_anonimo and not v:
    raise ValueError("El correo de contacto es obligatorio a menos que la solicitud sea anónima.")
```
Esto garantiza que la API impida que alguien envíe una solicitud identificada sin correo de notificación, retornando un código HTTP `422`.

---

## 5. ¿Qué es el código HTTP `422 Unprocessable Entity`?

**Respuesta corta:** Es el código que devuelve FastAPI cuando los datos enviados en el JSON no cumplen con las reglas del esquema Pydantic.

**Respuesta larga:**
Diferencia entre un error `400` y `422`:
- **400 Bad Request:** La petición ni siquiera se puede leer (JSON malformado, sintaxis rota).
- **422 Unprocessable Entity:** El JSON está bien escrito, pero los datos no cumplen con los tipos o reglas requeridas (por ejemplo, enviar un título de PQRS de 2 caracteres cuando el mínimo es 5, o enviar `"peticion"` mal escrito como `"peticion_123"`).

FastAPI genera una respuesta detallada con los campos exactos que fallaron:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "titulo"],
      "msg": "String should have at least 5 characters"
    }
  ]
}
```

---

## 6. ¿Por qué usamos una lista en memoria (`BD_PQRS_SIMULADA`) en la Semana 6 y no una base de datos real?

**Respuesta corta:** Para enfocarnos en los fundamentos de FastAPI (rutas, esquemas, verbos HTTP y validación) antes de introducir la complejidad de las bases de datos.

**Respuesta larga:**
En el aprendizaje por capas:
- **Semanas 6 a 10:** Aprendemos a estructurar endpoints, usar Pydantic, organizar routers, manejar middlewares y seguridad (JWT).
- **Semanas 12 y 13:** Conectaremos nuestra API a una base de datos real (SQLite en desarrollo y PostgreSQL en producción) mediante **SQLAlchemy** y **Alembic**.

Mantener una lista en memoria permite entender el flujo de entrada y salida sin preocuparnos todavía por migraciones, tablas o sesiones de BD.

---

## 7. ¿Por qué usamos `APIRouter` en lugar de poner todos los endpoints en `main.py`?

**Respuesta corta:** Para mantener el proyecto modular, ordenado y escalable.

**Respuesta larga:**
Si pusiéramos todos los endpoints de PQRS, usuarios, autenticación y reportes en `main.py`, el archivo tendría miles de líneas y sería imposible trabajar en equipo.
Con `APIRouter`:
- Creamos módulos independientes por dominio (ej. `app/routers/pqrs.py`).
- En `main.py` solo incluimos los routers: `app.include_router(pqrs.router, prefix="/api/v1")`.
- Facilita que diferentes desarrolladores trabajen en distintas carpetas sin generar conflictos en Git.

---

## 8. ¿Qué significa el flag `--reload` en `uvicorn app.main:app --reload`?

**Respuesta corta:** Hace que el servidor Uvicorn se reinicie automáticamente cada vez que guardas un cambio en el código Python.

**Respuesta larga:**
Durante la fase de desarrollo, no quieres detener y volver a ejecutar la terminal cada vez que modificas una línea en `pqrs.py` o `main.py`. El flag `--reload` escucha los cambios en los archivos `.py` y recarga el servidor en milisegundos.

> ⚠️ **Importante:** En entornos de producción (Render, AWS, etc.), NUNCA se debe usar `--reload`, ya que consume recursos innecesarios y puede causar inestabilidad.

---

## 9. ¿Cuál es la diferencia entre un esquema `PQRSCreate` y un esquema `PQRSResponse`?

| Característica | `PQRSCreate` (Esquema de Entrada) | `PQRSResponse` (Esquema de Salida) |
|---|---|---|
| **Propósito** | Define qué datos DEBE enviar el cliente al radicar. | Define qué datos DEVOLVERÁ la API al cliente. |
| **Campos incluidos** | Solo datos iniciales (`titulo`, `descripcion`, `tipo`, `email_contacto`). | Incluye datos iniciales + datos generados por el servidor (`id`, `codigo_radicado`, `fecha_creacion`, `estado`). |
| **Seguridad** | Evita que el cliente inyecte campos que no le corresponden. | Oculta campos internos de la BD o lógica privada. |

---

## 10. ¿FastAPI sirve para renderizar vistas HTML con CSS y JavaScript?

**Respuesta corta:** Sí se puede (usando Jinja2), pero no es su fortaleza principal.

**Respuesta larga:**
FastAPI puede servir plantillas HTML con Jinja2 o archivos estáticos (`StaticFiles`), pero el estándar moderno es usar FastAPI como **Backend puro (API REST)** y consumir sus endpoints desde una SPA (Single Page Application) hecha en React, Vue, Svelte o Vanilla JS/HTML.
