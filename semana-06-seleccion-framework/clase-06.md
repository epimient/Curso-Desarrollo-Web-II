# Clase 06 - Seleccion de un framework especifico

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 6  
**Unidad:** Unidad 2 - Desarrollo con FastAPI  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA2: Analizar las ventajas y desventajas de utilizar frameworks en el desarrollo de aplicaciones web mediante la comparacion de diferentes frameworks y su aplicabilidad en distintos contextos.
- RA3: Seleccionar un framework de desarrollo web adecuado para un proyecto especifico mediante la evaluacion de criterios tecnicos, funcionales y de sostenibilidad.

## 2. Proposito de la clase

Esta clase formaliza la decision de usar FastAPI como framework del curso. Despues de haber comparado frameworks en la semana 4, ahora toca defender esa decision con argumentos tecnicos concretos y entender exactamente que ofrece FastAPI y que no ofrece.

El objetivo no es convencer de que FastAPI es "el mejor framework". El objetivo es que cada estudiante pueda justificar por que FastAPI es la mejor opcion para el tipo de proyecto que vamos a construir: una API REST moderna, rapida y bien documentada.

## 3. Pregunta orientadora

**Por que FastAPI y no otro framework para este curso y estos proyectos?**

Esta pregunta obliga a pasar de la opinion personal a la justificacion tecnica.

## 4. Resumen: que vimos en la comparacion

En la semana 4 comparamos frameworks. Aqui el resumen rapido:

| Framework | Tipo | Lenguaje | Mejor para |
|-----------|------|----------|------------|
| Django | Full-stack | Python | Apps completas, admin, ORM integrado |
| Flask | Microframework | Python | Apps pequenas, flexibles, learning |
| Laravel | Full-stack | PHP | Apps web tradicionales, e-commerce |
| ASP.NET Core | Full-stack | C# | Empresarial, seguridad, alto rendimiento |
| **FastAPI** | **API framework** | **Python** | **APIs modernas, rapidas, tipadas** |

## 5. Por que FastAPI: argumentos tecnicos

### 5.1 Rendimiento

FastAPI es uno de los frameworks mas rapidos de Python. Gracias a Starlette y Uvicorn, puede manejar miles de peticiones por segundo.

**Comparacion approximate (requests/segundo):**

| Framework | Rendimiento |
|-----------|-------------|
| Flask | ~1,000 |
| Django | ~800 |
| FastAPI | ~12,000+ |

> **En espanol simple:** FastAPI es como un auto deportivo: esta disenado para velocidad. Django es como un camion: lleva mucha carga, pero no va tan rapido.

### 5.2 Tipo de aplicacion: API REST

El curso se enfoca en crear APIs REST, no en renderizar HTML del lado del servidor. FastAPI esta disenado exactamente para eso:

- Endpoints que reciben JSON y retornan JSON
- Documentacion automatica (Swagger UI)
- Validacion automatica de request/response
- Soporte nativo para async/await

Django y Laravel pueden hacer APIs, pero su fortaleza es el renderizado HTML del lado del servidor. FastAPI es especialista en APIs.

### 5.3 Validacion con Pydantic

FastAPI usa Pydantic para validar datos automaticamente. Esto significa:

- Validacion de tipos en runtime
- Documentacion automatica basada en los schemas
- Errores claros cuando los datos no son correctos
- Schemas reutilizables entre endpoints

```python
from pydantic import BaseModel, Field

class CursoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    creditos: int = Field(..., gt=0, le=10)
```

Si alguien envia `creditos: -5`, FastAPI rechaza automaticamente la peticion con un error claro. No necesitas escribir codigo de validacion manual.

### 5.4 Documentacion automatica

FastAPI genera Swagger UI y ReDoc automaticamente. Esto es enorme para:

- Probar endpoints sin herramientas externas
- Compartir la API con otros desarrolladores
- Documentar la API sin esfuerzo extra

```bash
# Swagger UI
http://localhost:8000/docs

# ReDoc
http://localhost:8000/redoc
```

### 5.5 Async nativo

FastAPI soporta `async/await` nativamente. Esto es importante para:

- Operaciones de red (consultas a BD, llamadas a APIs externas)
- Manejo de multiples peticiones concurrentes
- Aplicaciones que necesitan alto rendimiento

### 5.6 Dependencias e inyeccion

FastAPI tiene un sistema de dependencias que facilita:

