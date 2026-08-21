# Clase 11 - Testing con pytest y httpx

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II
**Enfoque del curso:** FastAPI como framework principal para el desarrollo de aplicaciones web y APIs modernas.
**Semana:** 11
**Unidad:** Unidad 4 - Calidad y despliegue
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.
**Resultado de aprendizaje asociado:**
- RA4: Implementar pruebas automatizadas para APIs REST utilizando pytest y httpx, asegurando la calidad del software mediante tests funcionales y unitarios.

## 2. Proposito de la clase

Hasta ahora has construido una API funcional con autenticacion, base de datos, middleware y manejo de errores. Pero **¿como sabes que funciona correctamente despues de cada cambio?** Cada vez que agregas una funcion nueva, existe el riesgo de romper algo que ya funcionaba.

Las pruebas automatizadas (tests) resuelven este problema: escribes una vez el comportamiento esperado y la maquina lo verifica cada vez que lo necesites.

En esta clase aprenderas a:
- Escribir tests automatizados para cada endpoint de tu API
- Usar pytest como framework de testing
- Usar TestClient de FastAPI (basado en httpx) para simular peticiones HTTP
- Aislar la base de datos en cada test usando fixtures
- Probar autenticacion, roles y errores
- Medir la cobertura de tus tests

## 3. ¿Por que es importante testear APIs?

> **En espanol simple:** Probar a mano con Swagger UI esta bien para explorar, pero cuando tu API tenga 50 endpoints, probarlos uno por uno cada vez que haces un cambio es imposible. Los tests automatizados verifican todo en segundos.

### 3.1 Antes de los tests (como trabajas ahora)

```
Haces un cambio en el codigo
       │
       ▼
Abras /docs
       │
       ▼
Pruebas 5 endpoints a mano
       │
       ▼
"Parece que funciona"
       │
       ▼
(Sin saberlo, rompiste el login)
```

### 3.2 Con tests automatizados

```
Escribes el test UNA VEZ
       │
       ▼
pytest (un solo comando)
       │
       ▼
Se ejecutan 30 tests en 2 segundos
       │
       ▼
Sabes exactamente que funciona y que no
```

### 3.3 Beneficios concretos

| Sin tests | Con tests |
|---|---|
| Confias en que "mas o menos funciona" | Tienes evidencia objetiva |
| Miedo a hacer cambios grandes | Libertad para refactorizar |
| Pruebas manuales que nadie hace | Pruebas que se ejecutan solas |
| Los bugs aparecen en produccion | Los bugs se detectan antes |

## 4. pytest — "El framework de testing mas popular de Python"

> **En espanol simple:** pytest es una herramienta que busca archivos llamados `test_*.py`, ejecuta las funciones que empiezan con `test_`, y te dice si pasaron o fallaron.

### 4.1 Instalacion

```bash
pip install pytest httpx pytest-cov
```

### 4.2 El test mas simple posible

```python
# test_simple.py
def test_que_python_funciona():
    assert 1 + 1 == 2
```

```bash
pytest
# → 1 passed
```

### 4.3 Reglas de pytest

| Regla | Explicacion |
|---|---|
| Los archivos deben llamarse `test_*.py` o `*_test.py` | pytest los descubre automaticamente |
| Las funciones deben empezar con `test_` | Solo esas se ejecutan como tests |
| Usa `assert` para verificar | Si la expresion es `True`, pasa. Si es `False`, falla. |
| Las fixtures se definen en `conftest.py` | Se comparten entre todos los tests |

### 4.4 Comandos utiles

```bash
pytest                    # Ejecuta todos los tests
pytest -v                 # Modo verboso (muestra cada test)
pytest -k "auth"          # Solo tests que contengan "auth" en el nombre
pytest --tb=short         # Traza corta en errores
pytest --cov=app          # Mide cobertura del paquete app
pytest --cov=app --cov-report=term-missing  # + lineas no cubiertas
```

## 5. TestClient — "Swagger UI pero desde codigo"

