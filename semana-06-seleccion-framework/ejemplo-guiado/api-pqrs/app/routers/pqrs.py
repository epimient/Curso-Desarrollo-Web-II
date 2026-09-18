from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query

from app.schemas.pqrs import (
    PQRSCreate,
    PQRSResponse,
    PQRSStatusUpdate,
    PQRSStatsResponse,
    PQRSTypeEnum,
    PQRSStatusEnum,
)

# Inicializamos el APIRouter para aislar la lógica del módulo de PQRS
router = APIRouter(
    prefix="/pqrs",
    tags=["PQRS - Peticiones, Quejas, Reclamos y Sugerencias"]
)

# Base de datos simulada en memoria para la Semana 06
# (En las semanas 12 y 13 aprenderemos a conectar SQLAlchemy con SQLite/PostgreSQL)
BD_PQRS_SIMULADA: List[dict] = [
    {
        "id": 1,
        "codigo_radicado": "PQRS-2026-0001",
        "titulo": "Consulta sobre proceso de matricula extemporanea",
        "descripcion": "Quisiera solicitar información sobre las fechas de matricula extemporánea para el periodo actual.",
        "tipo": PQRSTypeEnum.PETICION,
        "dependencia_destino": "Admisiones y Registro",
        "es_anonimo": False,
        "nombre_solicitante": "Ana Maria Gomez",
        "email_contacto": "ana.gomez@ejemplo.com",
        "estado": PQRSStatusEnum.RESUELTO,
        "dias_plazo_respuesta": 15,
        "fecha_creacion": datetime(2026, 3, 1, 9, 30, 0),
        "nota_respuesta": "Se envió el calendario de fechas extemporáneas al correo institucional de la estudiante."
    },
    {
        "id": 2,
        "codigo_radicado": "PQRS-2026-0002",
        "titulo": "Falla recurrente en la red WiFi de la biblioteca",
        "descripcion": "La conexión inalámbrica en el piso 2 de la biblioteca principal presenta caídas constantes desde el lunes.",
        "tipo": PQRSTypeEnum.QUEJA,
        "dependencia_destino": "Tecnología de la Información",
        "es_anonimo": True,
        "nombre_solicitante": None,
        "email_contacto": None,
        "estado": PQRSStatusEnum.EN_PROCESO,
        "dias_plazo_respuesta": 10,
        "fecha_creacion": datetime(2026, 3, 5, 14, 15, 0),
        "nota_respuesta": "El equipo técnico se encuentra realizando mantenimiento a los puntos de acceso del segundo piso."
    }
]

# Contador secuencial para simular IDs incrementales
_contador_id = 3


def _calcular_dias_plazo(tipo: PQRSTypeEnum) -> int:
    """
    Función auxiliar para determinar los días hábiles de plazo legal según el tipo de PQRS.
    - Petición: 15 días hábiles
    - Queja / Reclamo: 15 días hábiles
    - Sugerencia: 10 días hábiles
    """
    plazos = {
        PQRSTypeEnum.PETICION: 15,
        PQRSTypeEnum.QUEJA: 15,
        PQRSTypeEnum.RECLAMO: 15,
        PQRSTypeEnum.SUGERENCIA: 10,
    }
    return plazos.get(tipo, 15)


@router.post(
    "/",
    response_model=PQRSResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Radicar una nueva PQRS",
    description="Recibe los datos de una solicitud de PQRS, aplica validación de esquemas con Pydantic y genera un código de radicado único."
)
def crear_pqrs(pqrs_in: PQRSCreate):
    global _contador_id
    
    nuevo_id = _contador_id
    codigo = f"PQRS-2026-{nuevo_id:04d}"
    _contador_id += 1

    registro = {
        "id": nuevo_id,
        "codigo_radicado": codigo,
        "titulo": pqrs_in.titulo,
        "descripcion": pqrs_in.descripcion,
        "tipo": pqrs_in.tipo,
        "dependencia_destino": pqrs_in.dependencia_destino,
        "es_anonimo": pqrs_in.es_anonimo,
        "nombre_solicitante": None if pqrs_in.es_anonimo else pqrs_in.nombre_solicitante,
        "email_contacto": None if pqrs_in.es_anonimo else pqrs_in.email_contacto,
        "estado": PQRSStatusEnum.PENDIENTE,
        "dias_plazo_respuesta": _calcular_dias_plazo(pqrs_in.tipo),
        "fecha_creacion": datetime.now(),
        "nota_respuesta": None
    }

    BD_PQRS_SIMULADA.append(registro)
    return registro


@router.get(
    "/",
    response_model=List[PQRSResponse],
    summary="Listar todas las PQRS registradas",
    description="Retorna el listado completo de solicitudes radicadas. Permite filtrar por tipo y por estado mediante Query Parameters."
)
def listar_pqrs(
    tipo: Optional[PQRSTypeEnum] = Query(None, description="Filtrar por tipo de PQRS"),
    estado: Optional[PQRSStatusEnum] = Query(None, description="Filtrar por estado del radicado")
):
    resultados = BD_PQRS_SIMULADA

    if tipo:
        resultados = [p for p in resultados if p["tipo"] == tipo]
    if estado:
        resultados = [p for p in resultados if p["estado"] == estado]

    return resultados


@router.get(
    "/estadisticas/resumen",
    response_model=PQRSStatsResponse,
    summary="Obtener métricas y resumen estadístico",
    description="Muestra el conteo total de PQRS radicadas agrupadas por tipo y estado."
)
def obtener_estadisticas():
    total = len(BD_PQRS_SIMULADA)
    
    por_tipo = {t.value: 0 for t in PQRSTypeEnum}
    por_estado = {e.value: 0 for e in PQRSStatusEnum}

    for item in BD_PQRS_SIMULADA:
        por_tipo[item["tipo"].value if isinstance(item["tipo"], PQRSTypeEnum) else item["tipo"]] += 1
        por_estado[item["estado"].value if isinstance(item["estado"], PQRSStatusEnum) else item["estado"]] += 1

    return {
        "total_radicados": total,
        "por_tipo": por_tipo,
        "por_estado": por_estado
    }


@router.get(
    "/{codigo_radicado}",
    response_model=PQRSResponse,
    summary="Consultar una PQRS por su código de radicado",
    description="Busca una solicitud específica usando el código público (ejemplo: PQRS-2026-0001). Retorna 404 si no existe."
)
def obtener_pqrs_por_codigo(codigo_radicado: str):
    for pqrs in BD_PQRS_SIMULADA:
        if pqrs["codigo_radicado"].upper() == codigo_radicado.upper():
            return pqrs

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se encontró ninguna PQRS radicada con el código '{codigo_radicado}'."
    )


@router.patch(
    "/{codigo_radicado}/estado",
    response_model=PQRSResponse,
    summary="Actualizar el estado de una PQRS",
    description="Permite a los administradores o gestores modificar el estado del radicado (ejemplo: pasar de PENDIENTE a EN_PROCESO)."
)
def actualizar_estado_pqrs(codigo_radicado: str, datos_update: PQRSStatusUpdate):
    for pqrs in BD_PQRS_SIMULADA:
        if pqrs["codigo_radicado"].upper() == codigo_radicado.upper():
            pqrs["estado"] = datos_update.nuevo_estado
            if datos_update.nota_respuesta:
                pqrs["nota_respuesta"] = datos_update.nota_respuesta
            return pqrs

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar el estado: el radicado '{codigo_radicado}' no existe."
    )
