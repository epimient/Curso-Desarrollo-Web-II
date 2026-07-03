# Clase 04 - Instalacion, entorno y primer proyecto FastAPI

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 4  
**Unidad:** Unidad 2 - Uso de un Framework Especifico  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA3: Desarrollar habilidades para la creacion y manejo de rutas y controladores dentro del framework mediante la implementacion de logica de negocio en controladores o equivalentes pedagogicos.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

Esta clase marca el inicio tecnico formal del trabajo con FastAPI. El estudiante debe instalar y preparar su entorno, crear un primer proyecto, ejecutar el servidor con Uvicorn, revisar la documentacion automatica y comprender la estructura minima de una aplicacion.

La meta no es solamente que aparezca "Hello World". Eso seria muy 2007, aunque nostalgico. La meta es que el estudiante entienda que piezas intervienen cuando una API FastAPI se ejecuta:

- Python como lenguaje base.
- Entorno virtual para aislar dependencias.
- FastAPI como framework.
- Uvicorn como servidor ASGI.
- Un archivo principal con la instancia `FastAPI`.
- Endpoints declarados con decoradores.
- Documentacion automatica con Swagger UI y OpenAPI.

## 3. Pregunta orientadora

**Que se necesita para crear, ejecutar y probar una API minima con FastAPI?**

Responder esta pregunta implica dominar el flujo inicial de cualquier proyecto del curso: crear entorno, instalar dependencias, escribir aplicacion, levantar servidor y probar endpoints.

## 4. Conceptos clave

### 4.1 Python — "El idioma base"

> **En espanol simple:** Python es el idioma en el que escribiremos nuestra API. Sin Python instalado, no podemos hacer nada. Es como tener un horno pero no electricidad.

FastAPI se construye sobre Python. Por eso, antes de instalar FastAPI, el estudiante debe verificar que Python este instalado correctamente.

**Verifica tu version de Python:**

```bash
python --version
```

**Si no funciona, prueba con:**

```bash
python3 --version
```

**Que deberias ver:**
```text
Python 3.10.12   # o cualquier version 3.10 o superior
```

**¿Que hacer si el comando no funciona?**

1. Descarga Python desde: https://www.python.org/downloads/
2. Durante la instalacion, MARCA la casilla "Add Python to PATH" (esto permite usar `python` desde la terminal).
3. Reinicia la terminal y prueba de nuevo.

> Si el comando no funciona, el problema no es FastAPI: todavia no hemos llegado al jefe final. Primero hay que instalar Python y configurarlo en el PATH.

---

### 4.2 Entorno virtual — "La caja de herramientas aislada"

> **En espanol simple:** un entorno virtual es una "caja" separada donde guardamos las librerias de cada proyecto. Asi el Proyecto A puede tener una version de FastAPI y el Proyecto B otra, sin pelearse entre si.

**Analogia:** Imagina que trabajas en dos proyectos distintos:
- Proyecto A: necesita martillo y clavos.
- Proyecto B: necesita taladro y tornillos.

Sin entornos virtuales, mezclarias todo en una sola caja de herramientas (caos). Con entornos virtuales, cada proyecto tiene su propia caja (orden).

Un entorno virtual es una carpeta aislada donde se instalan las dependencias de un proyecto.

Sirve para evitar que todos los proyectos compartan las mismas librerias globales.

Sin entornos virtuales, tarde o temprano aparece esta tragedia:

> "Profe, ayer funcionaba, hoy actualice una libreria y se rompio todo".

El entorno virtual reduce ese caos.

**Paso 1 — Crear el entorno:**

```bash
python -m venv .venv
```

**Explicacion:** `python -m venv` usa el modulo `venv` de Python para crear un entorno virtual. El `.venv` es el nombre de la carpeta que se creara (podria llamarse `env` o `entorno`, pero por convencion se usa `.venv`).

**Paso 2 — Activar el entorno:**