> **En espanol simple:** TestClient es un objeto en Python que se comporta como si fuera un navegador haciendo peticiones a tu API. Puedes hacer GET, POST, PUT, DELETE y revisar las respuestas.

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.get("/health/")
assert response.status_code == 200
assert response.json() == {"status": "ok"}
```

### 5.1 Metodos de TestClient

```python
client.get("/url")
client.post("/url", json={"key": "value"})
client.put("/url", json={"key": "value"})
client.delete("/url")
client.options("/url", headers={"Origin": "..."})
```

Cada metodo retorna un objeto `Response` con:

| Atributo | Que contiene |
|---|---|
| `.status_code` | Codigo HTTP (200, 201, 404, etc.) |
| `.json()` | El cuerpo de la respuesta como diccionario Python |
| `.headers` | Los headers HTTP como diccionario |
| `.text` | El cuerpo como texto plano |

### 5.2 Diferencia con Swagger UI

| Swagger UI | TestClient |
|---|---|
| Pruebas manuales | Pruebas automatizadas |
| Ves el resultado en pantalla | El resultado lo verifica el codigo |
| Pruebas 1 endpoint a la vez | Pruebas 30 endpoints en 2 segundos |
| No guarda resultados | pytest te da un reporte |
| Ideal para explorar | Ideal para verificar |

## 6. Fixtures — "Los ingredientes preparados antes de cocinar"

> **En espanol simple:** Una fixture es codigo que se ejecuta ANTES de cada test para preparar el escenario. Por ejemplo: crear la base de datos, registrar un usuario, obtener un token.

### 6.1 Fixture basica

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture()
def client():
    return TestClient(app)


def test_health(client):
    response = client.get("/health/")
    assert response.status_code == 200
```

Cuando un test tiene `client` como parametro, pytest ejecuta la funcion `client()` primero y le pasa el resultado al test.

### 6.2 Fixtures que usan otras fixtures

```python
@pytest.fixture()
def test_user_data():
    return {"username": "ana", "email": "ana@mail.com", "password": "123456"}


@pytest.fixture()
def token(client, test_user_data):
    client.post("/users/register", json=test_user_data)
    response = client.post("/token", data={
        "username": test_user_data["username"],
        "password": test_user_data["password"],
    })
    return response.json()["access_token"]
```

### 6.3 ¿Donde van las fixtures?

- En el archivo `conftest.py` — las fixtures se comparten con todos los tests de esa carpeta y subcarpetas.
- En el mismo archivo de test — si solo las necesita ese archivo.

### 6.4 Ciclo de vida

```python
@pytest.fixture(autouse=True)   # Se ejecuta automaticamente en CADA test
def test_db():
    Base.metadata.create_all(bind=engine)   # Setup
    yield
    Base.metadata.drop_all(bind=engine)     # Teardown (despues del test)
```

El `yield` separa el setup del teardown. Todo lo que esta antes del `yield` se ejecuta antes del test. Todo lo que esta despues se ejecuta despues.

## 7. Aislar la base de datos en tests

> **En espanol simple:** Cada test debe empezar con la base de datos limpia. Si un test crea un usuario, el siguiente test no debe encontrar ese usuario.

### 7.1 El problema

```python
# Sin aislamiento:
def test_primero(client):
    client.post("/users/register", json={"username": "ana", "password": "123"})
    # → Crea usuario en la BD

def test_segundo(client):
    # El usuario "ana" ya existe del test anterior
    # Esto puede causar falsos positivos o negativos
```

### 7.2 La solucion: BD en memoria + recreate

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)    # Crea tablas
    yield
    Base.metadata.drop_all(bind=engine)      # Elimina tablas


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

Cada test:
1. Crea las tablas desde cero
2. Ejecuta el test
3. Elimina las tablas

**Resultado:** Cada test empieza con una BD limpia y predecible.

## 8. Probar autenticacion — "El flujo completo"

### 8.1 Registrar, hacer login, usar token

```python
def test_flujo_completo(client):
    # Paso 1: Registrar
    register_resp = client.post("/users/register", json={
        "username": "ana", "email": "ana@mail.com", "password": "123456"
    })
    assert register_resp.status_code == 201

    # Paso 2: Hacer login
    login_resp = client.post("/token", data={
        "username": "ana", "password": "123456"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Paso 3: Usar el token
    me_resp = client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "ana"
```

### 8.2 Probar que la autenticacion funciona (debe rechazar sin token)

```python
def test_endpoint_protegido_sin_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401
```

### 8.3 Probar contraseña incorrecta

```python
def test_login_fallido(client):
    register = {"username": "ana", "email": "ana@mail.com", "password": "123456"}
    client.post("/users/register", json=register)

    response = client.post("/token", data={
        "username": "ana", "password": "contraseña_incorrecta"
    })
    assert response.status_code == 401
```

## 9. Probar roles — "Admin vs Student"

### 9.1 Hacer admin a un usuario en el test

