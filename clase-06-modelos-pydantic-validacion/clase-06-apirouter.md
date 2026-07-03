# Clase 06 - Modelos Pydantic y validacion de datos

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 6  
**Unidad:** Unidad 2 - Uso de un Framework Especifico  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA3: Desarrollar habilidades para la creacion y manejo de rutas y controladores dentro del framework mediante la implementacion de logica de negocio en controladores o equivalentes pedagogicos.
- RA4: Aplicar principios de diseno de APIs RESTful en la construccion de servicios web mediante la implementacion de endpoints que cumplan con los estandares de la arquitectura REST.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

En la clase anterior (Clase 05) se introdujeron los schemas Pydantic basicos con `Field()` para validar longitud y rango. En esta clase se profundiza en el **sistema de validacion de Pydantic**, que es uno de los pilares de FastAPI.

Los estudiantes aprenderan a:

- usar todas las opciones de `Field()` para definir reglas precisas;
- escribir validadores personalizados con `@field_validator`;
- construir modelos anidados (un schema dentro de otro);
- configurar comportamientos globales con `model_config`;
- interpretar errores de validacion (error 422).

Al finalizar, el estudiante podra definir contratos de datos robustos que rechacen automaticamente datos invalidos antes de que lleguen a la logica de negocio.

## 3. Pregunta orientadora

**Como garantizamos que solo datos validos entren a nuestra API?**

No queremos que un cliente envie un precio negativo, un email sin arroba, una fecha de fin anterior a la fecha de inicio, o un nombre vacio. Pydantic + FastAPI nos dan herramientas para rechazar esos casos automaticamente.

---

> **En español simple:** Pydantic es como un filtro de agua. Toda la informacion que entra a tu API pasa por ese filtro. Si el agua trae impurezas (datos invalidos), el filtro la rechaza y devuelve un error claro. Tu logica de negocio nunca recibe agua sucia.

---

## 4. Conceptos previos requeridos

- Crear una instancia de FastAPI.
- Definir endpoints con `@app.get()` y `@app.post()`.
- Usar `BaseModel` de Pydantic para crear schemas basicos.
- Usar `Field()` con `min_length` y `max_length`.
- Ejecutar `uvicorn` y revisar `/docs`.

## 5. Recordatorio: schema basico (Clase 05)

```python
from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    credits: int = Field(ge=1, le=6)
```

Esto ya nos da validacion basica. Pero Pydantic puede hacer mucho mas.

## 6. Field() en profundidad

> **En español simple:** `Field()` es como las instrucciones de un formulario. Cada parametro le dice algo distinto a Pydantic sobre como validar ese campo.

### 6.1 Parametros de `Field()`

| Parametro | Que valida | Ejemplo |
|---|---|---|
| `min_length` | Longitud minima de un string | `Field(min_length=3)` |
| `max_length` | Longitud maxima de un string | `Field(max_length=80)` |
| `gt` | Mayor que (greater than) | `Field(gt=0)` → precio positivo |
| `ge` | Mayor o igual que (greater or equal) | `Field(ge=1)` |
| `lt` | Menor que (less than) | `Field(lt=100)` |
| `le` | Menor o igual que (less or equal) | `Field(le=6)` |
| `regex` | Patron de expresion regular | `Field(regex=r"^[A-Z]{3}\d{3}$")` |
| `default` | Valor por defecto | `Field(default="pendiente")` |
| `default_factory` | Funcion que genera valor por defecto | `Field(default_factory=list)` |
| `alias` | Nombre alternativo del campo (para JSON) | `Field(alias="nombre_completo")` |
| `description` | Texto descriptivo para la documentacion | `Field(description="Nombre del curso")` |
| `examples` | Ejemplos para Swagger | `Field(examples=["Matematicas"])` |

### 6.2 Ejemplo completo

