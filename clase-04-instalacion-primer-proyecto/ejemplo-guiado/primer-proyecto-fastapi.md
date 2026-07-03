# Ejemplo guiado — Primer proyecto FastAPI

## Objetivo

Crear, ejecutar y probar una API minima con FastAPI desde cero.

Al finalizar este ejemplo, tendras:
- Un proyecto FastAPI funcionando en tu computadora
- 4 endpoints operativos
- Documentacion automatica en Swagger UI
- Un `requirements.txt` con las dependencias

---

## Paso 1. Crear carpeta del proyecto

Abrimos una terminal y creamos la carpeta donde vivira nuestro proyecto:

```bash
mkdir primer-proyecto-fastapi
cd primer-proyecto-fastapi
```

**Explicacion:** `mkdir` crea una carpeta (make directory). `cd` entra en ella (change directory).

---

## Paso 2. Crear entorno virtual

> **¿Por que?** Para aislar las librerias de este proyecto de las de otros proyectos.

```bash
python -m venv .venv
```

**Explicacion:** Esto crea una carpeta oculta llamada `.venv` que contendra una copia limpia de Python donde instalaremos solo las librerias que necesita este proyecto.

**Activar el entorno (paso que el 90% de los estudiantes olvida):**

En macOS/Linux:
```bash
source .venv/bin/activate
```

En Windows:
```bash
.venv\Scripts\activate
```

**¿Como saber si esta activo?** Debes ver `(.venv)` al inicio de la linea de comandos:
```text
(.venv) usuario@pc:~/primer-proyecto-fastapi$
```

> **Si no ves `(.venv)`**, el entorno NO esta activo. Ningun comando de instalacion funcionara correctamente.

---

## Paso 3. Instalar dependencias

Con el entorno activo, instalamos FastAPI y Uvicorn:

```bash
pip install "fastapi[standard]"
```

**Alternativa (si la de arriba falla):**
```bash
pip install fastapi uvicorn
```

**Salida esperada:** Veras barras de progreso y un mensaje como:
```text
Successfully installed fastapi-0.x.x uvicorn-0.x.x ...
```

> **Pregunta frecuente:** ¿instalo una vez o cada vez que abro el proyecto? Una vez. Mientras el entorno virtual este activo, las librerias estaran disponibles.

---

## Paso 4. Crear estructura de archivos

Dentro de la carpeta del proyecto, creamos la estructura de carpetas y archivos:

```bash
mkdir app
touch app/__init__.py
touch app/main.py
```

**En Windows (si `touch` no existe):**
```powershell
New-Item app\__init__.py
New-Item app\main.py
```

**Resultado esperado:**
```text
primer-proyecto-fastapi/
  ├── .venv/           ← Se creo en el paso 2
  ├── app/
  │   ├── __init__.py  ← Vacio, marca la carpeta como paquete
  │   └── main.py      ← Aqui escribiremos el codigo
  └── ... (otros archivos)
```

---

## Paso 5. Escribir la aplicacion (con explicacion)

Abre `app/main.py` en tu editor de codigo (VS Code, Sublime, etc.) y escribe:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Primera API con FastAPI",
    description="Proyecto inicial para Desarrollo Web II",
    version="0.1.0",
)


@app.get("/")
def read_root():
    """Endpoint raiz: responde con un mensaje de bienvenida."""
    return {"mensaje": "Hola, Desarrollo Web II"}


@app.get("/estado")
def obtener_estado():
    """Endpoint de estado: indica que la API esta funcionando."""
    return {"estado": "ok", "framework": "FastAPI"}


@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    """
    Endpoint con parametro de ruta.
    Ejemplo: GET /saludo/Ana → {"mensaje": "Hola, Ana"}
    """
    return {"mensaje": f"Hola, {nombre}"}


@app.get("/cursos")
def listar_cursos(activo: bool = True):
    """
    Endpoint con parametro de query.
    Ejemplo: GET /cursos?activo=false
    """
    return {
        "activo": activo,
        "cursos": [
            {"id": 1, "nombre": "Desarrollo Web II", "activo": True},
            {"id": 2, "nombre": "Bases de Datos", "activo": False},
        ],
    }
```

**Explicacion de cada endpoint:**

| Endpoint | Metodo | Parametros | Que hace |
|---|---|---|---|
| `/` | GET | Ninguno | Responde con mensaje de bienvenida |
| `/estado` | GET | Ninguno | Indica que la API funciona |
| `/saludo/{nombre}` | GET | `nombre` (en la ruta) | Saluda a la persona |
| `/cursos` | GET | `activo` (query, opcional) | Lista cursos, puede filtrar |

---

## Paso 6. Ejecutar el servidor

Desde la raiz del proyecto (donde esta la carpeta `app/`):

```bash
uvicorn app.main:app --reload
```

**Interpretacion del comando:**
```text
uvicorn  app.main     :  app      --reload
  │        │             │          │
  │    main.py dentro    variable  recarga automatica
  │    de carpeta app/   FastAPI   al cambiar codigo
  │
  comando del servidor
