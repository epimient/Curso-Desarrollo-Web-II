# Anexo - Ejemplo extra de APIRouter: API de biblioteca

> Este anexo contiene material complementario sobre `APIRouter` para reforzar los conceptos de la Clase 05. Incluye un ejemplo completo de una API de biblioteca con dos routers (libros y autores) y una seccion de errores frecuentes.

---

## Ejemplo completo: API de biblioteca

### Estructura del proyecto

```text
biblioteca_api/
  main.py
  routers/
    __init__.py
    libros.py
    autores.py
  requirements.txt
```

### Paso 1: `main.py`

```python
from fastapi import FastAPI

from routers import libros, autores

app = FastAPI(
    title="API de Biblioteca",
    description="Ejemplo complementario de APIRouter",
    version="1.0.0",
)

app.include_router(libros.router)
app.include_router(autores.router)
```

### Paso 2: `routers/libros.py`

```python
from fastapi import APIRouter

router = APIRouter(prefix="/libros", tags=["Libros"])

LIBROS = [
    {"id": 1, "titulo": "Clean Code", "autor": "Robert C. Martin", "anio": 2008},
    {"id": 2, "titulo": "Fluent Python", "autor": "Luciano Ramalho", "anio": 2015},
    {"id": 3, "titulo": "Python Crash Course", "autor": "Eric Matthes", "anio": 2019},
]


@router.get("/")
def listar_libros():
    return LIBROS


@router.get("/{libro_id}")
def obtener_libro(libro_id: int):
    for libro in LIBROS:
        if libro["id"] == libro_id:
            return libro
    return {"error": "Libro no encontrado"}
```

### Paso 3: `routers/autores.py`

```python
from fastapi import APIRouter

router = APIRouter(prefix="/autores", tags=["Autores"])

AUTORES = [
    {"id": 1, "nombre": "Robert C. Martin", "nacionalidad": "EE.UU."},
    {"id": 2, "nombre": "Luciano Ramalho", "nacionalidad": "Brasil"},
    {"id": 3, "nombre": "Eric Matthes", "nacionalidad": "EE.UU."},
]


@router.get("/")
def listar_autores():
    return AUTORES


@router.get("/{autor_id}")
def obtener_autor(autor_id: int):
    for autor in AUTORES:
        if autor["id"] == autor_id:
            return autor
    return {"error": "Autor no encontrado"}
```

### Paso 4: Ejecutar

```bash
uvicorn main:app --reload
```

### Paso 5: Probar

| URL | Resultado esperado |
|---|---|
| `GET /libros` | Lista de 3 libros |
| `GET /libros/1` | Clean Code |
| `GET /libros/999` | `{"error": "Libro no encontrado"}` |
| `GET /autores` | Lista de 3 autores |
| `GET /autores/2` | Luciano Ramalho |
| `GET /docs` | Documentacion con grupos "Libros" y "Autores" |

---

## Errores frecuentes con APIRouter (recordatorio)

### Error 1: Olvidar `app.include_router()`

```python
# ❌ El router existe pero no esta conectado
from routers import libros
app = FastAPI(...)
# falta: app.include_router(libros.router)
```

**Sintoma:** Los endpoints no aparecen en `/docs`.  
**Solucion:** Agrega `app.include_router(libros.router)`.

### Error 2: Usar `@app.get()` en lugar de `@router.get()`

```python
# ❌ MAL: estas decorando la app, no el router
router = APIRouter()

@app.get("/test")  # ❌ Deberia ser @router.get("/test")
def test():
    return {"ok": True}
```

**Sintoma:** El endpoint funciona pero no esta agrupado.  
**Solucion:** Usa `@router.get()`, no `@app.get()`.

### Error 3: Duplicar el prefijo

```python
router = APIRouter(prefix="/libros")

@router.get("/libros")  # ❌ Resultado: /libros/libros
def listar():
    ...
```

**Sintoma:** La ruta queda duplicada (`/libros/libros`).  
**Solucion:** Usa `@router.get("/")`, no `@router.get("/libros")`.

### Error 4: Olvidar `__init__.py`

```python
# Si falta routers/__init__.py
from routers import libros  # ❌ ModuleNotFoundError
```

**Sintoma:** `ModuleNotFoundError: No module named 'routers'`.  
**Solucion:** Crea `routers/__init__.py` (puede estar vacio).

---

## Comparativa: Sin APIRouter vs Con APIRouter

| Aspecto | Sin APIRouter (todo en main.py) | Con APIRouter (archivos separados) |
|---|---|---|
| Tamano de main.py | 50+ lineas | 10-15 lineas |
| Encontrar un endpoint | Buscar en todo el archivo | Ir al archivo especifico |
| Trabajo en equipo | Conflictos de Git constantes | Cada quien edita su router |
| Reutilizar rutas | Copiar y pegar | Importar el router |
| Documentacion en /docs | Todo mezclado | Agrupado por tags |

---

## Ejercicio de practica adicional

Crea un tercer router `routers/prestamos.py` con:

```python
router = APIRouter(prefix="/prestamos", tags=["Prestamos"])
```

Endpoints:
- `GET /prestamos` → lista vacia (simula prestamos futuros)
- `GET /prestamos/{prestamo_id}` → `{"id": prestamo_id, "estado": "activo"}`

Registra el router en `main.py` y verifica en `/docs` que aparezcan los 3 grupos: Libros, Autores, Prestamos.
