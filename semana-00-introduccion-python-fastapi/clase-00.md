# Clase 00 — Introduccion a Python, APIs y FastAPI

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.
**Semana:** 0 (pre-requisito antes de la Semana 1)
**Unidad:** Pre-curso — Fundamentos
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.
**Resultado de aprendizaje asociado:**

- RA1: Analizar el modelo cliente-servidor y el protocolo HTTP como base de las aplicaciones web modernas.

## 2. Proposito de la clase

Esta clase es una introduccion completa a Python, aplicaciones web, APIs y FastAPI. Esta disenada para estudiantes que saben algo de programacion, pero que aun no tienen claro como pasamos de "un programa que corre en mi PC" a "un backend que recibe peticiones desde Internet".

No empezamos mostrando `@app.get("/")`, porque para un estudiante que aun no entiende que es una API eso se parece a un hechizo de nivel 17. Primero construimos el problema y despues presentamos FastAPI como la solucion.

## 3. Pregunta orientadora

**Como pasamos de un programa que corre en mi PC a un backend que recibe peticiones desde Internet?**

## 4. Objetivos de aprendizaje

Al terminar esta clase el estudiante deberia ser capaz de explicar:

- Que es Python.
- Como se escribe codigo basico en Python.
- Que diferencia existe entre un programa tradicional y una aplicacion web.
- Que es cliente y que es servidor.
- Que es HTTP.
- Que es una API.
- Que significa REST.
- Que son GET, POST, PUT y DELETE.
- Que es JSON.
- Que es un framework.
- Que es FastAPI.
- Para que sirve FastAPI.
- Que significa una ruta o endpoint.
- Como crear su primera API.
- Como probarla desde Swagger.
- Que vamos a construir durante el curso.

La idea conceptual que debe quedar al terminar la clase es esta:

```
Python
   ↓
Logica de programacion
   ↓
Funciones, clases y estructuras de datos
   ↓
FastAPI
   ↓
API / Backend
   ↓
HTTP
   ↓
Frontend / Aplicacion movil / Otro sistema
   ↓
Base de datos
```

## 5. Comencemos desde el principio: que es un programa?

Yo abriría la clase con una pregunta muy sencilla:

¿Qué hace realmente un programa?

Un programa no es más que una serie de instrucciones que una computadora ejecuta.

Por ejemplo:

print("Hola mundo")

Estamos diciéndole:

Computador:


muéstrame en pantalla el texto
"Hola mundo".

Y la computadora responde:

Hola mundo

Podemos hacer algo un poco más interesante:

nombre = input("¿Cómo te llamas? ")


print("Hola", nombre)

Aquí ya existe una interacción.

Usuario
   ↓
Introduce información
   ↓
Programa
   ↓
Procesa información
   ↓
Entrega un resultado

Este concepto aparentemente trivial será importantísimo más adelante.

Porque una API hace prácticamente lo mismo.

La diferencia es que quien le habla al programa ya no necesariamente es una persona.

Puede ser otro programa.

## 6. Que es Python?

Python es un lenguaje de programación.

Formalmente, Python es un lenguaje de propósito general, interpretado, con tipado dinámico y soporte para múltiples paradigmas, incluida la programación orientada a objetos.

La documentación oficial destaca precisamente su sintaxis relativamente sencilla, sus estructuras de datos de alto nivel y su naturaleza interpretada, características que lo hacen apropiado para desarrollo rápido de aplicaciones.

Para los estudiantes lo explicaría así:

Python es el idioma que utilizaremos para darle instrucciones al computador.

Igual que existen diferentes idiomas humanos:

Español
Inglés
Francés
Italiano

en programación existen diferentes lenguajes:

Python
C#
Java
JavaScript
C++
Go
Rust
PHP

Todos permiten decirle cosas a la computadora, pero utilizan sintaxis y filosofías diferentes.

## 7. Como se ve Python?

Puedes comparar rápidamente varios lenguajes.

En Java:

public class Main {
    public static void main(String[] args) {
        System.out.println("Hola mundo");
    }
}

En C#:

Console.WriteLine("Hola mundo");

En Python:

print("Hola mundo")

Python intenta reducir bastante el ruido sintáctico.

No significa que Python sea “un lenguaje de principiantes”.

Significa que permite expresar muchas operaciones con relativamente poco código.

