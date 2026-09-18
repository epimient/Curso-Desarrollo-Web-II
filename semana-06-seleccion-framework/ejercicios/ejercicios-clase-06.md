# Ejercicios - Clase 06

> **Nota para el estudiante:** Estos ejercicios te ayudarán a afianzar la justificación técnica de FastAPI y a practicar la creación de schemas y endpoints para un sistema de **PQRS (Peticiones, Quejas, Reclamos y Sugerencias)**. El Ejercicio 0 es de calentamiento.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las frases con las palabras del recuadro:

> **Palabras:** PYDANTIC | SWAGGER UI | UVICORN | APIROUTER | 422 UNPROCESSABLE ENTITY | 201 CREATED | FIELD | SCHEMA

1. FastAPI utiliza la librería _________ para la validación automática de tipos y datos en ejecución.
2. La documentación interactiva de la API accesible en `/docs` es generada por _________.
3. El servidor ASGI de alto rendimiento que ejecuta aplicaciones FastAPI se llama _________.
4. El código de estado HTTP _________ indica que una PQRS se radicó correctamente en el servidor.
5. Si un cliente envía un JSON con campos inválidos o incompletos, FastAPI retorna un error con código _________.
6. Para organizar endpoints en archivos o módulos separados utilizamos la clase _________.
7. En Pydantic, la función _________ permite definir restricciones como `min_length`, `max_length` y descripciones para la documentación.
8. Un _________ de Pydantic define la estructura de datos de entrada o salida de una petición HTTP.

---

## Ejercicio 1. Justificación de FastAPI para el Portal de PQRS

Imagina que trabajas para una entidad pública que necesita construir la API de su nuevo **Portal Ciudadano de PQRS**. La entidad exige:
- Alta velocidad de procesamiento para miles de peticiones simultáneas.
- Documentación OpenAPI estándar para que cualquier desarrollador externo pueda consumir la API.
- Validación estricta de formularios para evitar correos basura o textos incompletos.

Construye una **tabla comparativa** evaluando FastAPI frente a Django y Flask para este proyecto específico:

| Criterio | Peso (%) | FastAPI | Django | Flask |
|---|---|---|---|---|
| Validación de datos nativa | 25% | | | |
| Documentación automática (OpenAPI) | 25% | | | |
| Rendimiento concurrente (Async) | 20% | | | |
| Simplicidad de arquitectura modular | 15% | | | |
| Facilidad de prueba sin Postman | 15% | | | |
| **Puntaje Ponderado (1-10)** | **100%** | | | |

*Responde al final:*
- **¿Cuál framework obtuvo la calificación más alta y por qué?**
- **Justifica en 3 líneas por qué FastAPI encaja mejor en una API de PQRS.**

---

## Ejercicio 2. Ampliación del Esquema Pydantic para PQRS

Abre el archivo de esquemas del proyecto guiado (`app/schemas/pqrs.py`) y agrega un nuevo modelo llamado `PQRSAvanzadaCreate` que herede de `PQRSBase` e incluya los siguientes nuevos campos con sus respectivas validaciones:

1. `prioridad`: Un Enum `PQRSPriorityEnum` con valores `"baja"`, `"media"`, `"alta"`, `"urgente"`. Valor por defecto: `"media"`.
2. `adjunta_documentos`: Un booleano opcional que indica si el usuario subió evidencias en formato PDF. Valor por defecto: `False`.
3. `telefono_contacto`: Un string opcional de máximo 15 caracteres.
4. Un `@field_validator` que verifique que si `prioridad == "urgente"`, el campo `descripcion` deba tener al menos 50 caracteres para justificar la urgencia.

**Plantilla sugerida para tu código:**

```python
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class PQRSPriorityEnum(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"

class PQRSAvanzadaCreate(BaseModel):
    # Escribe aquí la definición de campos y validaciones
    pass
```

---

## Ejercicio 3. Endpoint de Búsqueda por Tipo de PQRS

En el archivo `app/routers/pqrs.py` del proyecto guiado, añade un nuevo endpoint con la siguiente firma:

- **Método HTTP:** `GET`
- **Ruta:** `/api/v1/pqrs/tipo/{tipo_solicitud}`
- **Descripción:** Recibe un tipo de PQRS por el Path (ejemplo: `peticion`, `queja`, `reclamo` o `sugerencia`) y retorna únicamente las PQRS que coincidan con dicho tipo.
- **Manejo de Errores:** Si no se encuentra ninguna PQRS con ese tipo en la lista, debe lanzar un `HTTPException(status_code=404, detail="No hay PQRS registradas para el tipo especificado")`.

---

## Ejercicio 4. Personalización de Swagger UI / OpenAPI

Abre `app/main.py` y personaliza los metadatos de tu API de PQRS:

1. Cambia el `title` a `"Sistema de Gestión de PQRS - Alcaldía Municipal"`.
2. Agrega una `contact` con tu nombre y correo electrónico en la configuración de `FastAPI()`.
3. En el endpoint `POST /api/v1/pqrs/`, agrega el argumento `response_description="Objeto PQRS creado exitosamente con código de radicado asignado"`.
4. Ingresa a `http://localhost:8000/docs` y toma una captura o verifica los cambios visuales en Swagger UI.

---

## Ejercicio 5. Análisis de Casos de Error

Analiza el siguiente intento de petición `POST` enviado por un usuario a la API de PQRS:

```json
{
  "titulo": "Hola",
  "descripcion": "Corta",
  "tipo": "reclamo_invalido",
  "es_anonimo": false
}
```

Responde las siguientes preguntas:
1. **¿Qué código de estado HTTP responderá FastAPI y por qué?**
2. **Identifica los 3 errores de validación presentes en ese JSON.**
3. **¿Cómo ayuda esta respuesta automática de FastAPI a los desarrolladores de frontend?**
