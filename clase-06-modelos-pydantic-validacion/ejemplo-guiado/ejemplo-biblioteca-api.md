# Ejemplo guiado - Validacion avanzada con Pydantic para una API de biblioteca

## Objetivo

Construir schemas Pydantic con validaciones reales: `Field()` avanzado, `@field_validator`, modelos anidados y `model_config`.

---

## Paso 1. Schema basico con Field() avanzado

Crea un archivo `schemas/book.py`:

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
```

**Desglose:**

| Campo | Reglas | Error si falla |
|---|---|---|
| `isbn` | 10-13 caracteres, solo digitos | "String should have at least 10 characters" / "String should match pattern" |
| `title` | 2-200 caracteres | "String should have at least 2 characters" |
| `year` | Mayor a 1900, menor a 2027 | "Input should be greater than 1900" |
| `rating` | 1.0 a 5.0, default 3.0 | "Input should be greater than or equal to 1" |

**Pruebas:**

| Envio | Resultado |
|---|---|
| `{"isbn": "9781234567890", "title": "Clean Code", "year": 2008}` | Creado con `rating=3.0` |
| `{"isbn": "123", "title": "Libro", "year": 2008}` | Error 422: isbn demasiado corto |
| `{"isbn": "9781234567890", "title": "Libro", "year": 1800}` | Error 422: year debe ser > 1900 |

---

## Paso 2. Schema con validador personalizado

Crea un archivo `schemas/author.py`:

```python
import re

from pydantic import BaseModel, Field, field_validator


class AuthorCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5, max_length=100)
    birth_year: int | None = Field(default=None, gt=1900, lt=2027)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value
```

**Desglose del validador:**

| Linea | Que hace |
|---|---|
| `@field_validator("email")` | Declara que esta funcion valida el campo `email` |
| `@classmethod` | Los validadores Pydantic deben ser metodos de clase |
| `def validate_email(cls, value):` | Recibe la clase y el valor a validar |
| `pattern = r"^...$"` | Expresion regular para emails basicos |
| `if not re.match(pattern, value):` | Si NO coincide con el patron |
| `raise ValueError("Invalid email format")` | Lanza error que Pydantic convierte en 422 |
| `return value` | Si pasa, devuelve el valor |

**Pruebas:**

| Envio | Resultado |
|---|---|
| `{"name": "Ana Lopez", "email": "ana@mail.com"}` | Creado |
| `{"name": "Ana Lopez", "email": "ana@.com"}` | Error 422: invalid email format |

---

## Paso 3. Schema con modelo anidado

Crea un archivo `schemas/book_detail.py`:

```python
from pydantic import BaseModel, Field

from schemas.book import BookCreate
from schemas.author import AuthorCreate


