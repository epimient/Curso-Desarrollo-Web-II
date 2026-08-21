# Ejercicios - Clase 02

> **Nota para el estudiante:** Estos ejercicios van de lo mas simple a lo mas complejo. Si te atascas en uno, revisa los conceptos de la clase o pregunta al docente. El ejercicio 0 es de calentamiento, no te lo saltes.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las frases con las palabras del recuadro:

> **Palabras:** MAIN.PY | ROUTER | SCHEMA | SERVICE | MODELO | VISTA | CONTROLADOR | MVC

1. _________ significa Modelo-Vista-Controlador.
2. El _________ define la estructura y reglas de los datos (como los ingredientes de una receta).
3. La _________ es lo que el usuario ve (HTML, JSON).
4. El _________ recibe solicitudes y coordina acciones (como un mesero).
5. En FastAPI, el archivo _________ es el punto de entrada de la aplicacion.
6. El _________ agrupa rutas por recurso (ej: `/cursos`).
7. El _________ valida los datos de entrada y salida con Pydantic.
8. El _________ contiene la logica de negocio (ej: "no duplicar nombres").

---

## Ejercicio 1. Clasificacion de responsabilidades

Clasifique cada responsabilidad en la capa mas adecuada: `main.py`, router, schema, service, model o middleware.

| Responsabilidad | Capa sugerida |
|---|---|
| Registrar el router de cursos | |
| Validar que `creditos` este entre 1 y 6 | |
| Definir `GET /cursos` | |
| Evitar que dos cursos tengan el mismo nombre | |
| Medir el tiempo de cada solicitud | |
| Definir la estructura de respuesta de un curso | |
| Consultar datos persistidos | |

**Ayuda:** preguntate "¿quien deberia hacer esto?":
- ¿Validar formato? → Schema
- ¿Validar reglas de negocio? → Service
- ¿Declarar rutas? → Router
- ¿Configurar la app? → main.py

---

## Ejercicio 2. Traducir MVC a FastAPI

Complete la tabla con la equivalencia en FastAPI y una breve justificacion:

| Concepto MVC | Equivalencia en FastAPI | Justificacion |
|---|---|---|
| Modelo | | |
| Vista | | |
| Controlador | | |

**Ejemplo de respuesta parcial:**

| Concepto MVC | Equivalencia en FastAPI | Justificacion |
|---|---|---|
| Modelo | Schemas Pydantic | Definen la estructura y validacion de los datos |
| Vista | Respuesta JSON | El cliente recibe JSON como representacion de los datos |
| Controlador | Funciones de ruta (APIRouter) | Reciben solicitudes, coordinan y responden |

---

## Ejercicio 3. Detectar anti-patrones (antes: "encuentra el error")

Lea el siguiente codigo que tiene **varios problemas**:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

cursos = []


@app.post("/cursos")
def crear_curso(curso: dict):
    if not curso.get("nombre"):
        raise HTTPException(status_code=400, detail="Nombre requerido")
    if curso.get("creditos", 0) <= 0:
        raise HTTPException(status_code=400, detail="Creditos invalidos")
    cursos.append(curso)
    return curso
```

**Preguntas:**

1. **¿Que responsabilidades estan mezcladas en este codigo?** (pista: ¿que cosas deberian estar separadas?)
2. **¿Que validaciones deberian ir en un schema Pydantic?** (pista: ¿que datos deberian validarse automaticamente?)
3. **¿Que reglas podrian ir en un service?** (pista: ¿que logica de negocio hay?)
4. **¿Como mejorarias la estructura?** (pista: ¿en que archivos separarias el codigo?)

**Respuesta modelo (para que verifiques despues de intentarlo):**

1. Mezcla: definicion de rutas, validacion de datos, reglas de negocio y almacenamiento, todo en el mismo archivo y funcion.
2. En schema: validar que `nombre` sea string no vacio, que `creditos` sea entero positivo, tipos de datos.
3. En service: la logica de agregar a la lista, evitar duplicados si aplica.
4. Separaria en: `app/schemas/curso.py`, `app/services/curso_service.py`, `app/routers/cursos.py`, `app/main.py`.

---

## Ejercicio 4. Diseno de estructura (aplica lo aprendido)

Proponga una estructura de carpetas para una API de biblioteca con los recursos:

- libros;
- autores;
- prestamos;
- usuarios.

Incluya al menos:

- routers (un archivo por recurso);
- schemas (un archivo por recurso);
- services (un archivo por recurso);
- models (opcional, para persistencia futura);
- main.py.

**Ejemplo de respuesta:**

```
app/
  main.py
  routers/
    libros.py
    autores.py
    prestamos.py
    usuarios.py
  schemas/
    libro.py
    autor.py
    prestamo.py
    usuario.py
  services/
    libro_service.py
    autor_service.py
    prestamo_service.py
    usuario_service.py
  models/
    libro.py
    autor.py
    prestamo.py
    usuario.py
  core/
    config.py
  tests/
    test_libros.py
    test_autores.py
```

---

## Ejercicio 5. Diagrama de flujo (visualiza el proceso)

Dibuje el flujo de una solicitud `POST /libros` desde el cliente hasta la respuesta.

Debe incluir:

- cliente;
- router;
- schema;
- service;
- almacenamiento;
- respuesta.

**Ejemplo de diagrama (puedes dibujarlo en papel o con herramientas):**

```text
[Cliente]                    [Servidor FastAPI]
    |                              |
    |--- POST /libros ------------>|
    |    {                         |
    |      "titulo": "1984",       |
    |      "autor": "Orwell",      |
    |      "anio": 1949            |
    |    }                         |
    |                              |
    |                         [router/libros.py]
    |                              | recibe la solicitud
    |                              v
    |                         [schema/libro.py]
    |                              | valida: titulo no vacio, anio > 0
    |                              v
    |                         [service/libro_service.py]
    |                              | aplica reglas: ISBN unico?
    |                              | guarda en lista/BD
    |                              v
    |<-- 201 Created --------------|
    |    {                         |
    |      "id": 1,                |
    |      "titulo": "1984",       |
    |      "autor": "Orwell",      |
    |      "anio": 1949            |
    |    }                         |
```

---

## Ejercicio 6. Reflexion tecnica

Explique con sus palabras:

**¿Por que separar responsabilidades ayuda a trabajar en equipo?**

Incluya al menos un ejemplo de conflicto que podria evitarse.

**Ayuda:** piensa en escenarios como:
- Dos personas trabajando en el mismo archivo: ¿que pasa?
- Un companero quiere cambiar como se guardan los datos: ¿tiene que modificar las rutas?
- Llega una persona nueva al proyecto: ¿donde mira primero para entender como funciona?

**Ejemplo de conflicto que se evita:** "Si todo el codigo esta en `main.py`, dos programadores no pueden trabajar al mismo tiempo porque siempre habra conflictos de merge. Con capas separadas, uno puede modificar `services/` mientras otro modifica `routers/` sin pisarse."