De hecho, Python se utiliza en áreas como:

Backend
Automatización
Inteligencia artificial
Machine Learning
Ciencia de datos
Ciberseguridad
IoT
Visión artificial
APIs
Scripting
DevOps
## 8. Variables en Python

Una variable es simplemente un nombre que utilizamos para guardar información.

Por ejemplo:

nombre = "Eduardo"
edad = 35
altura = 1.75
activo = True

Podemos imaginar la memoria así:

nombre ──────► "Eduardo"


edad ────────► 35


altura ──────► 1.75


activo ──────► True

Cada dato tiene un tipo.

nombre = "Ana"       # str
edad = 20            # int
altura = 1.68        # float
activo = True        # bool

Podemos comprobarlo:

print(type(nombre))
print(type(edad))
print(type(altura))
print(type(activo))
## 9. Tipos de datos basicos

Los cuatro tipos que inicialmente deben dominar son:

str     → texto
int     → números enteros
float   → números decimales
bool    → verdadero / falso

Ejemplos:

producto = "Laptop"
cantidad = 5
precio = 2500000.50
disponible = True

Aquí puedes hacer una pregunta a la clase:

¿Qué tipo utilizarían para almacenar un número de teléfono?

Probablemente alguno diga:

int

Pero ahí puedes mostrar que no todo lo que tiene números es necesariamente un número matemático.

Un teléfono sería mejor:

telefono = "3001234567"

Porque no vamos a:

sumar teléfonos
multiplicar teléfonos
dividir teléfonos
## 10. Python es de tipado dinamico

Podemos escribir:

edad = 20

Sin tener que escribir:

int edad = 20

Python determina el tipo durante la ejecución.

Incluso esto es técnicamente posible:

dato = 20
dato = "Hola"

Primero:

dato → entero

después:

dato → texto

Esto proporciona flexibilidad, aunque también significa que debemos ser disciplinados al programar.

## 11. Operaciones

Python permite operaciones matemáticas normales:

a = 10
b = 5


print(a + b)
print(a - b)
print(a * b)
print(a / b)

También comparaciones:

edad = 20


print(edad > 18)
print(edad < 18)
print(edad == 20)

Resultado:

True
False
True

Esto permitirá posteriormente tomar decisiones.

## 12. Condicionales

Un programa puede decidir qué hacer.

edad = 20


if edad >= 18:
    print("Es mayor de edad")
else:
    print("Es menor de edad")

Aquí aparece algo importantísimo de Python:

La indentación

Python utiliza la indentación para identificar bloques de código.

Correcto:

if edad >= 18:
    print("Mayor de edad")

Incorrecto:

if edad >= 18:
print("Mayor de edad")

En Python los espacios no son decoración.

Son parte de la sintaxis.

Sí. Los espacios finalmente consiguieron empleo.

## 13. Listas

Cuando queremos almacenar varios elementos utilizamos una lista.

estudiantes = [
    "Ana",
    "Carlos",
    "María"
]

Podemos acceder a ellos:

print(estudiantes[0])

Resultado:

Ana

Una lista se puede imaginar así:

Índice      Valor


0           Ana
1           Carlos
2           María
## 14. Diccionarios

Ahora introducimos una de las estructuras más importantes para FastAPI.

estudiante = {
    "nombre": "Ana",
    "edad": 20,
    "programa": "Ingeniería de Sistemas"
}

Tenemos parejas:

clave        valor


nombre       Ana
edad         20
programa     Ingeniería de Sistemas

Podemos acceder:

print(estudiante["nombre"])

Resultado:

Ana

¿Por qué quiero que entiendan muy bien los diccionarios?

Porque dentro de unos minutos tendremos esto:

return {
    "nombre": "Ana",
    "edad": 20
}

y FastAPI lo transformará en:

{
    "nombre": "Ana",
    "edad": 20
}

Aquí empieza a aparecer la conexión.

## 15. Que es JSON?

JSON significa:

JavaScript Object Notation

Pero no necesitamos JavaScript para utilizarlo.

JSON es simplemente un formato utilizado para intercambiar información entre sistemas.

Ejemplo:

{
    "nombre": "Ana",
    "edad": 20,
    "activo": true
}

Obsérvese la similitud con Python.

Python:

estudiante = {
    "nombre": "Ana",
    "edad": 20
}

