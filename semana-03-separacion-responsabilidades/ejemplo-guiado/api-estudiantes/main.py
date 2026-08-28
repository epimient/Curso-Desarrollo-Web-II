# main.py — EL MONOLITO (asi NO se deberia mantener)
# Este archivo existe como referencia para comparar con la version refactorizada en app/
from fastapi import FastAPI, HTTPException

app = FastAPI(title="API Estudiantes — Monolito")

# "Base de datos" en memoria
_estudiantes = []
_next_id = 1


@app.get("/estudiantes")
def listar():
    return _estudiantes


@app.get("/estudiantes/{estudiante_id}")
def obtener(estudiante_id: int):
    for e in _estudiantes:
        if e["id"] == estudiante_id:
            return e
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")


@app.post("/estudiantes", status_code=201)
def crear(nombre: str, email: str, semestre: int):
    global _next_id

    # Validacion manual
    if not nombre or len(nombre) < 2:
        raise HTTPException(status_code=400, detail="Nombre muy corto")
    if semestre < 1 or semestre > 10:
        raise HTTPException(status_code=400, detail="Semestre invalido")
    if any(e["email"] == email for e in _estudiantes):
        raise HTTPException(status_code=400, detail="Email duplicado")

    nuevo = {
        "id": _next_id,
        "nombre": nombre,
        "email": email,
        "semestre": semestre,
        "activo": True,
    }
    _estudiantes.append(nuevo)
    _next_id += 1
    return nuevo


@app.put("/estudiantes/{estudiante_id}")
def actualizar(estudiante_id: int, nombre: str, email: str, semestre: int):
    for e in _estudiantes:
        if e["id"] == estudiante_id:
            if semestre < 1 or semestre > 10:
                raise HTTPException(status_code=400, detail="Semestre invalido")
            e["nombre"] = nombre
            e["email"] = email
            e["semestre"] = semestre
            return e
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")


@app.delete("/estudiantes/{estudiante_id}", status_code=204)
def eliminar(estudiante_id: int):
    global _estudiantes
    original = len(_estudiantes)
    _estudiantes = [e for e in _estudiantes if e["id"] != estudiante_id]
    if len(_estudiantes) == original:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