class PublishingHouse(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    foundation_year: int = Field(gt=1800)


class BookDetail(BaseModel):
    book: BookCreate
    author: AuthorCreate
    publisher: PublishingHouse
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `book: BookCreate` | El campo `book` contiene OTRO schema completo |
| `author: AuthorCreate` | El campo `author` contiene OTRO schema completo |
| `publisher: PublishingHouse` | El campo `publisher` contiene OTRO schema completo |

**JSON que enviaria el cliente:**

```json
{
  "book": {
    "isbn": "9781234567890",
    "title": "Clean Code",
    "year": 2008,
    "rating": 4.5
  },
  "author": {
    "name": "Robert C. Martin",
    "email": "unclebob@mail.com"
  },
  "publisher": {
    "name": "Prentice Hall",
    "foundation_year": 1913
  }
}
```

**Validacion automatica:** Pydantic valida CADA nivel. Si `book.isbn` es invalido, recibes error 422 aunque el resto este bien.

---

## Paso 4. Schema con validador que compara dos campos

Crea un archivo `schemas/promotion.py`:

```python
from datetime import date

from pydantic import BaseModel, Field, field_validator


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

    @field_validator("start_date")
    @classmethod
    def start_must_be_future(cls, start_date):
        if start_date < date.today():
            raise ValueError("start_date must be today or future")
        return start_date
```

**Desglose del validador que compara dos campos:**

| Linea | Que hace |
|---|---|
| `def end_must_be_after_start(cls, end_date, info):` | `info` contiene acceso a TODOS los campos del modelo |
| `if "start_date" in info.data` | Verifica que `start_date` ya fue procesado |
| `end_date <= info.data["start_date"]` | Compara si end_date es anterior o igual a start_date |
| `raise ValueError("end_date must be after start_date")` | Error si la comparacion falla |

---

## Paso 5. Config global con `model_config`

Modifica cualquiera de los schemas anteriores para agregar configuracion global:

```python
from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    isbn: str = Field(
        min_length=10,
        max_length=13,
        regex=r"^\d{10,13}$",
    )
    title: str = Field(min_length=2, max_length=200)
    year: int = Field(gt=1900, lt=2027)
    rating: float = Field(ge=1.0, le=5.0, default=3.0)
```

**¿Que logramos?**

```python
# Cliente envia campo extra:
{"isbn": "9781234567890", "title": "Libro", "year": 2008, "hack": "malo"}
# → Error 422: Extra inputs are not permitted: 'hack'

# Cliente envia con espacios:
{"isbn": "  9781234567890  ", "title": "  Libro  ", "year": 2008}
# → isbn se limpia a "9781234567890", title se limpia a "Libro"
```

---

## Paso 6. Probar errores 422 intencionalmente

Crea un archivo `test_validation.py` junto a tus schemas:

```python
from schemas.book import BookCreate
from schemas.author import AuthorCreate
from schemas.promotion import PromotionCreate
from datetime import date

# Prueba 1: ISBN invalido
try:
    book = BookCreate(isbn="123", title="Libro", year=2008)
except Exception as e:
    print("Error 1:", e)  # ISBN demasiado corto

# Prueba 2: Email invalido
try:
    author = AuthorCreate(name="Ana", email="correo-mal")
except Exception as e:
    print("Error 2:", e)  # Invalid email format

# Prueba 3: Fechas invertidas
try:
    promo = PromotionCreate(
        name="Oferta",
        start_date=date(2026, 12, 31),
        end_date=date(2026, 1, 1),
        discount_percent=10,
    )
except Exception as e:
    print("Error 3:", e)  # end_date must be after start_date
```

---

## Paso 7. Analizar

Responde:

1. **¿Que campo de `BookCreate` tiene validacion con regex?** → `isbn`
2. **¿Que validador compara dos campos?** → `end_must_be_after_start` en `PromotionCreate`
3. **¿Que hace `default=3.0` en `rating`?** → Si el cliente no envia `rating`, toma 3.0
4. **¿Que hace `extra="forbid"`?** → Rechaza campos que no esten definidos en el schema
5. **¿Cuantos niveles de anidacion tiene `BookDetail`?** → 3 (`BookCreate`, `AuthorCreate`, `PublishingHouse`)

---

## Resumen de schemas creados

| Schema | Archivo | Validaciones destacadas |
|---|---|---|
| `BookCreate` | `schemas/book.py` | `regex` en isbn, `gt`/`lt` en year, `ge`/`le` en rating |
| `AuthorCreate` | `schemas/author.py` | `@field_validator` para email |
| `PublishingHouse` | `schemas/book_detail.py` | `gt` en foundation_year |
| `BookDetail` | `schemas/book_detail.py` | Modelo anidado con 3 sub-schemas |
| `PromotionCreate` | `schemas/promotion.py` | Validador que compara `end_date > start_date` |

---

## Cierre

Estos schemas demuestran el poder de Pydantic para definir contratos de datos precisos. Cualquier intento de enviar datos invalidos es rechazado automaticamente antes de llegar a la logica de tu API, con mensajes de error claros y especificos.
