# Dudas frecuentes - Clase 02

> Aqui encontraras las preguntas que los estudiantes suelen hacer (pero a veces da verguenza preguntar). Todas son validas. Si no encuentras tu duda aqui, preguntala en clase.

---

## 1. FastAPI es MVC?

**Respuesta corta:** No de forma literal, pero si aplica la idea.

**Respuesta larga:** FastAPI no te obliga a usar MVC como Laravel o Django. Pero te permite separar responsabilidades de forma similar:
- Los **schemas** son como el Modelo (definen datos).
- Las **respuestas JSON** son como la Vista (lo que ve el cliente).
- Los **routers** son como el Controlador (reciben y coordinan).

**Analogia:** FastAPI es como un restaurante de cocina abierta: los roles existen, pero no hay paredes rigidas entre ellos.

---

## 2. ¿Que seria el controlador en FastAPI?

**Respuesta corta:** Las funciones de ruta dentro de un `APIRouter`.

**Respuesta larga:** En FastAPI, las funciones que decoras con `@router.get()` o `@router.post()` actuan como controladores: reciben la solicitud, invocan servicios y devuelven respuestas. La diferencia es que en FastAPI son funciones (no clases) y deberian ser delgadas (poca logica propia).

---

## 3. ¿Que seria la vista si estoy construyendo una API?

**Respuesta corta:** La respuesta JSON que devuelves.

**Respuesta larga:** En una API, la "vista" no es una pagina HTML bonita, sino los datos estructurados (JSON) que el cliente va a consumir. Si usas Jinja2 (plantillas), entonces si serian paginas HTML.

**Diferencia clave:**
- API pura: `return {"nombre": "Web II"}` → JSON
- Con plantillas: `return templates.TemplateResponse("cursos.html", ...)` → HTML

---

## 4. ¿Para que sirve la capa de servicios?

**Respuesta corta:** Para poner la logica de negocio fuera de los endpoints.

**Respuesta larga:** El servicio es donde viven las "reglas del negocio":
- "No se puede crear un curso con nombre duplicado."
- "Un estudiante no puede tener mas de 5 cursos."
- "Si un prestamo vence, enviar recordatorio."

Sin servicios, estas reglas terminarian dentro de los endpoints, haciendo el codigo dificil de leer y probar.

**Analogia:** El router es el recepcionista que te atiende. El servicio es el gerente que toma las decisiones importantes. El recepcionista no deberia estar aprobando prestamos.

---

## 5. ¿Siempre debo crear carpeta `services`?

**Respuesta corta:** No siempre, pero recomendable cuando hay reglas de negocio.

**Respuesta larga:** 
- **Proyecto minimo** (3-4 endpoints, sin reglas complejas): puede bastar con routers + schemas.
- **Proyecto mediano** (reglas de negocio, varios recursos): los servicios ayudan mucho.
- **Proyecto grande** (muchas reglas, multiples fuentes de datos): los servicios son casi obligatorios.

**Regla practica:** Si tu endpoint tiene mas de 15-20 lineas, probablemente necesitas un servicio.

---

## 6. ¿Cual es la diferencia entre schema y modelo?

| Aspecto | Schema | Modelo |
|---|---|---|
| **Que es** | Define la estructura de datos que entran/salen | Representa la entidad en la base de datos |
| **Herramienta** | Pydantic (`BaseModel`, `Field`) | SQLModel, SQLAlchemy |
| **Responsabilidad** | Validar tipos, formatos, restricciones | Persistir datos, relaciones entre tablas |
| **Cuando se usa** | En cada solicitud HTTP | Cuando se interactua con la BD |

**Ejemplo concreto:**
- **Schema:** `CursoCreate` con `nombre: str = Field(min_length=3)`
- **Modelo:** `CursoDB` con `id: int`, `nombre: str`, `creado_en: datetime`

A veces los schemas y modelos se parecen, pero no deben mezclarse sin criterio.

---

## 7. ¿Es malo tener todo en `main.py`?

**Respuesta corta:** Depende del tamano del proyecto.

**Respuesta larga:**
- **Para una prueba rapida** (2-3 endpoints): no hay problema.
- **Para un proyecto real** (10+ endpoints, con reglas de negocio): si es problema.

**Sintoma de alerta:** Si abres `main.py` y tienes que hacer scroll por mas de 2 pantallas, es hora de separar en modulos.

---

## 8. ¿Como se si estoy agregando demasiadas capas?

**Respuesta corta:** Si una capa no tiene una responsabilidad clara, probablemente sobra.

**Respuesta larga:** La arquitectura debe resolver problemas, no coleccionar nombres elegantes. Preguntate:
- ¿Esta capa tiene una responsabilidad clara y unica?
- ¿Reduce duplicacion o complejidad?
- ¿Facilita las pruebas o los cambios?

Si la respuesta es "no" a todas, la capa probablemente sobra.

**Analogia:** No pongas una puerta blindada en una casa de munecas. La arquitectura debe crecer con el problema.

---

## 9. ¿Que pasa si mezclo las capas? ¿El codigo explota?

**Respuesta corta:** No explota, pero se vuelve dificil de mantener.

**Respuesta larga:** Python no te va a impedir poner logica de negocio dentro del router. El codigo va a funcionar. Pero:
- Es mas dificil de leer (no sabes donde buscar cada cosa).
- Es mas dificil de probar (tienes que simular toda la cadena HTTP para probar una regla simple).
- Es mas dificil de cambiar (modificar una regla puede romper la ruta).

Separar capas es como ordenar tu habitacion: no es obligatorio, pero cuando buscas algo, sabes donde esta.

---

## 10. ¿Que es el codigo 422 que aparece en FastAPI?

**Respuesta corta:** Es el codigo que devuelve FastAPI cuando los datos no pasan la validacion de Pydantic.

**Respuesta larga:** Cuando envias datos a un endpoint y no cumplen las reglas del schema (ej: `nombre` muy corto, `creditos` fuera de rango), FastAPI automaticamente devuelve un error **422 Unprocessable Entity** con los detalles de cada campo que fallo.

**Ventaja:** No tienes que escribir tu propia validacion para cada campo. Pydantic lo hace por ti.

**Ejemplo:**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "nombre"],
      "msg": "String should have at least 3 characters"
    }
  ]
}
```

Esto significa: "el campo `nombre` en el `body` tiene menos de 3 caracteres". Sin escribir una sola linea de `if`.

---

## 11. ¿Que diferencia hay entre PUT y PATCH? Por que no los usamos?

**Respuesta corta:** PUT reemplaza todo, PATCH actualiza parcialmente. No los usamos aun porque nuestro ejemplo es simple.

**Respuesta larga:**
- **PUT** (`reemplazar`): envias el recurso completo, incluso si solo cambias un campo.
- **PATCH** (`actualizar parcialmente`): envias solo los campos que cambian.

En nuestro ejemplo de cursos, si quisieramos actualizar el nombre de un curso, podriamos usar:
- `PUT /cursos/1` → enviar `{nombre, creditos, activo}` completo
- `PATCH /cursos/1` → enviar solo `{nombre: "Nuevo nombre"}`

Los veremos en clases posteriores cuando agreguemos mas operaciones CRUD.