```python
from app.models.user import User
from app.database import SessionLocal

@pytest.fixture()
def admin_token(client):
    # 1. Registrar usuario normal
    user_data = {"username": "admin", "email": "admin@mail.com", "password": "admin123"}
    client.post("/users/register", json=user_data)

    # 2. Cambiarle el rol directamente en BD
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "admin").first()
    user.role = "admin"
    db.commit()
    db.close()

    # 3. Hacer login (ahora es admin)
    response = client.post("/token", data={
        "username": "admin", "password": "admin123"
    })
    return response.json()["access_token"]
```

### 9.2 Probar que solo admin puede eliminar

```python
def test_eliminar_curso_solo_admin(client, created_course, auth_headers, admin_headers):
    course_id = created_course["id"]

    # Student intenta eliminar → 403
    response_student = client.delete(f"/courses/{course_id}", headers=auth_headers)
    assert response_student.status_code == 403

    # Admin elimina → 200
    response_admin = client.delete(f"/courses/{course_id}", headers=admin_headers)
    assert response_admin.status_code == 200
```

## 10. Probar errores — "No todo es 200"

> **En espanol simple:** Una API bien hecha no solo funciona cuando todo esta bien. Tambien responde correctamente cuando algo sale mal. Tus tests deben verificar ambos casos.

### 10.1 Errores que debes probar

| Codigo | Significado | Cuando ocurre |
|---|---|---|
| 200 | OK | Todo funciono |
| 201 | Creado | POST creo un recurso |
| 400 | Bad Request | Regla de negocio violada (curso duplicado) |
| 401 | Unauthorized | Token faltante o invalido |
| 403 | Forbidden | Usuario autenticado pero sin permiso |
| 404 | Not Found | Recurso no existe |
| 422 | Validation Error | Datos de entrada invalidos |

### 10.2 Ejemplos

```python
def test_404(client):
    response = client.get("/courses/9999")
    assert response.status_code == 404
    assert response.json()["mensaje"] == "Course con id 9999 no encontrado"


def test_422(client, auth_headers):
    response = client.post("/courses/", json={}, headers=auth_headers)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] is True
    assert "detalles" in data


def test_403(client, created_course, auth_headers):
    response = client.delete(f"/courses/{created_course['id']}", headers=auth_headers)
    assert response.status_code == 403
```

### 10.3 El error 422 en detalle

Cuando envias datos invalidos (ej: `POST /courses/` con `{}`), el handler personalizado retorna:

```json
{
  "error": true,
  "codigo": 422,
  "mensaje": "Datos invalidos",
  "detalles": [
    "body -> name: field required",
    "body -> credits: field required"
  ]
}
```

Tu test debe verificar esta estructura, no solo el codigo HTTP.

## 11. Probar middleware — "Headers y comportamiento global"

### 11.1 Verificar que X-Process-Time existe

```python
def test_x_process_time_header(client):
    response = client.get("/health/")
    assert "x-process-time" in response.headers
```

### 11.2 Verificar headers CORS

```python
def test_cors_headers(client):
    response = client.options(
        "/courses/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
```

## 12. Cobertura de codigo — "Que tanto de mi API esta siendo probado"

> **En espanol simple:** La cobertura te dice que porcentaje de tu codigo se ejecuta durante los tests. No garantiza que no haya bugs, pero te asegura que no hay partes que nunca se probaron.

### 12.1 Ejecutar con cobertura

```bash
pytest --cov=app --cov-report=term-missing
```

Salida:
```
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
app/__init__.py               0      0   100%
app/auth/dependencies.py     17      0   100%
app/auth/hash.py             5       0   100%
app/auth/jwt.py             12       0   100%
app/core/config.py           9       0   100%
...
app/services/course.py      10       0   100%
------------------------------------------------------
TOTAL                      120      10    92%
```

### 12.2 Interpretar la cobertura

| Cobertura | Que significa |
|---|---|
| 100% | Cada linea se ejecuto al menos una vez |
| 80-99% | Bien, pero hay codigo no probado |
| 50-79% | Faltan tests importantes |
| < 50% | Tu API sin tests es una caja de sorpresas |

### 12.3 ¿100% de cobertura = sin bugs?

**No.** La cobertura solo mide que lineas se ejecutaron, no que las verificaciones sean correctas. Puedes tener 100% de cobertura con tests que nunca hacen `assert`. La cobertura es una guia, no una garantia.

## 13. TDD — Test Driven Development

> **En espanol simple:** Escribir el test ANTES del codigo. El test falla porque la funcionalidad no existe. Luego escribes el codigo minimo para que el test pase. Luego refactorizas.

