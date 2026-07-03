# Clase 03 - Frameworks web: comparacion y eleccion tecnica

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 3  
**Unidad:** Unidad 1 - Introduccion a MVC y Frameworks  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA2: Analizar las ventajas y desventajas de utilizar frameworks en el desarrollo de aplicaciones web mediante la comparacion de diferentes frameworks y su aplicabilidad en distintos contextos.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

Esta clase busca que el estudiante compare frameworks web desde criterios tecnicos y pedagogicos, no desde gusto personal, moda o guerra de fandom. El objetivo es comprender que ningun framework es "el mejor" en abstracto. Cada framework responde mejor o peor dependiendo del problema, el equipo, el ecosistema, el tiempo disponible, los requisitos de seguridad, el tipo de aplicacion y la experiencia previa.

FastAPI sera el framework central del curso, pero eso no significa ignorar alternativas. Al contrario: entender por que se elige FastAPI requiere compararlo con otros frameworks como Django, Flask, Laravel y ASP.NET Core MVC.

La clase prepara a los estudiantes para justificar decisiones tecnicas. Elegir una tecnologia sin justificarla es como escoger personaje en un RPG solo porque tiene capa: puede funcionar, pero no es exactamente ingenieria.

## 3. Pregunta orientadora

**Como elegir un framework web segun el problema que se quiere resolver?**

Esta pregunta obliga a mirar mas alla de la sintaxis. Elegir framework implica analizar contexto, restricciones, comunidad, seguridad, escalabilidad, productividad y mantenibilidad.

## 4. Que significa elegir un framework

> **En espanol simple:** elegir un framework es como elegir un tipo de vehiculo para un viaje. No es solo "me gusta el color rojo". Es analizar: ¿vamos por ciudad o carretera? ¿cuanta carga llevamos? ¿cuantos pasajeros? ¿que presupuesto tenemos? Cada vehiculo es bueno para algo distinto.

Elegir un framework no es solo escoger una herramienta. Es adoptar:

- una forma de estructurar proyectos;
- una comunidad y ecosistema;
- convenciones de desarrollo;
- mecanismos de seguridad;
- estrategias de despliegue;
- estilo de pruebas;
- dependencias;
- curva de aprendizaje;
- posibilidades de contratacion y soporte.

**Analogia para entenderlo mejor:**

| Tipo de vehiculo | Framework equivalente | Para que es bueno |
|---|---|---|
| **Bicicleta** | Flask | Proyectos pequeños, flexibles, una persona |
| **Auto familiar** | Django | Aplicaciones completas, todo incluido, equipo grande |
| **Moto deportiva** | FastAPI | APIs rapidas, modernas, especificas |
| **Camioneta** | Laravel | Apps web tradicionales, mucha carga de trabajo |
| **Camion blindado** | ASP.NET Core | Sistemas empresariales, seguridad, largo plazo |

Un framework acelera decisiones, pero tambien introduce compromisos. Cada ventaja suele traer un costo.

Ejemplo:

- Un framework muy completo (auto familiar) puede aumentar productividad, pero traer mas convenciones y complejidad inicial.
- Un microframework (bicicleta) puede ser flexible, pero exigir mas decisiones arquitectonicas al equipo.
- Un framework orientado a APIs (moto deportiva) puede ser excelente para servicios, pero no necesariamente el mas comodo para paneles administrativos tradicionales.

> **La clave:** No existe "el mejor framework". Existe "el framework mas adecuado para TU problema".

## 5. Criterios para comparar frameworks

> **En espanol simple:** para comparar frameworks necesitas saber QUE mirar. Aqui tienes 7 criterios con los que puedes evaluar cualquier framework. Piensa en cada criterio como una "pregunta que hacerte antes de elegir".

### 5.1 Tipo de aplicacion

> **En espanol simple:** ¿QUE vas a construir? No es lo mismo construir un API para una app movil que un panel administrativo para una empresa. Cada framework tiene su especialidad.

No todas las aplicaciones web son iguales.

Tipos comunes:

- **API REST** para consumo por frontend o app movil.
- **Aplicacion monolitica** con vistas HTML.
- **Panel administrativo**.
- **Microservicio**.
- **Sistema empresarial robusto**.
- **Prototipo rapido**.
- **Aplicacion en tiempo real**.
- **Backend para inteligencia artificial o ciencia de datos**.