JSON:

{
    "nombre": "Ana",
    "edad": 20
}

Visualmente son muy parecidos.

Y esto será fundamental porque normalmente:

Cliente
   ↓
JSON
   ↓
FastAPI

y:

FastAPI
   ↓
JSON
   ↓
Cliente
## 16. Funciones

Ahora necesitamos otro concepto fundamental.

Supongamos que queremos sumar dos números.

Podríamos escribir:

a = 10
b = 20


resultado = a + b


print(resultado)

Pero si queremos hacerlo muchas veces, creamos una función:

def sumar(a, b):
    resultado = a + b
    return resultado

Y podemos utilizarla:

print(sumar(10, 20))
print(sumar(40, 50))
print(sumar(5, 8))

Conceptualmente:

          FUNCIÓN


datos ─────────────► procesamiento
                        │
                        ▼
                    resultado

Por ejemplo:

def saludar(nombre):
    return "Hola " + nombre

Entrada:

Eduardo

Proceso:

"Hola " + nombre

Salida:

Hola Eduardo

Guarden esta idea porque una ruta de FastAPI será básicamente:

Una función de Python que se ejecuta cuando alguien realiza una petición HTTP.

Esa frase es clave para toda la clase.

## 17. Anotaciones de tipos

Python moderno permite hacer esto:

def sumar(a: int, b: int):
    return a + b

Estamos diciendo:

a debería ser int
b debería ser int

También podemos indicar qué devuelve:

def sumar(a: int, b: int) -> int:
    return a + b

Visualmente:

a: int
    \
     → sumar() → int
    /
b: int

Las anotaciones no convierten Python en un lenguaje estrictamente tipado como Java o C#, pero proporcionan información que herramientas, editores y frameworks pueden aprovechar.

Y aquí aparece algo muy importante:

FastAPI utiliza intensivamente las anotaciones de tipos de Python para validar, convertir y documentar los datos automáticamente.

Por eso necesitamos entender:

nombre: str
edad: int
precio: float
activo: bool

antes de FastAPI.

## 18. Hasta ahora nuestros programas viven solos

Hasta este punto hemos realizado programas así:

Usuario
   │
   ▼
Programa Python
   │
   ▼
Terminal

Por ejemplo:

nombre = input("Nombre: ")


print("Hola", nombre)

Pero aparece un problema.

¿Qué ocurre si quiero que mi programa sea utilizado por:

una página web
una aplicación móvil
otra computadora
un ESP32
un sistema empresarial
una aplicación de escritorio

No podemos pedirles a todos que abran nuestra terminal.

Necesitamos permitir que otros sistemas se comuniquen con nuestro programa.

Y aquí nace el concepto fundamental de la clase.

## 19. Cliente y servidor

Imaginemos un restaurante.

Tenemos:

Cliente
Mesero
Cocina

El cliente solicita:

Quiero una hamburguesa.

El mesero lleva la solicitud a la cocina.

La cocina procesa la solicitud.

El mesero devuelve el resultado.

En una aplicación web tenemos algo parecido:

CLIENTE
   │
   │ petición
   ▼
SERVIDOR
   │
   │ procesamiento
   ▼
RESPUESTA

El cliente podría ser:

Chrome
Firefox
Aplicación móvil
React
Vue
Angular
Otro backend
ESP32
Postman

El servidor podría ser nuestra aplicación:

FastAPI
## 20. Internet no funciona con telepatia

Necesitamos reglas para que cliente y servidor puedan comunicarse.

Una de esas reglas es:

HTTP

HTTP significa:

HyperText Transfer Protocol

Es un protocolo de comunicación.

Podemos entender un protocolo simplemente como:

Un conjunto de reglas que dos sistemas acuerdan utilizar para comunicarse.

Como cuando dos personas deciden:

"Vamos a hablar español."

En aplicaciones web:

Cliente
   │
   │ HTTP
   ▼
Servidor
## 21. Peticion y respuesta

Cuando navegamos a una página ocurre algo parecido a:

CLIENTE


"Servidor, quiero información."


        │
        │ REQUEST
        ▼


SERVIDOR


"Entendido."


        │
        │ RESPONSE
        ▼


CLIENTE

Los términos técnicos son:

Request  → petición


Response → respuesta
## 22. Que es una API?

Ahora sí podemos introducirlo.