```python
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    isbn: str = Field(
        min_length=10,
        max_length=13,
        regex=r"^\d{10,13}$",
        description="ISBN del libro, solo numeros",
        examples=["9781234567890"],
    )
    title: str = Field(
        min_length=2,
        max_length=200,
        description="Titulo del libro",
    )
    year: int = Field(
        gt=1900,
        lt=2027,
        description="Anio de publicacion",
    )
    rating: float = Field(
        ge=1.0,
        le=5.0,
        default=3.0,
        description="Calificacion (1.0 a 5.0)",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Lista de etiquetas",
    )
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `isbn: str = Field(min_length=10, max_length=13, regex=r"^\d{10,13}$")` | El ISBN debe ser texto de 10 a 13 caracteres, solo numeros |
| `year: int = Field(gt=1900, lt=2027)` | El anio debe estar entre 1901 y 2026 |
| `rating: float = Field(ge=1.0, le=5.0, default=3.0)` | Calificacion de 1.0 a 5.0, si no se envia, vale 3.0 |
| `tags: list[str] = Field(default_factory=list)` | Si no se envia `tags`, se crea una lista vacia automaticamente |

### 6.3 `default` vs `default_factory`

**`default`**: para valores fijos (numeros, strings, booleanos).

```python
active: bool = Field(default=True)
```

**`default_factory`**: para valores que necesitan crearse cada vez (listas, dicts, objetos).

```python
tags: list[str] = Field(default_factory=list)
```

> ¿Por que no usar `default=[]`? Porque en Python, `[]` como valor por defecto se **comparte entre todas las instancias**. Si modificas la lista de una instancia, se modifica para todas. `default_factory=list` crea una lista NUEVA cada vez.

---

## 7. Campos opcionales

> **En español simple:** No todos los campos son obligatorios. `Optional[str]` significa "puede venir o no. Si no viene, vale `None`."

```python
from typing import Optional


class AuthorCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: Optional[str] = None
    birth_year: Optional[int] = None
```

**Comportamiento:**

| Envio del cliente | Resultado |
|---|---|
| `{"name": "Ana"}` | `email=None`, `birth_year=None` |
| `{"name": "Ana", "email": "ana@mail.com"}` | `email="ana@mail.com"`, `birth_year=None` |
| `{"name": "Ana", "birth_year": 1990}` | `birth_year=1990` |
| `{}` | **Error 422** → `name` es obligatorio |

> **Diferencia clave:** `Optional[str]` permite que el campo sea `None` o un string. Pero si el campo no tiene valor por defecto, sigue siendo obligatorio en el body. `= None` es lo que le da el valor por defecto.

---

## 8. Validadores personalizados con `@field_validator`

> **En español simple:** A veces `Field()` no alcanza. Por ejemplo: "la fecha de fin debe ser posterior a la fecha de inicio". Eso no se puede expresar solo con `gt`/`lt`. Ahi usamos `@field_validator`: una funcion Python que revisa la logica y rechaza si no cumple.

### 8.1 Sintaxis basica (Pydantic v2)

```python
from pydantic import BaseModel, field_validator
from datetime import date


class PromotionCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    start_date: date
    end_date: date
    discount_percent: float = Field(gt=0, le=100)

    @field_validator("end_date")
    @classmethod
    def end_must_be_after_start(cls, end_date, info):
        if "start_date" in info.data and end_date <= info.data["start_date"]:
            raise ValueError("end_date must be after start_date")
        return end_date
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `@field_validator("end_date")` | Declara que esta funcion valida el campo `end_date` |
| `@classmethod` | Los validadores deben ser metodos de clase |
| `def end_must_be_after_start(cls, end_date, info):` | `cls` es la clase, `end_date` es el valor a validar, `info` contiene los otros campos |
| `if "start_date" in info.data` | Verifica que `start_date` ya fue procesado |
| `raise ValueError("...")` | Si la validacion falla, lanza `ValueError`. Pydantic lo convierte en error 422 |
| `return end_date` | Si pasa la validacion, devuelve el valor (puedes modificarlo si quieres) |

### 8.2 Varios campos, un validador

```python
@field_validator("end_date", "start_date")
@classmethod
def dates_must_be_future(cls, value):
    if value < date.today():
        raise ValueError(f"{value} is in the past")
    return value
```

### 8.3 Validador de email (sin librerias externas)

```python
import re


class UserCreate(BaseModel):
    email: str = Field(min_length=5, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value
```

> **Asi NO ❌ vs Asi SI ✅**
>
> ❌ **Validacion en el endpoint (MAL):**
> ```python
> @router.post("/users")
> def create_user(user: dict):
>     if "@" not in user.get("email", ""):
>         return {"error": "invalid email"}
>     # 20 lineas mas...
> ```
>
> ✅ **Validacion en el schema (BIEN):**
> ```python
> class UserCreate(BaseModel):
>     email: str = Field(min_length=5)
>
>     @field_validator("email")
>     @classmethod
>     def validate_email(cls, value):
>         if not re.match(r"...", value):
>             raise ValueError("Invalid email format")
>         return value
> ```
>
> La validacion en el schema es **reutilizable** y **centralizada**. El endpoint no necesita saber las reglas.

