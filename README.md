# Desarrollo Web II — FastAPI

Curso completo de **17 semanas** (1 pre-requisito + 16 regulares) para aprender a construir APIs REST profesionales con **FastAPI**, desde los fundamentos de MVC hasta el despliegue en produccion con Render + Supabase.

**Docente:** Ing. Eduardo Pimienta

---

## Tabla de contenido

- [Acerca del curso](#acerca-del-curso)
- [Estructura por semanas](#estructura-por-semanas)
- [Parciales](#parciales)
- [Requisitos](#requisitos)
- [Stack tecnologico](#stack-tecnologico)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Como usar este curso](#como-usar-este-curso)
- [Navegador de clases (landing page)](#navegador-de-clases-landing-page)
- [Recursos adicionales](#recursos-adicionales)

---

## Acerca del curso

Este curso esta disenado para estudiantes que ya tienen conocimientos basicos de Python y desean especializarse en el desarrollo de APIs web modernas con FastAPI.

### Resultados de aprendizaje

| RA | Descripcion |
|---|---|
| RA1 | Comprender los conceptos fundamentales del patron MVC y los frameworks de desarrollo de software |
| RA2 | Analizar las ventajas y desventajas de utilizar frameworks en el desarrollo de aplicaciones web |
| RA3 | Seleccionar un framework de desarrollo web adecuado para un proyecto especifico |
| RA4 | Crear y configurar endpoints de una aplicacion web mediante la implementacion de rutas y controladores |
| RA5 | Implementar la logica de negocio de una aplicacion web mediante patrones de diseno y buenas practicas |
| RA6 | Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones |

### Metodologia

Cada semana incluye:

1. **Documento principal** (`clase-XX.md`) - Explicacion conceptual con analogias, tablas y ejemplos practicos
2. **Diapositivas** (`html/index.html`) - Presentacion estilo Tokio Nights para proyectar en clase
3. **Ejemplo guiado** (`ejemplo-guiado/`) - Tutorial paso a paso con codigo funcional
4. **Ejercicios** (`ejercicios/`) - Practica con ejercicios de codigo y desafios
5. **FAQ** (`dudas/`) - Preguntas frecuentes con respuestas en lenguaje simple
6. **Codigo fuente completo** - Proyectos funcionales listos para ejecutar

---

## Estructura por semanas

### Pre-requisito (Semana 0)

| # | Semana | Tema |
|---|--------|------|
| 00 | [Introduccion a Python, APIs y FastAPI](semana-00-introduccion-python-fastapi/) | Python basico, HTTP, APIs, REST, primera app FastAPI, Swagger |

### Unidad 1 — Fundamentos MVC y Frameworks (Semanas 1-5)

| # | Semana | Tema | Fecha |
|---|--------|------|-------|
| 01 | [Introduccion al curso](semana-01-introduccion-al-curso/) | HTTP, REST, cliente-servidor, diagnostico | Ago 10-16 |
| 02 | [Concepto, componentes e interaccion del MVC](semana-02-concepto-componentes-mvc/) | Patron MVC, componentes, interaccion | Ago 17-23 |
| 03 | [Separacion de responsabilidades](semana-03-separacion-responsabilidades/) | Separacion de capas, organizacion MVC | Ago 24-30 |
| 04 | [Frameworks web: conceptos, ventajas y limitaciones](semana-04-frameworks-web/) | Comparacion de frameworks, elegir framework | Ago 31-Sep 6 |
| 05 | [Parcial 1](semana-05-parcial-1/) | MVC y Frameworks | Sep 7-13 |

### Unidad 2 — FastAPI Fundamentals (Semanas 6-11)

| # | Semana | Tema | Fecha |
|---|--------|------|-------|
| 06 | [Seleccion de un framework especifico](semana-06-seleccion-framework/) | Justificacion de FastAPI | Sep 14-20 |
| 07 | [Instalacion y configuracion](semana-07-instalacion-configuracion/) | pip, venv, Uvicorn, configuracion | Sep 21-27 |
| 08 | [Estructura y organizacion de proyecto](semana-08-estructura-proyecto/) | Modularidad, routers, schemas, core | Sep 28-Oct 4 |
| 09 | [Creacion y configuracion de app basica](semana-09-app-basica/) | Pydantic v2, validacion, schemas | Oct 5-11 |
| 10 | [Ejecucion y validacion de la aplicacion](semana-10-ejecucion-validacion/) | Uvicorn, JWT, middleware, CORS | Oct 12-18 |
| 11 | [Parcial 2](semana-11-parcial-2/) | FastAPI Fundamentals | Oct 19-25 |

### Unidad 3 — FastAPI Intermedio (Semanas 12-15)

| # | Semana | Tema | Fecha |
|---|--------|------|-------|
| 12 | [Creacion y manejo de rutas](semana-12-creacion-rutas/) | APIRouter, path params, query params | Oct 26-Nov 1 |
| 13 | [Routers, logica de negocio y SQLAlchemy](semana-13-routers-logica-negocio/) | Routers como controllers, Depends, ORM | Nov 2-8 |
| 14 | [Motores de plantillas y testing](semana-14-plantillas-presentacion/) | pytest, TestClient, fixtures, cobertura | Nov 9-15 |
| 15 | [Parcial 3](semana-15-parcial-3/) | FastAPI Completo | Nov 16-22 |

### Unidad 4 — Cierre del Curso (Semana 16)

| # | Semana | Tema | Fecha |
|---|--------|------|-------|
| 16 | [Retroalimentacion y despliegue](semana-16-retroalimentacion-cierre/) | Render, Supabase, despliegue final | Nov 23-25 |

---

## Parciales

| Parcial | Semana | Fecha | Temas |
|---------|--------|-------|-------|
| Parcial 1 | 5 | Sep 7-13 | MVC, patrones, frameworks |
| Parcial 2 | 11 | Oct 19-25 | FastAPI, Pydantic, Uvicorn, middleware |
| Parcial 3 | 15 | Nov 16-22 | Rutas, SQLAlchemy, testing |

Cada parcial tiene un `spec-parcial-XX.md` con el formato, alcance y criterios de evaluacion.

---

## Requisitos

- Python 3.10+ instalado
- Conocimientos basicos de Python (variables, funciones, clases)
- Un editor de codigo (VS Code recomendado)
- Git (para control de versiones)
- Cuentas gratis en [GitHub](https://github.com), [Render](https://render.com) y [Supabase](https://supabase.com)

---

## Stack tecnologico

| Tecnologia | Proposito |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web principal |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM para persistencia |
| [Pydantic v2](https://docs.pydantic.dev/) | Validacion de datos y schemas |
| [python-jose](https://python-jose.readthedocs.io/) | Tokens JWT |
| [passlib](https://passlib.readthedocs.io/) + [bcrypt](https://pypi.org/project/bcrypt/) | Hashing de contrasenas |
| [pytest](https://docs.pytest.org/) + [httpx](https://www.python-httpx.org/) | Testing |
| [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Configuracion por entorno |
| [Render](https://render.com/) | Plataforma cloud (web service) |
| [Supabase](https://supabase.com/) | PostgreSQL gratis en la nube |

---

## Estructura del repositorio

```
curso-desarrollo-web-ii-fastapi/
├── engine/                          # Recursos compartidos
│   ├── slides.css                   # Estilo Tokio Nights para diapositivas
│   ├── slides.js                    # Navegacion de diapositivas
│   └── swagger-anatomia.md          # Guia rapida de Swagger UI
├── index.html                       # Landing page con explorador de clases
├── semana-XX-tema/
│   ├── clase-XX.md                  # Documento principal
│   ├── html/index.html              # Diapositivas
│   ├── ejemplo-guiado/              # Tutorial paso a paso
│   │   └── proyecto-ejemplo/        # Codigo fuente completo
│   ├── ejercicios/                  # Ejercicios practicos
│   └── dudas/                       # FAQ
└── semana-XX-parcial/
    ├── spec-parcial-XX.md           # Especificacion del examen
    └── README.md
```

---

## Como usar este curso

### Opcion 1: Navegador web (recomendado para estudiantes)

Abre `index.html` en tu navegador. La landing page ofrece:

- **Explorador lateral** con arbol de semanas organizado por unidades
- **Tarjetas de clase** con descripcion y etiquetas
- **Visor de diapositivas** en iframe
- **Renderizado de Markdown** con resaltado de sintaxis (usando marked.js + highlight.js)
- **Historial de navegacion** con boton "Volver" y tecla Escape
- **Seccion de recursos** con enlaces a documentacion oficial

### Opcion 2: Acceso directo por archivos

Cada semana es autocontenida. Puedes navegar directamente a:

```bash
# Ver el documento de una semana
semana-07-instalacion-configuracion/clase-04.md

# Ver las diapositivas
semana-07-instalacion-configuracion/html/index.html

# Explorar el codigo de ejemplo
semana-07-instalacion-configuracion/ejemplo-guiado/
```

### Para ejecutar los proyectos

Cada proyecto incluye `requirements.txt`. Para ejecutarlos:

```bash
cd semana-XX-tema/ejemplo-guiado/proyecto-ejemplo/
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
fastapi dev app/main.py
# Abrir http://localhost:8000/docs
```

---

## Navegador de clases (landing page)

La landing page (`index.html`) es una aplicacion de pagina unica construida con HTML, CSS y JavaScript vanilla. Sus caracteristicas:

- **Diseno Lazyvin glassmorphism** con colores Tokio Nights
- **Tema oscuro** con variables CSS personalizadas
- **Explorador lateral** con arbol expandible por semana
- **Vista de inicio** con tarjetas de clase, estadisticas y recursos
- **Visor de diapositivas** en iframe integrado
- **Renderizador de Markdown** que convierte archivos .md a HTML con sintaxis coloreada
- **Navegacion con historial** y atajo de teclado (Escape para volver)
- **Diseno responsive** para moviles y escritorio

---

## Recursos adicionales

### Documentacion oficial

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Render Docs](https://render.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [pytest](https://docs.pytest.org/)
- [JWT.io](https://jwt.io/introduction)

### Estandares y buenas practicas

- [MDN HTTP](https://developer.mozilla.org/es/docs/Web/HTTP)
- [OWASP API Security](https://owasp.org/API-Security/)
- [Python Packaging](https://packaging.python.org/)

---

## Licencia

Este material fue creado para fines educativos. Puede ser utilizado, modificado y compartido libremente para la ensenanza del desarrollo web con FastAPI.

---

*"El mejor modo de predecir el futuro es crearlo." — Peter Drucker*
