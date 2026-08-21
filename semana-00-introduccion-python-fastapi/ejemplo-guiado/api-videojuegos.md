# Ejemplo guiado — API de Videojuegos

## Objetivo

Crear una API basica de videojuegos usando FastAPI. Al final tendras:
- Un endpoint GET que retorne una lista de videojuegos
- Un endpoint GET individual por ID
- Swagger UI para probar todo

## Paso 0. Requisitos previos

- Python 3.10+ instalado
- pip instalado

## Paso 1. Crear entorno virtual

```bash
mkdir proyecto-videojuegos
cd proyecto-videojuegos
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
```

## Paso 2. Instalar FastAPI

```bash
pip install "fastapi[standard]"
```

## Paso 3. Crear el archivo main.py

```python
from fastapi import FastAPI

app = FastAPI(title="API de Videojuegos")

# Base de datos simulada
videojuegos = [
    {"id": 1, "titulo": "Doom", "anio": 1993, "genero": "Accion"},
    {"id": 2, "titulo": "Half-Life", "anio": 1998, "genero": "Accion"},
    {"id": 3, "titulo": "The Sims", "anio": 2000, "genero": "Simulacion"},
    {"id": 4, "titulo": "Minecraft", "anio": 2011, "genero": "Sandbox"},
]


@app.get("/")
def inicio():
    return {"mensaje": "API de videojuegos"}


@app.get("/videojuegos")
def obtener_videojuegos():
    return videojuegos


@app.get("/videojuegos/{id}")
def obtener_videojuego(id: int):
    for v in videojuegos:
        if v["id"] == id:
            return v
    return {"error": "Videojuego no encontrado"}
```

## Paso 4. Ejecutar

```bash
fastapi dev main.py
```

## Paso 5. Probar en Swagger

1. Abrir `http://localhost:8000/docs`
2. Probar `GET /` — debe retornar el mensaje de bienvenida
3. Probar `GET /videojuegos` — debe retornar la lista completa
4. Probar `GET /videojuegos/1` — debe retornar Doom
5. Probar `GET /videojuegos/99` — debe retornar error

## Paso 6. Experimentar

Intenta:
- Agregar un videojuego nuevo a la lista
- Cambiar el mensaje de bienvenida
- Agregar un campo nuevo (plataforma, calificacion)

## Conceptos clave aplicados

| Concepto | Ejemplo en el codigo |
|----------|---------------------|
| Funcion | `def inicio():` |
| Ruta | `@app.get("/")` |
| Parametro de ruta | `id: int` en `/videojuegos/{id}` |
| Respuesta JSON | `return {"mensaje": "..."}` |
| Lista Python | `videojuegos = [...]` |
| Diccionario | `{"id": 1, "titulo": "Doom"}` |
