from pydantic import BaseModel, Field


class EstudianteCreate(BaseModel):
    """Datos que el cliente envia para CREAR un estudiante."""

    nombre: str = Field(
        min_length=2,
        max_length=100,
        examples=["Maria Garcia"],
    )
    email: str = Field(
        min_length=5,
        max_length=120,
        examples=["maria@universidad.edu"],
    )
    semestre: int = Field(
        ge=1,
        le=10,
        examples=[3],
    )


class EstudianteUpdate(BaseModel):
    """Datos que el cliente envia para ACTUALIZAR un estudiante."""

    nombre: str = Field(
        min_length=2,
        max_length=100,
        examples=["Maria Garcia Lopez"],
    )
    email: str = Field(
        min_length=5,
        max_length=120,
        examples=["maria.garcia@universidad.edu"],
    )
    semestre: int = Field(
        ge=1,
        le=10,
        examples=[4],
    )


class EstudianteResponse(BaseModel):
    """Datos que el servidor DEVUELVE como respuesta."""

    id: int
    nombre: str
    email: str
    semestre: int
    activo: bool