**Preguntate:** ¿mi proyecto es un carrito de compras, una red social, un sistema de gestion o un API para una app?

FastAPI brilla especialmente en APIs, microservicios, servicios Python y backends donde la validacion y documentacion automatica importan bastante.

### 5.2 Productividad

> **En espanol simple:** ¿QUE TAN RAPIDO puedes construir cosas con este framework? Algunos frameworks ya vienen con muchas herramientas listas (como Django). Otros te dan lo minimo y tu agregas lo que necesitas (como Flask).

Un framework productivo permite construir funcionalidades comunes con menos friccion.

Preguntas para evaluar un framework:

- ¿Cuanto codigo repetitivo exige?
- ¿Tiene generadores o convenciones claras?
- ¿Incluye validacion, seguridad y documentacion?
- ¿Facilita pruebas?
- ¿Tiene integracion madura con bases de datos?

**Analogia:** Django es como una cocina industrial: tiene todos los electrodomesticos (ORM, admin, autenticacion, formularios). FastAPI es como una cocina moderna con solo lo esencial: los cuchillos son excelentes (Pydantic, OpenAPI), pero necesitas comprar el horno (ORM) y la batidora (autenticacion) por separado.

### 5.3 Curva de aprendizaje

> **En espanol simple:** ¿QUE TAN DIFICIL es aprender este framework? Algunos frameworks son faciles de empezar pero dificiles de dominar. Otros son dificiles al principio pero luego todo fluye.

La curva de aprendizaje depende del framework y del perfil del equipo.

Factores:

- lenguaje base;
- cantidad de conceptos iniciales;
- convenciones;
- documentacion;
- comunidad;
- herramientas de depuracion;
- experiencia previa del grupo.

**Preguntate:** ¿cuanto tiempo tengo para aprender antes de producir? ¿mi equipo ya conoce Python o tengo que enseñarlo tambien?

> FastAPI puede ser amigable si el estudiante conoce Python y tipos basicos. Pero si no domina Python, Pydantic, async o HTTP, puede parecer magia. Y la magia sin explicacion en desarrollo suele terminar en Stack Trace: The Animation.

### 5.4 Seguridad

> **En espanol simple:** ¿QUE TAN SEGURO es este framework por defecto? Algunos frameworks ya vienen con protecciones incorporadas (Django). Otros te dan las herramientas pero tu debes configurarlas (FastAPI).

La seguridad no depende solo del framework, pero el framework puede ayudar.

Criterios:

- autenticacion (inicio de sesion);
- autorizacion (permisos);
- proteccion CSRF (para formularios web);
- manejo de CORS (para APIs);
- validacion de entrada;
- sanitizacion;
- hashing de contrasenas;
- proteccion contra inyeccion SQL;
- gestion de sesiones o tokens;
- manejo seguro de errores.

**Preguntate:** ¿mi aplicacion manejara datos sensibles? ¿necesito autenticacion de usuarios? ¿el framework ya protege contra ataques comunes o tengo que hacerlo yo?

Django incluye muchas protecciones listas para aplicaciones server-rendered. FastAPI ofrece herramientas para seguridad en APIs, pero exige que el desarrollador integre correctamente dependencias, tokens, hashing, CORS y manejo de permisos.

### 5.5 Documentacion y comunidad

> **En espanol simple:** ¿QUE TAN FACIL es encontrar ayuda cuando te atascas? Un framework con buena documentacion y comunidad activa es como tener un manual de usuario + un grupo de WhatsApp donde siempre responden.

Un framework con buena documentacion reduce tiempo de aprendizaje y errores.

Preguntas para evaluar:

- ¿La documentacion oficial es clara?
- ¿Hay ejemplos actualizados?
- ¿La comunidad responde dudas (Stack Overflow, Discord, GitHub)?
- ¿Hay paquetes mantenidos por terceros?
- ¿Existen buenas practicas reconocidas?

**Preguntate:** ¿cuando tenga un error, encontrare solucion rapido en Google o estare solo frente al abismo?

