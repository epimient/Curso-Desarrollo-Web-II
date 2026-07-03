# Dudas frecuentes - Clase 05

> Aqui encontraras las preguntas que todo principiante se hace al organizar su primer proyecto FastAPI. Si tienes una duda, probablemente esta aqui.

---

## 1. ¿Siempre debo usar esta estructura de carpetas?

**Respuesta corta:** No. Es una estructura pedagogica y practica, no una regla universal.

**Respuesta larga:** FastAPI te da libertad total para organizar tu proyecto como quieras. Esta estructura (core/, routers/, schemas/, services/) es la que usamos en el curso porque:
- Separa responsabilidades claramente
- Es facil de entender para principiantes
- Escala bien para proyectos de tamano mediano
- Prepara el camino para agregar persistencia, seguridad y pruebas

**Analogia:** Es como aprender a cocinar con una receta estructurada (ingredientes por separado, pasos numerados). Cuando ya seas chef, puedes improvisar. Pero mientras aprendes, la estructura te salva de quemar la cocina.

---

## 2. ¿Por que no dejar todo en `main.py`?

**Respuesta corta:** Porque cuando el proyecto crece, `main.py` se convierte en un archivo enorme, ilegible e imposible de mantener.

**Respuesta larga:** Con 3 endpoints, `main.py` funciona bien. Con 30 endpoints, validaciones, reglas de negocio y configuracion, `main.py` se vuelve un "pergamino infinito" donde:
- Es dificil encontrar algo
- Dos personas no pueden trabajar al mismo tiempo (conflictos de Git)
- Las pruebas se vuelven complicadas
- Un error en una parte puede romper todo

**Analogia:** Es como tener toda tu casa en una sola habitacion. Puedes vivir ahi si estas solo y tienes pocas cosas. Pero si tu familia crece, necesitas separar: cocina, sala, dormitorios, bano.

---

## 3. ¿Que diferencia hay entre router y service?

**Respuesta corta:** El router maneja la comunicacion HTTP (rutas, parametros, codigos de respuesta). El service maneja la logica de negocio (reglas, validaciones, operaciones internas).

**Respuesta larga:**

| Aspecto | Router | Service |
|---|---|---|
| Responsabilidad | Interfaz HTTP | Logica interna |
| Recibe | Parametros de URL/query/body | Datos ya validados |
| Decide | Que codigo HTTP retornar | Que reglas aplicar |
| Ejemplo | `@router.get("/courses")` | `def list_courses():` |

**Analogia del restaurante:**
- **Router** = el mesero. Te toma la orden, la lleva a la cocina, te trae el plato.
- **Service** = el cocinero. Prepara la comida, aplica las recetas, decide si un ingrediente es valido.

El mesero no cocina. El cocinero no atiende mesas. Cada uno hace lo suyo.

---

## 4. ¿Que va en `schemas/`?

**Respuesta corta:** Los modelos Pydantic que definen como se reciben y se devuelven los datos.

**Respuesta larga:** `schemas/` contiene **contratos de datos**. Definen:
- **Entrada:** que datos debe enviar el cliente (ej: `CourseCreate` con `name` y `credits`)
- **Salida:** que datos devuelve la API (ej: `CourseResponse` con `id`, `name`, `credits`, `active`)

**Analogia:** `CourseCreate` es el formulario de solicitud que llenas para pedir un curso. `CourseResponse` es el certificado que recibes cuando el curso se crea. No son el mismo documento, aunque compartan informacion.

---

## 5. ¿Que va en `core/`?

**Respuesta corta:** Configuracion general y elementos transversales que usan varios modulos.

**Respuesta larga:** En `core/` se guarda todo lo que es "global" para la aplicacion:
- Nombre de la app
- Version
- Entorno (development, staging, production)
- Configuracion de CORS (que dominios pueden acceder)
- Variables de entorno
- Parametros de seguridad

**Analogia:** `core/` es como la placa de identificacion de un edificio: "Edificio Torre Central, Piso 12, 2026". No cambia seguido, pero todos los departamentos lo necesitan.

---

## 6. Si uso base de datos, ¿donde va?

**Respuesta corta:** En carpetas separadas: `models/` para los modelos de base de datos y `database/` para la conexion.

**Respuesta larga:** Cuando agregues persistencia (Clase 06 en adelante), la estructura crecera asi:

```text
app/
  models/        ← Modelos SQLAlchemy (la estructura de las tablas)
  database/      ← Conexion, sesiones, configuracion de BD
  services/      ← Sigue igual, pero ahora usa la BD en lugar de memoria
  schemas/       ← Sigue igual, separado de los modelos de BD
```

**No mezcles** `schemas/` (lo que el cliente ve) con `models/` (lo que se guarda en BD). Son conceptos distintos aunque tengan campos parecidos.

---

## 7. ¿Por que no aparece mi endpoint en `/docs`?

**Respuesta corta:** Probablemente olvidaste registrar el router con `app.include_router(...)`.