- Compartir logica entre endpoints
- Manejar sesiones de base de datos
- Autenticacion y autorizacion
- Testing con mocks

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/cursos")
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(Curso).all()
```

## 6. Que NO hace FastAPI (limitaciones)

| Limitacion | Explicacion | Solucion |
|------------|-------------|----------|
| No tiene admin panel | No genera un panel de administracion automatico | Usar SQLAlchemy Admin o crear uno manualmente |
| No tiene ORM integrado | No incluye un ORM como Django | Usar SQLAlchemy (lo hacemos en el curso) |
| No tiene sistema de autenticacion completo | No incluye login/registro como Django | Crear con python-jose y passlib (lo hacemos en el curso) |
| No renderiza HTML del lado del servidor | No tiene template engine integrado | Usar Jinja2 si es necesario, o enfocarse en APIs |
| No tiene migraciones integradas | No incluye un sistema de migraciones | Usar Alembic |

> **En espanol simple:** FastAPI es como un auto deportivo: es rapido y elegante, pero no viene con baule. Si necesitas baule (admin, ORM, auth), lo agregas tu. La ventaja es que solo agregas lo que necesitas.

## 7. Decision formal: FastAPI para el curso

### 7.1 Criterios de seleccion

| Criterio | Peso | FastAPI | Django | Flask |
|----------|------|---------|--------|-------|
| Enfoque en APIs | 30% | 10/10 | 6/10 | 7/10 |
| Rendimiento | 20% | 10/10 | 6/10 | 7/10 |
| Documentacion automatica | 15% | 10/10 | 4/10 | 3/10 |
| Curva de aprendizaje | 15% | 8/10 | 7/10 | 9/10 |
| Ecosistema Python | 10% | 8/10 | 10/10 | 8/10 |
| Async nativo | 10% | 10/10 | 5/10 | 4/10 |
| **Total** | **100%** | **9.35** | **6.35** | **6.55** |

### 7.2 Justificacion para el curso

FastAPI es la mejor opcion para este curso porque:

1. **Enfoque en APIs REST:** El curso enseña a crear APIs, no apps web tradicionales
2. **Velocidad:** Los estudiantes aprenden un framework que puede manejar produccion real
3. **Documentacion:** Swagger UI facilita el testing y la comprension
4. **Validacion:** Pydantic enseña buenas practicas de validacion desde el principio
5. **Modernidad:** Async/await es el futuro de Python web
6. **Minimalismo:** Solo instalamos lo que necesitamos, sin bloat

## 8. Que construiremos en el curso

Con FastAPI, los estudiantes crearan:

| Semana | Entregable |
|--------|------------|
| 7-8 | Primer proyecto con estructura modular |
| 9-10 | API con validacion Pydantic y middleware |
| 12-13 | CRUD completo con SQLAlchemy |
| 14 | Tests con pytest y TestClient |
| 16 | Despliegue en Render + Supabase |

## 9. Ejercicio guiado

### Ejercicio 0: Verificacion rapida

```bash
python --version
pip --version
```

### Ejercicio 1: Instalar FastAPI

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar FastAPI
pip install fastapi[standard]
```

### Ejercicio 2: Primera verificacion

Crea un archivo `main.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="Mi primera API")

@app.get("/")
def root():
    return {"mensaje": "FastAPI funciona correctamente"}
```

Ejecuta:

```bash
uvicorn main:app --reload
```

Abre `http://localhost:8000/docs` y verifica que Swagger UI funciona.

### Ejercicio 3: Comparacion rapida

Crea una tabla comparativa personalizada entre FastAPI y otro framework de tu eleccion. Incluye al menos 5 criterios tecnicos.

## 10. Preguntas frecuentes

**P: Por que no Django?**
R: Django es excelente para apps web completas con admin, ORM y template engine. Pero para APIs REST modernas, FastAPI es mas rapido, mas moderno y tiene mejor documentacion automatica.

**P: FastAPI es solo para APIs?**
R: Principalmente si. FastAPI puede servir archivos estaticos y usar Jinja2 para HTML, pero su fortaleza es las APIs REST y GraphQL.

**P: Que pasa si despues necesito Django?**
R: Los conceptos que aprendes en FastAPI (rutas, validacion, testing, estructura) son transferibles a otros frameworks. Aprender FastAPI no te cierra puertas.

**P: FastAPI es estable para produccion?**
R: Si. FastAPI es usado en empresas como Microsoft, Netflix y Uber. Es un framework maduro y bien mantenido.

## 11. Material de estudio

- Clase 04: Frameworks web - comparacion y eleccion
- Clase 05: Instalacion y configuracion
- Documentacion oficial: https://fastapi.tiangolo.com/