FastAPI tiene documentacion muy didactica y generacion automatica de documentacion OpenAPI, lo que es una ventaja fuerte para APIs.

### 5.6 Rendimiento y escalabilidad

> **En espanol simple:** ¿QUE TAN RAPIDO responde el framework cuando hay muchos usuarios? El rendimiento importa, pero no siempre es lo mas importante.

El rendimiento importa, pero rara vez es el unico criterio. Muchas aplicaciones fallan por mal diseno, consultas lentas o mala arquitectura antes que por el framework.

**Analogia:** Un motor potente (rendimiento) no salva a un conductor que maneja directo al muro (mal diseno). Primero aprende a manejar, luego preocupate por la velocidad.

FastAPI, al estar sobre ASGI y Starlette, tiene buen rendimiento para APIs, especialmente cuando se trabaja con operaciones I/O y servicios asincronos.

**Preguntate:** ¿mi app tendra 10 usuarios o 10 millones? ¿el cuello de botella será el framework o mi codigo/BD?

Pero cuidado: elegir un framework rapido no arregla codigo lento, consultas absurdas ni modelos de datos mal disenados. Un motor potente no salva a un conductor que maneja directo al muro.

### 5.7 Ecosistema y empleabilidad

> **En espanol simple:** ¿HAY TRABAJO para este framework? ¿Hay librerias, herramientas y personas que lo usan? No importa solo lo bueno que es tecnicamente, sino si puedes encontrar gente que sepa usarlo y empresas que lo contraten.

Tambien importa el ecosistema laboral y tecnico:

- ¿Hay desarrolladores disponibles en el mercado?
- ¿Se integra con herramientas del sector?
- ¿Es comun en empresas?
- ¿Tiene soporte a largo plazo?
- ¿Encaja con el stack tecnologico de la organizacion?

**Preguntate:** ¿cuando termine el curso, podre conseguir trabajo con este framework? ¿las empresas de mi zona lo usan?

Laravel es muy fuerte en ecosistemas PHP. ASP.NET Core MVC es frecuente en entornos Microsoft empresariales. Django tiene larga trayectoria en Python. FastAPI ha ganado fuerza en APIs modernas, servicios de datos, IA y microservicios.

## 6. Frameworks comparados (con ficha rapida)

> **En espanol simple:** aqui tienes una "ficha tecnica" de cada framework con sus fortalezas, debilidades y para que sirve cada uno. Usa esto como referencia cuando tengas que elegir.

### 6.1 FastAPI — "La moto deportiva"

| Aspecto | Descripcion |
|---|---|
| **Analogia** | Moto deportiva: rapida, moderna, disenada para una mision especifica (APIs) |
| **Lenguaje** | Python |
| **Tipo** | Framework de APIs moderno |
| **Eslogan** | "Construye APIs rapidas con Python moderno" |

**Fortalezas:**

- Excelente para APIs REST.
- Validacion con Pydantic.
- Documentacion OpenAPI automatica (Swagger UI en `/docs` sin escribir una linea).
- Buen rendimiento (ASGI).
- Soporte para async.
- Integracion natural con ecosistema Python (Pandas, NumPy, IA, ML).
- Muy util para servicios de datos, IA, automatizacion y microservicios.

**Limitaciones:**

- No trae ORM oficial obligatorio.
- No trae panel admin completo de fabrica.
- Requiere decisiones adicionales sobre estructura, persistencia y autenticacion.
- Para vistas HTML tradicionales, puede requerir mas configuracion que frameworks monoliticos.

**¿Cuando usarlo?**

- APIs modernas.
- Microservicios.
- Backends para frontend separado.
- Servicios conectados con ciencia de datos o IA.
- Proyectos donde la documentacion de API sea importante.

---

### 6.2 Django — "El auto familiar"

| Aspecto | Descripcion |
|---|---|
| **Analogia** | Auto familiar: trae todo incluido, seguro, confiable, pero pesado para viajes cortos |
| **Lenguaje** | Python |
| **Tipo** | Full-stack (completo) |
| **Eslogan** | "El framework web de Python para perfeccionistas con plazos" |

**Fortalezas:**

