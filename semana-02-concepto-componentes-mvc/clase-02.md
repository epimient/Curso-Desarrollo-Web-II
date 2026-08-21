# Clase 02 - MVC, patrones y equivalencia arquitectonica en FastAPI

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 2  
**Unidad:** Unidad 1 - Introduccion a MVC y Frameworks  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA1: Comprender los conceptos fundamentales del patron MVC y los frameworks de desarrollo de software mediante la identificacion de sus componentes y su interaccion.
- RA2: Analizar las ventajas y desventajas de utilizar frameworks en el desarrollo de aplicaciones web mediante la comparacion de diferentes frameworks y su aplicabilidad en distintos contextos.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

Esta clase busca que el estudiante comprenda el patron MVC como una estrategia de separacion de responsabilidades, no como una camisa de fuerza arquitectonica. El syllabus menciona MVC, rutas, controladores y plantillas; FastAPI, por su naturaleza, no replica exactamente la estructura de frameworks MVC clasicos como Laravel, ASP.NET MVC o Ruby on Rails. Por eso, el objetivo pedagogico es entender la intencion del patron y traducirla de forma correcta al ecosistema FastAPI.

La meta no es memorizar carpetas como si fueran mandamientos tallados en piedra. La meta es responder una pregunta mas importante: **donde debe vivir cada responsabilidad para que el proyecto sea mantenible, claro y escalable?**

## 3. Pregunta orientadora

**Como separamos responsabilidades en una aplicacion FastAPI sin forzar un MVC literal?**

Esta pregunta permite conectar los conceptos tradicionales del syllabus con una arquitectura realista en FastAPI.

## 4. Recordatorio: que es un patron de diseno

> **En espanol simple:** un patron de diseno es como una "receta de cocina" para resolver problemas que ya han resuelto muchos antes que tu. No tienes que inventar la forma de organizar tu codigo cada vez. Sigues una receta que ya funciona.

Un patron de diseno es una solucion reutilizable para un problema frecuente de diseno de software. No es una receta mecanica ni una plantilla sagrada. Es una forma de organizar decisiones.

**Analogia:** Imagina que quieres armar un mueble de IKEA. Viene con instrucciones (el patron). Puedes seguirlas y el mueble queda bien. O puedes ignorarlas y terminar con una repesera coja. El patron no es magia, es experiencia empaquetada.

En desarrollo web, los patrones ayudan a:

- **separar responsabilidades** (cada cosa en su lugar);
- **reducir duplicacion** (no escribir lo mismo dos veces);
- **facilitar pruebas** (probar piezas pequeñas es mas facil);
- **mejorar lectura del proyecto** (sabes donde buscar cada cosa);
- **permitir cambios sin romper todo** (cambias una pieza sin afectar las otras);
- **mantener la logica de negocio lejos del caos de entrada/salida**.

> **Advertencia:** Un patron mal entendido puede hacer dano. Si se aplica solo por moda, puede llenar el proyecto de capas innecesarias, nombres solemnes y carpetas que no hacen nada. Eso no es arquitectura; es cosplay empresarial.

## 5. El patron MVC

MVC significa **Modelo-Vista-Controlador**.

> **En espanol simple:** MVC es una forma de organizar tu codigo en tres grupos con responsabilidades distintas. Como en un restaurante: hay separacion entre quien toma la orden, quien cocina y como se sirve el plato.

**Analogia completa del restaurante para entender MVC:**

| Componente | Rol en restaurante | Rol en programacion |
|---|---|---|
| **Modelo** | La receta y los ingredientes | Los datos y reglas de negocio |
| **Vista** | El plato servido al cliente | Lo que el usuario ve (HTML, JSON) |
| **Controlador** | El mesero que toma la orden | Quien recibe la solicitud y coordina |

**Flujo en el restaurante:**
1. Tu (cliente) le dices al **mesero** (controlador): "quiero pizza margherita"
2. El mesero va a la **cocina** y le pasa la orden al **chef** (modelo/servicio)
3. El chef prepara la pizza siguiendo la **receta** (logica de negocio)
4. El mesero te trae el **plato servido** (vista)

Cada quien hace su trabajo. El mesero no cocina. El chef no toma ordenes. El plato no se prepara solo.

### 5.1 Modelo