**Respuesta larga:** FastAPI no descubre routers automaticamente. Tienes que conectarlos explicitamente en `main.py`:

```python
# ❌ MAL: el router existe pero no esta registrado
from app.routers import courses
app = FastAPI(...)
# falta: app.include_router(courses.router)

# ✅ BIEN:
from app.routers import courses
app = FastAPI(...)
app.include_router(courses.router)
```

**Checklist rapido:**
- [ ] ¿El archivo del router existe en `app/routers/`?
- [ ] ¿El router esta importado en `main.py`?
- [ ] ¿Usaste `app.include_router(...)`?
- [ ] ¿Reiniciaste el servidor?

**Analogia:** Es como comprar un telefono pero nunca conectarlo a la linea telefonica. El telefono existe, las funciones estan ahi, pero nadie puede llamarte.

---

## 8. ¿Que es un circular import?

**Respuesta corta:** Es cuando dos archivos se importan mutuamente, y Python no sabe cual cargar primero.

**Respuesta larga:** Sucede asi:

```python
# app/main.py
from app.routers import courses  # main importa courses

# app/routers/courses.py
from app.main import app  # courses importa main → CIRCULAR!
```

Python entra en un bucle: main necesita courses, courses necesita main, main necesita courses... y falla.

**Solucion:** Nunca importes `app` desde `main.py` dentro de un router. Si necesitas datos de configuracion, importa `settings` desde `core/config.py`.

```python
# ✅ CORRECTO
from app.core.config import settings
```

**Analogia:** Es como dos personas que esperan que la otra hable primero. "Tu primero." "No, tu primero." "No, tu." Y nunca pasa nada.

---

## 9. ¿Que es `global _next_id`?

**Respuesta corta:** Es una instruccion para que Python sepa que `_next_id` es una variable global, no local.

**Respuesta larga:** En Python, cuando asignas un valor a una variable dentro de una funcion, Python asume que es una variable **local** (solo existe dentro de la funcion). Si quieres modificar una variable que esta **fuera** de la funcion, necesitas la palabra clave `global`.

```python
_next_id = 2  # ← variable GLOBAL (fuera de la funcion)

def create_course(course_data):
    global _next_id  # ← "Oye Python, esta variable no es local, es la de afuera"
    _next_id += 1    # ← Ahora si podemos modificarla
```

**Analogia:** Es como si estuvieras en una habitacion (la funcion) y quisieras cambiar el termostato de toda la casa (variable global). Sin `global`, solo podrias cambiar la temperatura de tu habitacion.

---

## 10. ¿Que es `APIRouter` y como se diferencia de `FastAPI()`?

**Respuesta corta:** `APIRouter` es como un "mini-FastAPI" para agrupar rutas relacionadas. `FastAPI()` es la aplicacion principal.

**Respuesta larga:**

| Caracteristica | `FastAPI()` | `APIRouter` |
|---|---|---|
| Proposito | Aplicacion principal | Grupo de rutas |
| ¿Puede ejecutarse solo? | Si (`uvicorn app.main:app`) | No, necesita un `FastAPI()` |
| ¿Tiene `include_router()`? | Si | No (pero puede anidarse) |
| Ejemplo de uso | `app = FastAPI()` | `router = APIRouter(prefix="/courses")` |

Piensa en `FastAPI()` como el edificio completo, y `APIRouter` como un piso del edificio. El piso no funciona sin el edificio.

---

## 11. ¿Por que se usa `prefix="/courses"` y no `prefix="courses/"`?

**Respuesta corta:** Para que las rutas queden limpias: `/courses` en lugar de `courses/`.

**Respuesta larga:** El `prefix` se combina con la ruta del decorador:

```python
router = APIRouter(prefix="/courses")

@router.get("/")     → GET /courses
@router.get("/{id}") → GET /courses/1
```

Si usaras `prefix="courses/"`:
```python
router = APIRouter(prefix="courses/")

@router.get("/")     → GET courses//  ← feisimo
```

**Regla:** `prefix` empieza con `/` y NO termina con `/`. La ruta del decorador empieza con `/`.

---

## 12. ¿Que es `response_model` y para que sirve?

**Respuesta corta:** Es una declaracion del tipo de dato que devuelve el endpoint. FastAPI lo usa para validar, documentar y filtrar la respuesta.

**Respuesta larga:** `response_model` tiene tres funciones:

1. **Documentacion:** Swagger sabe exactamente que estructura devolvera.
2. **Validacion de salida:** Si el servicio devuelve algo que no coincide con el modelo, FastAPI lanza error.
3. **Filtrado:** Si el modelo de respuesta tiene menos campos que el modelo interno, solo se devuelven los declarados. Util para no exponer campos sensibles.

```python
@router.get("/courses", response_model=list[CourseResponse])
def read_courses():
    return list_courses()  # FastAPI verifica que la respuesta coincida
```

**Analogia:** `response_model` es como la descripcion del producto en una tienda online. El cliente ve eso y sabe exactamente que va a recibir, ni mas ni menos.
