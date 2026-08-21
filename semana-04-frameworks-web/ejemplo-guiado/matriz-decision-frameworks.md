# Ejemplo guiado — Matriz de decision para seleccionar framework

## Objetivo

Aprender a construir una matriz de decision para seleccionar un framework web segun un caso de negocio real.

Al finalizar este ejemplo, sabras:
- Identificar criterios relevantes para comparar frameworks
- Asignar pesos a cada criterio segun su importancia
- Calificar alternativas de forma objetiva
- Interpretar los resultados

---

## El caso

> Una universidad necesita construir una API para que una aplicacion movil permita:
> - consultar cursos matriculados;
> - ver notas;
> - registrar asistencia;
> - consultar anuncios;
> - autenticar estudiantes;
> - integrarse luego con otros sistemas academicos.
>
> El equipo conoce Python de forma intermedia y necesita documentacion clara para que otro equipo frontend consuma la API.

---

## Paso 1. Identificar el tipo de aplicacion

> **Pregunta clave:** ¿QUE estamos construyendo?

El producto principal es una **API** consumida por una **aplicacion movil**.

Esto significa que nos importa:
- rutas HTTP claras;
- documentacion automatica (OpenAPI);
- validacion de datos;
- seguridad con tokens;
- facilidad para pruebas;
- estructura mantenible.

> **Analogia:** Si el proyecto fuera un panel administrativo con formularios, criterios como "admin listo" o "ORM integrado" pesarian mas. Como es una API, criterios como "documentacion automatica" y "validacion" pesan mas.

---

## Paso 2. Definir las alternativas

> **Pregunta clave:** ¿QUE opciones vamos a comparar?

Vamos a comparar 3 frameworks de Python (porque el equipo conoce Python):

| Framework | Tipo | Por que lo incluimos |
|---|---|---|
| **FastAPI** | API moderno | Es el framework central del curso |
| **Django + DRF** | Full-stack + REST | Muy popular en Python, maduro |
| **Flask + extensiones** | Microframework | Flexible, conocido, minimalista |

---

## Paso 3. Definir criterios y asignar pesos

> **Pregunta clave:** ¿QUE es importante para ESTE proyecto?

No todos los criterios pesan igual. Para una API universitaria:

| Criterio | Peso | ¿Por que este peso? |
|---|---|---|
| **API REST moderna** | 25% | Es el core del proyecto |
| **Validacion de datos** | 20% | Los datos academicos deben ser correctos |
| **Documentacion automatica** | 15% | El equipo frontend necesita documentacion clara |
| **Curva para equipo Python** | 15% | El equipo conoce Python, no queremos perder tiempo |
| **Seguridad** | 15% | Datos de estudiantes son sensibles |
| **Escalabilidad del proyecto** | 10% | Debe crecer en el futuro |

> **Los pesos suman 100%.** Si un criterio no te importa, ponle 0% o 5%. Si te importa mucho, ponle 25% o 30%.

---

## Paso 4. Calificar cada alternativa

> **Pregunta clave:** ¿QUE tan bien se ajusta cada framework a cada criterio?

Usamos una escala del 1 al 5:

| Puntaje | Significado |
|---|---|
| **1** | Ajuste bajo o nulo |
| **2** | Ajuste limitado |
| **3** | Ajuste aceptable |
| **4** | Buen ajuste |
| **5** | Excelente ajuste |

**Tabla de calificaciones:**

| Criterio (Peso) | FastAPI | Django+DRF | Flask+ext |
|---|---|---|---|
| API REST moderna (25%) | **5** — Nacio para APIs | 4 — DRF lo hace bien | 3 — Se puede, pero no es nativo |
| Validacion de datos (20%) | **5** — Pydantic es bestia | 4 — DRF serializers | 2 — Manual con extensiones |
| Documentacion automatica (15%) | **5** — OpenAPI nativo | 3 — Con drf-spectacular | 2 — Con Flask-RESTful |
| Curva equipo Python (15%) | **4** — Tipado, claro | 3 — Muchos conceptos | 4 — Simple pero decisiones |
| Seguridad (15%) | **4** — Herramientas, configurable | **5** — Muy completo | 3 — Depende de extensiones |
| Escalabilidad (10%) | **4** — ASGI, async | 4 — Maduro, probado | 3 — Menos estructura |