- Incluye ORM, admin, autenticacion, formularios y plantillas. **Todo listo.**
- Muy maduro (existe desde 2005).
- Buen ecosistema.
- Excelente para aplicaciones monoliticas y paneles administrativos.
- Convenciones claras: "El framework de Django te dice como hacer las cosas".

**Limitaciones:**

- Puede sentirse pesado para microservicios simples.
- La construccion de APIs modernas suele apoyarse en Django REST Framework (DRF).
- Tiene mas conceptos iniciales que aprender.

**¿Cuando usarlo?**

- Sistemas administrativos.
- Aplicaciones monoliticas.
- Proyectos donde el admin y ORM sean centrales.
- Equipos que quieren muchas decisiones resueltas por el framework.

---

### 6.3 Flask — "La bicicleta"

| Aspecto | Descripcion |
|---|---|
| **Analogia** | Bicicleta: simple, ligera, flexible, pero tu decides la ruta y el esfuerzo |
| **Lenguaje** | Python |
| **Tipo** | Microframework (minimalista) |
| **Eslogan** | "Minimo, flexible, tu decides" |

**Fortalezas:**

- Simple para empezar ("Hola mundo" en 5 lineas).
- Muy flexible (no impone estructuras).
- Buen ecosistema de extensiones (Flask-SQLAlchemy, Flask-Login, etc.).
- Adecuado para prototipos y servicios pequenos.

**Limitaciones:**

- Muchas decisiones quedan a cargo del equipo.
- Puede volverse desordenado sin arquitectura (cada quien hace lo que quiere).
- No trae validacion, documentacion ni estructura fuerte por defecto.

**¿Cuando usarlo?**

- Prototipos.
- APIs pequenas.
- Servicios donde se quiere control fino.
- Aprendizaje inicial de conceptos web.

---

### 6.4 Laravel — "La camioneta"

| Aspecto | Descripcion |
|---|---|
| **Analogia** | Camioneta: carga mucha carga util, ideal para apps web tradicionales, pero ocupa espacio |
| **Lenguaje** | PHP |
| **Tipo** | Full-stack |
| **Eslogan** | "El framework PHP para artesanos de la web" |

**Fortalezas:**

- Ecosistema amplio (Laravel Nova, Forge, Vapor, etc.).
- Buenas herramientas para rutas, ORM (Eloquent), migraciones, autenticacion y plantillas (Blade).
- Alta productividad.
- Comunidad grande.

**Limitaciones:**

- Requiere ecosistema PHP (no Python).
- No es el enfoque central de este curso.
- Para servicios Python o IA no encaja tan naturalmente.

**¿Cuando usarlo?**

- Aplicaciones web tradicionales.
- Sistemas con vistas server-rendered.
- Proyectos PHP con alta productividad.
- Equipos familiarizados con Laravel.

---

### 6.5 ASP.NET Core MVC — "El camion blindado"

| Aspecto | Descripcion |
|---|---|
| **Analogia** | Camion blindado: robusto, seguro, empresarial, pero pesado y requiere chofer especializado |
| **Lenguaje** | C# (.NET) |
| **Tipo** | Full-stack/API |
| **Eslogan** | "La opcion empresarial para aplicaciones robustas" |

**Fortalezas:**

- Muy fuerte en entornos empresariales.
- Buen rendimiento (compilado, no interpretado).
- Integracion con ecosistema Microsoft (Azure, Active Directory, SQL Server).
- Soporte para MVC, APIs, seguridad, inyeccion de dependencias y despliegue empresarial.

**Limitaciones:**

- Requiere C# y ecosistema .NET (diferente a Python).
- Puede tener una curva inicial alta para estudiantes sin experiencia en ese entorno.
- No se alinea directamente con el ecosistema Python del curso.

**¿Cuando usarlo?**

- Aplicaciones empresariales.
- Organizaciones con infraestructura Microsoft.
- Sistemas robustos de largo plazo.

## 7. Matriz comparativa

> **En espanol simple:** esta tabla te permite ver TODOS los frameworks lado a lado con los mismos criterios. Es como una tabla comparativa de celulares: ves las especificaciones de todos al mismo tiempo y decides cual te conviene.

### Como leer esta matriz:

- Cada **fila** es un criterio de comparacion.
- Cada **columna** es un framework.
- Lee de izquierda a derecha: busca el criterio que mas te importa (ej: "validacion") y mira cual framework lo tiene mejor.

| Criterio | FastAPI | Django | Flask | Laravel | ASP.NET Core MVC |
|---|---|---|---|---|---|
| **Lenguaje** | Python | Python | Python | PHP | C# |
| **Tipo principal** | APIs | Full-stack | Microframework | Full-stack | Full-stack/API |
| **Curva inicial** | Media | Media-alta | Baja-media | Media | Media-alta |
| **Validacion** | Muy fuerte con Pydantic | Formularios/DRF | Depende de extensiones | Integrada | Integrada |
| **Documentacion API** | OpenAPI automatica | Con DRF/extensiones | Manual/extensiones | Paquetes | Integrada/extensiones |
| **Admin listo** | No nativo | **Si** | No | Parcial/ecosistema | No igual a Django |
| **Flexibilidad** | Alta | Media | **Muy alta** | Media | Media |
| **Estructura por defecto** | Media | **Alta** | Baja | Alta | Alta |
| **Ideal para** | APIs modernas | Monolitos/admin | Prototipos | Apps web PHP | Empresa .NET |

> **Nota importante:** Ningun framework gana en TODAS las categorias. La "mejor" opcion depende de que criterios son mas importantes para TU proyecto. Si necesitas admin listo, Django gana. Si necesitas APIs con documentacion automatica, FastAPI gana. Si necesitas algo simple y rapido, Flask gana. **No hay ganador universal.**

## 8. Como construir una decision tecnica (plantilla paso a paso)

> **En espanol simple:** elegir un framework no es "me gusta mas este". Es un proceso de 7 pasos. Aqui tienes una plantilla que puedes usar para tomar cualquier decision tecnica, no solo frameworks.

### Los 7 pasos para decidir:

| Paso | Pregunta que responder | Ejemplo |
|---|---|---|
| **1. Problema** | ¿Que necesito construir? | "Una API para que una app movil consulte cursos y notas" |
| **2. Restricciones** | ¿Que limitaciones tengo? | "Equipo conoce Python, 3 meses de desarrollo, presupuesto bajo" |
| **3. Criterios** | ¿Que es importante para mi? | "Validacion, documentacion, rendimiento, seguridad" |
| **4. Alternativas** | ¿Que opciones existen? | "FastAPI, Django+DRF, Flask+extensiones" |
| **5. Recomendacion** | ¿Cual elijo y por que? | "FastAPI porque cubre mejor los criterios criticos" |
| **6. Riesgos** | ¿Que puede salir mal? | "Arquitectura poco clara, seguridad incompleta" |
| **7. Mitigacion** | ¿Como evito que salga mal? | "Usar estructura por capas, implementar autenticacion" |

### Plantilla rellenable (copia esto para tu proyecto):

```text
1. PROBLEMA:
   [Describe que necesitas construir]

2. RESTRICCIONES:
   - Lenguaje del equipo: [Python / PHP / C# / ...]
   - Tiempo disponible: [semanas / meses]
   - Tipo de app: [API / web completa / microservicio / ...]
   - Otras: [presupuesto, equipo, infraestructura, ...]

3. CRITERIOS (marca los mas importantes para ti):
   [ ] Validacion de datos
   [ ] Documentacion automatica
   [ ] Seguridad incluida
   [ ] Curva de aprendizaje baja
   [ ] Rendimiento
   [ ] Admin panel
   [ ] ORM integrado
   [ ] Comunidad grande

4. ALTERNATIVAS EVALUADAS:
   - Framework A: [nombre]
   - Framework B: [nombre]
   - Framework C: [nombre]

5. RECOMENDACION:
   Framework recomendado: [nombre]
   Justificacion: [2-3 lineas explicando por que]

6. RIESGOS:
   - Riesgo 1: [descripcion]
   - Riesgo 2: [descripcion]

7. MITIGACIONES:
   - Para riesgo 1: [que haremos para evitarlo]
   - Para riesgo 2: [que haremos para evitarlo]
```

**Ejemplo ya resuelto:**

