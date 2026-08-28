# Dudas frecuentes — Clase 03

> Aqui encontraras las preguntas que los estudiantes suelen hacer sobre separacion de responsabilidades. Todas son validas. Si no encuentras tu duda aqui, preguntala en clase.

---

## 1. ¿La separacion de responsabilidades es lo mismo que MVC?

**Respuesta corta:** No. MVC es UNA forma de separar responsabilidades, pero no la unica.

**Respuesta larga:** La separacion de responsabilidades (SRP) es un principio general: cada parte del codigo debe tener una sola razon para cambiar. MVC es un patron especifico que aplica ese principio dividiendo en Modelo, Vista y Controlador.

Otros patrones que tambien aplican SRP:
- **Hexagonal** (puertos y adaptadores)
- **Clean Architecture** (capas concentricas)
- **CQRS** (separar lectura de escritura)

En FastAPI usamos una variante practica: routers + schemas + services. No es MVC puro, pero aplica el mismo principio.

---

## 2. ¿Cuantos archivos debo crear? ¿No es exagerado?

**Respuesta corta:** Depende del tamano del proyecto, pero la regla es: cada archivo debe tener UNA responsabilidad.

**Respuesta larga:** En un proyecto pequeno (2-3 endpoints), crear 5 archivos puede parecer excesivo. Pero piensa en el futuro:

| Endpoints | Recomendacion |
|---|---|
| 1-3 | Puedes empezar con un solo archivo y refactorizar despues |
| 4-8 | Ya conviene separar en capas |
| 10+ | Es casi obligatorio separar |

**Regla practica:** Si abres un archivo y tienes que hacer scroll para encontrar algo, es hora de separar.

**Analogia:** No construyes un armario para guardar 2 camisetas. Pero cuando tienes 30, lo agradeces.

---

## 3. ¿Que pasa si mi servicio solo tiene una linea?

**Respuesta corta:** Esta bien. Mejor un servicio simple que logica dispersa.

**Respuesta larga:** A veces el servicio es tan simple como:

```python
def listar_estudiantes():
    return _estudiantes
```

Y te preguntas: "¿vale la pena crear un archivo para esto?" La respuesta es si, porque:
- **Consistencia:** Todos los endpoints siguen el mismo patron (router → servicio).
- **Preparacion:** Hoy es una linea. Manana puede tener filtros, paginacion, cache.
- **Testeabilidad:** Puedes probar la funcion directamente sin simular HTTP.

---

## 4. ¿La validacion de Pydantic reemplaza las reglas de negocio?

**Respuesta corta:** No. Pydantic valida formato. Las reglas de negocio van en el servicio.

**Respuesta larga:** Son dos cosas diferentes:

| Tipo | Ejemplo | Donde va |
|---|---|---|
| Validacion de formato | "El nombre debe tener al menos 2 caracteres" | Schema (Pydantic) |
| Validacion de formato | "El semestre debe ser entre 1 y 10" | Schema (Pydantic) |
| Regla de negocio | "No puede haber dos estudiantes con el mismo email" | Servicio |
| Regla de negocio | "Un estudiante en semestre 10 debe tener proyecto de grado" | Servicio |

**¿Como se distingue?** Si la regla necesita consultar datos existentes (ej: verificar duplicados), es regla de negocio. Si solo mira el dato individual, es validacion de formato.

---

## 5. ¿El router puede tener logica? ¿O SIEMPRE tiene que delegar?

**Respuesta corta:** Puede tener logica minima, pero la regla de oro es que sea "delgado".

**Respuesta larga:** Lo ideal es que cada funcion del router tenga maximo 2-3 lineas:

```python
# BIEN — router delgado
@router.post("/")
def crear(estudiante: EstudianteCreate):
    return estudiante_service.crear_estudiante(estudiante)
```

```python
# MAL — router obeso
@router.post("/")
def crear(estudiante: EstudianteCreate):
    for e in _estudiantes:
        if e["email"] == estudiante.email:
            raise HTTPException(...)
    nuevo = {"id": _next_id, ...}
    _estudiantes.append(nuevo)
    return nuevo
```

**Excepciones aceptables:** Una transformacion simple de la respuesta (ej: extraer un campo) puede quedarse en el router. Pero si tienes un `if` o un `for`, probablemente deberia estar en el servicio.

---

## 6. ¿Por que separar EstudianteCreate de EstudianteUpdate si son iguales?

**Respuesta corta:** Porque no siempre seran iguales.

**Respuesta larga:** Hoy ambos schemas tienen los mismos campos. Pero en el futuro:

- `EstudianteUpdate` podria tener campos **opcionales** (para actualizar solo el nombre sin reenviar todo):
  ```python
  class EstudianteUpdate(BaseModel):
      nombre: str | None = None
      email: str | None = None
      semestre: int | None = None
  ```
- `EstudianteCreate` podria requerir campos que el update no necesita (ej: `contrasena_inicial`).
- `EstudianteResponse` podria incluir campos calculados (ej: `promedio`, `materias_aprobadas`).

Separar desde el inicio es mucho mas facil que fusionar despues.

---

## 7. ¿Que es el patron "controlador obeso" (Fat Controller)?

**Respuesta corta:** Es cuando el router/controlador hace todo: valida, procesa, consulta datos y responde.

**Respuesta larga:** Es el anti-patron mas comun. El monolito del ejemplo guiado lo sufre:

```python
# Controlador obeso — hace DEMASIADO
@app.post("/estudiantes")
def crear(nombre: str, email: str, semestre: int):
    if not nombre or len(nombre) < 2:           # validacion
        raise HTTPException(...)
    if any(e["email"] == email for e in ...):    # regla de negocio
        raise HTTPException(...)
    nuevo = {"id": _next_id, ...}               # creacion de datos
    _estudiantes.append(nuevo)                   # persistencia
    return nuevo                                 # respuesta
```

**Solucion:** Mover cada responsabilidad a su capa:
- Validacion → Schema
- Reglas de negocio → Servicio
- Respuesta → Router

---

## 8. ¿Siempre necesito `__init__.py`?

**Respuesta corta:** Si, en cada carpeta que quieras importar como paquete Python.

**Respuesta larga:** Sin `__init__.py`, Python no reconoce la carpeta como un paquete y no puedes hacer:

```python
from app.services import estudiante_service  # Error sin __init__.py
```

**¿Puede estar vacio?** Si. Un `__init__.py` vacio es perfectamente valido. Solo le dice a Python: "esta carpeta es un paquete".

> **Nota:** Desde Python 3.3 existen los "namespace packages" que no necesitan `__init__.py`, pero para proyectos de FastAPI es mejor incluirlos siempre para evitar confusiones.

---

## 9. ¿La memoria se borra cuando reinicio el servidor?

**Respuesta corta:** Si. Los datos en listas/diccionarios se pierden al reiniciar.

**Respuesta larga:** En nuestro ejemplo usamos listas en memoria (`_estudiantes = []`) como "base de datos temporal". Cada vez que reinicias uvicorn (o que `--reload` detecta un cambio), la lista se vacia.

**¿Como se resuelve?** Con una base de datos real (SQLite, PostgreSQL). Eso lo veremos en la Semana 13 con SQLAlchemy.

**Lo importante del ejemplo** no es la persistencia, sino la estructura. Cuando conectemos la base de datos, solo cambiaremos el servicio. Los routers y schemas quedaran intactos. Esa es la magia de separar responsabilidades.

---

## 10. ¿Que diferencia hay entre `raise HTTPException` y devolver un error manual?

**Respuesta corta:** `HTTPException` detiene la ejecucion y devuelve una respuesta HTTP con el codigo y mensaje que indiques.

**Respuesta larga:**

```python
# Con HTTPException (recomendado)
raise HTTPException(status_code=404, detail="No encontrado")

# Sin HTTPException (no recomendado)
return {"error": "No encontrado"}  # devuelve status 200!
```

El problema de devolver un diccionario con `"error"` es que el status HTTP sigue siendo **200 OK**, lo que confunde al cliente. Con `HTTPException`, FastAPI automaticamente:
1. Establece el codigo HTTP correcto (404, 400, etc.)
2. Formatea la respuesta como `{"detail": "..."}`.
3. Detiene la ejecucion de la funcion (no se ejecuta el codigo posterior al `raise`).

---

## 11. ¿Por que `DELETE` devuelve 204 y no 200?

**Respuesta corta:** 204 significa "exito, pero sin contenido en la respuesta".

**Respuesta larga:** Los codigos HTTP tienen significados especificos:

| Codigo | Nombre | Uso tipico |
|---|---|---|
| 200 | OK | Respuesta exitosa con datos |
| 201 | Created | Se creo un recurso nuevo |
| 204 | No Content | Exito, pero sin datos que devolver |
| 400 | Bad Request | Datos invalidos (regla de negocio) |
| 404 | Not Found | El recurso no existe |
| 422 | Unprocessable Entity | Datos no pasan validacion (Pydantic) |

Cuando eliminas un estudiante, no necesitas devolver nada. El cliente solo necesita saber que se elimino correctamente, y eso lo comunica el codigo 204.

---

## 12. ¿Que pasa si mas adelante tengo 20 servicios? ¿Se desordena?

**Respuesta corta:** No, si mantienes la estructura. Cada recurso tiene su propio archivo.

**Respuesta larga:** La estructura escala asi:

```
app/
  routers/
    estudiantes.py
    cursos.py
    profesores.py
    matriculas.py
  schemas/
    estudiante.py
    curso.py
    profesor.py
    matricula.py
  services/
    estudiante_service.py
    curso_service.py
    profesor_service.py
    matricula_service.py
```

Cada recurso tiene su propio trio (router + schema + service). Si necesitas tocar algo de estudiantes, sabes exactamente en que 3 archivos buscar. Eso no cambia si tienes 5 o 50 recursos.

---

## 13. ¿Puedo usar clases en vez de funciones para los servicios?

**Respuesta corta:** Si, pero en este curso usamos funciones por simplicidad.

**Respuesta larga:** Ambos enfoques son validos:

```python
# Enfoque funcional (lo que usamos)
def crear_estudiante(datos: EstudianteCreate):
    ...

# Enfoque orientado a objetos
class EstudianteService:
    def crear(self, datos: EstudianteCreate):
        ...
```

El enfoque con clases es util cuando el servicio necesita **estado** (ej: conexion a BD, configuracion). Con FastAPI y Depends, las clases pueden inyectarse como dependencias. Lo veremos en semanas posteriores.

Para esta etapa del curso, funciones son mas claras y directas.
