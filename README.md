# Desarrollo Web II — FastAPI

Curso completo de **13 semanas** para aprender a construir APIs REST profesionales con **FastAPI**, desde los fundamentos de HTTP hasta el despliegue en producción con Render + Supabase.

**Docente:** Ing. Eduardo Pimienta

---

## 📋 Tabla de contenido

- [Acerca del curso](#acerca-del-curso)
- [Estructura por unidades](#estructura-por-unidades)
- [Requisitos](#requisitos)
- [Stack tecnológico](#stack-tecnológico)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Cómo usar este curso](#cómo-usar-este-curso)
- [Navegador de clases (landing page)](#navegador-de-clases-landing-page)
- [Proyecto integrador](#proyecto-integrador)
- [Recursos adicionales](#recursos-adicionales)

---

## Acerca del curso

Este curso está diseñado para estudiantes que ya tienen conocimientos básicos de Python y desean especializarse en el desarrollo de APIs web modernas con FastAPI.

### Resultados de aprendizaje

| RA | Descripción |
|---|---|
| RA1 | Analizar el modelo cliente-servidor y el protocolo HTTP como base de las aplicaciones web modernas |
| RA2 | Construir APIs REST con FastAPI aplicando el patrón MVC y una estructura profesional por capas |
| RA3 | Implementar persistencia de datos con SQLAlchemy, incluyendo relaciones entre modelos |
| RA4 | Aplicar autenticación JWT, middleware, CORS y manejo global de errores |
| RA5 | Desplegar aplicaciones FastAPI en producción con variables de entorno, PostgreSQL en la nube y plataformas cloud |
| RA6 | Escribir pruebas automatizadas con pytest y lograr cobertura de código significativa |

### Metodología

Cada clase incluye:

1. **Documento principal** (`clase-XX.md`) — Explicación conceptual con analogías, tablas "Así NO vs Así SÍ", y ejemplos prácticos
2. **Diapositivas** (`html/index.html`) — Presentación estilo Tokio Nights para proyectar en clase
3. **Ejemplo guiado** (`ejemplo-guiado/`) — Tutorial paso a paso con código funcional
4. **Ejercicios** (`ejercicios/`) — Práctica con espacios en blanco, ejercicios de código y desafíos
5. **FAQ** (`dudas/`) — Preguntas frecuentes con respuestas en lenguaje simple
6. **Código fuente completo** — Proyectos funcionales listos para ejecutar

---

## Estructura por unidades

### Unidad 1 — Fundamentos (Clases 01-03)

| # | Clase | Temas clave |
|---|---|---|
| 01 | [Marco de aplicaciones web modernas](clase-01-marco-aplicaciones-web-modernas/) | HTTP, REST, cliente-servidor, diagnóstico de APIs públicas |
| 02 | [MVC, patrones y FastAPI](clase-02-mvc-patrones-fastapi/) | Patrón MVC, separación por capas, primeros pasos con FastAPI |
| 03 | [Frameworks: comparación y elección](clase-03-frameworks-comparacion-eleccion/) | FastAPI vs Django vs Flask, benchmarks, matriz de decisión |

### Unidad 2 — Desarrollo con FastAPI (Clases 04-08)

| # | Clase | Temas clave |
|---|---|---|
| 04 | [Instalación y primer proyecto](clase-04-instalacion-primer-proyecto/) | Entorno virtual, Uvicorn, rutas básicas, Swagger UI |
| 05 | [Estructura profesional](clase-05-estructura-profesional-proyecto/) | APIRouter, schemas, servicios, core, organización modular |
| 06 | [Modelos Pydantic y validación](clase-06-modelos-pydantic-validacion/) | Validación con tipos Python, Field, errores 422 |
| 07 | [Persistencia con SQLAlchemy](clase-07-persistencia-sqlalchemy/) | ORM, Session, CRUD real con SQLite, dependencia get_db |
| 08 | [Relaciones entre modelos](clase-08-relaciones-sqlalchemy/) | ForeignKey, relationship, eager/lazy loading, relaciones M:N |

### Unidad 3 — Calidad y Seguridad (Clases 09-10)

| # | Clase | Temas clave |
|---|---|---|
| 09 | [Autenticación con JWT](clase-09-autenticacion-seguridad/) | OAuth2PasswordBearer, python-jose, bcrypt, roles, rutas protegidas |
| 10 | [Middleware, CORS y errores](clase-10-middleware-cors-errores/) | Middleware personalizado, CORSMiddleware, manejadores globales, lifespan |

### Unidad 4 — Entrega y Cierre (Clases 11-13)

| # | Clase | Temas clave |
|---|---|---|
| 11 | [Testing con pytest](clase-11-testing-pytest/) | TestClient, httpx, fixtures, conftest, cobertura, TDD |
| 12 | [Despliegue en Render + Supabase](clase-12-despliegue-render-supabase/) | pydantic-settings, PostgreSQL en la nube, Render Python runtime, CI/CD |
| 13 | [Proyecto integrador](clase-13-proyecto-integrador/) | Sistema de Gestión Académica: M:N, paginación, PUT/PATCH, tests integrales |

---

## Requisitos

- Python 3.10+ instalado
- Conocimientos básicos de Python (variables, funciones, clases)
- Un editor de código (VS Code recomendado)
- Git (para control de versiones)
- Cuentas gratis en [GitHub](https://github.com), [Render](https://render.com) y [Supabase](https://supabase.com) (Clase 12)

---

## Stack tecnológico

| Tecnología | Propósito |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web principal |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM para persistencia |
| [Pydantic v2](https://docs.pydantic.dev/) | Validación de datos y schemas |
| [python-jose](https://python-jose.readthedocs.io/) | Tokens JWT |
| [passlib](https://passlib.readthedocs.io/) + [bcrypt](https://pypi.org/project/bcrypt/) | Hashing de contraseñas |
| [pytest](https://docs.pytest.org/) + [httpx](https://www.python-httpx.org/) | Testing |
| [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Configuración por entorno |
| [Render](https://render.com/) | Plataforma cloud (web service) |
| [Supabase](https://supabase.com/) | PostgreSQL gratis en la nube |

---

## Estructura del repositorio

```
curso-desarrollo-web-ii-fastapi/
├── engine/                          # Recursos compartidos
│   ├── slides.css                   # Estilo Tokio Nights para diapositivas
│   ├── slides.js                    # Navegación de diapositivas
│   └── swagger-anatomia.md          # Guía rápida de Swagger UI
├── index.html                       # Landing page con explorador de clases
├── clase-XX-tema/
│   ├── clase-XX.md                  # Documento principal
│   ├── html/index.html              # Diapositivas
│   ├── ejemplo-guiado/              # Tutorial paso a paso
│   │   └── proyecto-ejemplo/        # Código fuente completo
│   ├── ejercicios/                  # Ejercicios prácticos
│   └── dudas/                       # FAQ
└── clase-13-proyecto-integrador/
    ├── clase-13-proyecto-integrador.md
    ├── ejemplo-proyecto-integrador.md
    ├── html/index.html
    ├── ejercicios-clase-13.md
    ├── preguntas-frecuentes.md
    └── proyecto-final-integrador/   # Proyecto completo de referencia
```

---

## Cómo usar este curso

### Opción 1: Navegador web (recomendado para estudiantes)

Abre `index.html` en tu navegador. La landing page ofrece:

- **Explorador lateral** con árbol de clases organizado por unidades
- **Tarjetas de clase** con descripción y etiquetas
- **Visor de diapositivas** en iframe
- **Renderizado de Markdown** con resaltado de sintaxis (usando marked.js + highlight.js)
- **Historial de navegación** con botón "Volver" y tecla Escape
- **Sección de recursos** con enlaces a documentación oficial

### Opción 2: Acceso directo por archivos

Cada clase es autocontenida. Puedes navegar directamente a:

```bash
# Ver el documento de una clase
clase-04-instalacion-primer-proyecto/clase-04.md

# Ver las diapositivas
clase-04-instalacion-primer-proyecto/html/index.html

# Explorar el código de ejemplo
clase-04-instalacion-primer-proyecto/ejemplo-guiado/
```

### Para ejecutar los proyectos

Cada proyecto incluye `requirements.txt`. Para ejecutarlos:

```bash
cd clase-XX-tema/ejemplo-guiado/proyecto-ejemplo/
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
fastapi dev app/main.py
# Abrir http://localhost:8000/docs
```

---

## Navegador de clases (landing page)

La landing page (`index.html`) es una aplicación de página única construida con HTML, CSS y JavaScript vanilla. Sus características:

- **Diseño Lazyvin glassmorphism** con colores Tokio Nights
- **Tema oscuro** con variables CSS personalizadas
- **Explorador lateral** con árbol expandible por clase
- **Vista de inicio** con tarjetas de clase, estadísticas y recursos
- **Visor de diapositivas** en iframe integrado
- **Renderizador de Markdown** que convierte archivos .md a HTML con sintaxis coloreada
- **Navegación con historial** y atajo de teclado (Escape para volver)
- **Diseño responsive** para móviles y escritorio

---

## Proyecto integrador

La Clase 13 es el proyecto final del curso: un **Sistema de Gestión Académica** que integra todos los conceptos aprendidos.

### Funcionalidades implementadas

- **CRUD de cursos** con paginación, filtros y actualización PUT
- **Autenticación JWT** con roles (student/admin)
- **Relación M:N** entre estudiantes y cursos vía tabla Enrollment
- **Operaciones PATCH** en matrículas (actualización parcial de notas/estado)
- **Pruebas automatizadas** con pytest (41 tests, 96% de cobertura)
- **Despliegue** en Render con PostgreSQL en Supabase

### Para probar el proyecto final

```bash
cd clase-13-proyecto-integrador/proyecto-final-integrador/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
# Abrir http://localhost:8000/docs

# Ejecutar pruebas
pytest -v
pytest --cov=app --cov-report=term-missing
```

---

## Recursos adicionales

### Documentación oficial

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Render Docs](https://render.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [pytest](https://docs.pytest.org/)
- [JWT.io](https://jwt.io/introduction)

### Estándares y buenas prácticas

- [MDN HTTP](https://developer.mozilla.org/es/docs/Web/HTTP)
- [OWASP API Security](https://owasp.org/API-Security/)
- [Python Packaging](https://packaging.python.org/)

---

## Licencia

Este material fue creado para fines educativos. Puede ser utilizado, modificado y compartido libremente para la enseñanza del desarrollo web con FastAPI.

---

*"El mejor modo de predecir el futuro es crearlo." — Peter Drucker*
