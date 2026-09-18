# Ejemplo Guiado: API de PQRS con FastAPI

Este directorio contiene el proyecto funcional de demostración para la **Semana 06: Selección de un framework específico (FastAPI)**.

## 🎯 Objetivo

Demostrar las características técnicas clave que justifican la elección de FastAPI sobre otros frameworks (como Django o Flask):

1. **Validación automática** de tipos y estructuras con Pydantic.
2. **Documentación automática e interactiva** con Swagger UI (`/docs`).
3. **Organización modular** usando `APIRouter`.
4. **Manejo declarativo de respuestas HTTP** (201 Created, 404 Not Found, 422 Unprocessable Entity).

---

## 📁 Estructura del Proyecto

```text
api-pqrs/
├── app/
│   ├── __init__.py
│   ├── main.py              # Instancia principal de FastAPI y configuración
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── pqrs.py          # Modelos de Pydantic (entrada, salida y validaciones)
│   └── routers/
│       ├── __init__.py
│       └── pqrs.py          # Endpoints de la API de PQRS y lógica simulada
├── GUIA-COMPLETA.md         # Explicación paso a paso de cada componente
├── README.md                # Este archivo de instrucciones
└── requirements.txt         # Dependencias del proyecto
```

---

## 🚀 Pasos para Ejecutar

### 1. Crear y activar el entorno virtual

En la terminal (dentro de la carpeta `api-pqrs`):

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Iniciar el servidor Uvicorn

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Cómo Probar la API

Abre tu navegador de preferencia e ingresa a:

- **Swagger UI (Interactiva):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc (Lectura limpia):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Ejemplos de Pruebas Rápidas en Swagger UI:

1. **Radicar PQRS válida (`POST /api/v1/pqrs/`):**
   ```json
   {
     "titulo": "Inconveniente con usuario del aula virtual",
     "descripcion": "No puedo visualizar la asignatura de Web II en el panel de materias inscritas.",
     "tipo": "peticion",
     "dependencia_destino": "Sistemas de Información",
     "es_anonimo": false,
     "nombre_solicitante": "Laura Restrepo",
     "email_contacto": "laura.restrepo@ejemplo.com"
   }
   ```
   *Respuesta esperada:* `201 Created` con código generado como `PQRS-2026-0003`.

2. **Probar la validación de errores Pydantic (`422 Unprocessable Entity`):**
   Envía la petición anterior cambiando `"titulo": "Hola"` (menos de 5 caracteres) o omitiendo `"email_contacto"` cuando `es_anonimo` es `false`. Verás cómo FastAPI genera una respuesta de error detallada sin escribir código de validación manual.

3. **Consultar estadísticas (`GET /api/v1/pqrs/estadisticas/resumen`):**
   Retorna el conteo por tipo y estado.

4. **Consultar por código (`GET /api/v1/pqrs/PQRS-2026-0001`):**
   Retorna los detalles del radicado. Si consultas uno inexistente (`PQRS-2026-9999`), obtendrás un `404 Not Found`.

---

## 📖 Guía Explicativa Completa

Para un desglose conceptual línea por línea y la relación con los objetivos de la Semana 06, consulta el archivo [GUIA-COMPLETA.md](file:///home/eddy/Documentos/DOCENTE%202026/WEB%20II/curso-desarrollo-web-ii-fastapi/semana-06-seleccion-framework/ejemplo-guiado/api-pqrs/GUIA-COMPLETA.md).