> **En espanol simple:** el modelo son los "datos" y las "reglas" de tu aplicacion. Responde a: ¿que cosas existen? ¿que reglas deben cumplir?

El modelo representa los datos y reglas principales del dominio. En una aplicacion tradicional, puede incluir entidades, validaciones, consultas o estructuras relacionadas con persistencia.

Ejemplo conceptual:

- **Estudiante** (tiene nombre, edad, correo)
- **Curso** (tiene nombre, creditos, activo)
- **Producto** (tiene precio, stock, categoria)
- **Pedido** (tiene fecha, total, estado)
- **Prestamo** (tiene fecha_inicio, fecha_fin, estado)

El modelo responde preguntas como:

- ¿Que datos existen?
- ¿Que reglas deben cumplirse? (ej: "un curso debe tener al menos 1 credito")
- ¿Como se representa una entidad del dominio?

### 5.2 Vista

> **En espanol simple:** la vista es "lo que el usuario ve". En una pagina web son los HTML. En una API es el JSON que devuelves.

La vista es la forma como se presenta informacion al usuario. En frameworks MVC clasicos, suele estar asociada con plantillas HTML.

Ejemplos:

- una pagina que lista cursos;
- un formulario para crear estudiantes;
- una vista de detalle de producto;
- una tabla de prestamos.

En APIs modernas, muchas veces la "vista" no es HTML, sino una respuesta JSON consumida por un frontend, una app movil u otro servicio.

**Dato clave:** En FastAPI, la "vista" suele ser la respuesta JSON. Pero si usas Jinja2 (plantillas), puedes generar HTML tambien.

### 5.3 Controlador

> **En espanol simple:** el controlador es el "intermediario". Recibe la solicitud del cliente, llama a quien corresponde y devuelve la respuesta. No deberia hacer todo el trabajo el solo.

El controlador recibe solicitudes, coordina acciones y decide que respuesta entregar. Su papel es conectar la entrada del usuario con la logica del sistema.

En una aplicacion MVC clasica, el controlador podria:

- recibir una solicitud HTTP;
- leer parametros;
- invocar una consulta o servicio;
- seleccionar una vista;
- devolver una respuesta.

**El riesgo:** convertir el controlador en una criatura gigante que valida, consulta, decide, formatea, envia correos, hace cafe y posiblemente despliega a produccion. En terminos tecnicos: un controlador obeso. En terminos anime: villano de arco final con demasiadas transformaciones.

> **Regla de oro:** El controlador debe ser delgado. Recibe, delega, responde. Nada mas.

## 6. MVC clasico vs FastAPI

> **En espanol simple:** FastAPI no es MVC clasico (como Laravel o Django), pero aplica la misma idea: separar responsabilidades. Solo que lo hace a su manera.

FastAPI esta disenado principalmente para construir APIs. Su modelo mental se basa en:

- rutas declarativas;
- funciones de operacion;
- tipado de Python;
- validacion con Pydantic;
- inyeccion de dependencias;
- documentacion OpenAPI;
- middleware ASGI;
- respuestas JSON por defecto.

Por eso, no conviene decir que FastAPI "usa MVC" de forma literal. Es mas correcto decir que **permite aplicar la intencion de MVC mediante separacion de responsabilidades**.

**Tabla de equivalencia (con analogia incluida):**

| MVC clasico | Equivalencia en FastAPI | Analogia |
|---|---|---|
| **Modelo** | Schemas Pydantic, modelos de persistencia | La receta y los ingredientes |
| **Vista** | Respuestas JSON, plantillas Jinja2 | El plato servido al cliente |
| **Controlador** | Funciones de ruta y APIRouter | El mesero que toma la orden |
| **Servicio** | Capa de logica de negocio | El chef que aplica las reglas |
| **Middleware** | Comportamiento transversal | El control de calidad que revisa cada plato |
| **Router** | Agrupacion de endpoints | La seccion del menu (entradas, platos fuertes, postres) |

**¿Por que FastAPI no es MVC "literal"?**

En MVC clasico:
- El **Modelo** habla directamente con la base de datos.
- La **Vista** es HTML (no JSON).
- El **Controlador** suele ser una clase con metodos.

En FastAPI:
- Los **Schemas Pydantic** definen la forma de los datos (entrada/salida).
- Las **respuestas JSON** son la "vista" del API.
- Las **funciones de ruta** son ligeras, no clases pesadas.
- Los **Servicios** son una capa extra que no existe en MVC clasico.

