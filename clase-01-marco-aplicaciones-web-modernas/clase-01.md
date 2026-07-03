# Clase 01 - Presentacion del curso, diagnostico y marco de aplicaciones web modernas

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para el desarrollo de aplicaciones web y APIs modernas.  
**Semana:** 1  
**Unidad:** Unidad 1 - Introduccion a MVC y Frameworks  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**  

- RA1: Comprender los conceptos fundamentales del patron MVC y los frameworks de desarrollo de software mediante la identificacion de sus componentes y su interaccion.
- RA2: Analizar las ventajas y desventajas de utilizar frameworks en el desarrollo de aplicaciones web mediante la comparacion de diferentes frameworks y su aplicabilidad en distintos contextos.

## 2. Proposito de la clase

Esta primera clase abre el curso ubicando a los estudiantes en el ecosistema de las aplicaciones web modernas. Antes de escribir endpoints como si estuvieramos invocando hechizos de Python en una mazmorra, es necesario comprender que problema resuelve una aplicacion web, como viajan las solicitudes entre cliente y servidor, que papel cumplen los frameworks y por que FastAPI sera el eje tecnico del curso.

La clase tambien funciona como diagnostico. El docente podra identificar el nivel previo de los estudiantes en conceptos como HTTP, arquitectura cliente-servidor, APIs, JSON, Python basico, estructura de proyectos y uso de herramientas de desarrollo.

## 3. Pregunta orientadora

**Que ocurre realmente desde que un usuario presiona un boton en una aplicacion web hasta que recibe una respuesta del servidor?**

Esta pregunta parece simple, casi ofensivamente simple, como tutorial inicial de videojuego. Pero detras de ella aparecen los conceptos centrales del curso: solicitudes HTTP, rutas, controladores o manejadores, validacion, modelos de datos, respuestas, seguridad y experiencia de uso.

## 4. Conceptos clave

### 4.1 Aplicacion web

> **En espanol simple:** una aplicacion web es como una tienda por internet. Tu ves el escaparate (la pagina o app), pero detras hay un almacen (servidor), un sistema de inventario (base de datos), empleados que procesan pedidos (logica de negocio) y reglas de seguridad (como revisar que tu tarjeta sea valida). Todo funciona en conjunto, aunque tu solo veas el escaparate.

Una aplicacion web es un sistema de software que se ejecuta a traves de una arquitectura conectada por red, normalmente usando un navegador, una aplicacion movil u otro cliente que consume servicios expuestos por un servidor.

**Analogia para entenderlo mejor:**

Piensa en Netflix. Cuando abres la app:
- El **cliente** (tu telefono) le pide al servidor: "dame las peliculas disponibles".
- El **servidor** revisa su base de datos y responde: "aqui tienes el catalogo".
- Usa una **API** para que ambos se entiendan.
- Tiene **seguridad** para que no veas contenido de otro usuario.
- Usa **servicios externos** como el sistema de pago de tu tarjeta.

Una app web no es magia. Es un conjunto de piezas que conversan entre si.

En una aplicacion web moderna pueden intervenir:

- Un cliente, como navegador, aplicacion movil, herramienta de pruebas o frontend SPA.
- Un servidor, donde se procesa la logica de negocio.
- Una API, que define como el cliente conversa con el servidor.
- Una base de datos, donde se almacena informacion persistente.
- Servicios externos, como autenticacion, pagos, correo, almacenamiento o analitica.
- Reglas de seguridad, validacion, permisos y monitoreo.

La web moderna ya no es solo "una pagina que muestra informacion". Eso era una etapa temprana. Hoy muchas aplicaciones web son plataformas completas, sistemas de integracion, servicios internos, APIs publicas o soluciones empresariales conectadas con multiples capas.

### 4.2 Arquitectura cliente-servidor

> **En espanol simple:** el cliente pide, el servidor responde. Como cuando pides una pizza: tu eres el cliente, la pizzeria es el servidor. Tu no entras a la cocina a amasar la masa; solo pides y recibes.

