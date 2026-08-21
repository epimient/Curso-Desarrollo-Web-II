# Ejemplo guiado — Escribir tests para una API con pytest y httpx

## Objetivo

Escribir tests automatizados para todos los endpoints de la API academica usando pytest y el TestClient de FastAPI.

Al final de este ejemplo, tendras una suite de tests que verifica:
- Endpoints publicos (health)
- Autenticacion (registro, login, token, users/me)
- CRUD de cursos (con y sin autenticacion)
- Roles (admin vs student)
- Errores (404, 422, 403)
- Middleware (X-Process-Time, CORS)

---

## Paso 1. Instalar dependencias de testing

```bash
cd proyecto-con-testing
pip install pytest httpx pytest-cov
```

**Explicacion:** `pytest` es el framework de testing. `httpx` es el cliente HTTP que usa TestClient internamente. `pytest-cov` mide la cobertura de codigo.

**Verificacion:**
```bash
pytest --version
# → pytest 8.x
```

---

## Paso 2. Crear la estructura de tests

Dentro de `app/`, crea la carpeta `tests/`:

```bash
mkdir app/tests
touch app/tests/__init__.py
```

Tu estructura ahora es:

```
app/
  tests/
    __init__.py          # Vacio, le dice a Python que es un paquete
    conftest.py          # (lo crearemos en el paso 3)
    test_health.py       # (paso 4)
    test_auth.py         # (paso 5)
    test_courses.py      # (paso 6)
    test_errors.py       # (paso 7)
    test_middleware.py   # (paso 8)
```

**Explicacion:** Todos los archivos que empiezan con `test_` son descubiertos automaticamente por pytest. El archivo `conftest.py` contiene las fixtures que se comparten entre todos los tests.

---

## Paso 3. Crear conftest.py con las fixtures

Crea `app/tests/conftest.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.user import User

# --- Base de datos para tests ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# --- Fixtures ---

@pytest.fixture(autouse=True)
def test_db():
    """Crea las tablas antes de cada test y las elimina despues."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    """Cliente HTTP simulado para probar la API."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user_data():
    """Datos de un usuario de prueba."""
    return {"username": "ana", "email": "ana@mail.com", "password": "123456"}


@pytest.fixture()
def token(client, test_user_data):
    """Registra un usuario y retorna su token JWT."""
    client.post("/users/register", json=test_user_data)
    response = client.post("/token", data={
        "username": test_user_data["username"],
        "password": test_user_data["password"],
    })
    return response.json()["access_token"]


@pytest.fixture()
def auth_headers(token):
    """Headers con token de autenticacion."""
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_token(client):
    """Registra un admin y retorna su token."""
    user_data = {"username": "admin", "email": "admin@mail.com", "password": "admin123"}
    client.post("/users/register", json=user_data)
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "admin").first()
    user.role = "admin"
    db.commit()
    db.close()
    response = client.post("/token", data={"username": "admin", "password": "admin123"})
    return response.json()["access_token"]


@pytest.fixture()
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture()
def course_data():
    return {"name": "Fisica", "credits": 4}


@pytest.fixture()
def created_course(client, auth_headers, course_data):
    """Crea un curso y retorna sus datos."""
    response = client.post("/courses/", json=course_data, headers=auth_headers)
    return response.json()
```

**Explicacion linea por linea:**

| Linea | Que hace |
|---|---|
| `@pytest.fixture(autouse=True)` | Se ejecuta automaticamente en cada test sin necesidad de declararlo |
| `Base.metadata.create_all(bind=engine)` | Crea las tablas de la BD antes del test |
| `yield` | Pausa la fixture, ejecuta el test, luego continua |
| `Base.metadata.drop_all(bind=engine)` | Elimina las tablas despues del test |
| `app.dependency_overrides[get_db] = override_get_db` | Reemplaza la BD real por la de pruebas |
| `with TestClient(app) as c:` | Crea el cliente HTTP y lo cierra al terminar |

---

## Paso 4. Escribir tests de health

Crea `app/tests/test_health.py`:

```python
def test_health_status(client):
    """GET /health/ debe retornar 200 con status ok."""
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_version(client):
    """GET /health/version debe retornar datos de la app."""
    response = client.get("/health/version")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "environment" in data
```

