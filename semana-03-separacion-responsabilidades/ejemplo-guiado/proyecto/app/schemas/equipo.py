from pydantic import BaseModel, Field


class EquipoCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=80)
    categoria: str = Field(..., min_length=3, max_length=50)


class EquipoResponse(BaseModel):
    id: int
    nombre: str
    categoria: str
    disponible: bool