API significa:

Application Programming Interface

Una API permite que diferentes programas se comuniquen entre ellos mediante una interfaz definida.

Para explicarlo de forma sencilla:

Una API es una puerta controlada mediante la cual otros programas pueden solicitar información o ejecutar operaciones en nuestro sistema.

Por ejemplo, imaginemos una universidad.

Tenemos información de estudiantes en nuestro sistema.

Una aplicación podría solicitar:

"Dame los estudiantes."

La API responde:

[
    {
        "id": 1,
        "nombre": "Ana"
    },
    {
        "id": 2,
        "nombre": "Carlos"
    }
]

Otro sistema podría preguntar:

"Dame el estudiante número 2."

Respuesta:

{
    "id": 2,
    "nombre": "Carlos"
}
## 23. Una API no necesariamente tiene interfaz grafica

Este punto es importantísimo.

Los estudiantes muchas veces esperan algo como:

botones
ventanas
menús
formularios
colores
imágenes

Pero una API puede funcionar perfectamente sin nada de eso.

Podría devolver simplemente:

{
    "mensaje": "Hola mundo"
}

La API proporciona información y funcionalidades.

La interfaz gráfica puede construirse aparte.

Entonces podemos tener:

          ┌──────────────┐
          │    React     │
          └──────┬───────┘
                 │
                 │
                 ▼
          ┌──────────────┐
          │   FastAPI    │
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │ Base de datos│
          └──────────────┘

O:

Aplicación Android
        │
        ▼
     FastAPI
        │
        ▼
   Base de datos

Incluso:

ESP32
  │
  ▼
FastAPI
  │
  ▼
Base de datos

Ahí probablemente varios comienzan a entender para qué sirve.

## 24. Que significa REST?

Aquí no hace falta destruirlos con teoría arquitectónica todavía.

Puedes explicar:

REST es un estilo utilizado para diseñar APIs utilizando los conceptos de HTTP.

Normalmente trabajamos con recursos.

Por ejemplo:

estudiantes
productos
usuarios
vehículos
reservas
materias

Y tendremos direcciones como:

/estudiantes


/productos


/usuarios
## 25. Metodos HTTP

Ahora introducimos cuatro operaciones fundamentales:

GET
POST
PUT
DELETE

Puedes relacionarlas con CRUD.

CRUD	HTTP	Acción
Create	POST	Crear
Read	GET	Consultar
Update	PUT	Actualizar
Delete	DELETE	Eliminar

Ejemplo con estudiantes:

GET /estudiantes

Significa:

Dame los estudiantes.

GET /estudiantes/5

Significa:

Dame el estudiante 5.

POST /estudiantes

Significa:

Crea un estudiante.

PUT /estudiantes/5

Significa:

Actualiza el estudiante 5.

DELETE /estudiantes/5

Significa:

Elimina el estudiante 5.

Y acabamos de construir conceptualmente una API REST.

Sin escribir todavía una sola línea de FastAPI.

Eso es exactamente lo que queremos.

## 26. Entonces, que demonios es FastAPI?

Ahora sí.

FastAPI es un framework web moderno para Python orientado principalmente a construir APIs.

La definición oficial lo describe como un framework web moderno y de alto rendimiento para construir APIs utilizando anotaciones estándar de tipos de Python.

Separémoslo:

FastAPI


FAST
+
API

Pero más importante:

Python
   +
herramientas para recibir HTTP
   +
rutas
   +
validación
   +
JSON
   +
documentación
   +
seguridad
   +
muchas otras funcionalidades
## 27. Que es un framework?

Antes de seguir, debemos aclararlo.

Un framework es un conjunto de herramientas, estructuras y convenciones que nos ayuda a construir aplicaciones.

Podríamos hacerlo todo nosotros mismos.

Podríamos programar:

servidor HTTP
manejo de conexiones
interpretación de peticiones
conversión JSON
validación
errores
documentación
seguridad

Pero sería absurdo reinventar todo.

Sería como fabricar un motor antes de aprender a conducir.

FastAPI ya proporciona gran parte de esa infraestructura.

Nosotros nos concentramos en:

¿Qué debe hacer mi aplicación?
## 28. Nuestra primera aplicacion FastAPI

Ahora sí escribimos:

from fastapi import FastAPI


app = FastAPI()




