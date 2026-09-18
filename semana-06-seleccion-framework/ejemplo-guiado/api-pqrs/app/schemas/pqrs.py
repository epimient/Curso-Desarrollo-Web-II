from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, EmailStr, field_validator


class PQRSTypeEnum(str, Enum):
    """
    Tipos de solicitudes PQRS según la normativa legal y de atención al ciudadano.
    """
    PETICION = "peticion"
    QUEJA = "queja"
    RECLAMO = "reclamo"
    SUGERENCIA = "sugerencia"


class PQRSStatusEnum(str, Enum):
    """
    Estados por los que transita un radicado de PQRS.
    """
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    RESUELTO = "resuelto"
    RECHAZADO = "rechazado"


class PQRSBase(BaseModel):
    """
    Campos base compartidos para una solicitud de PQRS.
    """
    titulo: str = Field(
        ...,
        min_length=5,
        max_length=120,
        description="Resumen breve del motivo de la PQRS",
        examples=["Demora en la entrega de certificado académico"]
    )
    descripcion: str = Field(
        ...,
        min_length=15,
        max_length=1000,
        description="Detalle explicativo completo de la solicitud",
        examples=["El pasado 10 de marzo solicité mi certificado de notas y aún no he recibido respuesta en el correo institucional."]
    )
    tipo: PQRSTypeEnum = Field(
        ...,
        description="Tipo de solicitud: petición, queja, reclamo o sugerencia",
        examples=[PQRSTypeEnum.RECLAMO]
    )
    dependencia_destino: str = Field(
        default="Atención al Usuario",
        min_length=3,
        max_length=80,
        description="Dependencia u oficina encargada de gestionar la PQRS",
        examples=["Secretaría Académica"]
    )
    es_anonimo: bool = Field(
        default=False,
        description="Indica si la solicitud se radica de forma anónima"
    )


class PQRSCreate(PQRSBase):
    """
    Esquema de entrada para crear/radicar una PQRS.
    Incluye validaciones estrictas en el envío.
    """
    nombre_solicitante: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nombre completo del ciudadano (obligatorio si no es anónimo)",
        examples=["Carlos Eduardo Pérez"]
    )
    email_contacto: Optional[str] = Field(
        default=None,
        description="Correo electrónico para recibir notificaciones de respuesta",
        examples=["carlos.perez@ejemplo.com"]
    )

    @field_validator("email_contacto")
    @classmethod
    def validar_email_si_no_es_anonimo(cls, v: Optional[str], info) -> Optional[str]:
        """
        Valida que si la solicitud no es anónima, se provea un correo válido.
        """
        es_anonimo = info.data.get("es_anonimo", False)
        if not es_anonimo and not v:
            raise ValueError("El correo de contacto es obligatorio a menos que la solicitud sea anónima.")
        if v and "@" not in v:
            raise ValueError("El correo electrónico no tiene un formato válido.")
        return v


class PQRSStatusUpdate(BaseModel):
    """
    Esquema para actualizar el estado de una PQRS existente.
    """
    nuevo_estado: PQRSStatusEnum = Field(
        ...,
        description="Nuevo estado a asignar al radicado",
        examples=[PQRSStatusEnum.EN_PROCESO]
    )
    nota_respuesta: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Comentario o justificación del cambio de estado",
        examples=["El caso ha sido remitido a la coordinación de Admisiones para revisión de firma."]
    )


class PQRSResponse(PQRSBase):
    """
    Esquema de respuesta devuelto al cliente tras la radicación o consulta de una PQRS.
    """
    id: int = Field(..., description="Identificador numérico interno", examples=[1])
    codigo_radicado: str = Field(..., description="Código único de seguimiento público", examples=["PQRS-2026-0001"])
    nombre_solicitante: Optional[str] = Field(default=None, examples=["Carlos Eduardo Pérez"])
    email_contacto: Optional[str] = Field(default=None, examples=["carlos.perez@ejemplo.com"])
    estado: PQRSStatusEnum = Field(..., description="Estado actual de la PQRS", examples=[PQRSStatusEnum.PENDIENTE])
    dias_plazo_respuesta: int = Field(..., description="Días hábiles máximos para dar respuesta por norma", examples=[15])
    fecha_creacion: datetime = Field(..., description="Fecha y hora de radicación")
    nota_respuesta: Optional[str] = Field(default=None, description="Última nota o resolución del equipo")

    class Config:
        from_attributes = True


class PQRSStatsResponse(BaseModel):
    """
    Esquema para el resumen estadístico de la API de PQRS.
    """
    total_radicados: int = Field(..., examples=[42])
    por_tipo: Dict[str, int] = Field(..., examples=[{"peticion": 20, "queja": 10, "reclamo": 8, "sugerencia": 4}])
    por_estado: Dict[str, int] = Field(..., examples=[{"pendiente": 15, "en_proceso": 20, "resuelto": 7, "rechazado": 0}])