> **Consejo:** No intentes forzar FastAPI a ser Laravel. FastAPI tiene su propia personalidad. A veces la madurez tecnica consiste en no ponerle armadura medieval a un droide.

## 7. Arquitectura recomendada para el curso

> **En espanol simple:** Vamos a organizar nuestro codigo en carpetas, cada una con una responsabilidad clara. Como un edificio con pisos: cada piso tiene una funcion distinta (recepcion, oficinas, cafeteria), pero todos trabajan juntos.

Para este curso, se propone una arquitectura progresiva. No desde la primera clase con 27 carpetas, porque eso asusta mas que ayuda. Pero si con una idea clara de evolucion.

**Estructura sugerida (visual):**

```text
app/
├── main.py              # Punto de entrada - "La recepcion del edificio"
├── routers/
│   └── cursos.py        # Rutas - "La entrada de cada seccion"
├── schemas/
│   └── curso.py         # Validacion - "El formulario que debe llenarse"
├── services/
│   └── curso_service.py # Logica - "Las reglas del negocio"
├── models/
│   └── curso.py         # Datos - "El archivo donde se guarda info"
├── core/
│   └── config.py        # Config - "El cuadro electrico del edificio"
└── tests/
    └── test_cursos.py   # Pruebas - "El control de calidad"
```

**El flujo completo cuando alguien usa tu API:**

```
Usuario hace clic
      │
      v
  [main.py]  ─── recibe la solicitud, la envia al router correcto
      │
      v
  [routers/] ─── recibe la peticion, llama al servicio
      │
      v
  [schemas/] ─── valida que los datos sean correctos
      │
      v
  [services/] ─── aplica reglas de negocio
      │
      v
  [models/]  ─── guarda o consulta datos
      │
      v
  ¡Respuesta al usuario!
```

### 7.1 `main.py` - La recepcion del edificio

> **En espanol simple:** `main.py` es el punto de entrada. Cuando ejecutas tu API, esto es lo primero que se ejecuta. Aqui creas la aplicacion, registras los routers y configuras cosas generales.

Es el punto de entrada de la aplicacion. Crea la instancia de FastAPI y registra routers, middleware y configuraciones generales.

Responsabilidades:

- crear `app = FastAPI()`;
- registrar routers;
- configurar middleware;
- definir metadatos generales (titulo, version, descripcion);
- evitar acumular toda la logica del sistema.

`main.py` debe ser una recepcion organizada, no una bodega donde se tiran todos los muebles.

**ASÍ NO ❌ (todo en main.py):**
```python
from fastapi import FastAPI

app = FastAPI()

cursos = []

@app.get("/cursos")
def listar():
    return cursos

@app.post("/cursos")
def crear(curso: dict):
    if not curso.get("nombre"):
        return {"error": "nombre requerido"}
    cursos.append(curso)
    return curso
```

**ASÍ SÍ ✅ (main.py solo registra):**
```python
from fastapi import FastAPI
from app.routers import cursos

app = FastAPI(title="API Academica")
app.include_router(cursos.router)
```

### 7.2 `routers/` - La entrada de cada seccion

> **En espanol simple:** los routers son como las puertas de cada seccion del edificio. "Aqui se atienden los cursos", "aqui se atienden los usuarios". Cada recurso tiene su propio archivo.

Contiene rutas agrupadas por recurso o modulo. Por ejemplo:

- `usuarios.py`
- `cursos.py`
- `productos.py`
- `prestamos.py`

Responsabilidades:

- declarar endpoints;
- recibir parametros;
- definir codigos de respuesta;
- invocar servicios;
- devolver respuestas.

Los routers cumplen el papel mas cercano al controlador, pero no deberian contener toda la logica de negocio.

### 7.3 `schemas/` - El formulario que debe llenarse

> **En espanol simple:** los schemas definen "que forma tienen los datos". Como un formulario que dice: "nombre: texto de 3 a 80 caracteres, creditos: numero del 1 al 6". Si alguien envia datos que no cumplen, Pydantic (el validador) los rechaza automaticamente.

Contiene modelos Pydantic usados para validar entrada y salida.

Responsabilidades:

- definir estructura de datos recibidos;
- validar tipos;
- establecer campos obligatorios u opcionales;
- controlar que informacion se expone en la respuesta.

Ejemplo con explicacion:

```python
from pydantic import BaseModel, Field


class CursoCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=80)
    creditos: int = Field(ge=1, le=6)


class CursoResponse(BaseModel):
    id: int
    nombre: str
    creditos: int
```

**Explicacion:**
- `CursoCreate` es lo que el cliente debe enviar para crear un curso.
- `CursoResponse` es lo que el servidor devuelve como respuesta.
- `Field(min_length=3)` significa: el nombre debe tener al menos 3 caracteres.
- `Field(ge=1)` significa: creditos debe ser mayor o igual a 1.

**¿Por que separar entrada y salida?** Porque no siempre lo que entra es igual a lo que sale. Por ejemplo, al crear un usuario, envias contrasena, pero la respuesta nunca debe devolver la contrasena.

### 7.4 `services/` - Las reglas del negocio

> **En espanol simple:** los servicios contienen la "logica del negocio". No solo validar que un nombre tenga 3 caracteres (eso lo hace el schema). Sino cosas como: "no se puede crear un curso con nombre duplicado" o "un estudiante no puede tener mas de 5 cursos activos".

Contiene la logica de negocio. Esta capa permite que los endpoints no se llenen de reglas internas.

Responsabilidades:

- validar reglas del dominio;
- coordinar operaciones;
- consultar repositorios o almacenamiento;
- lanzar errores controlados;
- facilitar pruebas unitarias.

Ejemplo de regla que NO deberia estar en el router:

> "No se puede crear un curso con nombre duplicado."

Pydantic valida tipos y restricciones basicas. El servicio valida reglas del negocio. Son responsabilidades distintas. Mezclarlas sin cuidado es como poner CSS dentro de SQL: tecnicamente alguien puede intentarlo, pero espiritualmente algo se rompe.

### 7.5 `models/` - El archivo donde se guarda info

> **En espanol simple:** los modelos son la representacion de los datos en la base de datos. Por ahora usaremos datos en memoria (listas de Python), pero en fases posteriores usaremos SQLModel o SQLAlchemy para conectarnos a una BD real.

En fases posteriores, `models/` representara modelos de persistencia, por ejemplo con SQLModel o SQLAlchemy.

En esta clase todavia se puede trabajar con datos en memoria para concentrarse en la arquitectura.

### 7.6 `core/` - El cuadro electrico del edificio

> **En espanol simple:** `core/` guarda configuraciones generales: variables de entorno, claves de seguridad, constantes. No siempre lo usamos al inicio, pero es bueno saber que existe.

Contiene configuracion general: variables de entorno, seguridad, constantes y parametros de aplicacion.

No siempre se necesita al inicio, pero conviene conocer su proposito.

## 8. Flujo de una solicitud en la arquitectura propuesta

Ejemplo: crear un curso.

```text
Cliente
  |
  | POST /cursos
  v
Router cursos.py
  |
  | recibe CursoCreate
  v
Schema Pydantic
  |
  | valida estructura y tipos
  v
Service curso_service.py
  |
  | aplica reglas de negocio
  v
Almacenamiento o base de datos
  |
  | retorna curso creado
  v
Router
  |
  | responde CursoResponse
  v
Cliente
```

Este flujo permite explicar como se conserva la intencion de MVC:

- Entrada HTTP organizada por rutas.
- Datos estructurados por modelos/schemas.
- Reglas separadas en servicios.
- Respuesta clara para cliente o vista.

## 9. Anti-patrones frecuentes (errores que ya sabemos que vas a cometer)

> **En espanol simple:** un anti-patron es una "mala practica" que parece buena idea al principio, pero te va a doler despues. Aqui te mostramos los mas comunes y como evitarlos.

### 9.1 Todo en `main.py` ("el pergamino infinito")

**El problema:** Es tentador poner todo en un solo archivo. Funciona al inicio, pero cuando el proyecto crece, `main.py` se convierte en un monstruo de 500 lineas imposible de mantener.

**ASÍ NO ❌ (todo en main.py):**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/cursos")
def listar_cursos():
    return [{"id": 1, "nombre": "Web II"}]