En Windows:
```bash
.venv\Scripts\activate
```

En macOS/Linux:
```bash
source .venv/bin/activate
```

> **¿Como saber si esta activo?** Cuando el entorno esta activo, aparece `(.venv)` al inicio de la linea de comandos:
> ```text
> (.venv) usuario@pc:~/proyecto$
> ```

**Paso 3 — Cuando termines, desactiva:**
```bash
deactivate
```

> **Regla de oro:** Cada vez que abras una terminal para trabajar en este proyecto, lo PRIMERO que haces es activar el entorno virtual. El 90% de los errores de instalacion se solucionan con esto.

---

### 4.3 Pip — "El mensajero que trae paquetes"

> **En espanol simple:** pip es como un mensajero (rappi, uber eats) que va y trae las librerias que necesitas desde internet a tu computadora.

`pip` es el gestor de paquetes de Python. Permite instalar FastAPI, Uvicorn y otras dependencias.

**Actualizar pip (recomendado antes de instalar algo):**
```bash
python -m pip install --upgrade pip
```

**Instalar FastAPI (con todos sus complementos):**
```bash
pip install "fastapi[standard]"
```

**Alternativa clasica (solo lo minimo necesario):**
```bash
pip install fastapi uvicorn
```

Para el curso, cualquiera de las dos opciones puede funcionar. La opcion `fastapi[standard]` instala componentes adicionales recomendados por FastAPI (como `httptools` y `websockets`).

> **Pro tip:** Si ves `pip install` funcionando con barras de progreso, estas del otro lado. Si ves errores rojos, probablemente no activaste el entorno virtual.

---

### 4.4 FastAPI — "La fabrica de APIs"

> **En espanol simple:** FastAPI es el framework que nos permite crear APIs de forma rapida y ordenada. Es como tener una "fabrica" donde declaras rutas y automaticamente obtienes validacion, documentacion y rendimiento.

FastAPI es el framework que permite declarar endpoints HTTP de manera clara, tipada y documentada.

**Ejemplo minimo — con explicacion linea por linea:**

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"mensaje": "Hola, FastAPI"}
```

| Linea | Explicacion en espanol simple |
|---|---|
| `from fastapi import FastAPI` | Trae la clase `FastAPI` desde la libreria `fastapi` para poder usarla |
| `app = FastAPI()` | Crea una "aplicacion" llamada `app`. Es el objeto principal de nuestra API |
| `@app.get("/")` | Esto es un **decorador**. Le dice a FastAPI: "Cuando alguien haga una solicitud GET a la raiz (`/`), ejecuta la funcion de abajo" |
| `def read_root():` | Define la funcion que se ejecutara cuando alguien visite `GET /` |
| `return {"mensaje": "Hola, FastAPI"}` | Devuelve un diccionario Python. FastAPI lo convierte automaticamente a **JSON** para la respuesta |

> **Magia que no ves:** FastAPI automaticamente:
> - Convierte tu diccionario Python a JSON ✅
> - Genera documentacion en `/docs` ✅
> - Valida tipos de datos ✅
> - Asigna el codigo HTTP 200 ✅

---

### 4.5 Uvicorn — "El motor que enciende la app"

> **En espanol simple:** FastAPI es la fabrica (crea la API). Uvicorn es el motor que la enciende y la mantiene funcionando. Sin Uvicorn, tu API existe pero no puede recibir visitas.

Uvicorn es un servidor ASGI. Sirve para ejecutar aplicaciones web asincronas en Python, como FastAPI.

**Comando para encender la API:**

```bash
uvicorn app.main:app --reload
```

**Explicacion visual de `app.main:app`:**

```text
uvicorn   app.main   :   app   --reload
   |          |          |        |
   |       archivo    variable  reinicio
comando  main.py en  que tiene  automatico
         carpeta     la        al cambiar
         app/        instancia  codigo
                     FastAPI
