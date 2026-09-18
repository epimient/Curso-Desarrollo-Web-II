# Guía Completa: Construcción de una API de PQRS con FastAPI (Semana 06)

Bienvenido a la guía explicativa del proyecto guiado de la **Semana 06**. En esta guía analizaremos paso a paso el código del **Sistema de PQRS (Peticiones, Quejas, Reclamos y Sugerencias)** para entender cómo FastAPI resuelve problemas comunes del desarrollo de APIs web de forma moderna, rápida y segura.

---

## 💡 ¿Por qué un Sistema de PQRS para evaluar FastAPI?

El dominio de PQRS es muy común en aplicaciones gubernamentales, universitarias y corporativas. Presenta retos típicos que todo desarrollador backend debe resolver:

- **Diferentes tipos de solicitudes** (Petición, Queja, Reclamo, Sugerencia) con reglas y plazos legales específicos.
- **Validación de entrada estricta** (correos válidos, campos obligatorios condicionales como el anonimato).
- **Ciclo de vida de estados** (Pendiente → En Proceso → Resuelto / Rechazado).
- **Necesidad de documentación interactiva** para que el equipo de frontend o los ciudadanos entiendan cómo interactuar con el servicio.

---

## 🔍 Análisis del Código por Componentes

### 1. Definición de Esquemas con Pydantic (`app/schemas/pqrs.py`)

En frameworks como Flask, los datos que vienen en la petición HTTP (`request.json`) deben ser validados manualmente con `if/else` o con librerías externas.

En **FastAPI**, **Pydantic** se integra de forma nativa:

```python
class PQRSCreate(PQRSBase):
    nombre_solicitante: Optional[str] = Field(default=None, max_length=100)
    email_contacto: Optional[str] = Field(default=None)

    @field_validator("email_contacto")
    @classmethod
    def validar_email_si_no_es_anonimo(cls, v: Optional[str], info) -> Optional[str]:
        es_anonimo = info.data.get("es_anonimo", False)
        if not es_anonimo and not v:
            raise ValueError("El correo de contacto es obligatorio a menos que la solicitud sea anónima.")
        if v and "@" not in v:
            raise ValueError("El correo electrónico no tiene un formato válido.")
        return v
```

#### Ventajas clave demostradas aquí:
- **Parseo y tipado automático:** Si el cliente envía `es_anonimo: "falso"`, Pydantic no falla a menos que la conversión sea imposible.
- **Mensajes de error estandarizados (`422 Unprocessable Entity`):** FastAPI genera una estructura de error legible automáticamente indicando exactamente qué campo falló.

---

### 2. Endpoints y Controladores Modularizados (`app/routers/pqrs.py`)

El uso de `APIRouter` permite organizar el proyecto en módulos separados, evitando archivos gigantescos.

```python
router = APIRouter(
    prefix="/pqrs",
    tags=["PQRS - Peticiones, Quejas, Reclamos y Sugerencias"]
)
```

#### Endpoint para Radicar una PQRS (`POST /api/v1/pqrs/`):

```python
@router.post(
    "/",
    response_model=PQRSResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Radicar una nueva PQRS"
)
def crear_pqrs(pqrs_in: PQRSCreate):
    ...
```

#### Lo que FastAPI hace tras bambalinas:
1. Lee el cuerpo JSON de la petición HTTP.
2. Inyecta los datos parseados en el objeto `pqrs_in` del tipo `PQRSCreate`.
3. Ejecuta la función `crear_pqrs`.
4. Filtra y serializa el diccionario resultante según `PQRSResponse` (garantizando que no filtremos campos sensibles).
5. Devuelve la respuesta con código `201 Created` e `Content-Type: application/json`.

---

### 3. Manejo Elegante de Errores con `HTTPException`

Para consultar una PQRS por su número de radicado:

```python
@router.get("/{codigo_radicado}", response_model=PQRSResponse)
def obtener_pqrs_por_codigo(codigo_radicado: str):
    for pqrs in BD_PQRS_SIMULADA:
        if pqrs["codigo_radicado"].upper() == codigo_radicado.upper():
            return pqrs

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se encontró ninguna PQRS radicada con el código '{codigo_radicado}'."
    )
```

Al lanzar `HTTPException`, FastAPI detiene la ejecución inmediatamente y retorna un JSON con el mensaje formateado y el código HTTP `404`.

---

### 4. Configuración Principal y Swagger UI (`app/main.py`)

```python
app = FastAPI(
    title="API de PQRS - Sistema de Atención al Ciudadano",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

Sin escribir una sola línea de código HTML o YAML para Swagger, FastAPI inspecciona los comentarios, los modelos de Pydantic y los tipos de retorno para generar la documentación en `http://localhost:8000/docs`.

---

## 📊 Cuadro Comparativo: FastAPI vs Flask vs Django en este Caso

| Criterio en el Caso PQRS | FastAPI | Flask | Django |
|--------------------------|---------|-------|--------|
| **Validación de Datos en `POST /pqrs`** | Automática con Pydantic | Manual o con Marshmallow / Webargs | Mediante Django Forms / Serializers DRF |
| **Documentación Interactivas `/docs`** | Incluida de fábrica (OpenAPI 3.0) | Requiere librerías extra (Flasgger) | Requiere DRF + drf-spectacular |
| **Estructura Modular** | `APIRouter` limpia y liviana | `Blueprints` | `Apps` completas (excesivas para microservicios) |
| **Rendimiento** | Basado en Starlette + Uvicorn (Ultra rápido) | WSGI Tradicional (más lento) | WSGI Tradicional |

---

## 🎯 Conclusión para los Estudiantes

Este proyecto demuestra que **FastAPI es la mejor elección para aplicaciones orientadas a APIs REST**:
1. Nos permite enfocarnos en las reglas de negocio (plazos de PQRS, tipos de radicado, estados) en lugar de escribir código repetitivo de infraestructura.
2. Produce APIs documentadas desde el minuto 1.
3. El código es fácil de leer, mantener y escalar a medida que agreguemos bases de datos en las siguientes semanas.