---

## 9. Modelos anidados

> **En español simple:** Un modelo anidado es un schema dentro de otro. Es como un formulario que contiene otro formulario. Ejemplo: un Curso tiene un Profesor dentro.

```python
class Instructor(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value


class CourseDetail(BaseModel):
    id: int
    name: str
    credits: int
    instructor: Instructor  # ← Modelo anidado
```

**Uso en un endpoint:**

```python
@router.post("/courses", response_model=CourseDetail)
def create_course(course: CourseDetail):
    # course.instructor.name → "Ana"
    # course.instructor.email → "ana@mail.com"
    return course
```

**JSON que enviaria el cliente:**

```json
{
  "id": 1,
  "name": "Desarrollo Web II",
  "credits": 4,
  "instructor": {
    "name": "Ana Lopez",
    "email": "ana@mail.com"
  }
}
```

**Analogia:** El modelo `CourseDetail` es como un curriculum vitae. Tiene tus datos personales, y dentro tiene una seccion de "Experiencia Laboral" que a su vez contiene empresa, cargo, fechas. Es un formulario dentro de otro formulario.

### 9.1 Listas de modelos anidados

```python
class Review(BaseModel):
    user: str
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=1, max_length=500)


class BookDetail(BaseModel):
    id: int
    title: str
    reviews: list[Review] = Field(default_factory=list)
```

```json
{
  "id": 1,
  "title": "Clean Code",
  "reviews": [
    {"user": "Ana", "rating": 5, "comment": "Excelente libro"},
    {"user": "Luis", "rating": 4, "comment": "Muy bueno"}
  ]
}
```

---

## 10. `model_config` — configuracion global del modelo

> **En español simple:** `Field()` configura cada campo individualmente. `model_config` configura el comportamiento GENERAL del schema.

```python
from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",       # Rechazar campos no definidos
        frozen=True,          # Hacer el modelo inmutable
        str_min_length=1,     # Longitud minima global para strings
        str_strip_whitespace=True,  # Eliminar espacios al inicio/final
    )

    name: str
    credits: int = Field(ge=1, le=6)
```

### 10.1 `extra="forbid"` — Rechazar campos no esperados

```python
# Cliente envia:
{"name": "Matematicas", "credits": 4, "secret_field": "hackeado"}

# Con extra="forbid" → Error 422:
# Extra inputs are not permitted: 'secret_field'
```

### 10.2 `frozen=True` — Modelo inmutable (solo lectura)

```python
course = CourseCreate(name="Matematicas", credits=4)
course.name = "Fisica"  # Error: CourseCreate is frozen
```

### 10.3 `str_strip_whitespace` — Limpiar espacios

```python
# Cliente envia:
{"name": "  Matematicas  ", "credits": 4}

# Sin strip: name = "  Matematicas  " (con espacios)
# Con strip: name = "Matematicas" (limpio)
```

---

## 11. Entendiendo el error 422

> **En español simple:** Cuando falla la validacion, FastAPI responde con error 422 y un JSON explicando exactamente que fallo y por que.

```json
// POST /books con body invalido
// Respuesta 422:
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "isbn"],
      "msg": "String should have at least 10 characters",
      "input": "123"
    },
    {
      "type": "greater_than",
      "loc": ["body", "year"],
      "msg": "Input should be greater than 1900",
      "input": 1800
    }
  ]
}
```

**Lectura del error:**

| Campo | Significado |
|---|---|
| `type` | Tipo de error (`string_too_short`, `greater_than`, `missing`, `value_error`) |
| `loc` | Donde ocurrio (`["body", "isbn"]` → en el body, campo `isbn`) |
| `msg` | Mensaje legible |
| `input` | El valor que el cliente envio (lo que causo el error) |

### 11.1 Checklist de troubleshooting para error 422

Cuando veas 422:

- [ ] ¿El campo es obligatorio y no lo enviaste?
- [ ] ¿El tipo de dato es correcto? (string, int, float, bool)
- [ ] ¿Cumple con `min_length`/`max_length`?
- [ ] ¿Cumple con `gt`/`lt`/`ge`/`le`?
- [ ] ¿Cumple con el `regex`?
- [ ] Si hay `@field_validator`, ¿tu logica esta bien?
- [ ] ¿Hay un campo extra que no deberia estar? (si usas `extra="forbid"`)

---

## 12. Actividad central de clase

### 12.1 Enunciado

Eres el desarrollador de una API para una biblioteca. Debes crear schemas Pydantic para:

1. **`BookCreate`**: isbn (10-13 digitos), title (2-200 chars), year (1901-2026), rating opcional (1.0-5.0, default 3.0)
2. **`AuthorCreate`**: name (3-100 chars), email (validado con regex), birth_year opcional
3. **`PublishingHouse`**: name (3-100 chars), foundation_year (gt=1800)
4. **`BookDetail`**: todos los campos de `BookCreate` + `author` (modelo anidado `AuthorCreate`) + `publisher` (modelo anidado `PublishingHouse`)
5. Validador personalizado: `end_date` debe ser posterior a `start_date` en un schema `PromotionCreate`
6. Config global: `extra="forbid"` en todos los schemas

### 12.2 Producto de clase — Checklist de verificacion

- [ ] `BookCreate` usa `Field()` con `min_length`, `max_length`, `regex`, `gt`, `lt`, default
- [ ] `AuthorCreate` tiene campo `email` con validador `@field_validator`
- [ ] `PublishingHouse` usa `gt` para `foundation_year`
- [ ] `BookDetail` contiene modelos anidados (`AuthorCreate`, `PublishingHouse`)
- [ ] `PromotionCreate` tiene `@field_validator` que compara `end_date > start_date`
- [ ] Todos los schemas tienen `model_config = ConfigDict(extra="forbid")`
- [ ] Probaste enviar datos invalidos y obtuviste error 422 con mensaje claro
- [ ] Probaste enviar un campo extra y obtuviste error 422

---

## 13. Errores comunes y troubleshooting

### 13.1 Error: "Field validator not defined correctly"

```text
TypeError: Validator fields must be defined as classmethods
```

**Causa:** Olvidaste `@classmethod` en el validador.

**Solucion:** Agrega `@classmethod` debajo de `@field_validator`:

```python
@field_validator("end_date")
@classmethod  # ← NO olvidar
def validate_end_date(cls, end_date, info):
    ...
```

### 13.2 Error: "Extra inputs are not permitted"

```text
422: Extra inputs are not permitted: 'campo_extra'
```

**Causa:** El cliente envio un campo que no esta definido en el schema y tienes `extra="forbid"`.

**Solucion:** O agrega el campo al schema, o elimina `extra="forbid"` si quieres ignorar campos extra.

### 13.3 Error: "Field required"

```text
422: Field required
```

**Causa:** El cliente omitio un campo obligatorio.

**Solucion:** Envia el campo faltante, o hazlo opcional con `Optional[type] = None`.

### 13.4 Error: "Input should be a valid integer"

**Causa:** El campo espera `int` pero recibio texto.

**Solucion:** Revisa el tipo de dato en el JSON enviado.

### 13.5 Error: "Cannot modify frozen model"

**Causa:** Intentaste modificar un campo de un modelo que tiene `frozen=True`.

**Solucion:** Si necesitas modificarlo, quita `frozen=True` o crea una nueva instancia.

---

## 14. Cierre conceptual

Pydantic no solo valida tipos de datos. Permite definir **contratos precisos** entre el cliente y la API. Con `Field()`, `@field_validator`, modelos anidados y `model_config`, puedes expresar practicamente cualquier regla de validacion sin escribir logica repetitiva en cada endpoint.

Un buen schema es como una aduana bien organizada: los datos incorrectos no pasan, y cuando alguien intenta pasar algo invalido, recibe un mensaje claro explicando por que.

---

## 15. Trabajo independiente

Para la siguiente clase, los estudiantes deben:

1. Completar los schemas de la actividad central de clase.
2. Agregar un schema `UserCreate` con validacion de email y password (min 8 chars, al menos un numero).
3. Crear un modelo anidado `OrderResponse` que contenga `list[OrderItemResponse]`.
4. Escribir un `@field_validator` que valide que `end_date > start_date` en una clase `EventCreate`.
5. Agregar `model_config` con `extra="forbid"` en todos los schemas del proyecto.

---

## 16. Bibliografia y referencias utiles

- Pydantic. (s. f.). *Validators*. https://docs.pydantic.dev/latest/concepts/validators/
- Pydantic. (s. f.). *Fields*. https://docs.pydantic.dev/latest/concepts/fields/
- Pydantic. (s. f.). *Config*. https://docs.pydantic.dev/latest/api/config/
- FastAPI. (s. f.). *Request Body*. https://fastapi.tiangolo.com/tutorial/body/
- FastAPI. (s. f.). *Field validators*. https://fastapi.tiangolo.com/tutorial/body-fields/
