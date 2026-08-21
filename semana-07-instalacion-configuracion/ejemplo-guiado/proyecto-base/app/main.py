from fastapi import FastAPI

app = FastAPI(
    title="Primera API con FastAPI",
    description="Proyecto inicial para Desarrollo Web II",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"mensaje": "Hola, Desarrollo Web II"}


@app.get("/estado")
def obtener_estado():
    return {"estado": "ok", "framework": "FastAPI"}


@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}


@app.get("/cursos")
def listar_cursos(activo: bool = True):
    cursos = [
        {"id": 1, "nombre": "Desarrollo Web II", "activo": True},
        {"id": 2, "nombre": "Bases de Datos", "activo": False},
        {"id": 3, "nombre": "Ingenieria de Software", "activo": True},
    ]

    filtrados = [curso for curso in cursos if curso["activo"] == activo]

    return {"activo": activo, "total": len(filtrados), "cursos": filtrados}