La arquitectura cliente-servidor separa responsabilidades:

- **Cliente:** el que solicita informacion o acciones. Puede ser un navegador (Chrome, Firefox), una app movil, o incluso otro programa. El cliente muestra interfaces, captura datos del usuario y envia peticiones.
- **Servidor:** el que recibe la solicitud, procesa reglas de negocio, consulta datos y responde. El servidor vive en una computadora remota (no en tu casa) y esta esperando a que alguien le pida algo.

**Ejemplo paso a paso con Maria, una estudiante real:**

Maria quiere ver sus notas en la plataforma academica.

1. Maria abre la plataforma en su navegador (Chrome).
2. El navegador (cliente) envia una solicitud al servidor: "dame las notas de Maria".
3. El servidor recibe la solicitud en una ruta especifica: `/estudiantes/maria/notas`.
4. El servidor revisa: "esta Maria autenticada?" (seguridad).
5. El servidor busca las notas en la base de datos.
6. El servidor empaqueta las notas como JSON y las envia de vuelta.
7. El navegador recibe los datos y los muestra bonitos en pantalla.

**Todo esto ocurre en segundos.** El usuario solo ve "mis notas aparecieron". Pero detras hay una coreografia de 7 pasos entre cliente y servidor.

Este flujo parece obvio, pero es el esqueleto de casi todo lo que se construira en el curso. La diferencia entre una aplicacion limpia y una bola de cables backend con ansiedad es la forma como se organizan esas responsabilidades.

### 4.3 HTTP como lenguaje de comunicacion

> **En espanol simple:** HTTP es el "idioma" que usan cliente y servidor para entenderse. Como el espanol, tiene verbos (metodos), sustantivos (rutas) y reglas gramaticales (codigos de estado). Sin este idioma comun, cliente y servidor no podrian comunicarse.

**Analogia del restaurante:**

Imagina que vas a un restaurante. Tu eres el **cliente** y la cocina es el **servidor**.

| Accion tuya | Metodo HTTP equivalente | Explicacion |
|---|---|---|
| "¿Que tienen de menu?" | **GET** /menu | Pides informacion, sin cambiar nada |
| "Quiero una pizza margherita" | **POST** /pedidos | Creas un pedido nuevo |
| "Cambie la pizza por una napolitana" | **PUT** /pedidos/1 | Reemplazas todo el pedido |
| "Agregue queso extra" | **PATCH** /pedidos/1 | Solo cambias una parte |
| "Ya no quiero nada, cancelo" | **DELETE** /pedidos/1 | Eliminas el recurso |

**¿Que pasa si hay un problema?**

| Respuesta del mesero | Codigo HTTP | Significado |
|---|---|---|
| "Enseguida se lo traigo" | **200 OK** | Todo bien, aqui tienes |
| "Su pedido esta en cocina" | **201 Created** | Se creo correctamente |
| "Disculpe, no entendi" | **400 Bad Request** | La solicitud esta mal hecha |
| "Necesito su identificacion" | **401 Unauthorized** | No has iniciado sesion |
| "Usted no puede ver esa cuenta" | **403 Forbidden** | No tienes permiso |
| "Ese plato no esta en el menu" | **404 Not Found** | La ruta no existe |
| "La pizza no puede tener -3 ingredientes" | **422 Unprocessable Entity** | Datos invalidos |
| "Se quemo la cocina" | **500 Internal Server Error** | Error interno del servidor |

**En detalle tecnico:**

HTTP es el protocolo que permite la comunicacion entre clientes y servidores web. Una solicitud HTTP normalmente incluye:

- **Metodo:** indica la accion deseada (GET, POST, PUT, PATCH, DELETE).
- **URL o ruta:** indica el recurso solicitado (`/cursos`, `/usuarios/1`).
- **Headers:** transportan metadatos (como "idioma acepto: espanol" o "token de seguridad").
- **Body:** contiene datos enviados al servidor (solo en POST, PUT, PATCH).

Codigos de respuesta comunes:

- **200 OK:** solicitud exitosa. Como "aqui tienes lo que pediste".
- **201 Created:** recurso creado. Como "tu pedido ya se registro".
- **400 Bad Request:** solicitud mal formada. Como "no entendi lo que dijiste".
- **401 Unauthorized:** falta autenticacion. Como "muestrame tu identificacion primero".
- **403 Forbidden:** autenticado, pero sin permiso. Como "si, se quien eres, pero no puedes entrar ahi".
- **404 Not Found:** recurso no encontrado. Como "eso que buscas no existe".
- **422 Unprocessable Entity:** datos no validos. Muy comun en FastAPI cuando Pydantic detecta errores. Como "me enviaste un texto donde esperaba un numero".
- **500 Internal Server Error:** error interno del servidor. Como "se rompio algo del otro lado y no sabemos que".

FastAPI ayuda a trabajar estos conceptos de manera clara porque cada endpoint declara metodo, ruta, parametros, tipos de datos y respuesta esperada.

### 4.4 API

> **En espanol simple:** una API es como un mesero en un restaurante. Tu no entras a la cocina a preparar tu comida. Le dices al mesero lo que quieres, el se lo comunica a la cocina, y te trae el resultado. La API es ese mesero: el intermediario que sabe como pedir las cosas y como traer las respuestas.

Una API, o interfaz de programacion de aplicaciones, define una forma controlada para que sistemas distintos se comuniquen.

En el contexto de este curso, una API web permite que un cliente (tu app, tu navegador, tu telefono) consuma funcionalidades del servidor mediante rutas HTTP.

**Ejemplo conceptual:**
- El cliente hace: `GET /cursos` (dame la lista de cursos)
- El servidor responde:

```json
[
  {
    "id": 1,
    "nombre": "Desarrollo Web II",
    "creditos": 3
  }
]
```

**La API es un contrato.** Piensa en un contrato de arrendamiento: ambas partes (arrendador e inquilino) acuerdan reglas claras. En una API pasa igual:
- El **cliente** sabe que puede pedir `GET /cursos` y recibira una lista.
- El **servidor** sabe que cuando llegue `GET /cursos`, debe responder con datos estructurados.

Si ese contrato cambia sin cuidado (ej: antes devolvia `nombre` y ahora devuelve `titulo`), el cliente se rompe. Aparecen errores, caos, reuniones innecesarias y posiblemente alguien diciendo "en mi maquina funciona". Terrible arco argumental.

**Pero... ¿y si no hay internet para probar?**

El docente puede simular una API local con un diccionario de Python (lo veremos en el mini-laboratorio). La ventaja de Python es que puedes practicar este concepto aunque no tengas conexion.

### 4.5 Framework

> **En espanol simple:** un framework es como un kit de herramientas pre-armadas. Imagina que quieres armar un mueble. Puedes cortar la madera, comprar los clavos y hacer todo desde cero. O puedes comprar un kit de IKEA que ya viene con instrucciones, herramientas y piezas listas. El framework es ese kit: te da una base para que no tengas que inventar todo desde cero.

Un framework es un conjunto organizado de herramientas, convenciones y estructuras que facilita el desarrollo de software.

**Sin framework:** tendrias que escribir tu propio servidor web, tu propio sistema de rutas, tu propia validacion de datos, tu propia documentacion... Seria como construir una casa haciendo tus propios ladrillos.

**Con framework:** usas herramientas ya probadas. Solo te concentras en la logica de tu aplicacion.

En desarrollo web, un framework puede ofrecer:

- **Sistema de rutas:** defines que pasa cuando alguien visita `/cursos` o `/usuarios`.
- **Manejo de solicitudes y respuestas:** recibe datos del cliente y envia respuestas.
- **Validacion de datos:** revisa que los datos enviados sean correctos.
- **Inyeccion de dependencias:** conecta componentes entre si.
- **Integracion con plantillas:** genera HTML si es necesario.
- **Seguridad:** protege contra ataques comunes.
- **Middleware:** ejecuta codigo antes o despues de cada solicitud.
- **Documentacion:** genera documentacion automatica de tu API.
- **Pruebas:** facilita probar tu codigo.
- **Conexion con bases de datos:** interactua con BD de forma sencilla.

