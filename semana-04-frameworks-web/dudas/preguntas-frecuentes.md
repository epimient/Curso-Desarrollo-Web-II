# Dudas frecuentes - Clase 03

> Aqui encontraras las preguntas que los estudiantes suelen hacer sobre como comparar frameworks. Recuerda: no hay framework "mejor", hay framework "mas adecuado para tu problema".

---

## 1. FastAPI es mejor que Django?

**Respuesta corta:** Depende del contexto.

**Respuesta larga:** 

**FastAPI** suele ser mejor opcion para:
- APIs modernas
- Servicios ligeros
- Documentacion OpenAPI automatica
- Proyectos conectados a ciencia de datos e IA

**Django** suele ser mejor opcion para:
- Aplicaciones monoliticas con panel administrativo
- ORM integrado
- Proyectos que necesitan muchas funcionalidades listas "de fabrica"

**Analogia:** FastAPI es como un bisturi (preciso para una tarea especifica). Django es como una navaja suiza (tiene muchas herramientas integradas). ¿Cual es mejor? Depende de si necesitas una cirugia o abrir una botella de vino.

---

## 2. Flask ya no sirve?

**Respuesta corta:** Si sirve. Pero hay que usarlo con criterio.

**Respuesta larga:** Flask es como una bicicleta: simple, ligera, flexible. Ideal para:
- Prototipos rapidos
- Servicios muy pequenos
- Aprender conceptos web desde cero

**Pero:** como no impone estructura, un proyecto puede desordenarse si el equipo no define buenas practicas. Para proyectos grandes, necesitas agregar muchas extensiones y decision arquitectonica.

---

## 3. ¿Por que no usamos Laravel si el syllabus lo menciona?

**Respuesta corta:** Porque el curso esta enfocado en Python y FastAPI.

**Respuesta larga:** El syllabus menciona Laravel como referencia comparativa, no como framework principal del curso. El enfoque definido es FastAPI por:
- Usa Python (el lenguaje del curso)
- Es moderno y orientado a APIs
- Tiene validacion Pydantic y OpenAPI automatico
- Es ideal para el perfil del curso (desarrollo web con APIs)

Laravel es excelente... en PHP. Este curso es de Python.

---

## 4. ¿Que significa que un framework sea "full-stack"?

**Respuesta corta:** Que incluye muchas piezas listas para construir una aplicacion completa.

**Respuesta larga:** Un framework full-stack (como Django, Laravel, ASP.NET) incluye:
- Sistema de rutas
- ORM para base de datos
- Sistema de plantillas (HTML)
- Autenticacion
- Formularios con validacion
- Panel administrativo
- Migraciones de BD

**Analogia:** Es como comprar una casa amueblada vs comprar un terreno y construir. El full-stack es la casa amueblada: todo listo para vivir, pero menos flexible para cambios estructurales.

---

## 5. FastAPI sirve para aplicaciones grandes?

**Respuesta corta:** Si, siempre que se disene una buena arquitectura.

**Respuesta larga:** FastAPI no impone una estructura gigante de fabrica (como Django). Eso significa que el equipo debe decidir:
- Como organizar las capas (routers, schemas, services, models)
- Que ORM usar (SQLModel, SQLAlchemy)
- Como manejar autenticacion
- Como hacer pruebas

**Si el equipo tiene criterio**, FastAPI escala muy bien. **Si el equipo no tiene criterio**, cualquier framework se vuelve un desastre, incluso Django.

---

## 6. ¿El rendimiento deberia ser el criterio principal?

**Respuesta corta:** No siempre.

**Respuesta larga:** El rendimiento importa, pero muchos proyectos fracasan por:
- Mal diseno de base de datos
- Codigo ineficiente
- Falta de pruebas
- Mala arquitectura

**Analogia:** Un motor potente no salva a un conductor que maneja directo al muro. Primero asegurate de que el diseno sea solido, luego preocupate por la velocidad.

**Orden de prioridad sugerido:**
1. Que el framework sea adecuado para el tipo de proyecto
2. Que el equipo pueda usarlo productivamente
3. Que tenga buena documentacion y comunidad
4. Que sea seguro por defecto
5. **Luego** el rendimiento

---

## 7. ¿Que framework deberia elegir para mi proyecto integrador?

**Respuesta corta:** Para este curso, FastAPI.

**Respuesta larga:** El curso esta disenado alrededor de FastAPI. Las clases, ejercicios y ejemplos usan FastAPI. Pero la clase de hoy te prepara para:
- **Justificar** por que FastAPI es adecuado para tu proyecto
- **Reconocer los riesgos** de usar FastAPI
- **Mitigar** esos riesgos con buenas practicas

No se trata de "FastAPI es el mejor". Se trata de "FastAPI es el mas adecuado para este curso y este contexto".

---

## 8. ¿Que son los "pesos" en la matriz de decision?

**Respuesta corta:** Son porcentajes que indican que tan importante es cada criterio.

**Respuesta larga:** Si estas comparando frameworks, no todos los criterios importan igual. Por ejemplo:
- Si tu proyecto es una **API**, el criterio "API REST moderna" puede pesar 25%.
- Si tu proyecto es un **panel admin**, "Admin listo" puede pesar 30%.

Los pesos deben **sumar 100%**. Asi evitas que todos los criterios tengan la misma importancia cuando en la realidad no es asi.

---

## 9. ¿Que significa que FastAPI tenga "documentacion OpenAPI automatica"?

**Respuesta corta:** Que cuando ejecutas tu API, ya tienes una pagina web con la documentacion lista.

**Respuesta larga:** OpenAPI es un estandar para documentar APIs. FastAPI lo genera automaticamente a partir de tu codigo. Solo por definir rutas, schemas y tipos, ya tienes:
- **Swagger UI** en `/docs` (interfaz interactiva para probar endpoints)
- **ReDoc** en `/redoc` (documentacion mas legible)

**Sin escribir una sola linea de documentacion.** Django y Flask necesitan librerias extra para lograr lo mismo.

---

## 10. ¿Que pasa si en mi matriz TODOS los frameworks puntuan similar?

**Respuesta corta:** Significa que cualquiera funcionaria. Elige el que mas conozcas.

**Respuesta larga:** Si despues de hacer la matriz todos los frameworks quedan entre 3.8 y 4.2, significa que todos son opciones validas. En ese caso:
1. Elige el que mejor conozca el equipo (menor curva de aprendizaje)
2. Elige el que tenga mejor comunidad/soporte
3. Haz un prototipo de 1 dia con cada uno y decide por experiencia

> La matriz no decide por ti. Solo hace visible tu razonamiento.
