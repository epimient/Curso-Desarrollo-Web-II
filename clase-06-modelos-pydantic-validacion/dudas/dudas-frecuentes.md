# Dudas frecuentes - Clase 06

> Aqui encontraras las preguntas mas comunes sobre Pydantic y validacion de datos en FastAPI.

---

## 1. ¿Que diferencia hay entre `str` y `Field(min_length=3)`?

**Respuesta corta:** `str` solo dice "esto es texto". `Field()` agrega reglas adicionales.

**Respuesta larga:** Todos los campos en Pydantic tienen un tipo (`str`, `int`, `float`, `bool`, etc.). `Field()` agrega **restricciones** sobre ese tipo:

| Sin Field | Con Field |
|---|---|
| `name: str` → acepta cualquier texto | `name: str = Field(min_length=3)` → solo texto de 3+ caracteres |
| `age: int` → acepta cualquier entero | `age: int = Field(ge=18)` → solo enteros >= 18 |

**Analogia:** `str` es como decir "puedes traer cualquier bebida". `Field(min_length=3)` es como decir "puedes traer cualquier bebida, pero tiene que venir en un envase de al menos 3 dl".

---

## 2. ¿Para que sirven `gt`/`lt`/`ge`/`le`?

**Respuesta corta:** Validan rangos numericos.

**Respuesta larga:**

| Parametro | Significado | Ejemplo | Acepta |
|---|---|---|---|
| `gt` | greater than (mayor que) | `Field(gt=0)` | 1, 2, 3... (no 0) |
| `ge` | greater or equal (mayor o igual) | `Field(ge=1)` | 1, 2, 3... (si 0) |
| `lt` | less than (menor que) | `Field(lt=100)` | 99, 98... (no 100) |
| `le` | less or equal (menor o igual) | `Field(le=6)` | 6, 5, 4... (si 6) |

**Analogia:** Son como las rejas de un estacionamiento. `gt(2)` solo deja pasar autos con altura mayor a 2 metros. `ge(2)` deja pasar autos de 2 metros o mas.

---

## 3. ¿Que es `Optional[str]` y cuando usarlo?

**Respuesta corta:** Indica que el campo puede ser `None` (no enviado).

**Respuesta larga:**

```python
class UserCreate(BaseModel):
    email: Optional[str] = None  # Puede venir o no
    phone: str  # Obligatorio, siempre debe venir
```

**Comportamiento:**

| Envio | Resultado |
|---|---|
| `{"phone": "123"}` | `email=None` |
| `{"phone": "123", "email": "a@b.com"}` | `email="a@b.com"` |
| `{}` | Error 422: `phone` es obligatorio |

**Analogia:** `Optional[str]` es como decir "puedes darme tu numero de telefono o no, no es obligatorio". Sin `Optional`, es como "dame tu numero o no entras".

---

## 4. ¿Que es `@field_validator` y como se escribe?

**Respuesta corta:** Es un decorador para escribir logica de validacion que `Field()` no puede expresar.

**Respuesta larga:** `Field()` solo valida cosas simples: tipo, longitud, rango, patron. Cuando necesitas logica mas compleja (comparar dos campos, validar formato de email, verificar que un codigo no este repetido), usas `@field_validator`.

**Estructura:**

```python
@field_validator("nombre_del_campo")
@classmethod
def nombre_del_validador(cls, valor, info):
    if not condicion:
        raise ValueError("Mensaje de error")
    return valor
```

**Analogia:** `Field()` es un filtro de malla gruesa (atrapa piedras grandes). `@field_validator` es un filtro de malla fina (atrapa impurezas mas pequeñas que la malla gruesa deja pasar).

---

## 5. ¿Que es `model_config`?

**Respuesta corta:** Configuracion global que aplica a TODO el modelo, no a un campo especifico.

**Respuesta larga:** Mientras `Field()` configura cada campo individualmente, `model_config` establece reglas para todo el modelo:

```python
class ProductCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",              # Rechazar campos no definidos
        frozen=True,                 # Hacer inmutable
        str_strip_whitespace=True,   # Limpiar espacios
        str_min_length=1,            # Longitud minima global
    )
```

**Analogia:** `Field()` son las reglas de cada jugador de futbol (no usar las manos, no hacer faltas). `model_config` son las reglas del partido entero (duracion, numero de jugadores, cambios permitidos).

---

## 6. ¿Que significa error 422?

**Respuesta corta:** "Los datos que enviaste no pasaron la validacion."

