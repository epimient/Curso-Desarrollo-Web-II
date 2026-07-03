# Dudas frecuentes - Clase 01

> Aqui encontraras las preguntas que los estudiantes suelen hacer (pero a veces da verguenza preguntar). Todas son validas.

---

## 1. Una pagina web y una aplicacion web son lo mismo?

**Respuesta corta:** No.

**Respuesta larga:** Una **pagina web** es estatica. Muestra informacion que no cambia (como un folleto digital). Una **aplicacion web** es interactiva: permite iniciar sesion, enviar datos, procesar informacion, etc.

**Ejemplo:**
- **Pagina web:** un articulo de Wikipedia (lectura)
- **Aplicacion web:** Instagram (publicas, comentas, das like, chateas)

---

## 2. FastAPI sirve para hacer paginas web completas?

**Respuesta corta:** Si, pero no es su especialidad.

**Respuesta larga:** FastAPI se especializa en construir **APIs** (backends). Pero tambien puede servir paginas HTML usando Jinja2 (plantillas). En este curso lo usaremos principalmente para APIs, que es donde brilla.

**Analogia:** FastAPI es como un excelente chef de cocina. Puede preparar la comida (API), pero no es mesero (frontend). Para eso hay otros frameworks.

---

## 3. Entonces FastAPI no usa MVC?

**Respuesta corta:** No de forma clasica, pero si aplica la idea.

**Respuesta larga:** MVC (Modelo-Vista-Controlador) es un patron de organizacion. FastAPI no lo implementa al pie de la letra como Laravel o Django, pero si permite separar responsabilidades: los schemas (modelo), las respuestas JSON (vista), y las funciones de ruta (controlador). La **intencion** de MVC se conserva.

---

## 4. ¿Por que HTTP es tan importante?

**Respuesta corta:** Porque es el idioma que hablan cliente y servidor.

**Respuesta larga:** Sin entender HTTP, estarias construyendo APIs a ciegas. HTTP define:
- **Como** se pide (metodos: GET, POST, etc.)
- **Que** se pide (rutas: `/cursos`, `/usuarios`)
- **Que** pasa si funciona (codigos 200, 201)
- **Que** pasa si falla (codigos 400, 404, 500)

> Sin HTTP, construir APIs seria como jugar sin ver la barra de vida.

---

## 5. ¿Que significa que una API sea un contrato?

**Respuesta corta:** Que ambas partes (cliente y servidor) acuerdan reglas claras.

**Respuesta larga:** Cuando una API dice "si envias un GET a `/cursos`, recibiras un JSON con una lista de cursos", eso es un contrato. El cliente confia en que recibira eso. El servidor confia en que el cliente enviara las cosas correctas.

**Si el contrato se rompe:** Si el servidor cambia la respuesta sin avisar (ej: antes devolvia `nombre` y ahora devuelve `titulo`), el cliente se rompe. De ahi la importancia de versionar las APIs.

**Analogia:** Es como pedir una pizza por telefono. Tu dices "quiero una margherita" y esperas recibir una pizza margherita. Si el restaurante decide enviarte una hawaiana porque "le parecio mejor", el contrato se rompe.

---

## 6. ¿Por que usar un framework y no programar todo desde cero?

**Respuesta corta:** Porque ahorras tiempo y evitas errores.

**Respuesta larga:** Un framework resuelve problemas que ya resolvieron miles de programadores antes que tu:
- Manejo de rutas
- Validacion de datos
- Seguridad basica
- Documentacion
- Pruebas

**Imagina construir una casa:** Puedes hacer tus propios ladrillos (programar desde cero) o comprar ladrillos ya hechos (usar framework). Con los ladrillos ya hechos, te concentras en el diseno de la casa, no en hacer ladrillos.

---

## 7. ¿Que deberia saber de Python antes de avanzar?

**Respuesta corta:** Lo basico para no "pelearte" con la sintaxis.

**Respuesta larga:** Necesitas sentirte comodo con:

| Concepto | Ejemplo minimo |
|---|---|
| **Variables** | `nombre = "Ana"` |
| **Funciones** | `def saludar():` |
| **Listas** | `cursos = ["Web I", "Web II"]` |
| **Diccionarios** | `estudiante = {"nombre": "Ana", "edad": 22}` |
| **Condicionales** | `if edad >= 18:` |
| **Modulos/imports** | `import requests` |
| **Errores basicos** | `try: ... except: ...` |
| **Entornos virtuales** | `python -m venv .venv` |

> No hace falta ser hechicero senior de Python, pero si conviene no pelearse con la sintaxis cada cinco minutos.

---

## 8. ¿Que es JSON? ¿Es lo mismo que un diccionario de Python?

**Respuesta corta:** JSON es un formato de texto. Python lo convierte en diccionario.

**Respuesta larga:** JSON (JavaScript Object Notation) es un formato ligero para intercambiar datos. Se parece mucho a un diccionario de Python, pero no es exactamente igual.

**Ejemplo JSON:**
```json
{
  "nombre": "Ana",
  "edad": 22,
  "activo": true
}
```

**Ejemplo diccionario Python:**
```python
{
  "nombre": "Ana",
  "edad": 22,
  "activo": True   # True con mayuscula en Python
}
```

Las diferencias son minimas pero importantes. La libreria `json` de Python se encarga de convertir uno en otro automaticamente.

---

## 9. ¿Que pasa si no entiendo algo de esta clase?

**Respuesta:** Es normal. Los conceptos de hoy (HTTP, API, framework, JSON) son la base de todo el curso. Si algo no quedo claro:

1. Vuelve a leer la seccion con la analogia.
2. Revisa el ejemplo guiado y ejecutalo tu mismo.
3. Pregunta en clase. Si tienes una duda, probablemente otros 5 companeros tambien.
4. Practica con los ejercicios. La teoria se entiende mejor cuando la aplicas.

---

## 10. ¿Vamos a escribir codigo de verdad en la proxima clase?

**Respuesta:** Si. En la Clase 02 construiras tu primera API con FastAPI usando una arquitectura ordenada. La clase de hoy instala los conceptos; la siguiente los pone en practica.