> **Importante:** Usar un framework no significa que el framework piense por el desarrollador. Significa que proporciona una base comun para resolver problemas repetitivos. El criterio tecnico sigue siendo responsabilidad humana. El framework entrega la espada; no garantiza que el jugador sepa esquivar.

**Dato clave:** FastAPI es nuestro framework. Pero no es el unico. Existen Django, Flask (Python), Laravel (PHP), Spring Boot (Java), Next.js (JavaScript)... Todos resuelven problemas similares, pero cada uno tiene su personalidad. En este curso nos enfocamos en FastAPI porque es moderno, rapido y perfecto para aprender buenas practicas.

## 5. Por que FastAPI en Desarrollo Web II

FastAPI es un framework moderno de Python para construir APIs rapidas, tipadas y documentadas automaticamente.

Sus ventajas pedagogicas para este curso son:

- Permite comprender claramente rutas, metodos HTTP y respuestas.
- Usa tipado de Python para validar datos.
- Integra Pydantic para modelos de entrada y salida.
- Genera documentacion OpenAPI automaticamente.
- Facilita pruebas con herramientas como TestClient.
- Permite trabajar seguridad, OAuth2, JWT, CORS y middleware.
- Es adecuado para aplicaciones modernas orientadas a servicios y APIs.

FastAPI tambien permite reinterpretar temas tradicionales del syllabus:

| Tema del syllabus | Adaptacion en FastAPI |
|---|---|
| MVC | Separacion de responsabilidades: routers, schemas, services, models, templates |
| Controladores | Funciones de ruta y APIRouter |
| Modelos | Entidades, schemas Pydantic y modelos de persistencia |
| Vistas | Respuestas JSON y plantillas Jinja2 cuando se requiera HTML |
| Middleware | Middleware ASGI, dependencias y filtros transversales |
| Seguridad | OAuth2, JWT, hashing, CORS, validacion y manejo seguro de errores |
| APIs | Endpoints HTTP documentados con OpenAPI |

Esta adaptacion evita forzar FastAPI dentro de una etiqueta que no le pertenece por completo. No todo debe parecer Laravel o ASP.NET MVC para ser pedagogicamente valido. A veces la madurez tecnica consiste en no ponerle armadura medieval a un droide.

## 6. Diagnostico inicial sugerido

El diagnostico no debe sentirse como examen sorpresa de jefe final. Su objetivo es reconocer el punto de partida del grupo.

### 6.1 Preguntas de discusion

1. Que diferencia hay entre una pagina web y una aplicacion web?
2. Que ocurre cuando un navegador visita una URL?
3. Que es una API?
4. Que metodos HTTP conocen?
5. Que significa que una respuesta tenga codigo 404?
6. Que ventajas ofrece usar un framework?
7. Que problemas aparecen cuando una aplicacion no separa responsabilidades?
8. Que conocimientos previos tienen de Python?
9. Han usado Swagger UI para explorar APIs?
10. Que entienden por seguridad en aplicaciones web?

### 6.2 Actividad diagnostica rapida

**Actividad:** Analisis de una aplicacion web conocida.

El docente pide a los estudiantes seleccionar una aplicacion web que usen con frecuencia: plataforma academica, tienda en linea, red social, servicio bancario, sistema de reservas, gestor de tareas o videojuego con servicios web.

Los estudiantes identifican:

- Que acciones realiza el usuario.
- Que datos solicita o envia.
- Que posibles rutas o endpoints existirian en el backend.
- Que datos deberian protegerse.
- Que errores podrian ocurrir.
- Que partes podrian desarrollarse con FastAPI.

Ejemplo:

Aplicacion: plataforma academica.