```

**En detalle:**

| Parte | Significado |
|---|---|
| `uvicorn` | El comando para ejecutar el servidor |
| `app.main` | El archivo `main.py` DENTRO de la carpeta `app/` |
| `:app` | La variable que contiene la instancia de FastAPI (llamada `app`) |
| `--reload` | Reinicia el servidor automaticamente cada vez que modificas el codigo. **Solo para desarrollo.** |

**Analogia completa de la ejecucion:**

```text
Tu computadora es un edificio
  ├── Python es la electricidad
  ├── FastAPI es la fabrica (app = FastAPI())
  ├── Uvicorn es el interruptor que enciende la fabrica
  ├── main.py son los planos de la fabrica
  └── --reload es como tener un vigilante que actualiza los planos
      cada vez que haces un cambio
```

## 5. Estructura minima del primer proyecto

> **En espanol simple:** asi se organizan los archivos de tu primer proyecto FastAPI. Es como los muebles de una casa: cada cosa en su lugar.

Estructura sugerida:

```text
primer-proyecto-fastapi/
  ├── app/
  │   ├── __init__.py    # "Tarjeta de presentacion" de la carpeta
  │   └── main.py        # El codigo principal de nuestra API
  ├── requirements.txt   # Lista de "compras": librerias que necesita el proyecto
  └── README.md          # Manual de instrucciones del proyecto
```

### 5.1 Carpeta `app/` — "El taller"

> Contiene el codigo fuente de la aplicacion. Todo lo que escribamos estara aqui.

### 5.2 Archivo `__init__.py` — "La tarjeta de presentacion"

> **En espanol simple:** este archivo vacio le dice a Python: "oye, esta carpeta es un paquete, puedes importar cosas de aqui". Sin el, `from app.main import ...` no funcionaria.

Permite que Python reconozca la carpeta como paquete.

Puede estar vacio. Su sola presencia es suficiente.

### 5.3 Archivo `main.py` — "El corazon"

> Es el punto de entrada de la aplicacion. Aqui escribiremos la instancia de FastAPI y nuestros primeros endpoints.

### 5.4 Archivo `requirements.txt` — "La lista del super"

> **En espanol simple:** este archivo lista todas las librerias que necesita tu proyecto. Cuando alguien mas clone tu proyecto, ejecutara `pip install -r requirements.txt` y tendra todo lo necesario.

Ejemplo:
```text
fastapi[standard]
```

O:
```text
fastapi
uvicorn
```

---

## 6. Primer endpoint — "Nuestra primera ruta"

> **En espanol simple:** un endpoint es una "direccion URL" que nuestra API entiende. Cuando alguien visita esa direccion, nuestra API responde con datos.

Archivo: `app/main.py`

```python
from fastapi import FastAPI

app = FastAPI(
    title="Primera API con FastAPI",
    description="Proyecto inicial para Desarrollo Web II",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"mensaje": "Hola, Desarrollo Web II"}
```

**Explicacion linea por linea:**

| Linea | Que hace | Traduccion |
|---|---|---|
| `from fastapi import FastAPI` | Importa la clase principal de FastAPI | "Trae la herramienta principal" |
| `app = FastAPI(...)` | Crea la aplicacion | "Crea la fabrica con nombre y version" |
| `@app.get("/")` | Decorador: asocia una URL con una funcion | "Cuando alguien visite `/`, ejecuta esto" |
| `def read_root():` | Define la funcion que se ejecutara | "La funcion que responde" |
| `return {"mensaje": "Hola"}` | Devuelve datos en formato diccionario | "La respuesta que enviara al navegador" |

**¿Que pasa cuando alguien visita `GET /`?**

```text
Navegador: "Oye servidor, dame lo que hay en /"
FastAPI:   "Claro, ejecuto la funcion read_root()"
           "Convierto el diccionario a JSON"
           "Respondo con 200 OK y el JSON"
