# Parcial 3 — FastAPI Completo

**Semana 15** | 16 al 22 de nov.

## Alcance

- Creación y manejo de rutas (APIRouter)
- Routers como equivalente MVC de controladores
- Dependency injection y manejo de solicitudes
- Integración con SQLAlchemy (persistencia)
- Testing con pytest y TestClient

## Temas evaluados

| Tema | Peso | Detalle |
|------|------|---------|
| Rutas y APIRouter | 25% | Path params, query params, POST/PUT/DELETE |
| Routers + DI | 25% | Depends, dependency injection, lógica de negocio |
| SQLAlchemy | 25% | Modelos ORM, Session, CRUD, relaciones |
| Testing | 25% | pytest, TestClient, fixtures, cobertura |

## Formato del examen

- **Duración:** 120 minutos
- **Tipo:** Práctico (proyecto integrador)
- **Puntaje:** 100 puntos

### Parte 1: Rutas y Routers (30 pts)

1. Crear un módulo de rutas con APIRouter para un recurso (ej: cursos) (15 pts)
2. Implementar CRUD completo: GET (lista + individual), POST, PUT, DELETE (15 pts)

### Parte 2: Lógica de negocio + BD (35 pts)

1. Crear modelo SQLAlchemy con al menos 2 campos (10 pts)
2. Implementar dependency injection para la sesión de BD (10 pts)
3. Crear endpoint que realice operaciones CRUD reales contra la BD (15 pts)

### Parte 3: Testing (35 pts)

1. Escribir al menos 3 tests para los endpoints creados (15 pts)
2. Usar fixture de TestClient y override_get_db (10 pts)
3. Verificar códigos de estado y estructura de respuesta (10 pts)

## Requisitos previos

- FastAPI + SQLAlchemy instalados
- Proyecto con estructura modular (routers/, models/, schemas/)
- pytest instalado

## Material de estudio

- Semanas 12-14
- Ejemplos guiados de rutas, SQLAlchemy y testing
- Ejercicios de CRUD completo

## Criterios de evaluación

- Uso correcto de APIRouter y dependency injection
- Modelos SQLAlchemy bien definidos con relaciones
- Tests que cubran los casos principales (éxito, error, validación)
- Código modular y siguiendo arquitectura de capas
