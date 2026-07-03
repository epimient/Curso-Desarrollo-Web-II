# Ejemplo guiado - Consumir una API publica con Python

## Objetivo

Consumir una API publica usando Python, inspeccionar el codigo de estado y leer datos en formato JSON.

Al final de este ejemplo, habras hecho que tu computadora hable con los servidores de GitHub y obtengas informacion real. Como si tu programa hiciera una llamada telefonica a otro programa y recibiera una respuesta.

---

## Paso 1. Crear un entorno de trabajo

Primero, necesitamos un lugar limpio para trabajar, sin mezclar librerias con otros proyectos.

```bash
mkdir api-demo
cd api-demo
```

**Explicacion:** `mkdir api-demo` crea una carpeta llamada `api-demo`. `cd api-demo` entra en esa carpeta.

Crear entorno virtual:

```bash
python -m venv .venv
```

**Explicacion:** Un entorno virtual es como una "caja" aislada donde instalaremos solo las librerias que necesita este proyecto. Asi no ensuciamos el Python global de tu computadora.

Activar entorno:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

**Explicacion:** Al activar el entorno, ves algo como `(.venv)` al inicio de la linea de comandos. Eso significa que estas dentro de tu "caja" aislada.

---

## Paso 2. Instalar dependencia

```bash
pip install requests
```

**Explicacion:** `pip` es el gestor de paquetes de Python. `requests` es una libreria que permite hacer solicitudes HTTP desde Python de forma sencilla. Sin ella, tendriamos que escribir mucho mas codigo.

**Verifica que se instalo correctamente:** Si ves un mensaje como `Successfully installed requests-2.x.x`, todo bien. Si ves errores, verifica que tengas internet y que el entorno virtual este activado.

---

## Paso 3. Crear archivo principal

Crear un archivo llamado `main.py` dentro de la carpeta `api-demo`. Puedes usar cualquier editor de texto (VS Code, Sublime, Notepad++, o incluso el bloc de notas).

```python
import requests

url = "https://api.github.com/repos/tiangolo/fastapi"

response = requests.get(url)

print("Codigo de estado:", response.status_code)
```

### Explicacion linea por linea:

| Linea | Que hace |
|---|---|
| `import requests` | Trae la libreria `requests` para poder usarla |
| `url = "..."` | Guarda la direccion del recurso que queremos consultar |
| `response = requests.get(url)` | Envia una solicitud GET a GitHub y guarda la respuesta |
| `print(...)` | Muestra en pantalla el codigo de estado HTTP |

Ejecutar:

```bash
python main.py
```

**Salida esperada:** `Codigo de estado: 200`

Si ves `200`, felicidades. Acabas de hacer tu primera solicitud HTTP desde Python.

---

## Paso 4. Interpretar el codigo de estado

El codigo de estado es como el "semafaro" de la comunicacion:

| Codigo | Significado | Traduccion |
|---|---|---|
| **200** | OK - Todo funciono | "Si, aqui tienes lo que pediste" |
| **404** | Not Found - No existe | "Eso que buscas no esta aqui" |
| **403** | Forbidden - Prohibido | "No tienes permiso para esto" |
| **500** | Internal Server Error | "El servidor se rompio" |

Si la respuesta es `200`, la solicitud fue exitosa. 

Si aparece `404`, probablemente la URL esta mal escrita o el recurso no existe.

Si aparece `403`, puede haber restricciones por permisos o limite de solicitudes.

> El codigo de estado es una senal rapida del resultado de la conversacion entre cliente y servidor. Es como el indicador de mision completada, pero menos dramatico.

---

## Paso 5. Leer el JSON

Ahora vamos a extraer informacion de la respuesta. Actualiza tu `main.py`:

```python
import requests

url = "https://api.github.com/repos/tiangolo/fastapi"

response = requests.get(url)
data = response.json()

print("Nombre:", data["name"])
print("Descripcion:", data["description"])
print("Estrellas:", data["stargazers_count"])
print("Lenguaje:", data["language"])
```