**Respuesta larga:** El codigo 422 (Unprocessable Entity) significa que el servidor entiende la peticion pero no puede procesarla porque los datos son invalidos. FastAPI devuelve un JSON explicando exactamente que fallo:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "name"],
      "msg": "String should have at least 3 characters",
      "input": "Ab"
    }
  ]
}
```

**Analogia:** Es como llenar un formulario del banco y que el cajero te diga "entiendo que quieres abrir una cuenta, pero tu numero de telefono tiene 4 digitos y necesito al menos 7. Corrigelo y vuelve."

---

## 7. ¿Puedo tener un campo que sea otro Pydantic model?

**Respuesta corta:** Si. Se llaman modelos anidados.

**Respuesta larga:** Un campo de un schema puede ser OTRO schema completo:

```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class UserResponse(BaseModel):
    name: str
    address: Address  # ← Modelo anidado
```

Pydantic valida automaticamente todos los niveles. Si `address.street` es invalido, recibes error 422.

**Analogia:** Es como un formulario de empleo que dentro tiene una seccion de "Referencias personales" que a su vez tiene nombre, telefono y relacion. Un formulario dentro de otro formulario.

---

## 8. ¿Como valido que un string sea un email valido?

**Respuesta corta:** Con `@field_validator` y una expresion regular.

**Respuesta larga:**

```python
import re
from pydantic import BaseModel, Field, field_validator


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

Para produccion, existen librerias como `pydantic[email]` o `email-validator` que hacen esto mejor.

---

## 9. ¿Que es `default_factory` y cuando usarlo?

**Respuesta corta:** Es una funcion que genera el valor por defecto CADA VEZ que se crea una instancia.

**Respuesta larga:** Se usa cuando el valor por defecto debe ser un objeto mutable (lista, dict, set):

| Forma | Problema |
|---|---|
| `tags: list[str] = []` | ❌ La lista se comparte entre todas las instancias |
| `tags: list[str] = Field(default_factory=list)` | ✅ Cada instancia tiene su propia lista |

**Analogia:** `default_factory=list` es como tener una maquina de tickets que te da un ticket nuevo cada vez. `default=[]` es como tener una pila de tickets donde todos agarran del mismo monton.

---

## 10. ¿Que pasa si el cliente envia campos que no defini en el schema?

**Respuesta corta:** Depende de `model_config`. Por defecto se ignoran. Con `extra="forbid"` se rechazan.

**Respuesta larga:**

| Configuracion | Comportamiento |
|---|---|
| `extra="ignore"` (default) | Los campos extra se **ignoran** silenciosamente |
| `extra="forbid"` | Los campos extra causan **error 422** |
| `extra="allow"` | Los campos extra se **incluyen** en el modelo (poco comun) |

```python
class BookCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    year: int

# Cliente envia: {"title": "Libro", "year": 2008, "hack": "malo"}
# → Error 422: Extra inputs are not permitted: 'hack'
```

**Analogia:** Con `extra="forbid"` es como un edificio con guardia de seguridad. Si intentas entrar con algo que no esta en la lista de permitidos, el guardia te rechaza. Con `extra="ignore"` el guardia simplemente ignora lo que traes de mas.

---

## 11. ¿Como hago para que un campo sea de solo lectura?

**Respuesta corta:** Usa `frozen=True` en `model_config`.

**Respuesta larga:** `frozen=True` hace que el modelo sea inmutable. Una vez creado, no puedes cambiar ningun campo:

```python
class CourseCreate(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    credits: int

course = CourseCreate(name="Matematicas", credits=4)
course.name = "Fisica"  # ❌ Error: CourseCreate is frozen
```

Si solo quieres que un campo sea de solo lectura, puedes combinarlo con `Field(..., alias="_")` u otras estrategias, pero lo mas simple es `frozen=True` en todo el modelo.

---

## 12. ¿Pydantic v2 es muy diferente de v1?

**Respuesta corta:** Si, hay cambios importantes. Este curso usa Pydantic v2.

**Respuesta larga:** Diferencias clave:

| Aspecto | Pydantic v1 | Pydantic v2 (este curso) |
|---|---|---|
| Validadores | `@validator` | `@field_validator` |
| Config | Clase interna `Config` | `model_config = ConfigDict(...)` |
| Velocidad | Escritura en Python | Escritura en Rust (5-50x mas rapido) |
| `@root_validator` | `@root_validator` | `@model_validator` |

**Ejemplo de migracion:**

```python
# Pydantic v1 (ANTIGUO)
class User(BaseModel):
    name: str

    class Config:
        extra = "forbid"

    @validator("name")
    def name_must_not_be_empty(cls, v):
        ...

# Pydantic v2 (ACTUAL - lo que usamos)
class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        ...
```

**Analogia:** Pydantic v1 era un auto con motor a combustion. Pydantic v2 es el mismo auto pero con motor electrico: mas rapido, mas eficiente, y algunos botones cambiaron de lugar.
