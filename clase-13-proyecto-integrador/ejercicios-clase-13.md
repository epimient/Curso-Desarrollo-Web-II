# Ejercicios — Clase 13: Proyecto Integrador

## Ejercicio 1: Filtrar cursos por rango de créditos

Agrega un filtro por rango de créditos a GET /courses/:

```python
@router.get("/")
def list_courses(
    ...
    min_credits: int | None = None,
    max_credits: int | None = None,
    ...
):
```

**Pistas:**
- Usa `Course.credits >= min_credits` y `Course.credits <= max_credits`
- Ambos parámetros deben ser opcionales

---

## Ejercicio 2: Endpoint PATCH /courses/{id}

Agrega un endpoint PATCH para actualización parcial de cursos (no requiere todos los campos, a diferencia de PUT).

**Requisitos:**
- Usa el mismo `CourseUpdate` schema que PUT
- Solo usuarios autenticados pueden usarlo (no requiere admin)
- Valida que el nombre no esté duplicado si se actualiza

---

## Ejercicio 3: Historial de cambios en matrículas

Crea un modelo `EnrollmentLog` que registre cada cambio en una matrícula:

```python
class EnrollmentLog(Base):
    __tablename__ = "enrollment_logs"
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    changed_by = Column(Integer, ForeignKey("users.id"))
    field = Column(String(50))
    old_value = Column(String(255), nullable=True)
    new_value = Column(String(255), nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)
```

**Pistas:**
- Actualiza el servicio `update` para crear un log por cada campo cambiado
- Usa `getattr(enrollment, field)` para leer valores viejos

---

## Ejercicio 4: Pruebas de paginación

Escribe tests que verifiquen la paginación de GET /courses/:

```python
def test_pagination_default(client, created_course):
    response = client.get("/courses/")
    data = response.json()
    assert "items" in data
    assert "page" in data
    assert "per_page" in data
    assert "total" in data
```

Crea al menos 15 cursos con un fixture y prueba:
- `page=1, per_page=5` → 5 items, 3 páginas
- `page=3, per_page=5` → últimos 5 items
- `page=99` → lista vacía

---

## Desafío: Reporte de estadísticas

Crea un endpoint GET /reports/stats que devuelva:

```json
{
  "total_students": 10,
  "total_courses": 5,
  "total_enrollments": 23,
  "avg_grade": 82.5,
  "courses_by_status": {
    "active": 4,
    "inactive": 1
  },
  "enrollments_by_status": {
    "enrolled": 15,
    "completed": 6,
    "cancelled": 2
  }
}
```

**Requisitos adicionales:**
- Solo admins pueden acceder
- Usa `func.avg()`, `func.count()` de SQLAlchemy para eficiencia
- Crea un router separado `routers/reports.py`

---

## Checklist de verificación

- [ ] Ejercicio 1 funciona con Swagger
- [ ] Ejercicio 2: PATCH respeta permisos
- [ ] Ejercicio 3: cada cambio queda registrado
- [ ] Ejercicio 4: pytest pasa con 3+ casos de paginación
- [ ] Desafío: reporte con datos agregados
- [ ] Todos los tests pasan: `pytest -v`
- [ ] Cobertura ≥ 90%
