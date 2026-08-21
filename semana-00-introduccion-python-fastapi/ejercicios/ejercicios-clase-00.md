# Ejercicios — Clase 00: Introduccion a Python, APIs y FastAPI

## Ejercicio 0: Verificacion rapida

Antes de empezar, verifica que tienes Python y pip:

```bash
python --version
pip --version
```

Si no los tienes, instala Python desde https://www.python.org/downloads/

---

## Ejercicio 1: Primera funcion Python

Crea un archivo `ejercicio1.py` con una funcion que reciba un nombre y retorne un saludo:

```python
def saludar(nombre):
    return "Hola " + nombre

print(saludar("Ana"))
print(saludar("Carlos"))
```

Ejecuta:

```bash
python ejercicio1.py
```

**Pregunta:** Que imprime?

---

## Ejercicio 2: Diccionarios y listas

Crea una lista de estudiantes donde cada uno sea un diccionario con nombre, edad y carrera:

```python
estudiantes = [
    {"nombre": "Ana", "edad": 20, "carrera": "Sistemas"},
    {"nombre": "Carlos", "edad": 22, "carrera": "Telematica"},
    {"nombre": "Maria", "edad": 19, "carrera": "Sistemas"},
]

for e in estudiantes:
    print(e["nombre"], "-", e["carrera"])
```

**Desafio:** Agrega un campo "promedio" a cada estudiante e imprime solo los que tienen promedio mayor a 4.0.

---

## Ejercicio 3: Tu primera API

1. Crea una carpeta `mi-api`
2. Crea un entorno virtual:
   ```bash
   cd mi-api
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instala FastAPI:
   ```bash
   pip install "fastapi[standard]"
   ```
4. Crea `main.py` con esta API de peliculas:

```python
from fastapi import FastAPI

app = FastAPI()

peliculas = [
    {"id": 1, "titulo": "Inception", "anio": 2010},
    {"id": 2, "titulo": "Matrix", "anio": 1999},
    {"id": 3, "titulo": "Interstellar", "anio": 2014},
]

@app.get("/")
def inicio():
    return {"mensaje": "API de peliculas"}

@app.get("/peliculas")
def obtener_peliculas():
    return peliculas

@app.get("/peliculas/{id}")
def obtener_pelicula(id: int):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            return pelicula
    return {"error": "Pelicula no encontrada"}
```

5. Ejecuta:
   ```bash
   fastapi dev main.py
   ```
6. Abre `http://localhost:8000/docs` y prueba cada endpoint.

---

## Ejercicio 4: Agregar POST

Tomando la API del Ejercicio 3, agrega un endpoint para crear peliculas:

```python
from pydantic import BaseModel

class Pelicula(BaseModel):
    titulo: str
    anio: int

@app.post("/peliculas")
def crear_pelicula(pelicula: Pelicula):
    nueva = {"id": len(peliculas) + 1, **pelicula.model_dump()}
    peliculas.append(nueva)
    return nueva
```

Prueba enviando JSON desde Swagger:

```json
{
    "titulo": "Avatar",
    "anio": 2009
}
```

---

## Ejercicio 5: Query parameters

Agrega un endpoint que filtre peliculas por anio:

```python
@app.get("/peliculas/buscar")
def buscar_peliculas(anio: int = None):
    if anio:
        return [p for p in peliculas if p["anio"] == anio]
    return peliculas
```

Prueba:
- `GET /peliculas/buscar?anio=1999` → Matrix
- `GET /peliculas/buscar` → todas

---

## Ejercicio 6: Refactorizar

Toma la API del Ejercicio 4 y refactorizala para que sea una API de **canciones**:

- Modelo: titulo, artista, anio, genero
- Endpoints: GET lista, GET individual, POST crear
- Agrega query parameter para filtrar por genero

**Bonus:** Agrega un endpoint PUT para actualizar una cancion.