Navegador: "Gracias, muestro esto en pantalla"
```

**Respuesta esperada en el navegador:**
```json
{
  "mensaje": "Hola, Desarrollo Web II"
}
```

---

## 7. Ejecutar el servidor — "Encender la API"

> **En espanol simple:** hasta ahora solo escribimos codigo. Para que alguien pueda visitar nuestra API, necesitamos "encenderla" con Uvicorn.

Desde la raiz del proyecto:

```bash
uvicorn app.main:app --reload
```

**Interpretacion del comando:**

```text
uvicorn   app.main  :  app   --reload
   |          |        |        |
  enciende  main.py   la      recarga
  el motor  dentro    variable automatica
            de app/   FastAPI  al cambiar
                              el codigo
```

**Salida esperada (aproximada):**
```text
Uvicorn running on http://127.0.0.1:8000
```

**Ahora abre tu navegador y visita:**
```text
http://127.0.0.1:8000/
```

Deberias ver:
```json
{
  "mensaje": "Hola, Desarrollo Web II"
}
```

> Si ves el JSON, **felicidades: tu primera API esta funcionando**. 🎉
>
> Si no funciona, bienvenido al desarrollo web real. Respire. Lea el error. No reinicie el computador como primer instinto ancestral. Vaya a la seccion de errores comunes (seccion 10) para solucionarlo.

---

## 8. Documentacion automatica — "El manual que se escribe solo"

> **En espanol simple:** FastAPI genera automaticamente una pagina web con la documentacion de tu API. Sin escribir una sola linea de documentacion, ya tienes Swagger UI, ReDoc y el esquema OpenAPI.

FastAPI genera documentacion automaticamente a partir de tu codigo.

**Swagger UI — Interfaz interactiva para probar endpoints:**
```text
http://127.0.0.1:8000/docs
```
Aqui puedes hacer clic en "Try it out" y ejecutar tus endpoints desde el navegador. Swagger UI muestra cada endpoint con su metodo HTTP, parametros, cuerpo de la peticion, codigos de respuesta, y hasta el modelo de datos esperado. Consulta `engine/swagger-anatomia.md` para una guia visual detallada de cada parte de la interfaz.

**ReDoc — Documentacion mas legible (solo lectura):**
```text
http://127.0.0.1:8000/redoc
```

**OpenAPI JSON — El esquema en formato JSON:**
```text
http://127.0.0.1:8000/openapi.json
```
Esto es lo que consumen herramientas externas para generar clientes de API.

> **¿Por que es importante?** Normalmente hay que escribir la documentacion a mano (y cuando el codigo cambia, la documentacion queda desactualizada). Con FastAPI, la documentacion SE GENERA SOLA a partir del codigo. Cambias el codigo, la documentacion se actualiza. Fin del problema.

---

## 9. Parametros de ruta y query — "Partes variables de la URL"

> **En espanol simple:** a veces queremos que nuestra API reciba datos desde la URL. Hay dos formas: **parametros de ruta** (parte de la direccion) y **parametros de query** (despues del signo `?`).

### 9.1 Parametro de ruta — "El nombre va en la direccion"

> **Analogia:** es como decir "dame el curso con ID 5": `/cursos/5`. El `5` es parte del camino.

```python
@app.get("/cursos/{curso_id}")
def obtener_curso(curso_id: int):
    return {"curso_id": curso_id}
```

**¿Que pasa cuando visitas `GET /cursos/10`?**

```text
FastAPI recibe /cursos/10
  → Saca el valor 10 de la URL
  → Lo convierte a entero (int)
  → Lo pasa a la funcion como curso_id=10
  → La funcion devuelve {"curso_id": 10}