@app.get("/")
def inicio():
    return {
        "mensaje": "Hola mundo"
    }

La documentación oficial utiliza esencialmente esta misma estructura como el ejemplo mínimo de una aplicación FastAPI.

Ahora vamos línea por línea.

## 29. Primera linea
from fastapi import FastAPI

Significa:

Del paquete fastapi, quiero utilizar la clase FastAPI.

Es parecido a sacar una herramienta de una caja.

fastapi
│
├── FastAPI
├── herramientas
├── clases
└── funcionalidades
## 30. Creamos nuestra aplicacion
app = FastAPI()

Estamos creando un objeto FastAPI.

Podemos visualizarlo:

FastAPI
   │
   ▼
┌───────────────┐
│      app      │
│               │
│ Nuestra API   │
└───────────────┘

app será nuestra aplicación.

## 31. Nuestra primera ruta
@app.get("/")

Aquí debemos detenernos.

Tenemos dos cosas:

GET

y:

/

GET significa:

Quiero obtener información.

/ representa una dirección.

Por ejemplo:

http://localhost:8000/
## 32. Que es un endpoint?

Un endpoint es básicamente un punto de acceso a nuestra API.

Ejemplo:

GET /estudiantes

Otro:

GET /productos

Otro:

POST /usuarios

La combinación importante es:

Método HTTP + Ruta

Por ejemplo:

GET + /estudiantes

Eso identifica una operación.

## 33. Y que hace esta funcion?

Tenemos:

def inicio():
    return {
        "mensaje": "Hola mundo"
    }

Eso ya lo conocemos.

Es una función Python.

Entonces:

@app.get("/")
def inicio():
    return {"mensaje": "Hola mundo"}

se puede leer como:

Cuando alguien haga una petición GET a /, ejecuta la función inicio().

Esta frase deberían escribirla.

Porque si entienden esto, ya entendieron el corazón de FastAPI.

Visualmente:

GET /
 │
 │
 ▼
inicio()
 │
 │
 ▼
{"mensaje": "Hola mundo"}
 │
 │
 ▼
JSON
## 34. Ejecutar nuestra API

La documentación actual de FastAPI recomienda instalar el paquete estándar y permite utilizar su CLI directamente. Con pip, por ejemplo:

python -m venv .venv

En Linux/macOS:

source .venv/bin/activate

Instalamos:

pip install "fastapi[standard]"

La instalación fastapi[standard] y el comando fastapi dev forman parte del flujo documentado actualmente por FastAPI.

Creamos:

main.py

con:

from fastapi import FastAPI


app = FastAPI()




@app.get("/")
def inicio():
    return {
        "mensaje": "Hola desde FastAPI"
    }

Ejecutamos:

fastapi dev main.py

Y tendremos normalmente:

http://127.0.0.1:8000
## 35. Que significa localhost?

Aquí conviene detenerse otra vez.

localhost

significa:

Esta misma computadora.

127.0.0.1 representa la interfaz de loopback local.

Por eso:

http://127.0.0.1:8000

significa aproximadamente:

Protocolo
   │
   ▼
http://127.0.0.1:8000
       │          │
       │          └── puerto
       │
       └── mi propia computadora
## 36. Probemos nuestra API

Entramos desde el navegador:

http://127.0.0.1:8000

Respuesta:

{
    "mensaje": "Hola desde FastAPI"
}

Y aquí puedes hacerles notar algo:

Nosotros escribimos un diccionario Python.

{
    "mensaje": "Hola desde FastAPI"
}

Pero el navegador recibió JSON.

{
    "mensaje": "Hola desde FastAPI"
}

FastAPI realizó la conversión.

## 37. La sorpresa: Swagger

Ahora entramos en:

http://127.0.0.1:8000/docs

Aparece Swagger UI.

FastAPI genera automáticamente documentación interactiva basada en OpenAPI; también ofrece una interfaz alternativa con ReDoc.

Esto es espectacular para una primera clase.

Porque podemos probar nuestra API sin instalar Postman.

Swagger permite:

ver endpoints
probar endpoints
enviar parámetros
enviar JSON
ver respuestas
ver errores

Es prácticamente un laboratorio para nuestra API.

## 38. Creamos varias rutas

Ahora:

from fastapi import FastAPI


app = FastAPI()




@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido"}




