# Preguntas frecuentes — Clase 00

## Python y FastAPI

**P: Python y FastAPI son lo mismo?**
R: No. Python es el lenguaje de programacion. FastAPI es un framework construido para Python. Es como la diferencia entre el idioma espanol y un libro escrito en espanol.

**P: Por que Python y no otro lenguaje?**
R: Python tiene una sintaxis sencilla, una gran comunidad, y es el lenguaje mas utilizado para APIs modernas, ciencia de datos e inteligencia artificial.

**P: FastAPI es lo mismo que Django?**
R: No. Django es un framework completo (incluye admin, ORM, etc.). FastAPI se especializa en APIs REST y es mas rapido y moderno. Ambos son excelentes, pero tienen enfoques distintos.

---

## API y HTTP

**P: Que es una API?**
R: Application Programming Interface. Es una puerta controlada mediante la cual otros programas pueden solicitar informacion o ejecutar operaciones en nuestro sistema.

**P: Una API tiene interfaz grafica?**
R: No necesariamente. Una API puede funcionar devolviendo simplemente JSON. La interfaz grafica se construye aparte (React, Vue, aplicacion movil, etc.).

**P: Que es HTTP?**
R: HyperText Transfer Protocol. Es el protocolo de comunicacion que usan cliente y servidor para intercambiar informacion en la web.

**P: Que diferencia hay entre GET y POST?**
R: GET consulta informacion (como leer). POST crea informacion (como escribir). GET no modifica datos, POST si.

**P: Que es REST?**
R: Un estilo para disenar APIs que utiliza los conceptos de HTTP. Trabajamos con recursos (estudiantes, productos, etc.) y operaciones sobre ellos.

---

## FastAPI y Swagger

**P: Que es Swagger?**
R: Una herramienta que FastAPI genera automaticamente para probar tu API. No necesitas instalar Postman. Solo abres `/docs` en el navegador.

**P: FastAPI es un frontend?**
R: No. FastAPI es backend. El frontend (React, Vue, HTML) se comunica con FastAPI via HTTP y JSON.

**P: FastAPI es una base de datos?**
R: No. FastAPI es el servidor que procesa peticiones. La base de datos se conecta despues (SQLAlchemy, PostgreSQL, etc.).

**P: Que es un endpoint?**
R: Un punto de acceso a tu API. Es la combinacion de un metodo HTTP y una ruta. Ejemplo: `GET /estudiantes`.

**P: Que es un framework?**
R: Un conjunto de herramientas y convenciones que te ayuda a construir aplicaciones sin reinventar la rueda. FastAPI ya resuelve HTTP, validacion, documentacion, etc.

---

## Validacion y Pydantic

**P: Que es Pydantic?**
R: Una libreria que FastAPI usa para validar datos. Si defines `edad: int` y alguien envia texto, Pydantic rechaza automaticamente la peticion.

**P: Que pasa si envio datos incorrectos?**
R: FastAPI retorna un error 422 con un mensaje claro sobre que esta mal. Tu no tienes que escribir codigo de validacion manual.

---

## Sobre el curso

**P: Que vamos a construir?**
R: Una API completa de gestion academica: estudiantes, cursos, matriculas, autenticacion JWT, testing y despliegue en Render + Supabase.

**P: Necesito saber HTML/CSS/JavaScript?**
R: No es obligatorio. El curso se enfoca en el backend (FastAPI + Python). El frontend es opcional.

**P: Puedo usar Windows/Mac/Linux?**
R: Si. FastAPI funciona en todos los sistemas operativos.