```

**Respuesta:**
```json
{
  "curso_id": 10
}
```

**¿Que pasa si envias texto donde se espera un numero?**

Si visitas `GET /cursos/hola` (donde `hola` no es un numero), FastAPI responde con error 422:

```json
{
  "detail": [
    {
      "loc": ["path", "curso_id"],
      "msg": "Input should be a valid integer"
    }
  ]
}
```

> Traduccion: "Esperaba un numero entero en la ruta, pero recibiste texto." FastAPI valida los tipos automaticamente.

### 9.2 Parametro de query — "Los detalles van despues del ?"

> **Analogia:** es como los filtros de busqueda. `GET /cursos?activo=true` significa "dame los cursos que esten activos". El `activo=true` es un detalle extra, no parte del camino.

```python
@app.get("/cursos")
def listar_cursos(activo: bool = True):
    return {"activo": activo}
```

**Solicitud:**
```text
GET /cursos?activo=false
```

**Respuesta:**
```json
{
  "activo": false
}
```

**Diferencias clave entre parametro de ruta y query:**

| Aspecto | Parametro de ruta | Parametro de query |
|---|---|---|
| **Ejemplo URL** | `/cursos/5` | `/cursos?activo=true` |
| **Donde va** | En la ruta misma (`/cursos/{id}`) | Despues del `?` (`?clave=valor`) |
| **Obligatorio?** | Generalmente si | Generalmente no (tiene valor por defecto) |
| **Para que sirve** | Identificar un recurso especifico (un curso, un usuario) | Filtrar, ordenar, paginar (detalles) |
| **Tipo de dato** | Suele ser int o str | Puede ser bool, int, str, etc. |

**Ejemplo con ambos tipos de parametros:**

```python
@app.get("/cursos/{curso_id}")
def obtener_curso(curso_id: int, incluir_notas: bool = False):
    if incluir_notas:
        return {"curso_id": curso_id, "notas": [4.5, 5.0, 4.0]}
    return {"curso_id": curso_id}
```

- `GET /cursos/5` → solo ID
- `GET /cursos/5?incluir_notas=true` → ID + notas

## 10. Errores comunes y como resolverlos

> **En espanol simple:** aqui tienes los errores que casi todos los estudiantes cometen la primera vez. Si te pasa algo, revisa esta tabla antes de entrar en panico.

### 10.1 `command not found: uvicorn` (Uvicorn no encontrado)

**Causa mas probable (90% de los casos):** El entorno virtual no esta activo.

**Solucion rapida:**

En macOS/Linux:
```bash
source .venv/bin/activate
pip install fastapi uvicorn
```

En Windows:
```bash
.venv\Scripts\activate
pip install fastapi uvicorn
```

| Error tipico | Por que ocurre | Solucion |
|---|---|---|
| `command not found: uvicorn` | No activaste el entorno virtual | Activa el entorno con `source .venv/bin/activate` |
| `uvicorn: command not found` | Uvicorn no esta instalado | `pip install fastapi uvicorn` |
| Funciona en terminal A pero no en B | Cada terminal tiene su propio entorno activado | Activa el entorno en cada terminal nueva |

### 10.2 `ModuleNotFoundError: No module named 'app'` (Modulo app no encontrado)

**Causas posibles:**
- Ejecutaste el comando desde la carpeta equivocada.
- La estructura del proyecto esta mal.
- Falta `__init__.py` dentro de `app/`.

**Solucion:**

Asegurate de ejecutar DESDE la raiz del proyecto (donde esta la carpeta `app/`):

```bash
# ✅ CORRECTO: estas en la raiz del proyecto
~/proyectos/primer-proyecto-fastapi$ uvicorn app.main:app --reload

# ❌ INCORRECTO: estas dentro de app/
~/proyectos/primer-proyecto-fastapi/app$ uvicorn app.main:app --reload
```

### 10.3 Puerto ocupado

**Mensaje:** `Address already in use`

**¿Por que ocurre?** Ya hay otro programa usando el puerto 8000 (quizas otra instancia de Uvicorn que dejaste abierta).

**Soluciones:**

```bash
# Opcion 1: Usar otro puerto
uvicorn app.main:app --reload --port 8001

