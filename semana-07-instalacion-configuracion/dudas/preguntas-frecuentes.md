# Dudas frecuentes - Clase 04

> Aqui encontraras las preguntas que todo principiante se hace al crear su primer proyecto FastAPI. No tengas vergüenza: el 90% de estos errores los hemos tenido todos.

---

## 1. ¿Que version de Python debo usar?

**Respuesta corta:** Python 3.10 o superior.

**Respuesta larga:** FastAPI aprovecha el tipado moderno de Python. Las versiones 3.8+ funcionan, pero 3.10+ es mejor porque tiene sintaxis como `list[Curso]` en lugar de `List[Curso]`.

**Para verificar tu version:**
```bash
python --version
```

---

## 2. ¿Para que sirve el entorno virtual?

**Respuesta corta:** Para aislar las librerias de cada proyecto.

**Respuesta larga:** Sin entorno virtual, todas las librerias se instalan "globalmente" en tu computadora. Si el Proyecto A necesita FastAPI 0.100 y el Proyecto B necesita FastAPI 0.110, se rompe uno de los dos.

Con entorno virtual, cada proyecto tiene su propia caja aislada con las versiones que necesita.

**Analogia:** Es como tener una mochila distinta para cada clase del colegio, en lugar de mezclar todos los libros en una sola mochila gigante.

---

## 3. FastAPI y Uvicorn son lo mismo?

**Respuesta corta:** No. Son dos cosas distintas que trabajan juntas.

**Respuesta larga:**
- **FastAPI** es el framework con el que escribes tu API (las rutas, la logica, los modelos).
- **Uvicorn** es el servidor que ejecuta tu API (el que "enciende" la aplicacion).

**Analogia:** FastAPI es el motor de un auto. Uvicorn es la llave que lo enciende y el volante que lo mantiene funcionando. Necesitas ambos para que el auto se mueva.

---

## 4. ¿Que significa `app.main:app`?

**Respuesta corta:** "Busca el archivo `main.py` dentro de `app/` y usa la variable `app` que contiene FastAPI."

**Respuesta larga:** El comando `uvicorn app.main:app --reload` se descompone asi:

| Parte | Significado |
|---|---|
| `app.main` | El archivo `app/main.py` |
| `:` | Separador entre archivo y variable |
| `app` | La variable dentro de `main.py` que tiene `= FastAPI()` |
| `--reload` | Recarga automatica al cambiar codigo |

**Visualmente:**
```
uvicorn   app.main : app   --reload
              │        │
        main.py DENTRO  variable llamada 'app'
        de carpeta app/  que tiene FastAPI()
```

---

## 5. ¿Por que aparece `/docs` automaticamente?

**Respuesta corta:** Porque FastAPI genera documentacion OpenAPI automaticamente a partir de tu codigo.

**Respuesta larga:** Solo por definir rutas, tipos de parametros y modelos de respuesta, FastAPI construye automaticamente:
- **Swagger UI** (`/docs`): interfaz interactiva para probar endpoints
- **ReDoc** (`/redoc`): documentacion de solo lectura mas elegante
- **OpenAPI JSON** (`/openapi.json`): esquema en JSON para herramientas externas

**Sin escribir una sola linea de documentacion.** En otros frameworks (Django, Flask) necesitas librerias adicionales para lograr lo mismo.

---

## 6. ¿Que hago si `uvicorn` no se reconoce como comando?

**Respuesta corta:** Activa el entorno virtual primero.

**Respuesta larga:** El 80% de las veces que `uvicorn` no funciona es porque el entorno virtual no esta activo.

```bash
# Verifica que (.venv) aparece en tu terminal
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Luego prueba
uvicorn app.main:app --reload
```

Si aun asi falla, reinstala:
```bash
pip install fastapi uvicorn
```

---

## 7. ¿Debo subir la carpeta `.venv` al repositorio?

**Respuesta corta:** NO. Nunca.

**Respuesta larga:** La carpeta `.venv` es personal de cada computadora. Puede pesar cientos de megas. En lugar de compartir `.venv`, compartes `requirements.txt` (que pesa 1 KB) y cada persona reconstruye su entorno con `pip install -r requirements.txt`.

**Crea un archivo `.gitignore`** y agrega esta linea:
```text
.venv/
```

---

## 8. ¿Por que FastAPI devuelve error 422?

**Respuesta corta:** Porque enviaste datos que no cumplen con el tipo o formato esperado.

**Respuesta larga:** FastAPI valida automaticamente los tipos de datos. Si tu endpoint espera un `int` y recibes texto, FastAPI responde con 422 y los detalles del error.

**Ejemplo:**
```python
@app.get("/cursos/{curso_id}")
def obtener_curso(curso_id: int):
    ...
```

Si visitas `GET /cursos/hola`, FastAPI responde:
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

**Traduccion:** "Esperaba un numero entero en `curso_id`, pero recibiste 'hola'."

---

## 9. ¿Que diferencia hay entre `/docs` y `/redoc`?

| Aspecto | Swagger UI (`/docs`) | ReDoc (`/redoc`) |
|---|---|---|
| **Propósito** | Probar endpoints interactivamente | Leer documentacion de forma limpia |
| **¿Puedo ejecutar endpoints?** | Si ("Try it out") | No (solo lectura) |
| **Diseño** | Interfaz con botones y formularios | Documento estatico estilo manual |
| **¿Cuando usarlo?** | Desarrollo y pruebas | Compartir con otros equipos |

Ambas son generadas automaticamente por FastAPI desde el mismo codigo.

---

## 10. ¿Que significa el `--reload` en el comando de Uvicorn?

**Respuesta corta:** Hace que el servidor se reinicie automaticamente cada vez que modificas el codigo.

**Respuesta larga:** Sin `--reload`, cada vez que cambies tu codigo tendrias que:
1. Detener el servidor (Ctrl+C)
2. Volver a ejecutar `uvicorn app.main:app`

Con `--reload`, Uvicorn "observa" tus archivos y, si detecta cambios, se reinicia solo. **Util solo para desarrollo.** En produccion, jamas uses `--reload`.

---

## 11. ¿Que es un decorador (`@app.get`)?

**Respuesta corta:** Es una forma de decirle a FastAPI "cuando alguien visite esta URL, ejecuta esta funcion".

**Respuesta larga:** El simbolo `@` en Python es un **decorador**. Modifica el comportamiento de la funcion que le sigue.

```python
@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}
```

**Traduccion:** "FastAPI, cuando alguien haga una peticion GET a `/saludo/{nombre}`, ejecuta la funcion `saludar` con el `nombre` extraido de la URL."

---

## 12. ¿Que pasa si no puedo abrir `http://127.0.0.1:8000` en el navegador?

**Respuesta corta:** Revisa que el servidor este corriendo en la terminal.

**Respuesta larga:** Checklist de solucion:

- [ ] ¿La terminal muestra `Uvicorn running on http://127.0.0.1:8000`?
- [ ] ¿Usaste `http://` y no `https://`?
- [ ] ¿Usaste `127.0.0.1` y no `localhost`? (a veces `localhost` no resuelve)
- [ ] ¿El puerto es 8000? (si cambiaste con `--port`, usa ese)
- [ ] ¿No hay otro programa usando el puerto 8000?
