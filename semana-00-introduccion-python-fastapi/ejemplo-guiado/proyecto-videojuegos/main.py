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
