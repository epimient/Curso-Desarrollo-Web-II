# Clase 13 — Proyecto Integrador: Sistema de Gestión Académica

**Curso:** Desarrollo Web II — FastAPI  
**Unidad:** IV — Cierre y Revisión  
**Semana:** 13  
**RA asociados:** RA1, RA2, RA3, RA4, RA5, RA6

---

## Objetivos

1. Integrar **todos los conceptos** del curso en un solo proyecto funcional.
2. Implementar una **relación M:N** (muchos a muchos) entre estudiantes y cursos.
3. Agregar **operaciones de actualización** (PUT/PATCH) faltantes.
4. Implementar **paginación y filtros** en endpoints de listado.
5. Escribir **pruebas integrales** que cubran el nuevo feature.
6. Desplegar el proyecto final en **Render + Supabase**.

---

## 1. Recorrido del curso — ¿Qué aprendimos?

### Unidad I — Fundamentos (Clases 01-03)

| Clase | Tema | Concepto clave |
|-------|------|----------------|
| 01 | Marco de apps web modernas | Cliente-servidor, HTTP, APIs REST |
| 02 | MVC y patrones | Separación de responsabilidades |
| 03 | Comparación de frameworks | ¿Por qué FastAPI? |

### Unidad II — Desarrollo con FastAPI (Clases 04-08)

| Clase | Tema | Concepto clave |
|-------|------|----------------|
| 04 | Instalación y primer proyecto | `fastapi dev`, rutas básicas |
| 05 | Estructura profesional | `app/`, `routers/`, `schemas/`, `services/` |
| 06 | Modelos Pydantic | Validación con tipos Python |
| 07 | SQLAlchemy y persistencia | ORM, `Session`, CRUD |
| 08 | Relaciones SQLAlchemy | `ForeignKey`, `relationship`, M:N |

### Unidad III — Calidad y Seguridad (Clases 09-10)

| Clase | Tema | Concepto clave |
|-------|------|----------------|
| 09 | Autenticación JWT | `OAuth2PasswordBearer`, `python-jose`, bcrypt |
| 10 | Middleware, CORS, errores | `@app.middleware`, `CORSMiddleware`, handlers globales |

### Unidad IV — Entrega y Cierre (Clases 11-13)

| Clase | Tema | Concepto clave |
|-------|------|----------------|
| 11 | Testing | `pytest`, `httpx`, `TestClient`, fixtures, coverage |
| 12 | Despliegue | Render, Supabase, `pydantic-settings` |
| **13** | **Proyecto integrador** | **Todo lo anterior + relaciones M:N** |

---

## 2. Arquitectura completa del proyecto

```
proyecto-final-integrador/
├── requirements.txt
├── .env.example
├── render.yaml
├── app/
│   ├── main.py                  # FastAPI app, lifespan, startup
│   ├── database.py              # SQLAlchemy engine + session
│   ├── auth/
│   │   ├── jwt.py               # JWT create/decode
│   │   ├── hash.py              # bcrypt hash/verify
│   │   └── dependencies.py      # get_current_user
│   ├── core/
│   │   └── config.py            # pydantic-settings
│   ├── models/
│   │   ├── course.py            # Course (id, name, credits, active)
│   │   ├── user.py              # User (id, username, email, role)
│   │   └── enrollment.py        # ★ NUEVO: Enrollment (M:N)
│   ├── schemas/
│   │   ├── course.py            # CourseCreate, CourseResponse
│   │   ├── user.py              # UserCreate, UserResponse
│   │   ├── token.py             # Token, TokenData
│   │   └── enrollment.py        # ★ NUEVO: EnrollmentCreate, etc.
│   ├── services/
│   │   ├── course_service.py
│   │   ├── user_service.py
│   │   └── enrollment_service.py # ★ NUEVO
│   ├── routers/
│   │   ├── health.py            # GET /health/
│   │   ├── auth.py              # POST /token, /users/register, GET /users/me
│   │   ├── courses.py           # CRUD cursos + paginación
│   │   └── enrollments.py       # ★ NUEVO: endpoints matrícula
│   ├── middleware/
│   │   └── logging.py
│   ├── errors/
│   │   ├── exceptions.py
│   │   └── handlers.py
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_courses.py
│       ├── test_enrollments.py  # ★ NUEVO
│       └── test_health.py
```

> **Nota:** Las secciones marcadas con ★ son las que deberás implementar en este proyecto integrador. Todo lo demás ya existe y funciona.

---

## 3. El proyecto final — Especificación

### Tema