# 100 lineas despues...
@app.post("/cursos")
def crear_curso(datos):
    # validacion...
    # reglas de negocio...
    # guardar en BD...
    # enviar email...
    # todo aqui dentro
    pass
```

**ASÍ SÍ ✅ (main.py solo registra):**
```python
from fastapi import FastAPI
from app.routers import cursos

app = FastAPI(title="API Academica")
app.include_router(cursos.router)
```

> **Sintoma de alerta:** Si `main.py` parece pergamino infinito, es hora de separar.

### 9.2 Logica de negocio dentro del endpoint ("el controlador obeso")

**El problema:** El endpoint recibe la solicitud, valida datos, aplica reglas, guarda en BD, envia correos... hace de todo. Esto viola el principio de "cada cosa en su lugar".

**ASÍ NO ❌ (logica en el endpoint):**
```python
@app.post("/cursos")
def crear_curso(curso: CursoCreate):
    if curso.nombre in nombres_existentes:       # Regla de negocio AQUI
        raise HTTPException(status_code=400, detail="Curso duplicado")
    if curso.creditos < 1:                        # Validacion AQUI
        raise HTTPException(status_code=400, detail="Creditos invalidos")
    # mas reglas...
    # mas validaciones...
    # mas persistencia...
    return curso
```

**ASÍ SÍ ✅ (coordinacion delegada):**
```python
@app.post("/cursos", response_model=CursoResponse, status_code=201)
def registrar_curso(curso: CursoCreate):
    return crear_curso(curso)  # El servicio hace el trabajo pesado
```

> **Sintoma de alerta:** Si tu funcion de ruta tiene mas de 15-20 lineas, probablemente esta haciendo cosas que no deberia.

### 9.3 Usar el mismo schema para entrada y salida ("exponer datos privados")

**El problema:** Usar el mismo modelo Pydantic para recibir datos y para devolverlos puede exponer informacion sensible.

**ASÍ NO ❌ (un solo schema para todo):**
```python
class Usuario(BaseModel):
    email: str
    password: str     # Si usas esto como respuesta, EXPONES la contrasena
    es_admin: bool    # Esto tampoco deberia ir en la respuesta
```

**ASÍ SÍ ✅ (separar entrada y salida):**
```python
class UsuarioCreate(BaseModel):
    email: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    email: str
    # Sin password, sin es_admin...
```

> **Sintoma de alerta:** Si una API devuelve passwords, no es un bug: es una alarma de evacuacion.

**Regla practica:**
- **Entrada:** solo lo necesario para crear/actualizar.
- **Salida:** solo lo que el cliente necesita ver.
- **Persistencia:** lo que se guarda en BD (puede incluir datos internos).

### 9.4 Arquitectura demasiado compleja demasiado pronto ("sobreingenieria")

**El problema opuesto:** Crear 10 capas, 5 abstract factories y 3 interfaces para una API que solo lista 3 cursos. La arquitectura debe crecer con el problema.

**ASÍ NO ❌ (arquitectura prematura):**
```text
app/
  core/
    abstract/
      base_repository.py
      base_service.py
      base_router.py
    factories/
      repository_factory.py
      service_factory.py
  ...
```

Para listar 3 cursos en memoria.

**ASÍ SÍ ✅ (arquitectura progresiva):**
```text
Empieza simple con:
app/
  main.py
  routers/
  schemas/
  services/

Cuando necesites BD, agrega:
  models/

Cuando necesites config, agrega:
  core/

Cuando necesites tests, agrega:
  tests/
```

> **Principio docente:** Empezar simple, pero no desordenado.

## 10. Actividad central de clase

### 10.1 Actividad: desarmar una aplicacion CRUD en capas

El docente presenta un caso sencillo: API para administrar cursos academicos.

Recurso: `Curso`

Campos:

- `id`
- `nombre`
- `creditos`
- `activo`

Los estudiantes deben decidir donde ubicar cada responsabilidad:

| Responsabilidad | Capa sugerida |
|---|---|
| Declarar `GET /cursos` | Router |
| Validar que `creditos` sea mayor que cero | Schema Pydantic |
| Evitar nombres duplicados | Service |
| Guardar temporalmente cursos | Service o repositorio temporal |
| Devolver JSON al cliente | Router / FastAPI |
| Configurar titulo de la API | main.py |
| Agregar CORS | Middleware/configuracion |

### 10.2 Discusion

Preguntas:

1. Que responsabilidades se parecen al Modelo?
2. Que responsabilidades se parecen al Controlador?
3. Que seria la Vista si la aplicacion responde JSON?
4. Por que conviene tener servicios?
5. Cuando una capa adicional ayuda y cuando estorba?

## 11. Ejemplo completo de codigo (con explicacion linea por linea)

A continuacion, el codigo completo de nuestra API de cursos, archivo por archivo, con cada linea explicada.

### 11.1 Schema (`app/schemas/curso.py`)

```python
from pydantic import BaseModel, Field


class CursoCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=80)
    creditos: int = Field(ge=1, le=6)


class CursoResponse(BaseModel):
    id: int
    nombre: str
    creditos: int
    activo: bool
```

**Explicacion linea por linea:**

| Linea | Explicacion |
|---|---|
| `from pydantic import BaseModel, Field` | Importa las herramientas de Pydantic para crear modelos de datos. |
| `class CursoCreate(BaseModel):` | Define un modelo para los datos que el cliente ENVIA al crear un curso. |
| `nombre: str = Field(min_length=3, max_length=80)` | El campo `nombre` debe ser texto (str) de entre 3 y 80 caracteres. |
| `creditos: int = Field(ge=1, le=6)` | El campo `creditos` debe ser un numero entero (int) entre 1 y 6. |
| `class CursoResponse(BaseModel):` | Define un modelo para los datos que el servidor DEVUELVE como respuesta. |
| `id: int` | El ID del curso (lo genera el servidor, el cliente no lo envia). |
| `nombre: str` | El nombre del curso. |
| `creditos: int` | Los creditos del curso. |
| `activo: bool` | Estado del curso (activo o inactivo). El servidor lo asigna automaticamente. |

> **Diferencia clave:** `CursoCreate` es lo que el cliente ENVIA. `CursoResponse` es lo que el servidor DEVUELVE. Son modelos distintos porque no siempre coinciden (ej: el cliente no envia `id`, pero el servidor si lo devuelve).

### 11.2 Service (`app/services/curso_service.py`)

```python
from fastapi import HTTPException
from app.schemas.curso import CursoCreate

_cursos = []           # Lista en memoria donde guardaremos los cursos
_next_id = 1            # Contador para asignar IDs automaticamente


def listar_cursos():
    """Devuelve todos los cursos almacenados."""
    return _cursos


def crear_curso(curso: CursoCreate):
    """Crea un nuevo curso, validando que no haya duplicados."""
    global _next_id     # Necesitamos modificar la variable global

    # Revisa si ya existe un curso con el mismo nombre (sin importar mayusculas/minusculas)
    existe = any(item["nombre"].lower() == curso.nombre.lower() for item in _cursos)

    if existe:
        # Si existe, lanza un error HTTP 400 (Bad Request)
        raise HTTPException(
            status_code=400,
            detail="Ya existe un curso con ese nombre"
        )

    # Crea el diccionario del nuevo curso
    nuevo = {
        "id": _next_id,
        "nombre": curso.nombre,
        "creditos": curso.creditos,
        "activo": True,      # Por defecto, los cursos se crean activos
    }

    _cursos.append(nuevo)    # Agrega el curso a la lista
    _next_id += 1            # Incrementa el contador para el proximo ID

    return nuevo             # Devuelve el curso creado
```

**Explicacion linea por linea:**

| Linea | Explicacion |
|---|---|
| `_cursos = []` | Crea una lista vacia para almacenar cursos. El guion bajo (`_`) indica que es "privada" (no deberia usarse fuera de este archivo). |
| `_next_id = 1` | Variable que lleva la cuenta del proximo ID disponible. |
| `def listar_cursos():` | Funcion que devuelve la lista de cursos. Simple y directa. |
| `def crear_curso(curso: CursoCreate):` | Funcion que recibe un objeto `CursoCreate` validado. |
| `global _next_id` | Necesario porque vamos a modificar `_next_id` dentro de la funcion. Sin esto, Python crearia una variable local. |
| `any(item["nombre"].lower() == ...)` | `any()` revisa si algun elemento de la lista cumple la condicion. Si encuentra un nombre igual (en minusculas), `existe` sera `True`. |
| `raise HTTPException(...)` | Si el curso ya existe, lanzamos un error HTTP controlado. FastAPI lo convierte en una respuesta JSON con codigo 400. |
| `nuevo = { ... }` | Creamos un diccionario con los datos del nuevo curso. |
| `_cursos.append(nuevo)` | Agregamos el curso a la lista de cursos. |
| `_next_id += 1` | Aumentamos el contador para que el proximo curso tenga un ID diferente. |

### 11.3 Router (`app/routers/cursos.py`)

```python
from fastapi import APIRouter, status