@app.get("/estudiantes")
def obtener_estudiantes():
    return [
        {
            "id": 1,
            "nombre": "Ana"
        },
        {
            "id": 2,
            "nombre": "Carlos"
        }
    ]




@app.get("/profesores")
def obtener_profesores():
    return [
        {
            "id": 1,
            "nombre": "Eduardo"
        }
    ]

Tenemos:

GET /
GET /estudiantes
GET /profesores
## 39. Parametros en la URL

Supongamos que quiero un estudiante específico.

Podemos hacer:

@app.get("/estudiantes/{id}")
def obtener_estudiante(id: int):
    return {
        "id": id,
        "nombre": "Estudiante de prueba"
    }

Ahora:

GET /estudiantes/1

devuelve:

{
    "id": 1,
    "nombre": "Estudiante de prueba"
}

Y:

GET /estudiantes/27

devuelve:

{
    "id": 27,
    "nombre": "Estudiante de prueba"
}

Aquí aparece nuestro viejo conocido:

id: int

FastAPI aprovecha esa anotación para validar y convertir información.

## 40. Hagamos un pequeno experimento

Tenemos:

@app.get("/estudiantes/{id}")
def obtener_estudiante(id: int):
    return {
        "id": id
    }

Probemos:

/estudiantes/10

Funciona.

Ahora:

/estudiantes/pepito

FastAPI responde con un error de validación.

¿Por qué?

Porque nosotros declaramos:

id: int

Es decir:

Aquí solamente acepto números enteros.

Esto muestra una de las grandes ventajas de FastAPI.

## 41. Query parameters

Ahora introducimos otro concepto.

Ruta:

/productos/10

El 10 identifica un recurso.

Pero también podemos tener:

/productos?categoria=computadores

Aquí:

categoria=computadores

es un parámetro de consulta.

En FastAPI:

@app.get("/productos")
def obtener_productos(categoria: str):
    return {
        "categoria": categoria
    }

Llamamos:

/productos?categoria=laptops

Respuesta:

{
    "categoria": "laptops"
}
## 42. Crear informacion: POST

Hasta ahora solo consultamos.

Pero queremos crear datos.

Por ejemplo:

POST /estudiantes

Para eso necesitamos enviar información:

{
    "nombre": "María",
    "edad": 20
}

Aquí aparece Pydantic.

## 43. Modelo de datos

Podemos escribir:

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()




class Estudiante(BaseModel):
    nombre: str
    edad: int

Estamos definiendo cómo debería verse un estudiante.

Estudiante


nombre → str
edad   → int

Ahora:

@app.post("/estudiantes")
def crear_estudiante(estudiante: Estudiante):
    return estudiante

Código completo:

from fastapi import FastAPI
from pydantic import BaseModel




app = FastAPI()




class Estudiante(BaseModel):
    nombre: str
    edad: int




@app.post("/estudiantes")
def crear_estudiante(estudiante: Estudiante):
    return estudiante

Desde Swagger enviamos:

{
    "nombre": "María",
    "edad": 20
}

FastAPI:

recibe JSON
   ↓
valida información
   ↓
convierte a objeto Python
   ↓
ejecuta nuestra función
   ↓
genera respuesta JSON
## 44. Que pasa si enviamos informacion incorrecta?

Supongamos:

{
    "nombre": "María",
    "edad": "tengo veinte años"
}

Pero nuestro modelo dice:

edad: int

FastAPI detectará el problema.

Nosotros no tuvimos que escribir manualmente:

if edad ...

para cada validación básica.

Aquí los estudiantes comienzan a entender por qué usamos un framework.

## 45. Construyamos una mini API

Ahora podemos juntar todo.

from fastapi import FastAPI
from pydantic import BaseModel




app = FastAPI()




class Producto(BaseModel):
    nombre: str
    precio: float




productos = []




@app.get("/")
def inicio():
    return {
        "mensaje": "API de productos"
    }




@app.get("/productos")
def obtener_productos():
    return productos




@app.post("/productos")
def crear_producto(producto: Producto):
    productos.append(producto)


    return {
        "mensaje": "Producto creado",
        "producto": producto
    }

Ahora podemos usar Swagger.

Primero:

GET /productos

Resultado:

[]

Después:

POST /productos

Enviamos:

{
    "nombre": "Teclado mecánico",
    "precio": 250000
}