**Explicacion:** Son los tests mas simples: solo verifican que los endpoints publicos respondan correctamente.

**Ejecutar:**
```bash
pytest -v -k "health"
# → 2 passed
```

---

## Paso 5. Escribir tests de autenticacion

Crea `app/tests/test_auth.py`:

```python
def test_register_success(client, test_user_data):
    """Registrar un usuario debe retornar 201 con los datos."""
    response = client.post("/users/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert data["role"] == "student"
    assert data["active"] is True


def test_register_duplicate(client, test_user_data):
    """Registrar el mismo usuario dos veces debe dar 400."""
    client.post("/users/register", json=test_user_data)
    response = client.post("/users/register", json=test_user_data)
    assert response.status_code == 400


def test_login_success(client, test_user_data):
    """Login correcto debe retornar un token."""
    client.post("/users/register", json=test_user_data)
    response = client.post("/token", data={
        "username": test_user_data["username"],
        "password": test_user_data["password"],
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client, test_user_data):
    """Login con contrasena incorrecta debe dar 401."""
    client.post("/users/register", json=test_user_data)
    response = client.post("/token", data={
        "username": test_user_data["username"],
        "password": "wrongpass",
    })
    assert response.status_code == 401


def test_users_me_without_token(client):
    """GET /users/me sin token debe dar 401."""
    response = client.get("/users/me")
    assert response.status_code == 401


def test_users_me_with_token(client, test_user_data, token):
    """GET /users/me con token debe retornar el usuario."""
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == test_user_data["username"]
```

**Explicacion:** Cada test verifica un aspecto del flujo de autenticacion. Nota que no necesitamos limpiar la BD porque `test_db` lo hace automaticamente.

**Ejecutar:**
```bash
pytest -v -k "auth"
# → 6 passed
```

---

## Paso 6. Escribir tests de cursos

Crea `app/tests/test_courses.py`:

```python
def test_list_courses_empty(client):
    """Al inicio no debe haber cursos."""
    response = client.get("/courses/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_course_without_token(client, course_data):
    """Crear curso sin autenticacion debe dar 401."""
    response = client.post("/courses/", json=course_data)
    assert response.status_code == 401


def test_create_course_with_token(client, auth_headers, course_data):
    """Crear curso autenticado debe dar 201."""
    response = client.post("/courses/", json=course_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == course_data["name"]


def test_create_duplicate_course(client, auth_headers, course_data):
    """Curso con nombre duplicado debe dar 400."""
    client.post("/courses/", json=course_data, headers=auth_headers)
    response = client.post("/courses/", json=course_data, headers=auth_headers)
    assert response.status_code == 400


def test_get_course_by_id(client, created_course, course_data):
    """Obtener curso por ID debe retornar el curso."""
    response = client.get(f"/courses/{created_course['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == course_data["name"]


def test_get_course_not_found(client):
    """Curso inexistente debe dar 404."""
    response = client.get("/courses/9999")
    assert response.status_code == 404


def test_delete_course_as_student(client, auth_headers, created_course):
    """Estudiante no puede eliminar cursos (403)."""
    response = client.delete(
        f"/courses/{created_course['id']}", headers=auth_headers
    )
    assert response.status_code == 403


def test_delete_course_as_admin(client, admin_headers, created_course):
    """Admin puede eliminar cursos (200)."""
    response = client.delete(
        f"/courses/{created_course['id']}", headers=admin_headers
    )
    assert response.status_code == 200
```

**Explicacion:** Los tests de cursos cubren el CRUD completo y los permisos. Nota como las fixtures `auth_headers` y `admin_headers` nos permiten probar ambos roles.

**Ejecutar:**
```bash
pytest -v -k "course"
# → 8 passed
```

---

## Paso 7. Escribir tests de errores y middleware

### 7.1 test_errors.py

```python
def test_422_validation_error(client, auth_headers):
    """Enviar JSON vacio debe retornar 422 con formato personalizado."""
    response = client.post("/courses/", json={}, headers=auth_headers)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] is True
    assert data["codigo"] == 422
    assert "detalles" in data
    assert len(data["detalles"]) > 0


def test_404_not_found_format(client):
    """Error 404 debe tener formato personalizado."""
    response = client.get("/courses/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] is True
    assert "no encontrado" in data["mensaje"].lower()


def test_403_forbidden_format(client, auth_headers, created_course):
    """Error 403 debe tener formato personalizado."""
    response = client.delete(
        f"/courses/{created_course['id']}", headers=auth_headers
    )
    assert response.status_code == 403
    data = response.json()
    assert data["error"] is True
    assert "permisos" in data["mensaje"].lower()
```