from app.schemas.curso import CursoCreate, CursoResponse
from app.services.curso_service import crear_curso, listar_cursos

router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("/", response_model=list[CursoResponse])
def obtener_cursos():
    """Devuelve la lista de todos los cursos."""
    return listar_cursos()


@router.post("/", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def registrar_curso(curso: CursoCreate):
    """Crea un nuevo curso (validacion incluida)."""
    return crear_curso(curso)
```

**Explicacion linea por linea:**

| Linea | Explicacion |
|---|---|
| `from fastapi import APIRouter, status` | `APIRouter` permite agrupar rutas. `status` da nombres a los codigos HTTP. |
| `router = APIRouter(prefix="/cursos", tags=["Cursos"])` | Crea un router. `prefix="/cursos"` significa que todas las rutas aqui empiezan con `/cursos`. `tags` es para la documentacion. |
| `@router.get("/", response_model=list[CursoResponse])` | Define un endpoint GET en `GET /cursos`. La respuesta sera una lista de `CursoResponse`. |
| `def obtener_cursos():` | Funcion que maneja la solicitud. Solo llama al servicio. |
| `@router.post("/", response_model=CursoResponse, status_code=201)` | Define un endpoint POST en `POST /cursos`. Devuelve codigo 201 (Creado). |
| `def registrar_curso(curso: CursoCreate):` | Recibe un `CursoCreate` (ya validado por Pydantic). Solo llama al servicio. |

> **Nota importante:** El router NO valida duplicados, NO guarda en memoria, NO asigna IDs. Solo coordina: recibe la solicitud, llama al servicio correspondiente, y devuelve la respuesta. El trabajo pesado lo hace el servicio.

### 11.4 Main (`app/main.py`)

```python
from fastapi import FastAPI
from app.routers import cursos

app = FastAPI(title="API academica")

app.include_router(cursos.router)
```

**Explicacion linea por linea:**

| Linea | Explicacion |
|---|---|
| `from fastapi import FastAPI` | Importa la clase principal de FastAPI. |
| `from app.routers import cursos` | Importa el router de cursos que definimos antes. |
| `app = FastAPI(title="API academica")` | Crea la aplicacion FastAPI. El `title` aparece en la documentacion. |
| `app.include_router(cursos.router)` | Registra el router de cursos para que FastAPI sepa que existe. Sin esta linea, las rutas no funcionarian. |

### Resumen visual del flujo completo

```
CLIENTE                        SERVIDOR (FastAPI)
   |                               |
   |--- POST /cursos ------------->|
   |    {                          |
   |      "nombre": "Web II",      |
   |      "creditos": 3            |
   |    }                          |
   |                               |
   |                          [main.py] recibe la solicitud
   |                               |  la envia al router de cursos
   |                               v
   |                          [router] recibe los datos
   |                               |  los pasa al schema para validar
   |                               v
   |                          [schema] valida tipo y formato
   |                               |  si todo bien, pasa al service
   |                               v
   |                          [service] verifica duplicados
   |                               |  guarda en memoria
   |                               v
   |<-- 201 Created ---------------|
   |    {                          |
   |      "id": 1,                 |
   |      "nombre": "Web II",      |
   |      "creditos": 3,           |
   |      "activo": true           |
   |    }                          |
```

## 12. Cierre conceptual

### ¿Que aprendimos hoy?

Hoy dimos el salto de "consumir APIs" a "disenar la arquitectura de nuestras APIs". Los conceptos clave:

1. **MVC es una forma de pensar**, no una camisa de fuerza. Separar datos (Modelo), presentacion (Vista) y coordinacion (Controlador).
2. **FastAPI no es MVC literal**, pero aplica la misma intencion con sus propias herramientas: routers, schemas, services.
3. **Cada capa tiene una responsabilidad:** `main.py` registra, `routers/` coordina, `schemas/` valida, `services/` aplica reglas, `models/` persiste.
4. **Los anti-patrones existen:** todo en main.py, logica en endpoints, schemas sin criterio, sobreingenieria.
5. **La arquitectura progresiva:** empieza simple, agrega capas cuando las necesites.

MVC sigue siendo util como patron de pensamiento: separar datos, presentacion y coordinacion. Pero FastAPI invita a una arquitectura mas orientada a APIs, contratos y servicios.

Al cierre de esta clase, el estudiante debe poder explicar:

- que problema intenta resolver MVC;
- por que FastAPI no es MVC literal;
- como traducir MVC a routers, schemas, services y responses;
- por que separar responsabilidades mejora mantenibilidad;
- que riesgos aparecen cuando todo se mezcla en un solo archivo.

La arquitectura no es decoracion. Es la diferencia entre un proyecto que crece y un proyecto que se convierte en ruina arqueologica con endpoints.

## 13. Trabajo independiente (6 horas sugeridas)

### 13.1 Diagrama de arquitectura (2 horas)

Elabora un diagrama de arquitectura para una API sencilla (puede ser la misma del proyecto integrador). No necesitas un programa especial, puede ser en papel, en una pizarra, o usando herramientas como:
- **Draw.io / diagrams.net** (gratis, online)
- **Miro** (pizarra colaborativa)
- **Lucidchart** (con plantillas)
- **Papel y lapiz** (perfectamente valido)

El diagrama debe mostrar:

```
[Cliente] --> [Router] --> [Schema] --> [Service] --> [Almacenamiento]
     ^                                                        |
     |________________________________________________________|
```

Con etiquetas que expliquen que hace cada componente.

### 13.2 Recursos del proyecto integrador (2 horas)

Identifica minimo **tres recursos** (entidades) de tu proyecto. Por ejemplo, si tu proyecto es una biblioteca:

| Recurso | Rutas principales | Schema inicial | Reglas de negocio |
|---|---|---|---|
| **Libros** | GET /libros, POST /libros, GET /libros/{id} | titulo, autor, isbn, anio | ISBN debe ser unico; titulo no vacio |
| **Autores** | GET /autores, POST /autores | nombre, nacionalidad, fecha_nac | Nombre obligatorio |
| **Prestamos** | GET /prestamos, POST /prestamos | libro_id, usuario_id, fecha_prestamo | No prestar si el usuario debe libros |

### 13.3 Comparacion de frameworks (2 horas)

Prepara una comparacion breve entre FastAPI y al menos dos frameworks web (Django, Flask, Laravel, Spring Boot, Next.js, etc.). Usa criterios como:

| Criterio | FastAPI | Django | Flask |
|---|---|---|---|
| Tipo | API moderno | Web completo | Microframework |
| Curva de aprendizaje | Baja-media | Alta | Baja |
| Documentacion automatica | Si (OpenAPI) | No nativa | No nativa |
| Tipado obligatorio | Si | No | No |
| Ideal para | APIs | Aplicaciones completas | Proyectos pequenos |

## 14. Producto esperado

**Evidencia sugerida:** diagrama arquitectonico comentado + tabla de recursos.

### Checklist de entregable:

- [ ] **Diagrama arquitectonico** mostrando cliente, rutas, schemas, servicios, almacenamiento y respuesta (puede ser dibujado a mano y fotografiado).
- [ ] **Tabla con 3+ recursos** del proyecto integrador, con rutas, schemas y reglas de negocio.
- [ ] **Comparacion breve** de FastAPI vs otros 2 frameworks.
- [ ] **Reflexion personal** (opcional pero recomendada): "¿Que fue lo mas dificil de entender hoy? ¿Que concepto necesito repasar?"

### El diagrama debe incluir:

- cliente;
- rutas;
- schemas;
- servicios;
- modelo o almacenamiento;
- respuesta;
- responsabilidades de cada parte.

## 15. Bibliografia y referencias utiles

- FastAPI. (s. f.). *Bigger Applications - Multiple Files*. https://fastapi.tiangolo.com/tutorial/bigger-applications/
- FastAPI. (s. f.). *Path Operation Configuration*. https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
- FastAPI. (s. f.). *Body - Fields*. https://fastapi.tiangolo.com/tutorial/body-fields/
- Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