| Accion del usuario | Posible endpoint | Metodo | Datos sensibles |
|---|---:|---:|---|
| Consultar cursos matriculados | `/estudiantes/{id}/cursos` | GET | Identidad del estudiante |
| Registrar asistencia | `/asistencias` | POST | Fecha, curso, estudiante |
| Ver calificaciones | `/estudiantes/{id}/notas` | GET | Notas academicas |
| Actualizar perfil | `/usuarios/{id}` | PATCH | Correo, telefono |

## 7. Mini-laboratorio: consumir una API publica con Python

Este mini-laboratorio permite mostrar que una API no es una idea abstracta encerrada en un diagrama bonito. Es una conversacion real entre sistemas. Tu script de Python va a hablar con los servidores de GitHub y pedir informacion.

### 7.1 Objetivo

Consumir una API publica desde Python, revisar la respuesta JSON e identificar componentes del flujo HTTP.

### 7.2 Requisitos

- Python instalado (3.8 o superior).
- Entorno virtual recomendado (para no mezclar librerias).
- Libreria `requests` (la instalaremos ahora).

Instalacion:

```bash
pip install requests
```

> **Explicacion:** `requests` es una libreria que permite hacer solicitudes HTTP desde Python de forma sencilla. Sin ella, tendriamos que usar modulos mas complejos como `urllib`. `requests` hace que el codigo sea mas legible.

### 7.3 Codigo base - con explicacion linea por linea

Aqui tienes el codigo completo PRIMERO para que lo veas de una sola vez, y DESPUES lo explicamos linea por linea:

```python
import requests

url = "https://api.github.com/repos/tiangolo/fastapi"

response = requests.get(url)

print("Codigo de estado:", response.status_code)

data = response.json()

print("Nombre:", data["name"])
print("Descripcion:", data["description"])
print("Estrellas:", data["stargazers_count"])
print("Lenguaje:", data["language"])
```

#### Desglose linea por linea (lo mas importante para entender):

```python
import requests
```
**Esto hace:** importa la libreria `requests` para poder usarla. Sin esta linea, no podrias hacer solicitudes HTTP.

```python
url = "https://api.github.com/repos/tiangolo/fastapi"
```
**Esto hace:** guarda en una variable llamada `url` la direccion del recurso que queremos consultar. En este caso, es la URL del repositorio de FastAPI en GitHub.

> **Pregunta frecuente:** ¿Como supe que esa era la URL correcta? La documentacion de la API de GitHub la define. Cada API tiene su propia "carta" de URLs disponibles.

```python
response = requests.get(url)
```
**Esto hace:** envia una solicitud HTTP **GET** a la URL que definimos. El servidor de GitHub responde y guardamos toda esa respuesta en la variable `response`.

**GET** significa "dame informacion". No estamos creando ni modificando nada, solo consultando.

```python
print("Codigo de estado:", response.status_code)
```
**Esto hace:** imprime en pantalla el codigo de estado HTTP que devolvio el servidor. Si todo sale bien, veras `200`. Si ves `404`, la URL no existe. Si ves `403`, GitHub te nego el acceso.

```python
data = response.json()
```
**Esto hace:** convierte la respuesta del servidor (que viene en formato JSON) a un diccionario de Python. JSON es el formato estandar para intercambiar datos entre sistemas. Es como un diccionario con `clave: valor`.

```python
print("Nombre:", data["name"])
```
**Esto hace:** del diccionario `data`, obtiene el valor asociado a la clave `"name"` y lo imprime.

> **Analogia:** imagina que recibes una caja con etiquetas. `data["name"]` es como abrir la caja etiquetada "name" y sacar lo que hay dentro.

### 7.4 Preguntas para analizar

1. **Que metodo HTTP se uso?** (Respuesta: GET, porque solo estamos consultando)
2. **Que recurso se solicito?** (El repositorio `tiangolo/fastapi` en GitHub)
3. **Que codigo de estado respondio el servidor?** (200 si funciono)
4. **Que tipo de dato recibimos?** (JSON, que Python convierte a diccionario)
5. **Que pasaria si la URL no existe?** (Recibiras un error, o codigo 404)
6. **Por que es util que la respuesta tenga una estructura predecible?** (Porque sabes exactamente donde buscar cada dato: `data["name"]` siempre te dara el nombre)

