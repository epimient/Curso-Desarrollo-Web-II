# Guia rapida de Swagger UI

## ¿Que es Swagger UI?

Es la pagina web que FastAPI genera automaticamente en `http://127.0.0.1:8000/docs`. Te permite ver y probar TODOS los endpoints de tu API sin instalar nada extra.

## Anatomia de la pagina /docs

```
┌─────────────────────────────────────────────────────────────┐
│  [localhost:8000/docs]                                       │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  FastAPI            [Servidor: http://localhost:8000]   │ │
│  │  API Academica                                          │ │
│  │  [Schemas ▼]                          [Authorize 🔒]    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─ Health ─────────────────────────────────────────────┐   │
│  │  GET /health/                          [Try it out]  │   │
│  │  GET /health/version                   [Try it out]  │   │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─ Auth ───────────────────────────────────────────────┐   │
│  │  POST /token                            [Try it out]  │   │
│  │  POST /users/register                   [Try it out]  │   │
│  │  GET  /users/me               🔒       [Try it out]  │   │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─ Courses ────────────────────────────────────────────┐   │
│  │  GET  /courses/                         [Try it out]  │   │
│  │  GET  /courses/{course_id}              [Try it out]  │   │
│  │  POST /courses/              🔒         [Try it out]  │   │
│  │  DELETE /courses/{course_id} 🔒         [Try it out]  │   │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Partes de Swagger UI

### 1. Barra superior
| Elemento | Que muestra |
|---|---|
| Titulo | El nombre de tu API (definido en `FastAPI(title=...)`) |
| Servidor | La URL base (`http://localhost:8000`) |
| `Schemas ▼` | Lista de todos los modelos Pydantic con sus campos y tipos |
| `Authorize` 🔒 | Boton para ingresar el token JWT (aparece cuando usas `OAuth2PasswordBearer`) |

### 2. Grupos de endpoints (tags)
Los endpoints se agrupan por el `tags=["..."]` que definiste en el `APIRouter`. Cada grupo es una seccion colapsable.

### 3. Cada endpoint muestra
```
GET /courses/{course_id}                 [Try it out]
├── Parameters                           ← si tiene path/query params
│   course_id: integer (required)
└── Responses
    200: CourseResponse                  ← modelo de respuesta
    404: HTTPValidationError
    422: HTTPValidationError
```

| Seccion | Que contiene |
|---|---|
| Path / metodo HTTP | La ruta y el verbo (GET, POST, etc.) |
| `Try it out` | Boton para ejecutar el endpoint desde el navegador |
| `Parameters` | Path y query parameters que necesita el endpoint |
| `Request body` | El JSON que debes enviar (solo POST/PUT/PATCH) |
| `Responses` | Los codigos HTTP posibles y el modelo de respuesta |
| 🔒 Candado | Indica que ese endpoint requiere autenticacion |
| `Schemas` | Modelos Pydantic que aparecen como tipo de dato |

### 4. Boton Authorize
Cuando haces clic en `Authorize` 🔒 se abre un modal donde pegas tu token JWT:

```
┌─ Authorize ──────────────────────────┐
│                                      │
│  Value: Bearer <pega_tu_token_aqui>  │
│                                      │
│  [Authorize]    [Close]              │
└──────────────────────────────────────┘
```

Una vez autorizado, todos los endpoints protegidos (con 🔒) pueden ejecutarse sin pedir el token cada vez.

---

## Como probar un endpoint con Swagger — paso a paso

```
1. Abre http://localhost:8000/docs

2. Busca el endpoint que quieres probar
   → Cada endpoint esta dentro de un grupo (Health, Auth, Courses)

3. Haz clic en el endpoint para expandirlo
   → Se ven los detalles: parametros, body, respuestas

4. Haz clic en "Try it out"
   → Los campos dejan de ser solo-lectura y se vuelven editables

5. Completa los datos necesarios:
   - Path parameters: escribe el valor (ej: course_id = 1)
   - Query parameters: aparecen como campos de texto
   - Request body: edita el JSON directamente

6. Haz clic en "Execute"
   → Swagger envia la peticion real a tu API

7. Revisa la respuesta:
   - Curl: el comando curl equivalente (por si lo necesitas)
   - Request URL: la URL completa que se llamo
   - Server response: el JSON que devolvio el servidor
   - Response headers: los headers HTTP de la respuesta
```

---

## Como leer una respuesta en Swagger

```
┌─ Server response ─────────────────────┐
│                                      │
│  Response body:                       │
│  {                                   │
│    "id": 1,                          │
│    "name": "Desarrollo Web II",      │
│    "credits": 3,                     │
│    "active": true                    │
│  }                                   │
│                                      │
│  Status: 200                         │
│  Duration: 0.023s                    │
│                                      │
│  Response headers:                   │
│  content-type: application/json      │
│  x-process-time: 0.0234              │
└──────────────────────────────────────┘
```

| Campo | Que significa |
|---|---|
| `Response body` | El JSON que devolvio tu endpoint |
| `Status` | Codigo HTTP (200 = bien, 404 = no encontrado, 422 = error validacion) |
| `Duration` | Cuanto tardo la peticion (util para detectar lentitud) |
| `Response headers` | Headers que envio el servidor |

---

## Errores comunes al usar Swagger

| Error | Solucion |
|---|---|
| No encuentro el endpoint en /docs | Revisa que lo registraste con `app.include_router()` en main.py |
| El boton Execute no hace nada | El servidor debe estar corriendo. Ejecuta `uvicorn app.main:app --reload` |
| Aparece error 422 al ejecutar | Faltan campos obligatorios o el tipo de dato es incorrecto. Revisa el modelo Pydantic. |
| Aparece error 401 (no autorizado) | El endpoint requiere token. Usa el boton Authorize para ingresar el JWT. |
| No veo el boton Authorize | No hay endpoints protegidos con OAuth2PasswordBearer en tu API. |
| Los datos que envio no se reflejan | Revisa que el JSON del Request body tenga los nombres de campo exactos del modelo. |
| La pagina no carga | El servidor no esta corriendo o el puerto es incorrecto. Verifica con `uvicorn`. |