> **Problema:** API academica consumida por un frontend separado.
> **Restricciones:** Equipo conoce Python, necesidad de documentacion automatica, validacion estricta.
> **Criterios clave:** Validacion (alto), documentacion (alto), curva (medio).
> **Alternativas:** FastAPI, Django+DRF, Flask+extensiones.
> **Recomendacion:** FastAPI. Porque tiene validacion Pydantic, documentacion OpenAPI automatica, y curva amigable para equipos Python.
> **Riesgos:** Arquitectura poco clara, seguridad incompleta.
> **Mitigaciones:** Estructura por capas (routers/schemas/services), implementar autenticacion JWT, CORS y pruebas.

## 9. Actividad central de clase

### 9.1 ABP: seleccionar framework para casos de negocio

> **Instrucciones:** formen equipos. Cada equipo recibe un caso de negocio. Deben comparar al menos 3 frameworks y elegir el mas adecuado usando la plantilla de 7 pasos de la seccion 8.

El grupo se divide en equipos. Cada equipo recibe o elige un caso:

**Caso A — Una API universitaria**
> Una universidad necesita una API para que una app movil consulte cursos, notas y asistencias. El equipo conoce Python.
>
> **Pista:** ¿Que framework esta especializado en APIs? ¿Cual genera documentacion automatica util para el equipo frontend?

**Caso B — Panel administrativo**
> Una empresa necesita un panel administrativo interno para gestionar inventario, usuarios y reportes. El equipo conoce Python.
>
> **Pista:** ¿Que framework trae panel admin, ORM y autenticacion listos "de fabrica"?

**Caso C — Prototipo rapido**
> Una startup necesita un prototipo rapido para validar una idea de reservas. No saben si funcionara. Quieren minimo esfuerzo inicial.
>
> **Pista:** ¿Que framework permite empezar en 5 minutos con 5 lineas de codigo?

**Caso D — Empresa Microsoft**
> Una empresa con infraestructura Microsoft (Azure, SQL Server, Active Directory) necesita renovar su sistema interno de gestion.
>
> **Pista:** ¿Que framework se integra naturalmente con el ecosistema Microsoft?

**Caso E — Ciencia de datos**
> Un equipo de ciencia de datos necesita exponer modelos predictivos por API. Usan Python, Pandas, NumPy y Scikit-learn.
>
> **Pista:** ¿Que framework es moderno, rapido, y se integra naturalmente con el ecosistema Python de datos?

### 9.2 Criterios obligatorios

Para cada caso, la decision debe considerar:

- tipo de aplicacion;
- lenguaje y experiencia del equipo;
- seguridad;
- productividad;
- documentacion;
- escalabilidad;
- ecosistema;
- riesgos.

### 9.3 Formato de entrega

Cada equipo debe presentar:

1. **Matriz comparativa** (3+ frameworks, 6+ criterios).
2. **Recomendacion** (framework elegido).
3. **Justificacion** (2-3 parrafos).
4. **Riesgos y mitigaciones** (tabla con 3+ riesgos).

## 10. Producto esperado

**Evidencia sugerida:** matriz comparativa + justificacion de eleccion (usando la plantilla de 7 pasos).

### Checklist de entregable:

- [ ] **Matriz comparativa** con:
  - Minimo 3 frameworks
  - Minimo 6 criterios
  - Calificacion o descripcion por criterio
- [ ] **Recomendacion final** (framework elegido)
- [ ] **Justificacion breve** (3-5 lineas explicando el por que)
- [ ] **Riesgos y mitigaciones** (minimo 3 riesgos con sus soluciones)

## 11. Ejemplo de matriz de decision

> **En espanol simple:** asi se ve una matriz de decision completa. Los numeros son calificaciones del 1 al 5. Los pesos representan que tan importante es cada criterio para el proyecto.

**Escenario:** API para app movil universitaria, equipo Python, necesitan documentacion automatica.

| Criterio | Peso | FastAPI | Django | Flask |
|---|---|---|---|---:|---:|---:|
| API REST moderna | 25% | 5 | 4 | 3 |
| Validacion de datos | 20% | 5 | 4 | 2 |
| Documentacion automatica | 15% | 5 | 3 | 2 |
| Curva para equipo Python | 15% | 4 | 3 | 4 |
| Seguridad | 15% | 4 | 5 | 3 |
| Escalabilidad del proyecto | 10% | 4 | 4 | 3 |