Después:

GET /productos

Resultado:

[
    {
        "nombre": "Teclado mecánico",
        "precio": 250000
    }
]

Acabamos de construir una mini aplicación backend.

## 46. Pero profesor, donde esta la base de datos?

Excelente pregunta.

Todavía no tenemos.

Tenemos:

productos = []

Todo está almacenado en memoria RAM.

Si apagamos el servidor:

POOF.

Adiós productos.

Más adelante cambiaremos:

Lista Python

por:

Base de datos

Entonces nuestro sistema evolucionará:

ANTES


Cliente
   ↓
FastAPI
   ↓
Lista Python

Después:

Cliente
   ↓
FastAPI
   ↓
Lógica
   ↓
Base de datos

Y más adelante:

Frontend
    │
    ▼
FastAPI
    │
    ▼
Servicios
    │
    ▼
Repositorios
    │
    ▼
Base de datos

Ahora sí estamos construyendo software real.

## 47. Entonces, FastAPI es el frontend?

No.

Esto debe quedar clarísimo.

FastAPI normalmente estará de este lado:

BACKEND

Por ejemplo:

┌───────────────────┐
│      FRONTEND     │
│                   │
│ HTML              │
│ CSS               │
│ JavaScript        │
│ React/Vue/etc.    │
└─────────┬─────────┘
          │
          │ HTTP + JSON
          ▼
┌───────────────────┐
│      BACKEND      │
│                   │
│      FastAPI      │
│      Python       │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   BASE DE DATOS   │
└───────────────────┘
## 48. FastAPI es MVC?

Aquí conectaría con el curso.

FastAPI no obliga a utilizar una arquitectura MVC tradicional.

Pero podemos organizar una aplicación separando responsabilidades.

Podemos relacionarlo conceptualmente:

Cliente
   │
   ▼
Routes / Controllers
   │
   ▼
Servicios
   │
   ▼
Modelos
   │
   ▼
Base de datos

Una estructura futura podría ser:

proyecto/
│
├── main.py
│
├── routers/
│   ├── estudiantes.py
│   └── usuarios.py
│
├── models/
│
├── schemas/
│
├── services/
│
└── database/

Pero no les mostraría esto durante los primeros diez minutos.

Primero:

@app.get("/")

Después arquitectura.

Porque enseñar arquitectura antes de que sepan qué están arquitecturando es básicamente mostrarles el plano de la Estrella de la Muerte antes de explicar qué es una nave.

## 49. Que vamos a hacer durante el curso?

Aquí aterrizaría definitivamente a los estudiantes.

Les diría:

Durante el curso vamos a pasar progresivamente de pequeños programas Python a construir un backend web completo.

La evolución será esta:

ETAPA 1
Python
│
├── variables
├── estructuras
├── funciones
└── clases


         ↓


ETAPA 2
HTTP y APIs
│
├── Request
├── Response
├── JSON
├── GET
├── POST
├── PUT
└── DELETE


         ↓


ETAPA 3
FastAPI
│
├── rutas
├── parámetros
├── modelos
└── validaciones


         ↓


ETAPA 4
CRUD


Create
Read
Update
Delete


         ↓


ETAPA 5
Base de datos


FastAPI
   ↓
SQL
   ↓
Base de datos


         ↓


ETAPA 6
Arquitectura


Routers
## 50. El proyecto mental que deben tener

Yo utilizaría desde la primera clase un mismo ejemplo.

Por ejemplo:

Sistema académico

Queremos construir una API que permita administrar:

Estudiantes
Profesores
Materias
Cursos
Notas

Inicialmente tendremos:

GET /estudiantes

Después:

GET /estudiantes/{id}

Después:

POST /estudiantes

Después:

PUT /estudiantes/{id}

Después:

DELETE /estudiantes/{id}

Finalmente:

FastAPI
     │
     ▼
Base de datos

Así cada tema nuevo tiene un propósito.

## 51. La pelicula completa

Al final de la explicación dibujaría esto en el tablero:

                USUARIO
                   │
                   ▼
            ┌─────────────┐
            │  FRONTEND   │
            │ Web / móvil │
            └──────┬──────┘
                   │
                   │ HTTP
                   │ JSON
                   ▼
            ┌─────────────┐
            │   FastAPI   │
            │   Python    │
            └──────┬──────┘
                   │
                   │ lógica
                   ▼
            ┌─────────────┐
            │   Servicio  │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │ Base datos  │
            └─────────────┘