### Explicacion de las nuevas lineas:

| Linea | Que hace |
|---|---|
| `data = response.json()` | Convierte la respuesta JSON a un diccionario de Python |
| `data["name"]` | Obtiene el valor de la clave "name" del diccionario |
| `data["stargazers_count"]` | Obtiene cuantas estrellas tiene el repositorio |

**Ejecuta de nuevo:** `python main.py`

**Salida esperada (similar a):**
```
Nombre: fastapi
Descripcion: FastAPI framework, alto rendimiento, facil de aprender...
Estrellas: 80000
Lenguaje: Python
```

**¿Que acaba de pasar?** Tu programa:
1. Pregunto a GitHub: "dame info del repo fastapi"
2. GitHub respondio con un JSON enorme lleno de datos
3. Tu programa extrajo solo 4 datos especificos
4. Los mostro en pantalla

---

## Paso 6. Agregar control basico de errores

No siempre las solicitudes salen bien. Agreguemos un "plan B" por si algo falla:

```python
import requests

url = "https://api.github.com/repos/tiangolo/fastapi"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Nombre:", data["name"])
    print("Descripcion:", data["description"])
    print("Estrellas:", data["stargazers_count"])
else:
    print("Error al consultar la API")
    print("Codigo:", response.status_code)
```

### Explicacion:

- **`if response.status_code == 200:`** Solo ejecuta el bloque si la respuesta fue exitosa.
- **`else:`** Si el codigo NO es 200, ejecuta el otro bloque.
- Esto evita que el programa intente leer datos de una respuesta que vino con error.

> **Analogia:** Es como llamar a alguien por telefono. Si contesta (200), hablas. Si no contesta (404/500), dejas un mensaje de error en lugar de quedarte en silencio esperando.

---

## Paso 7. ¿Que pasaria si...?

**Escenario 1: La URL no existe**
```python
url = "https://api.github.com/repos/esto-no-existe"
```
**Resultado:** Codigo 404. Tu programa mostrara "Error al consultar la API. Codigo: 404".

**Escenario 2: La API cambia la estructura**
Si GitHub decidiera cambiar `"name"` por `"title"`, tu programa fallaria con `KeyError: 'name'`. Por eso las APIs tienen **versiones** y documentacion.

**Escenario 3: Sin internet**
Si no hay conexion, `requests.get()` lanzara una excepcion y el programa se rompera. Para eso existe el bloque `try/except` (lo veremos mas adelante).

---

## Paso 8. Discusion docente

Preguntas para orientar la conversacion:

1. **Cual fue el cliente en este ejemplo?** (Tu script de Python)
2. **Cual fue el servidor?** (Los servidores de GitHub)
3. **Que metodo HTTP se uso?** (GET - solo consultamos, no creamos nada)
4. **Que datos devolvio la API?** (JSON con info del repositorio)
5. **Que pasaria si la API cambia la estructura de la respuesta?** (Tu codigo se romperia porque busca claves que ya no existen)
6. **Como se relaciona este ejercicio con lo que construiremos despues en FastAPI?** (Aqui fuimos cliente. Despues seremos servidor y construiremos nuestras propias APIs)

---

## Resumen de conceptos aplicados

| Concepto | Como se aplico aqui |
|---|---|
| **Cliente** | Tu script de Python |
| **Servidor** | Los servidores de GitHub |
| **HTTP** | Protocolo usado para la comunicacion |
| **GET** | Metodo HTTP para consultar datos |
| **URL** | `https://api.github.com/repos/tiangolo/fastapi` |
| **Codigo 200** | Respuesta exitosa |
| **JSON** | Formato de los datos recibidos |
| **API** | La interfaz de GitHub que permite consultar repositorios |

---

## Cierre

Este ejemplo muestra el consumo de una API existente desde el lado del **cliente**. En las siguientes clases, el estudiante pasara al otro lado del espejo: construira sus propias APIs con FastAPI para que otros clientes puedan consumirlas. Pasaremos de ser el que pregunta a ser el que responde.