**Interpretacion:**

- **FastAPI (4.6/5):** gana porque el proyecto es una API y necesita validacion + documentacion. Perfecto para el caso.
- **Django (3.8/5):** buena opcion si ademas necesitaras panel admin. Pero para API pura, es mas pesado de lo necesario.
- **Flask (2.9/5):** funcional para un prototipo, pero requeriria muchas extensiones y decisiones extra.

> **Dato curioso:** si el caso fuera "panel administrativo con formularios", Django probablemente ganaria. Por eso NO existe un "mejor framework" en abstracto. Todo depende del contexto.

## 12. Cierre conceptual

### ¿Que aprendimos hoy?

1. **Elegir un framework no es opinion personal:** es un proceso de 7 pasos (problema, restricciones, criterios, alternativas, recomendacion, riesgos, mitigaciones).
2. **No existe un ganador universal:** cada framework es bueno para algo distinto. FastAPI para APIs, Django para monolitos, Flask para prototipos, Laravel para apps PHP, ASP.NET para empresa.
3. **La matriz de decision es tu amiga:** pone los criterios sobre la mesa y hace visible el razonamiento. Sin ella, las decisiones se basan en "me gusta mas" o "lo vi en Twitter".
4. **FastAPI es nuestro framework del curso:** porque se alinea con APIs modernas, Python, validacion Pydantic, documentacion OpenAPI, seguridad y microservicios.

Elegir un framework es una decision de arquitectura, equipo y contexto. No existe un ganador universal. FastAPI sera el framework principal del curso porque se alinea con APIs modernas, Python, validacion, documentacion automatica, seguridad y microservicios.

Pero el estudiante debe salir de esta clase con una idea mas profesional: una tecnologia no se defiende con fanatismo, se justifica con criterios.

La ingenieria empieza cuando dejamos de decir "me gusta mas" y empezamos a decir "para este problema, bajo estas restricciones, esta opcion tiene mas sentido". Menos guerra santa, mas matriz de decision. Triste para Twitter, excelente para proyectos reales.

## 13. Trabajo independiente (6 horas sugeridas)

### 13.1 Matriz comparativa (2 horas)

Completa una matriz comparativa entre:
- **FastAPI, Django y Flask** (si te interesa Python puro)
- **O** FastAPI, Laravel y ASP.NET Core MVC (si quieres comparar con otros lenguajes)

Usa al menos 6 criterios de la seccion 5. Dale pesos porcentuales a cada criterio segun lo que consideres importante.

### 13.2 Justificacion del proyecto integrador (2 horas)

Selecciona un caso para tu proyecto integrador y usando la plantilla de 7 pasos:

1. Describe el problema que resuelve tu proyecto.
2. Enumera las restricciones.
3. Define los criterios mas importantes.
4. Compara al menos 3 frameworks.
5. Recomienda uno.
6. Identifica 3 riesgos.
7. Propone mitigaciones.

### 13.3 Preparar entorno tecnico (2 horas)

Instala Python y prepara el entorno para la Clase 04 (donde empezaremos a escribir codigo FastAPI de verdad):

```bash
python --version   # Debe ser 3.8+
pip install fastapi uvicorn
```

Verifica que funciona:
```bash
python -c "import fastapi; print('FastAPI listo:', fastapi.__version__)"
```

Si ves un numero de version, estas listo para la siguiente clase.

## 14. Bibliografia y referencias utiles

- FastAPI. (s. f.). *FastAPI Documentation*. https://fastapi.tiangolo.com/
- Django Software Foundation. (s. f.). *Django Documentation*. https://docs.djangoproject.com/
- Pallets. (s. f.). *Flask Documentation*. https://flask.palletsprojects.com/
- Laravel. (s. f.). *Laravel Documentation*. https://laravel.com/docs/
- Microsoft. (s. f.). *ASP.NET Core Documentation*. https://learn.microsoft.com/aspnet/core/
- OWASP Foundation. (s. f.). *OWASP API Security Top 10*. https://owasp.org/API-Security/
