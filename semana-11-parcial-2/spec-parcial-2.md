# Parcial 2 — FastAPI Fundamentals

**Semana 11** | 19 al 25 de oct.

## Alcance

- Instalación y configuración de FastAPI
- Estructura de un proyecto FastAPI
- Creación de una aplicación básica
- Modelos Pydantic y validación
- Ejecución con Uvicorn y validación de endpoints

## Temas evaluados

| Tema | Peso | Detalle |
|------|------|---------|
| Instalación y config | 15% | pip, venv, Uvicorn, estructura de proyecto |
| Estructura del proyecto | 20% | Modularidad, carpetas, archivos principales |
| App básica + Pydantic | 35% | Endpoints, modelos, validación, schemas |
| Ejecución y validación | 30% | Uvicorn, testing con Swagger, CORS, errores |

## Formato del examen

- **Duración:** 90 minutos
- **Tipo:** Práctico (con código)
- **Puntaje:** 100 puntos

### Parte teórica (30 pts)

1. Explicar la estructura de un proyecto FastAPI y el rol de cada carpeta (15 pts)
2. Diferencia entre Pydantic BaseModel y schema de respuesta (15 pts)

### Parte práctica (70 pts)

1. Crear un endpoint GET que retorne una lista de elementos con validación Pydantic (25 pts)
2. Crear endpoints POST y PUT con validación de campos, retornar códigos de estado correctos (25 pts)
3. Configurar middleware CORS y manejo global de errores (20 pts)

## Requisitos previos

- FastAPI instalado con `pip install fastapi[standard]`
- Entorno virtual activo
- Swagger UI accesible en `http://localhost:8000/docs`

## Material de estudio

- Semanas 06-10
- Ejemplos guiados de instalación, estructura y app básica
- Ejercicios de Pydantic y endpoints

## Criterios de evaluación

- Estructura de proyecto organizada y modular
- Validación correcta con Pydantic v2
- Uso apropiado de HTTP methods y status codes
- Código limpio y siguiendo convenciones de FastAPI