### 7.5 Variante sin depender de GitHub (cuando no hay internet)

Si no hay internet o la red decide hacer cosplay de firewall corporativo, el docente puede simular una respuesta JSON local usando un diccionario de Python:

```python
curso = {
    "id": 1,
    "nombre": "Desarrollo Web II",
    "framework": "FastAPI",
    "creditos": 3,
    "temas": ["HTTP", "APIs", "MVC", "Seguridad"]
}

print(curso["nombre"])       # Imprime: Desarrollo Web II
print(curso["framework"])    # Imprime: FastAPI
print(curso["temas"][0])     # Imprime: HTTP (el primer elemento de la lista)
```

**¿Que esta pasando aqui?**
- Creamos un diccionario llamado `curso` con varias claves (`id`, `nombre`, `framework`, etc.)
- Accedemos a los valores usando `curso["clave"]`
- `curso["temas"]` devuelve una lista, y con `[0]` accedemos al primer elemento

Esto simula lo que pasaria si hubieramos recibido un JSON de un servidor real. La logica es identica: recibes datos estructurados y extraes la informacion que necesitas.

### 7.6 Errores comunes y como resolverlos

| Error tipico | Por que ocurre | Como solucionarlo |
|---|---|---|
| `ModuleNotFoundError: No module named 'requests'` | No instalaste la libreria `requests` | Ejecuta `pip install requests` |
| `NameError: name 'requests' is not defined` | Olvidaste poner `import requests` al inicio | Agrega `import requests` al principio del archivo |
| `KeyError: 'name'` | La API cambio la estructura y ya no tiene esa clave | Imprime `data.keys()` para ver que claves estan disponibles |
| `ConnectionError` | No tienes internet o la URL esta mal | Verifica tu conexion y que la URL sea correcta |
| `IndentationError` | Olvidaste indentar (espacios) correctamente | Python es sensible a la indentacion. Revisa espacios y tabulaciones |

## 8. Cierre conceptual de la clase

### ¿Que aprendimos hoy?

Hoy construimos los cimientos. Antes de escribir una sola linea de FastAPI, entendemos:

1. **Que es una aplicacion web:** no es solo una pagina bonita, es un sistema con cliente, servidor, API, BD y seguridad trabajando juntos.
2. **Como funciona cliente-servidor:** el cliente pide, el servidor responde. 7 pasos simples que ocurren en segundos.
3. **Que es HTTP:** es el idioma que hablan cliente y servidor. Verbos (GET, POST, PUT, PATCH, DELETE) y codigos de estado (200, 404, 500, etc.).
4. **Que es una API:** el mesero entre el cliente y el servidor. Un contrato que define como se pide y como se responde.
5. **Que es un framework:** un kit de herramientas que evita que reinventemos la rueda. FastAPI es nuestro framework.
6. **Que es JSON:** el formato en que los datos viajan entre sistemas. Como un diccionario de Python con `clave: valor`.

### ¿Que sigue?

En la **Clase 02** veremos como organizar todo esto en una arquitectura limpia usando el patron MVC y FastAPI. Pasaremos de consumir APIs a construir las nuestras.

Al finalizar la clase, el estudiante debe comprender que el curso no se limita a "aprender comandos de FastAPI". El objetivo es aprender a estructurar aplicaciones web con criterio, a usar frameworks para resolver problemas reales y a construir APIs seguras, mantenibles y comprensibles.

FastAPI sera la herramienta principal, pero el aprendizaje de fondo es mas amplio:

- entender solicitudes y respuestas;
- modelar recursos;
- separar responsabilidades;
- validar datos;
- construir rutas;
- proteger informacion;
- documentar y probar servicios;
- trabajar en equipo sobre un proyecto integrador.

