# Ejercicios - Clase 01

> **Nota para el estudiante:** No importa si al principio no sabes todas las respuestas. Estos ejercicios son para practicar, no para examinarte. Si te atascas, revisa la guia de la clase o pregunta al docente.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las siguientes frases con las palabras del recuadro:

> **Palabras:** API | Cliente | Servidor | HTTP | GET | JSON | Framework | 200

1. El _________ es quien solicita informacion (ej: navegador, app movil).
2. El _________ es quien procesa la solicitud y responde.
3. _________ es el protocolo de comunicacion entre cliente y servidor.
4. El metodo _________ se usa para obtener informacion.
5. Una _________ es un intermediario que permite que sistemas se comuniquen.
6. El formato _________ se usa para intercambiar datos estructurados.
7. El codigo _________ significa que la solicitud fue exitosa.
8. Un _________ es un kit de herramientas que facilita el desarrollo.

---

## Ejercicio 1. Identificacion de componentes web

Seleccione una aplicacion web que use con frecuencia (Instagram, Netflix, YouTube, plataforma academica, banco, etc.) e identifique:

- **Cliente o clientes posibles:** (ej: app movil, navegador web)
- **Servidor o servicios principales:** (ej: servidores de Instagram)
- **Datos que se envian:** (ej: fotos, likes, comentarios)
- **Datos que se reciben:** (ej: feed de fotos, notificaciones)
- **Acciones principales del usuario:** (ej: publicar foto, dar like, comentar)
- **Riesgos de seguridad visibles:** (ej: datos personales, contrasenas)

**Producto:** tabla corta con minimo cinco acciones del usuario.

**Ejemplo parcial:**

| Accion | Que datos envia | Que recibe |
|---|---|---|
| Iniciar sesion | Usuario y contrasena | Token de acceso |
| Ver feed | Nada (solo pide) | Lista de publicaciones |
| Dar like | ID de la publicacion | Confirmacion |
| Comentar | Texto del comentario | Comentario publicado |
| Cerrar sesion | Token de acceso | Confirmacion |

---

## Ejercicio 2. Metodos HTTP

Relacione cada accion con el metodo HTTP mas apropiado:

| Accion | Metodo sugerido |
|---|---|
| Consultar lista de cursos | GET |
| Crear un nuevo estudiante | |
| Actualizar el correo de un usuario | |
| Eliminar una tarea | |
| Consultar una calificacion especifica | |

**Ayuda:** recuerda la analogia del restaurante:
- **GET** = mirar el menu (solo consulta)
- **POST** = hacer un pedido nuevo (crear)
- **PUT/PATCH** = modificar un pedido (actualizar)
- **DELETE** = cancelar un pedido (eliminar)

Despues justifique cada respuesta en una frase. Ejemplo: "GET para consultar cursos porque solo quiero ver la informacion, no modificarla."

---

## Ejercicio 3. Diseno inicial de endpoints

Imagine una API para administrar una biblioteca academica.

Proponga endpoints para:
- listar libros;
- consultar un libro por id;
- registrar un libro;
- actualizar datos de un libro;
- eliminar un libro;
- listar prestamos activos.

Use esta estructura:

```text
Metodo: GET
Ruta: /libros
Descripcion: lista todos los libros registrados.
```

**Ejemplo de respuesta parcial:**

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | /libros | Listar todos los libros |
| GET | /libros/{id} | Consultar un libro por su ID |
| POST | /libros | Registrar un libro nuevo |
| PUT | /libros/{id} | Actualizar datos de un libro |
| DELETE | /libros/{id} | Eliminar un libro |
| GET | /prestamos?activos=true | Listar prestamos activos |

> **Pista:** `{id}` significa que el ID se reemplaza por un numero real, ej: `/libros/5`

---

## Ejercicio 4. Analisis de respuesta JSON

Revise el siguiente JSON que devuelve una API de cursos:

```json
{
  "id": 7,
  "nombre": "Desarrollo Web II",
  "creditos": 3,
  "framework": "FastAPI",
  "activo": true
}
```

Responda:

1. **¿Que tipo de dato tiene `id`?** (pista: es un numero entero)
2. **¿Que tipo de dato tiene `activo`?** (pista: es verdadero o falso)
3. **¿Que campo podria usarse para filtrar cursos por framework?** (pista: el nombre del campo donde dice "FastAPI")
4. **¿Que validaciones aplicaria antes de guardar estos datos?** (ej: "el nombre no debe estar vacio", "los creditos deben ser positivos")

**Respuesta esperada (para que verifiques):**
1. `id` es un numero entero (`int`)
2. `activo` es un booleano (`bool`): verdadero o falso
3. El campo `framework` permitiria filtrar ("dame todos los cursos donde framework = FastAPI")
4. Validaciones posibles: `nombre` no vacio, `creditos` > 0, `framework` debe ser un string valido

---

## Ejercicio 5. Reflexion tecnica

Explique en un parrafo:

**¿Por que un framework puede mejorar la calidad de una aplicacion web, pero no garantiza automaticamente que la aplicacion este bien disenada?**

**Ayuda:** piensa en la analogia del kit de herramientas. Tener un martillo y una sierra no te convierte en carpintero. El framework da las herramientas, pero el criterio para usarlas bien es tuyo.

Sea concreto. No invoque "buenas practicas" como frase magica sin explicar nada. Eso no compila.
