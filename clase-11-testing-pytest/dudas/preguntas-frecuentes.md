# Dudas frecuentes — Clase 11

> Aqui encontraras las preguntas que los estudiantes suelen hacer (pero a veces da verguenza preguntar). Todas son validas.

---

## 1. ¿Por que usamos TestClient y no `requests`?

**Respuesta corta:** Porque TestClient no necesita un servidor corriendo.

**Respuesta larga:** `requests` hace peticiones HTTP reales a una URL. Necesitas tener `uvicorn` corriendo. TestClient de FastAPI inyecta las peticiones directamente en la aplicacion FastAPI sin pasar por la red. Es mas rapido, no requiere puertos, y puedes controlar las dependencias (como la base de datos).

```python
# Con requests (necesitas servidor corriendo):
import requests
response = requests.get("http://localhost:8000/health/")

# Con TestClient (no necesita servidor):
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
response = client.get("/health/")
```

---

## 2. ¿Cual es la diferencia entre test funcional y test unitario?

**Respuesta corta:** Funcional prueba el sistema completo. Unitario prueba una funcion aislada.

**Respuesta larga:**

| Aspecto | Test funcional | Test unitario |
|---|---|---|
| Que prueba | Un endpoint completo (ruta → servicio → BD → respuesta) | Una funcion especifica (ej: `hash_password()`) |
| Velocidad | Mas lento (toca BD, aunque sea en memoria) | Muy rapido (no toca BD) |
| Dependencias | Reales (BD, auth, etc.) | Simuladas (mocks) |
| Confianza | Alta (prueba el flujo real) | Media (depende de que el mock sea correcto) |
| Ejemplo | `client.get("/courses/")` | `create_user(UserCreate(...), mock_db)` |

**Regla practica:** Empieza con tests funcionales (cubren mas). Agrega tests unitarios solo para logica compleja.

---

## 3. ¿Como aseguro que cada test empiece con la BD limpia?

**Respuesta corta:** Usa `@pytest.fixture(autouse=True)` con `create_all` + `drop_all`.

**Respuesta larga:** La fixture `test_db` en `conftest.py` se ejecuta automaticamente antes y despues de cada test:

```python
@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)  # Antes del test
    yield                                  # Durante el test
    Base.metadata.drop_all(bind=engine)    # Despues del test
```

Esto garantiza que cada test vea una base de datos recien creada. No importa si el test anterior creo, modifico o elimino datos.

---

## 4. Mis tests son lentos, ¿que hago?

**Respuesta corta:** Usa BD en memoria (`sqlite://`) en lugar de archivo.

**Respuesta larga:** Si usas `sqlite:///./test.db` (archivo), cada test escribe en disco. Cambia a `sqlite://` (sin ruta, en memoria pura) para tests mas rapidos:

```python
SQLALCHEMY_DATABASE_URL = "sqlite://"  # En memoria, mas rapido
```

Sin embargo, para propositos educativos es mejor usar un archivo (`.test.db`) porque puedes inspeccionarlo si un test falla y quieres ver el estado de la BD.

Otras tecnicas:
- Usa `pytest -x` para detenerte en el primer fallo (no ejecutas tests que no pasaran)
- Usa `pytest -k "expresion"` para probar solo un subconjunto

---

## 5. ¿Que significa "coverage" exactamente?

**Respuesta corta:** El porcentaje de lineas de tu codigo que se ejecutaron durante los tests.

**Respuesta larga:** Cuando ejecutas `pytest --cov=app`, pytest registra cada linea de codigo que se ejecuta. Al final, calcula:

```
Cobertura = (Lineas ejecutadas / Total de lineas) × 100
```

Si tienes 200 lineas y los tests ejecutaron 180, la cobertura es 90%.

**Importante:** 100% de cobertura NO significa que no haya bugs. Solo significa que cada linea se ejecuto al menos una vez. Un test puede ejecutar una linea y no verificar nada:

```python
def test_malo(client):
    client.get("/health/")  # Ejecuta la linea, pero no hace assert
    # 100% cobertura, 0% utilidad
```

La cobertura es una herramienta, no un objetivo.

---

## 6. ¿Debo probar cada middleware por separado?

**Respuesta corta:** No necesariamente. Prueba el efecto del middleware, no su implementacion.

**Respuesta larga:** No necesitas un test que diga "LoggingMiddleware se llama con tal argumento". En su lugar, prueba el resultado visible:

| Middleware | Que probar |
|---|---|
| LoggingMiddleware | Que la respuesta tiene header `X-Process-Time` |
| CORSMiddleware | Que los headers CORS estan presentes |
| TrustedHostMiddleware | Que un host no permitido es rechazado (400) |

El middleware se prueba indirectamente a traves de los endpoints. Si el middleware falla, los tests de los endpoints tambien fallaran (o se comportaran de forma inesperada).
