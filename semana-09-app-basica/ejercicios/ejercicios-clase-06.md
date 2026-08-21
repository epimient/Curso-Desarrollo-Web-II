# Ejercicios - Clase 06

> **Nota:** El ejercicio 0 es de calentamiento. Los ejercicios 1-4 construyen sobre el ejemplo guiado de la biblioteca. El desafio extra es opcional.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las frases con las palabras del recuadro:

> **Palabras:** FIELD_VALIDATOR | GT_LT | OPTIONAL | DEFAULT_FACTORY | MODEL_CONFIG | REGEX | EXTRA_FORBID | FROZEN

1. _________ permite definir un valor por defecto que se crea cada vez (ej: `list`).
2. _________ se usa para validar que un numero sea mayor o menor que un valor.
3. _________ permite definir un patron que el string debe cumplir.
4. _________ es un decorador para escribir validacion personalizada.
5. _________ se usa para indicar que un campo puede ser `None`.
6. _________ evita que el modelo sea modificado despues de creado.
7. _________ rechaza campos no definidos en el schema.
8. _________ es el objeto que contiene la configuracion global del modelo.

---

## Ejercicio 1. Completar schemas

Dado el siguiente enunciado, completa los schemas con las validaciones apropiadas:

Crea un schema `StudentCreate` que valide:

1. `name`: string, entre 3 y 100 caracteres
2. `email`: string, entre 5 y 100 caracteres, debe contener "@" y "."
3. `age`: entero, entre 18 y 99
4. `gpa`: float, entre 0.0 y 5.0, con default 0.0
5. `enrolled`: booleano, default True

**Pista:** Usa `Field()` con `min_length`, `max_length`, `ge`, `le`, `gt`, `lt` segun corresponda.

```python
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(...)           # Completa
    email: str = Field(...)          # Completa
    age: int = Field(...)            # Completa
    gpa: float = Field(...)          # Completa
    enrolled: bool = Field(...)      # Completa
```

---

## Ejercicio 2. Escribir un @field_validator

Dado el schema `DiscountCreate`:

```python
from pydantic import BaseModel, Field, field_validator


class DiscountCreate(BaseModel):
    original_price: float = Field(gt=0)
    discount_percent: float = Field(gt=0, le=100)
    final_price: float = Field(gt=0)
```

Escribe un `@field_validator` para `final_price` que verifique:

```python
final_price == original_price - (original_price * discount_percent / 100)
```

**Es decir:** El precio final debe ser el precio original menos el descuento aplicado.

**Pista:** Usa `info.data` para acceder a `original_price` y `discount_percent`.

**Pruebas:**

| Envio | Resultado |
|---|---|
| `original_price=100, discount_percent=20, final_price=80` | ✅ Valido |
| `original_price=100, discount_percent=20, final_price=90` | ❌ Error: "final_price must equal original_price - discount" |

---

## Ejercicio 3. Modelo anidado

Crea un schema `ClassroomResponse` que contenga:

1. `name`: string (3-50 chars)
2. `capacity`: int (10-100)
3. `students`: lista de `StudentResponse` (modelo anidado)

Donde `StudentResponse` es:

```python
class StudentResponse(BaseModel):
    id: int
    name: str
    gpa: float
```

**Prueba:**

```python
data = {
    "name": "Matematicas 101",
    "capacity": 30,
    "students": [
        {"id": 1, "name": "Ana", "gpa": 4.5},
        {"id": 2, "name": "Luis", "gpa": 3.8},
    ],
}

classroom = ClassroomResponse(**data)
print(classroom.students[0].name)  # → "Ana"
```

---

## Ejercicio 4. Depurar errores 422

Para cada error, identifica:

1. ¿Que campo fallo?
2. ¿Cual fue la regla que se violo?

**Error A:**
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

**Error B:**
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["body", "credits"],
      "msg": "Input should be greater than or equal to 1",
      "input": 0
    }
  ]
}
```

**Error C:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "end_date"],
      "msg": "Value error, end_date must be after start_date",
      "input": "2026-01-01"
    }
  ]
}
```

**Error D:**
```json
{
  "detail": [
    {
      "type": "extra_forbidden",
      "loc": ["body", "hack"],
      "msg": "Extra inputs are not permitted",
      "input": "malo"
    }
  ]
}
```

---

## Ejercicio 5. Config global

Agrega `model_config` al schema del Ejercicio 1 (`StudentCreate`) para que:

1. Rechace campos no definidos
2. Limpie espacios al inicio y final de los strings
3. Haga el modelo inmutable

```python
class StudentCreate(BaseModel):
    model_config = ConfigDict(
        ...  # Completa
    )
    # ... campos del Ejercicio 1
```

**Prueba:**

```python
# Esto deberia fallar por frozen:
student = StudentCreate(name="Ana", email="ana@mail.com", age=20, gpa=4.0)
student.name = "Otro nombre"  # ❌ Debe lanzar error
```

---

## Desafio extra (opcional)

Crea un schema `EventCreate` con las siguientes reglas:

1. `title`: string, 5-100 caracteres
2. `description`: string, 10-500 caracteres
3. `start_date`: `date`
4. `end_date`: `date`, debe ser posterior a `start_date`
5. `capacity`: int, 10-1000
6. `price`: float, mayor a 0
7. `tags`: lista de strings, cada tag entre 2 y 20 caracteres, al menos 1 tag

**Pista:** Necesitaras:
- `Field()` para reglas basicas
- `@field_validator` para comparar fechas
- Otro `@field_validator` para validar cada tag en la lista

```python
class EventCreate(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    start_date: date
    end_date: date
    capacity: int = Field(...)
    price: float = Field(...)
    tags: list[str] = Field(...)

    @field_validator("end_date")
    @classmethod
    def end_must_be_after_start(cls, end_date, info):
        ...

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags):
        ...
```

**Verificacion:**

| Envio | Resultado |
|---|---|
| `{"title": "Conferencia", "description": "Evento anual de tecnologia", "start_date": "2026-06-01", "end_date": "2026-06-02", "capacity": 100, "price": 25.0, "tags": ["tech", "python"]}` | ✅ Valido |
| `{"title": "X", ...}` | ❌ Error: title demasiado corto |
| `end_date` anterior a `start_date` | ❌ Error: end_date debe ser posterior |
| `tags: ["a"]` | ❌ Error: tag demasiado corto |