---

## Paso 5. Calcular resultados

> **Formula:** (Peso del criterio × Calificacion) sumado de todos los criterios

**FastAPI:**
(25% × 5) + (20% × 5) + (15% × 5) + (15% × 4) + (15% × 4) + (10% × 4)
= 1.25 + 1.00 + 0.75 + 0.60 + 0.60 + 0.40 = **4.60 / 5.00**

**Django + DRF:**
(25% × 4) + (20% × 4) + (15% × 3) + (15% × 3) + (15% × 5) + (10% × 4)
= 1.00 + 0.80 + 0.45 + 0.45 + 0.75 + 0.40 = **3.85 / 5.00**

**Flask + extensiones:**
(25% × 3) + (20% × 2) + (15% × 2) + (15% × 4) + (15% × 3) + (10% × 3)
= 0.75 + 0.40 + 0.30 + 0.60 + 0.45 + 0.30 = **2.80 / 5.00**

---

## Paso 6. Interpretar los resultados

| Framework | Puntaje | Veredicto |
|---|---|---|
| **FastAPI** | **4.60** | 🏆 Gana claramente para este caso |
| Django + DRF | 3.85 | Opcion valida si el proyecto creciera hacia admin |
| Flask + ext | 2.80 | Funcional para prototipo, pero exige demasiadas decisiones |

**¿Por que gano FastAPI?**
- Esta **disenado para APIs** (no es un framework full-stack adaptado).
- **Pydantic** da validacion de datos automatica y clara.
- **OpenAPI** se genera solo, sin librerias extra.
- Se integra bien con Python (el equipo ya lo conoce).
- Permite arquitectura modular (buena para escalar).

**¿Cuando ganaria Django?**
- Si el proyecto necesitara **panel administrativo** completo.
- Si necesitaramos **ORM integrado** sin decidir cual usar.
- Si el equipo prefiriera "todo incluido" desde el inicio.

---

## Paso 7. ¿Que pasa si dos frameworks empatan?

Si FastAPI y Django hubieran empatado (ej: 4.2 vs 4.2), deberias:

1. **Revisar los pesos:** ¿estan bien asignados? ¿algun criterio deberia pesar mas?
2. **Agregar criterios:** ¿falto algun criterio importante (ej: "tiempo de desarrollo", "contratacion")?
3. **Desempatar con un criterio subjetivo:** ¿cual framework conoce mejor el equipo? ¿cual tiene mejor comunidad de soporte?
4. **Hacer un prototipo:** prueba ambos con un endpoint simple y decide por experiencia.

> **Importante:** la matriz no decide por ti. Solo hace visible tu razonamiento. Si dos opciones empatan, significa que ambas son viables y la decision final puede basarse en otros factores.

---

## Paso 8. Riesgos y mitigaciones

| Riesgo | Mitigacion |
|---|---|
| Arquitectura poco clara | Usar estructura por capas: routers, schemas, services, models |
| Seguridad incompleta | Implementar autenticacion (JWT), autorizacion, hashing y CORS |
| Persistencia mal definida | Seleccionar SQLModel o SQLAlchemy desde el inicio |
| Dependencia solo de documentacion automatica | Revisar manualmente schemas y codigos HTTP |

---

## Resumen de conceptos aplicados

| Concepto | Como se aplico |
|---|---|
| **Pesos porcentuales** | Asignamos 25% a API REST porque es el core del proyecto |
| **Calificacion 1-5** | Evaluamos cada framework contra cada criterio |
| **Calculo ponderado** | Multiplicamos peso × calificacion y sumamos |
| **Interpretacion** | FastAPI gano porque sus fortalezas coinciden con el caso |
| **Riesgos** | Identificamos 4 riesgos con sus mitigaciones |

---

## Cierre

La matriz no decide por magia. Sirve para hacer visible el razonamiento tecnico. Si un equipo no puede justificar su eleccion, probablemente no eligio: solo siguio la musica del hype, y el hype rara vez escribe pruebas unitarias.

**Ahora te toca a ti:** toma el caso de tu proyecto integrador y construye tu propia matriz de decision.