### 7.2 test_middleware.py

```python
def test_x_process_time_header(client):
    """Toda respuesta debe incluir X-Process-Time."""
    response = client.get("/health/")
    assert "x-process-time" in response.headers


def test_cors_headers_present(client):
    """OPTIONS debe incluir headers CORS."""
    response = client.options(
        "/courses/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" in response.headers


def test_cors_allows_specific_origin(client):
    """El origin configurado debe estar permitido."""
    response = client.options(
        "/courses/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
```

**Explicacion:** Estos tests verifican comportamiento transversal (middleware) que aplica a TODAS las rutas.

**Ejecutar:**
```bash
pytest -v -k "error or middleware"
# → 6 passed
```

---

## Paso 8. Ejecutar todos los tests y medir cobertura

### 8.1 Ejecutar todos los tests

```bash
pytest -v
```

Deberias ver algo como:
```
app/tests/test_health.py::test_health_status PASSED
app/tests/test_health.py::test_health_version PASSED
app/tests/test_auth.py::test_register_success PASSED
app/tests/test_auth.py::test_register_duplicate PASSED
app/tests/test_auth.py::test_login_success PASSED
app/tests/test_auth.py::test_login_wrong_password PASSED
app/tests/test_auth.py::test_users_me_without_token PASSED
app/tests/test_auth.py::test_users_me_with_token PASSED
app/tests/test_courses.py::test_list_courses_empty PASSED
app/tests/test_courses.py::test_create_course_without_token PASSED
...
```

### 8.2 Medir cobertura

```bash
pytest --cov=app --cov-report=term-missing
```

Salida esperada:
```
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
app/__init__.py                   0      0   100%
app/auth/__init__.py              0      0   100%
app/auth/dependencies.py         17      0   100%
app/auth/hash.py                  5      0   100%
app/auth/jwt.py                  12      0   100%
app/core/__init__.py              0      0   100%
app/core/config.py               10      0   100%
app/database.py                  11      0   100%
app/errors/__init__.py            0      0   100%
app/errors/exceptions.py         10      0   100%
app/errors/handlers.py           20      0   100%
app/main.py                      29      0   100%
app/middleware/__init__.py        0      0   100%
app/middleware/logging.py        12      0   100%
app/models/__init__.py            0      0   100%
app/models/course.py              8      0   100%
app/models/user.py                8      0   100%
app/routers/__init__.py           0      0   100%
app/routers/auth.py              28      0   100%
app/routers/courses.py           25      0   100%
app/routers/health.py             7      0   100%
app/schemas/__init__.py           0      0   100%
app/schemas/course.py             5      0   100%
app/schemas/token.py              3      0   100%
app/schemas/user.py               5      0   100%
app/services/__init__.py          0      0   100%
app/services/course_service.py   15      0   100%
app/services/user_service.py     11      0   100%
-----------------------------------------------------------
TOTAL                           241      0   100%
```

### 8.3 Generar reporte HTML (opcional)

```bash
pytest --cov=app --cov-report=html
```

Abre `htmlcov/index.html` en el navegador para ver un reporte visual con el codigo coloreado por cobertura.

---

## Resumen: lo que lograste

| Paso | Que hiciste | Archivos creados |
|---|---|---|
| 1 | Instalaste pytest, httpx, pytest-cov | `requirements.txt` actualizado |
| 2 | Creaste la carpeta tests | `app/tests/__init__.py` |
| 3 | Escribiste las fixtures compartidas | `app/tests/conftest.py` |
| 4 | Tests de health | `app/tests/test_health.py` |
| 5 | Tests de autenticacion | `app/tests/test_auth.py` |
| 6 | Tests de cursos | `app/tests/test_courses.py` |
| 7 | Tests de errores y middleware | `test_errors.py`, `test_middleware.py` |
| 8 | Ejecutaste todos los tests y mediste cobertura | Reporte de pytest |
