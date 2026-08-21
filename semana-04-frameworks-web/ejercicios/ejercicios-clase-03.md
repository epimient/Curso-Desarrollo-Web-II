# Ejercicios - Clase 03

> **Nota para el estudiante:** Estos ejercicios te ayudaran a practicar la comparacion de frameworks. No se trata de memorizar tablas, sino de entender POR QUE se elige una tecnologia sobre otra. El ejercicio 0 es de calentamiento.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las frases con las palabras del recuadro:

> **Palabras:** MATRIZ | PESO | PYTHON | PHP | FULL-STACK | MICROFRAMEWORK | API | MITIGACION

1. Un framework _________ trae todo incluido: ORM, admin, autenticacion (ej: Django, Laravel).
2. Un _________ es minimalista y deja las decisiones al equipo (ej: Flask).
3. FastAPI esta especializado en construir _________ modernas.
4. La _________ de decision permite comparar frameworks con criterios objetivos.
5. El _________ porcentual indica que tan importante es un criterio para el proyecto.
6. Una _________ es una accion para reducir el riesgo de una decision.
7. FastAPI y Django usan _________, Laravel usa _________.

---

## Ejercicio 1. Comparacion rapida

Complete la tabla comparando FastAPI, Django y Flask segun lo que recuerdes de la clase:

| Criterio | FastAPI | Django | Flask |
|---|---|---|---|
| Tipo de aplicacion ideal | | | |
| Curva de aprendizaje | | | |
| Validacion de datos | | | |
| Documentacion API | | | |
| Seguridad | | | |
| Estructura por defecto | | | |

**Respuesta modelo (para verificar despues de intentarlo):**

| Criterio | FastAPI | Django | Flask |
|---|---|---|---|
| Tipo ideal | APIs modernas | Monolitos, admin | Prototipos, APIs pequenas |
| Curva aprendizaje | Media | Media-alta | Baja-media |
| Validacion | Muy fuerte (Pydantic) | Formularios/DRF | Extensiones |
| Documentacion API | Automatica (OpenAPI) | Con DRF | Manual/extensiones |
| Seguridad | Herramientas (configurable) | Muy completo listo | Extensiones |
| Estructura | Media | Alta | Baja |

---

## Ejercicio 2. Elegir framework segun caso (con pistas)

Seleccione el framework mas adecuado para cada caso y justifique en 2-3 lineas.

**Caso 1:** API para una app movil universitaria.
> **Pista:** ¿Que framework nacio para construir APIs?
> **Respuesta:** FastAPI. Porque esta disenado especificamente para APIs, tiene documentacion OpenAPI automatica y validacion Pydantic.

**Caso 2:** Panel administrativo de inventario con usuarios y reportes.
> **Pista:** ¿Que framework trae panel admin listo "de fabrica"?
> **Tu respuesta:** _________

**Caso 3:** Prototipo pequeno para validar una idea de reservas.
> **Pista:** ¿Que framework permite empezar con 5 lineas de codigo?
> **Tu respuesta:** _________

**Caso 4:** Sistema empresarial en una organizacion que ya usa Microsoft y C#.
> **Pista:** ¿Que framework de Microsoft usarian?
> **Tu respuesta:** _________

**Caso 5:** Servicio que expone un modelo de machine learning por HTTP.
> **Pista:** ¿Que framework Python es moderno, rapido y se integra con Pandas/NumPy?
> **Tu respuesta:** _________

---

## Ejercicio 3. Matriz ponderada (construye la tuya)

Construya una matriz ponderada para **TU proyecto integrador** con:

- Minimo 3 frameworks
- Minimo 6 criterios
- Pesos porcentuales que sumen 100%
- Calificaciones del 1 al 5

**Plantilla:**

| Criterio | Peso | Framework A | Framework B | Framework C |
|---|---|---|---|---|
| | % | | | |
| | % | | | |
| | % | | | |
| | % | | | |
| | % | | | |
| | % | | | |
| **Total** | **100%** | | | |

Al final, responde:
- **¿Que framework gano?**
- **¿Por que?** (3-5 lineas de justificacion)
- **¿Que riesgos identificas y como los mitigarias?**

---

## Ejercicio 4. Riesgos y mitigaciones

Para FastAPI, identifique tres riesgos al usarlo en un proyecto academico y proponga mitigaciones.

**Ejemplo:**

| Riesgo | Mitigacion |
|---|---|
| El equipo no define estructura clara | Usar arquitectura por capas: routers, schemas, services |

**Tu turno:**

| Riesgo | Mitigacion |
|---|---|
| 1. | |
| 2. | |
| 3. | |

---

## Ejercicio 5. Argumento tecnico breve

Redacte un parrafo que responda:

**¿Por que FastAPI es una opcion adecuada para el proyecto integrador del curso?**

Incluya al menos cuatro criterios tecnicos. Prohibido responder "porque es rapido" y desaparecer como personaje secundario.

**Estructura sugerida:**
> "FastAPI es adecuado para mi proyecto porque [criterio 1], [criterio 2], [criterio 3] y [criterio 4]. Sin embargo, debo mitigar [riesgo 1] y [riesgo 2] mediante [mitigaciones]."

---

## Ejercicio 6. Debate

Prepare una defensa breve de un framework **diferente a FastAPI**.

Debe incluir:
- contexto donde seria mejor opcion;
- ventajas sobre FastAPI en ese contexto;
- riesgos de usarlo;
- por que no seria la opcion central de este curso.

**Ayuda:** Revisa las fichas de la seccion 6 de la clase para inspirarte.

| Framework | Contexto donde gana |
|---|---|
| Django | Panel admin, ORM, app monolitica |
| Flask | Prototipo, microservicio simple |
| Laravel | App web PHP tradicional |
| ASP.NET Core | Empresa Microsoft |
