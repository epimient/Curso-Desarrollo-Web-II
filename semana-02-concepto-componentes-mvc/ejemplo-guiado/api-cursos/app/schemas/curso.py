from pydantic import BaseModel, Field


class CursoCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=80)
    creditos: int = Field(ge=1, le=6)


class CursoResponse(BaseModel):
    id: int
    nombre: str
    creditos: int
    activo: bool