La primera clase instala el vocabulario comun. Sin ese vocabulario, el resto del curso se vuelve una pelea contra errores que parecen escritos por un villano con acceso a Stack Overflow.

## 9. Trabajo independiente (6 horas sugeridas)

Para la siguiente clase, los estudiantes deben preparar:

### 9.1 Mapa conceptual (2 horas)

Crea un mapa conceptual (puede ser en papel, en una herramienta como Canva, Miro, o incluso en tu cuaderno) que conecte estos conceptos:

```
APLICACION WEB
  ├── Cliente (navegador, app movil)
  ├── Servidor (donde vive la logica)
  ├── API (el intermediario)
  │     └── HTTP (el idioma: GET, POST, PUT, DELETE)
  ├── Base de datos (donde se guarda la info)
  └── Framework (kit de herramientas: FastAPI)
```

**Ejemplo de conexion:** "El cliente usa HTTP (GET) para pedir datos a la API, la API se comunica con el servidor, el servidor consulta la BD y devuelve los datos en formato JSON."

### 9.2 Matriz comparativa de frameworks (2 horas)

Investiga y completa esta tabla comparando al menos 3 frameworks:

| Caracteristica | FastAPI | Django | Flask |
|---|---|---|---|
| Lenguaje | Python | Python | Python |
| Tipo | API moderno | Web completo | Minimo |
| Dificultad | Baja-media | Alta | Baja |
| Documentacion automatica | Si (OpenAPI) | No nativa | No nativa |
| Tipado | Si (Python typing) | No obligatorio | No obligatorio |

Puedes cambiar Django/Flask por Laravel (PHP), Spring Boot (Java), Next.js (JavaScript) o cualquier otro que conozcas o te interese.

### 9.3 Idea inicial de proyecto (2 horas)

Escribe una descripcion de 5-10 lineas de una posible aplicacion/API que te gustaria desarrollar durante el curso. No necesitas saber como programarla aun. Solo describe:

- **¿Que problema resuelve?** (ej: "una API para gestionar prestamos de libros en la biblioteca")
- **¿Quien la usaria?** (ej: "bibliotecarios y estudiantes")
- **¿Que recursos principales tendria?** (ej: "libros, autores, prestamos, usuarios")
- **¿Que acciones basicas?** (ej: "crear libro, listar libros, prestar libro, devolver libro")

**No te preocupes por los detalles tecnicos aun.** Esto es solo una lluvia de ideas que podremos refinar durante el curso. Lo importante es que empieces a pensar como disenador de sistemas, no solo como programador.

## 10. Producto esperado de la semana

**Evidencia sugerida:** diagnostico inicial + mapa conceptual + idea de proyecto.

### Checklist de entregable

Antes de la siguiente clase, asegurate de tener:

- [ ] **Diagnostico inicial respondido** (las 10 preguntas de discusion de la seccion 6.1). No importa si no sabes todas las respuestas. El diagnostico es para medir tu punto de partida.
- [ ] **Mapa conceptual** conectando: Aplicacion Web, Cliente, Servidor, HTTP, API, JSON, Framework, FastAPI.
- [ ] **Matriz comparativa** de al menos 3 frameworks (FastAPI + otros 2).
- [ ] **Idea inicial de proyecto** (5-10 lineas describiendo una posible API).

### El producto debe mostrar que identificas:

- componentes de una aplicacion web;
- flujo cliente-servidor;
- papel de HTTP;
- utilidad de una API;
- funcion de un framework;
- razones iniciales para estudiar FastAPI.

## 11. Bibliografia y referencias utiles

- FastAPI. (s. f.). *FastAPI Documentation*. https://fastapi.tiangolo.com/
- MDN Web Docs. (s. f.). *HTTP*. https://developer.mozilla.org/
- Fielding, R. (2000). *Architectural Styles and the Design of Network-based Software Architectures*.
- OWASP Foundation. (s. f.). *OWASP API Security Top 10*. https://owasp.org/API-Security/
- Pydantic. (s. f.). *Pydantic Documentation*. https://docs.pydantic.dev/