**Sistema de Gestión Académica** — API REST para administrar estudiantes, cursos y matrículas (enrollments). Un estudiante puede estar inscrito en múltiples cursos, y un curso puede tener múltiples estudiantes.

### Requisitos funcionales

1. **Gestión de usuarios** (ya implementado)
   - Registro de usuarios con rol `student` o `admin`
   - Autenticación JWT

2. **Gestión de cursos** (ya implementado, extender)
   - CRUD completo: GET, POST, GET by id, **PUT**, **DELETE** (admin-only)
   - **Paginación** en GET /courses/ (page, per_page)
   - **Filtros** por nombre, créditos, estado activo

3. **Gestión de matrículas** (★ nuevo)
   - POST /enrollments/ — Inscribir un estudiante en un curso
   - GET /enrollments/ — Listar matrículas (con filtros por student_id, course_id)
   - GET /enrollments/{id} — Obtener detalle de matrícula
   - PATCH /enrollments/{id} — Actualizar nota o estado
   - DELETE /enrollments/{id} — Cancelar matrícula (admin-only)

4. **Seguridad**
   - Solo usuarios autenticados pueden inscribirse
   - Solo admins pueden eliminar matrículas y cursos
   - Un estudiante no puede inscribirse dos veces al mismo curso

5. **Pruebas**
   - Tests para todos los nuevos endpoints
   - Tests de integración con base de datos de prueba

6. **Despliegue**
   - Desplegado en Render con PostgreSQL (Supabase)

### Requisitos técnicos

- FastAPI + SQLAlchemy + Pydantic v2
- Autenticación JWT (OAuth2PasswordBearer)
- Base de datos: SQLite en desarrollo, PostgreSQL en producción
- Pruebas con pytest + httpx TestClient
- CORS configurado para múltiples orígenes
- Middleware de logging
- Manejo global de errores
- Variables de entorno con pydantic-settings

---

## 4. Implementación paso a paso

Consulta el archivo `ejemplo-proyecto-integrador.md` para una guía detallada de cada paso:

1. Copiar el proyecto base y configurar el entorno
2. Crear el modelo `Enrollment` (M:N entre User y Course)
3. Crear los schemas Pydantic para Enrollment
4. Implementar el servicio de Enrollment
5. Crear el router de Enrollment con todos sus endpoints
6. Registrar el router en `main.py`
7. Agregar paginación y filtros a GET /courses/
8. Agregar endpoint PUT /courses/{id}
9. Escribir tests para Enrollment
10. Probar todo con Swagger UI
11. Desplegar en Render + Supabase

---

## 5. Criterios de evaluación

| Criterio | Peso | Descripción |
|----------|------|-------------|
| Modelo Enrollment | 15% | Relación M:N correcta con campos: student_id, course_id, grade, status |
| CRUD Enrollment | 20% | POST, GET, GET by id, PATCH, DELETE funcionando |
| PUT /courses/{id} | 10% | Actualización completa de curso |
| Paginación y filtros | 15% | Query params: page, per_page, name, credits |
| Pruebas unitarias | 20% | Tests para todos los nuevos endpoints (mín 10 tests) |
| Seguridad | 10% | Permisos correctos: student vs admin |
| Despliegue | 10% | App funcionando en Render con Supabase |

---

## 6. Checklist de entregables

- [ ] Modelo `Enrollment` creado con `id`, `student_id` (FK → users), `course_id` (FK → courses), `grade` (Float, nullable), `status` (enum: enrolled, completed, cancelled)
- [ ] Schemas `EnrollmentCreate`, `EnrollmentResponse`, `EnrollmentUpdate`
- [ ] Servicio `EnrollmentService` con CRUD + validación de duplicados
- [ ] Router `enrollments.py` con 5 endpoints
- [ ] Router `courses.py` actualizado con PUT + paginación + filtros
- [ ] Router `courses.py` registrado en `main.py` con prefijo y tags
- [ ] Pruebas en `tests/test_enrollments.py` (mín 8 tests)
- [ ] Pruebas actualizadas en `tests/test_courses.py`
- [ ] Todos los tests pasan: `pytest -v`
- [ ] Cobertura mínima 90%: `pytest --cov=app`
- [ ] Swagger UI funcional en `/docs`
- [ ] Desplegado en Render

---

## 7. Recursos adicionales

- `ejemplo-proyecto-integrador.md` — Guía paso a paso
- `ejercicios-clase-13.md` — Ejercicios complementarios
- `preguntas-frecuentes.md` — FAQ y troubleshooting
- `proyecto-final-integrador/` — Proyecto de referencia (solución completa)

---

*"El mejor modo de predecir el futuro es crearlo." — Peter Drucker*