# Opcion 2: Matar el proceso anterior (Linux/macOS)
kill $(lsof -ti:8000)
```

### 10.4 Error de indentacion en Python

**Sintoma:** Python se queja con `IndentationError` y no ejecuta el codigo.

**¿Por que ocurre?** Python usa espacios para agrupar bloques de codigo. Un espacio de mas o de menos rompe todo.

**Solucion:**
- Usa SIEMPRE 4 espacios para indentar (no tabs).
- Configura tu editor para que convierta tabs a espacios.
- VS Code: `Ctrl+Shift+P` → "Convert Indentation to Spaces".

**Ejemplo de error:**
```python
@app.get("/")
def read_root():
return {"mensaje": "Hola"}  # ❌ Falta indentacion
```

**Ejemplo correcto:**
```python
@app.get("/")
def read_root():
    return {"mensaje": "Hola"}  # ✅ 4 espacios
```

### 10.5 Checklist rapido si algo no funciona

Si tu API no responde, revisa esto en orden:

- [ ] ¿El entorno virtual esta activo? (debes ver `(.venv)` en la terminal)
- [ ] ¿Instalaste las dependencias? (`pip install fastapi uvicorn`)
- [ ] ¿Ejecutas desde la raiz del proyecto? (donde esta la carpeta `app/`)
- [ ] ¿El servidor esta corriendo? (debes ver "Uvicorn running on ...")
- [ ] ¿Usaste `http://127.0.0.1:8000` y no `https://`?
- [ ] ¿El codigo no tiene errores de indentacion?

---

## 11. Actividad central de clase — Taller guiado

### 11.1 Pasos del taller

> **Instrucciones:** sigue estos pasos en orden. Si te atascas, revisa la seccion de errores y luego pide ayuda.

El estudiante debe:

| Paso | Que hacer | Verificacion |
|---|---|---|
| 1 | Crear carpeta del proyecto (`mkdir mi-primera-api`) | La carpeta existe |
| 2 | Crear entorno virtual (`python -m venv .venv`) | Aparece carpeta `.venv` |
| 3 | Activar entorno (`source .venv/bin/activate`) | Ves `(.venv)` en la terminal |
| 4 | Instalar dependencias (`pip install fastapi uvicorn`) | Sin errores rojos |
| 5 | Crear estructura (`app/`, `__init__.py`, `main.py`) | Los archivos existen |
| 6 | Definir endpoint raiz (`GET /`) | Responde JSON |
| 7 | Definir endpoint `/saludo/{nombre}` | Responde "Hola, [nombre]" |
| 8 | Definir endpoint `/estado` | Responde estado del servidor |
| 9 | Ejecutar servidor (`uvicorn app.main:app --reload`) | Ves "Uvicorn running" |
| 10 | Probar `/docs` | Ves la interfaz Swagger |

### 11.2 Codigo de los endpoints sugeridos

Agrega estos endpoints a tu `app/main.py`:

```python
@app.get("/estado")
def obtener_estado():
    return {"estado": "ok", "framework": "FastAPI"}


@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}
```

**Explicacion de los nuevos endpoints:**

| Endpoint | Que hace | Ejemplo |
|---|---|---|
| `GET /estado` | Devuelve el estado de la API | `GET /estado` → `{"estado": "ok", ...}` |
| `GET /saludo/{nombre}` | Saluda a la persona cuyo nombre va en la ruta | `GET /saludo/Ana` → `{"mensaje": "Hola, Ana"}` |

> **Nota:** `{nombre}` es un parametro de ruta. El valor que pongas ahi se pasa a la funcion como variable `nombre`.

---

## 12. Producto esperado

**Evidencia sugerida:** repositorio o carpeta de proyecto base funcionando.

### Checklist de entregable:

- [ ] **Estructura del proyecto** (`app/main.py`, `app/__init__.py`)
- [ ] **Entorno virtual configurado** (`.venv/` existe, no lo subas al repo)
- [ ] **`requirements.txt`** generado con `pip freeze > requirements.txt`
- [ ] **`app/main.py`** con minimo 3 endpoints funcionando
- [ ] **Captura de pantalla** de `/docs` mostrando los endpoints
- [ ] **README.md** con instrucciones de instalacion y ejecucion

---

## 13. Cierre conceptual

### ¿Que aprendimos hoy?

Hoy dimos el salto de la teoria a la practica. Creamos nuestra primera API FastAPI funcional.

1. **Python** es el lenguaje base. Sin el, nada funciona.
2. **Entorno virtual** aísla las dependencias de cada proyecto (adiós a "es que en mi maquina si funciona").
3. **Pip** trae las librerias que necesitamos desde internet.
4. **FastAPI** es el framework que nos permite declarar rutas y obtener validacion + documentacion automatica.
5. **Uvicorn** es el servidor que ejecuta nuestra API.
6. **Los parametros de ruta y query** permiten que nuestra API reciba datos desde la URL.
7. **La documentacion automatica** en `/docs` y `/redoc` es una superventaja de FastAPI.

Al finalizar esta clase, el estudiante debe poder crear y ejecutar una API minima con FastAPI. Tambien debe comprender que el entorno de desarrollo es parte del proyecto: no basta con escribir codigo si no se sabe instalar, aislar dependencias, levantar servidor y probar rutas.

FastAPI permite avanzar rapido, pero exige disciplina tecnica desde el inicio. Una API que corre solo en la maquina de una persona no es un proyecto: es una leyenda urbana con `requirements.txt` incompleto.

---

## 14. Trabajo independiente (6 horas sugeridas)

### 14.1 Completar el proyecto base (2 horas)

- Termina los 3 endpoints minimos (raiz, saludo, estado).
- Agrega **2 endpoints adicionales** que se te ocurran (ej: `GET /fecha`, `GET /version`, `GET /materias`).
- Crea un `README.md` con:

```markdown
# Nombre del proyecto
Breve descripcion.

## Requisitos
- Python 3.10+
- Entorno virtual

## Instalacion
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion
```bash
uvicorn app.main:app --reload
```

## Endpoints
- `GET /`
- `GET /estado`
- `GET /saludo/{nombre}`
```

### 14.2 Explorar la documentacion (1 hora)

- Abre `/docs` y prueba TODOS los endpoints desde Swagger UI.
- Abre `/redoc` y compara los estilos de documentacion.
- Abre `/openapi.json` y revisa el esquema generado.

### 14.3 Preparar preguntas (1 hora)

Escribe 3 preguntas que tengas sobre estructura profesional de proyecto para la Clase 05.
Ejemplos: "¿Como organizo muchos endpoints?", "¿Cuando debo usar routers?", "¿Como agrego una base de datos?"

### 14.4 Desafio extra (2 horas, opcional)

Agrega un endpoint que reciba DOS parametros (uno de ruta y uno de query):

```python
@app.get("/usuarios/{user_id}")
def obtener_usuario(user_id: int, incluir_notas: bool = False):
    # Tu codigo aqui
    pass
```

Prueba:
- `GET /usuarios/1` → solo ID
- `GET /usuarios/1?incluir_notas=true` → ID + notas

## 15. Bibliografia y referencias utiles

- FastAPI. (s. f.). *First Steps*. https://fastapi.tiangolo.com/tutorial/first-steps/
- FastAPI. (s. f.). *Path Parameters*. https://fastapi.tiangolo.com/tutorial/path-params/
- FastAPI. (s. f.). *Query Parameters*. https://fastapi.tiangolo.com/tutorial/query-params/
- Uvicorn. (s. f.). *Uvicorn Documentation*. https://www.uvicorn.org/
- Python Packaging Authority. (s. f.). *Installing packages using pip and virtual environments*. https://packaging.python.org/
