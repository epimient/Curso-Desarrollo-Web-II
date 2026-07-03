# Ejercicios - Clase 04

> **Nota:** Estos ejercicios te guian paso a paso para crear tu primera API FastAPI. El ejercicio 0 es de calentamiento para asegurarnos de que los conceptos basicos estan claros.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las frases con las palabras del recuadro:

> **Palabras:** ENTORNO VIRTUAL | PIP | UVICORN | GET | DECORADOR | JSON | 8000 | DOCS

1. Un _________ es una carpeta aislada donde se instalan las dependencias de un proyecto.
2. _________ es el gestor de paquetes de Python que instala librerias.
3. _________ es el servidor que ejecuta nuestra aplicacion FastAPI.
4. El metodo HTTP _________ se usa para obtener informacion.
5. El símbolo `@app.get("/")` se llama _________ y asocia una URL con una funcion.
6. FastAPI convierte automaticamente los diccionarios Python a formato _________.
7. Por defecto, Uvicorn ejecuta la API en el puerto _________.
8. La documentacion interactiva de FastAPI aparece en la ruta _________.

---

## Ejercicio 1. Verificacion del entorno

Ejecute y registre la salida de los siguientes comandos:

```bash
python --version
pip --version
```

Despues responda:

1. **¿Que version de Python tiene instalada?**
   - Ejemplo: `Python 3.10.12`

2. **¿Que version de pip aparece?**
   - Ejemplo: `pip 24.0`

3. **¿El comando funciona igual en su sistema con `python3`?**
   - En Linux/macOS a veces necesitas `python3` en lugar de `python`.

---

## Ejercicio 2. Crear entorno virtual

Crea un proyecto llamado `mi-primera-api` y dentro:

1. Crea un entorno virtual (`.venv`).
2. Activa el entorno (debes ver `(.venv)` en la terminal).
3. Instala FastAPI y Uvicorn.
4. Genera un archivo `requirements.txt`:

```bash
pip freeze > requirements.txt
```

**Verificacion:** El archivo `requirements.txt` debe contener al menos `fastapi` y `uvicorn`.

---

## Ejercicio 3. Primer endpoint

Crea la estructura de carpetas:
```bash
mkdir app
touch app/__init__.py app/main.py
```

En `app/main.py`, escribe un endpoint raiz:

```python
from fastapi import FastAPI

app = FastAPI(title="Mi primera API")


@app.get("/")
def read_root():
    return {"mensaje": "Mi primera API con FastAPI"}
```

Ejecuta el servidor:
```bash
uvicorn app.main:app --reload
```

**Verificacion:** Abre `http://127.0.0.1:8000/` y debe mostrar:
```json
{"mensaje": "Mi primera API con FastAPI"}
```

---

## Ejercicio 4. Endpoint con parametro de ruta

Agrega este endpoint a `app/main.py`:

```python
@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}
```

**Prueba estas URLs:**
| URL | Respuesta esperada |
|---|---|
| `GET /saludo/Ana` | `{"mensaje": "Hola, Ana"}` |
| `GET /saludo/Carlos` | `{"mensaje": "Hola, Carlos"}` |

**Pregunta:** ¿Que pasa si visitas `GET /saludo/` sin nombre? ¿Y si visitas `GET /saludo/123`?

---

## Ejercicio 5. Endpoint con parametro de query

Agrega este endpoint:

```python
@app.get("/cursos")
def listar_cursos(activo: bool = True):
    return {"mensaje": f"Mostrando cursos activos={activo}"}
```

**Prueba estas URLs:**
| URL | Respuesta esperada |
|---|---|
| `GET /cursos` | `{"mensaje": "Mostrando cursos activos=True"}` |
| `GET /cursos?activo=false` | `{"mensaje": "Mostrando cursos activos=False"}` |

**Pregunta:** ¿Que pasa si no envias el parametro `activo`? ¿Por que?

> **Ayuda:** Revisa el parametro `= True` en la definicion de la funcion. Eso es un **valor por defecto**.

---

## Ejercicio 6. Exploracion de documentacion

Con el servidor corriendo, abre en tu navegador:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

Responde:

1. **¿Que diferencias ves entre `/docs` y `/redoc`?**
   - Pista: uno permite probar endpoints, el otro es solo lectura.

2. **¿Que informacion aparece en `/openapi.json`?**
   - Pista: es un JSON enorme con todas las rutas, parametros y tipos.

3. **¿Como ayuda esta documentacion a un equipo frontend?**
   - Pista: ellos necesitan saber que rutas existen y que datos enviar.

---

## Ejercicio 7. README tecnico

Crea un archivo `README.md` en la raiz de tu proyecto que incluya:

```markdown
# [Nombre del proyecto]

[Breve descripcion de tu API]

## Requisitos
- Python 3.10+
- Entorno virtual

## Instalacion
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt

## Ejecucion
uvicorn app.main:app --reload

## Endpoints
- GET / → [descripcion]
- GET /saludo/{nombre} → [descripcion]
- GET /cursos → [descripcion]
```

**Completa los datos con la informacion de tu proyecto.**

---

## Desafio extra (opcional)

Crea un endpoint que reciba DOS parametros:

```python
@app.get("/usuarios/{user_id}")
def obtener_usuario(user_id: int, incluir_notas: bool = False):
    if incluir_notas:
        return {"user_id": user_id, "notas": [4.5, 5.0, 4.0]}
    return {"user_id": user_id}
```

**Prueba:**
- `GET /usuarios/1` → solo ID
- `GET /usuarios/1?incluir_notas=true` → ID + notas
- `GET /usuarios/hola` → ? (¿que crees que pasara?)