Y les dices:

Este semestre nuestro territorio será principalmente esta parte.

            ┌──────────────────────┐
            │                      │
            │       FastAPI        │
            │       Python         │
            │                      │
            │       Backend        │
            │                      │
            └──────────────────────┘
## 52. Ejercicio guiado para terminar la clase

Les daría este reto extremadamente sencillo.

Construir una API para videojuegos.

Primero:

from fastapi import FastAPI


app = FastAPI()

Crear:

GET /

que devuelva:

{
    "mensaje": "API de videojuegos"
}

Después:

GET /videojuegos

que devuelva:

[
    {
        "id": 1,
        "titulo": "Doom",
        "anio": 1993
    },
    {
        "id": 2,
        "titulo": "Half-Life",
        "anio": 1998
    }
]

Solución:

from fastapi import FastAPI




app = FastAPI()




@app.get("/")
def inicio():
    return {
        "mensaje": "API de videojuegos"
    }




@app.get("/videojuegos")
def obtener_videojuegos():
    return [
        {
            "id": 1,
            "titulo": "Doom",
            "anio": 1993
        },
        {
            "id": 2,
            "titulo": "Half-Life",
            "anio": 1998
        }
    ]

Luego preguntar:

¿Cómo creen que podríamos obtener solamente Doom?

Y dejas que ellos propongan.

Hasta llegar a:

GET /videojuegos/1

Y escribimos:

@app.get("/videojuegos/{id}")
def obtener_videojuego(id: int):
    return {
        "id": id,
        "titulo": "Doom",
        "anio": 1993
    }

Ya tienen:

Ruta
Método HTTP
Parámetro
Función
Respuesta
JSON

en un ejemplo diminuto.

## 53. Las preguntas que deberian poder responder al final

Yo terminaría preguntándoles oralmente:

¿Python y FastAPI son lo mismo?

No.

Python es el lenguaje.

FastAPI es un framework construido para Python.

¿FastAPI es una base de datos?

No.

¿FastAPI es un frontend?

No principalmente; nuestro uso será backend/API.

¿Qué es una API?

Una interfaz mediante la cual programas pueden comunicarse.

¿Qué significa GET?

Consultar información.

¿Qué significa POST?

Crear/enviar información.

¿Qué significa JSON?

Un formato estructurado utilizado para intercambiar datos.

¿Qué hace esto?

@app.get("/usuarios")

Define que una función atenderá una petición GET realizada sobre /usuarios.

¿Qué hace esto?

def obtener_usuarios():

Define una función de Python.

¿Qué hace esto?

return {"nombre": "Ana"}

Devuelve datos que FastAPI puede serializar en una respuesta JSON.

## 54. La frase con la que cerraria la clase

FastAPI no sustituye Python. FastAPI utiliza Python para convertir nuestras funciones y nuestra lógica de programación en servicios que pueden ser utilizados a través de una red.

Y todavía más sencillo:

Antes:


Persona → Programa Python




Ahora:


Aplicación
    ↓
Internet
    ↓
FastAPI
    ↓
Python
    ↓
Datos

Esa es la transición conceptual que tienen que entender.

A partir de ahí, @app.get, Pydantic, routers, bases de datos, autenticación y arquitectura dejan de parecer una colección arbitraria de sintaxis y empiezan a tener sentido.

La documentación oficial actual confirma además tres ideas que conviene reforzar desde la primera clase: FastAPI está construido alrededor de Python moderno y sus anotaciones de tipos; utiliza OpenAPI/JSON Schema; y genera automáticamente documentación interactiva con Swagger UI y ReDoc.

Para una primera sesión, yo no avanzaría todavía a SQLAlchemy, JWT, async/await, inyección de dependencias ni arquitectura por capas. Primero conseguiría que todos puedan explicar sin mirar apuntes esta secuencia:

Python
↓
Función
↓
FastAPI
↓
Endpoint
↓
HTTP Request
↓
Procesamiento
↓
HTTP Response
↓
JSON

Si dominan eso, ya tenemos los cimientos. Lo demás son habitaciones; sin los cimientos, terminamos con el Castillo Ambulante de Howl pero construido por estudiantes de primer corte.

 