```

**Salida esperada:**
```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     (Press CTRL+C to quit)
```

> **No cierres esta terminal.** Dejala abierta mientras trabajas. Para detener el servidor, presiona `Ctrl+C`.

---

## Paso 7. Probar los endpoints

Abre tu navegador y visita estas URLs:

| URL | Que deberias ver |
|---|---|
| `http://127.0.0.1:8000/` | `{"mensaje": "Hola, Desarrollo Web II"}` |
| `http://127.0.0.1:8000/estado` | `{"estado": "ok", "framework": "FastAPI"}` |
| `http://127.0.0.1:8000/saludo/Ana` | `{"mensaje": "Hola, Ana"}` |
| `http://127.0.0.1:8000/cursos` | Lista de cursos filtrados por activo=true |
| `http://127.0.0.1:8000/cursos?activo=false` | Lista de cursos filtrados por activo=false |

---

## Paso 8. Revisar la documentacion automatica

Sin escribir una sola linea de documentacion, FastAPI genera:

**Swagger UI — Documentacion interactiva:**
```text
http://127.0.0.1:8000/docs
```
Aqui puedes:
- Ver todos los endpoints documentados
- Hacer clic en "Try it out" para probarlos
- Ver los esquemas de respuesta

**ReDoc — Documentacion de solo lectura (mas limpia):**
```text
http://127.0.0.1:8000/redoc
```

**OpenAPI JSON — Esquema en formato JSON:**
```text
http://127.0.0.1:8000/openapi.json
```
Esto lo usan herramientas externas para generar clientes de API.

---

## Paso 9. Crear archivo requirements.txt

Con el entorno activo, ejecuta:

```bash
pip freeze > requirements.txt
```

**Explicacion:** `pip freeze` lista todas las librerias instaladas con sus versiones. `> requirements.txt` guarda esa lista en un archivo.

**Contenido esperado de `requirements.txt`:**
```text
fastapi==0.x.x
pydantic==2.x.x
uvicorn==0.x.x
```

> **Para que sirve:** Si alguien mas quiere ejecutar tu proyecto, solo necesita:
> ```bash
> pip install -r requirements.txt
> ```
> Y tendra exactamente las mismas versiones de librerias que tu.

---

## Paso 10. ¿Que pasaria si...?

**Escenario 1: Olvidaste activar el entorno**
```bash
# ❌ Esto falla si el entorno no esta activo
pip install fastapi
# → ERROR: no se encuentra el comando pip, o instala en otro lado
```
**Solucion:** Activa el entorno primero.

**Escenario 2: Ejecutaste desde la carpeta equivocada**
```bash
# ❌ Estas dentro de app/
~/proyecto/app$ uvicorn app.main:app --reload
# → ModuleNotFoundError: No module named 'app'
```
**Solucion:** Ejecuta desde la raiz del proyecto (donde esta la carpeta `app/`).

**Escenario 3: El puerto 8000 ya esta ocupado**
```bash
# ❌ Address already in use
uvicorn app.main:app --reload
```
**Solucion:** Usa otro puerto:
```bash
uvicorn app.main:app --reload --port 8001
```

**Escenario 4: Cambiaste el codigo pero el servidor no se actualiza**
- Si usaste `--reload`, el servidor deberia actualizarse solo.
- Si no ves los cambios, revisa que guardaste el archivo (Ctrl+S).
- Si aun asi no funciona, deten el servidor (Ctrl+C) y vuelve a ejecutarlo.

---

## Paso 11. Analisis final

Responde estas preguntas para verificar tu comprension:

1. **¿Que archivo contiene la instancia de FastAPI?**
   - `app/main.py`. Ahi creamos `app = FastAPI(...)`.

2. **¿Que funcion cumple Uvicorn?**
   - Ejecuta la aplicacion FastAPI como un servidor web listo para recibir solicitudes.

3. **¿Que endpoint usa parametro de ruta?**
   - `GET /saludo/{nombre}`. El `{nombre}` se reemplaza por un valor real.

4. **¿Que endpoint usa parametro de query?**
   - `GET /cursos?activo=true`. El `activo` va despues del `?`.

5. **¿Que informacion genera automaticamente `/docs`?**
   - La documentacion interactiva de todos los endpoints, con sus parametros, tipos de datos y respuestas esperadas.

---

## Resumen de comandos utiles

| Comando | Que hace |
|---|---|
| `python -m venv .venv` | Crea entorno virtual |
| `source .venv/bin/activate` | Activa entorno (Linux/Mac) |
| `.venv\Scripts\activate` | Activa entorno (Windows) |
| `pip install fastapi uvicorn` | Instala dependencias |
| `uvicorn app.main:app --reload` | Ejecuta servidor |
| `pip freeze > requirements.txt` | Genera lista de dependencias |
| `deactivate` | Desactiva el entorno virtual |

---

## Cierre

Este primer proyecto sera la base para las siguientes clases. A partir de aqui se agregaran estructura profesional, routers, schemas, servicios, validacion, persistencia, pruebas y seguridad.

**Tu primera API FastAPI esta funcionando. Bien hecho. 🎉**