### 13.1 El ciclo TDD

```
1. ROJO: Escribes un test que falla
2. VERDE: Escribes el codigo minimo para que pase
3. REFACTOR: Mejoras el codigo sin cambiar el comportamiento
```

### 13.2 Ejemplo TDD en accion

Quieres agregar un endpoint `GET /health/ping` que retorne `{"pong": true}`.

**Paso 1 — Escribes el test:**
```python
def test_ping(client):
    response = client.get("/health/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}
```

Ejecutas:
```bash
pytest -k "ping"
# → FAIL: 404 Not Found
```

**Paso 2 — Escribes el codigo minimo:**
```python
@router.get("/ping")
def ping():
    return {"pong": True}
```

Ejecutas:
```bash
pytest -k "ping"
# → PASS
```

**Paso 3 — Refactorizas:** El codigo ya es minimo. No hay nada que refactorizar. Pasas al siguiente feature.

### 13.3 Ventajas de TDD

| Sin TDD | Con TDD |
|---|---|
| Escribes codigo y luego "piensas" en probarlo | Piensas en el comportamiento primero |
| Los tests se sienten como trabajo extra | Los tests guian el diseno |
| A veces "no hay tiempo" para tests | El test ES la definicion de "terminado" |
| El codigo tiende a ser mas complejo | El codigo tiende a ser mas simple (solo lo necesario para pasar el test) |

## 14. Estructura recomendada de tests

```
app/
  tests/
    __init__.py              # Vacio
    conftest.py              # Fixtures compartidas
    test_health.py           # Tests de health
    test_auth.py             # Tests de autenticacion
    test_courses.py          # Tests de cursos
    test_errors.py           # Tests de errores
    test_middleware.py       # Tests de middleware
```

### 14.1 ¿Que poner en cada archivo?

| Archivo | Que contiene |
|---|---|
| `conftest.py` | `client`, `test_db`, `test_user_data`, `token`, `auth_headers`, `admin_headers`, `course_data`, `created_course` |
| `test_health.py` | Tests de endpoints publicos que no requieren preparacion |
| `test_auth.py` | Tests de registro, login, token, users/me |
| `test_courses.py` | Tests de CRUD de cursos con y sin autenticacion |
| `test_errors.py` | Tests de formato de errores (404, 422, 403) |
| `test_middleware.py` | Tests de headers, CORS, logging |

### 14.2 Convenciones de nombres

| Elemento | Convencion | Ejemplo |
|---|---|---|
| Archivo | `test_<modulo>.py` | `test_auth.py` |
| Funcion | `test_<que_prueba>` | `test_login_success()` |
| Clase (opcional) | `Test<Modulo>` | `TestAuth` |
| Fixture | `<sustantivo>` | `client`, `token`, `auth_headers` |

## 15. Checklist de implementacion

- [ ] `pip install pytest httpx pytest-cov`
- [ ] Carpeta `app/tests/` con `__init__.py`
- [ ] `conftest.py` con `test_db`, `client`, `auth_headers`, `admin_headers`
- [ ] `test_health.py` — GET /health/ y /health/version
- [ ] `test_auth.py` — register, login, users/me (con y sin token)
- [ ] `test_courses.py` — CRUD, duplicados, permisos admin
- [ ] `test_errors.py` — formato de errores 404, 422, 403
- [ ] `test_middleware.py` — X-Process-Time, CORS headers
- [ ] `pytest -v` → todos pasan
- [ ] `pytest --cov=app` → cobertura minima 80%
- [ ] Escribir AL MENOS un test siguiendo TDD

## 16. Cierre conceptual

Los tests automatizados son la red de seguridad que te permite hacer cambios sin miedo. Con pytest + TestClient puedes verificar que tu API funciona correctamente en segundos, no en horas de pruebas manuales.

La regla de oro: **si no esta probado, esta roto** — solo que aun no lo sabes.

### Conceptos clave

| Concepto | Resumen |
|---|---|
| pytest | Framework que ejecuta funciones `test_*` y verifica con `assert` |
| TestClient | Cliente HTTP simulado para probar FastAPI desde Python |
| Fixture | Codigo que prepara el escenario antes de cada test |
| conftest.py | Archivo donde van las fixtures compartidas |
| Cobertura | Porcentaje del codigo que se ejecuta durante los tests |
| TDD | Escribir el test antes del codigo (rojo → verde → refactor) |

### Proxima clase
**Despliegue en Render + Supabase** — Llevaremos nuestra API a produccion para que cualquiera pueda usarla desde internet.
