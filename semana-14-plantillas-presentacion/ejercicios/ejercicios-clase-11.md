# Ejercicios — Clase 11

> **Nota para el estudiante:** Los tests son la red de seguridad de tu codigo. Si no sabes por donde empezar, los ejercicios 0 y 1 son el camino mas corto. El desafio extra es para quienes ya se sienten comodos con pytest.

---

## Ejercicio 0. Rellenar espacios en blanco (calentamiento)

Completa las siguientes frases con las palabras del recuadro:

> **Palabras:** pytest | TestClient | fixture | assert | cobertura | conftest.py | TDD | 200

1. _________ es el framework de testing que usamos para ejecutar pruebas en Python.
2. _________ es el cliente HTTP simulado de FastAPI para hacer peticiones a la API sin necesidad de un servidor real.
3. Una _________ es una funcion que prepara el escenario antes de cada test (ej: crear la BD, registrar un usuario).
4. Las fixtures compartidas entre todos los tests se colocan en el archivo _________.
5. La palabra clave _________ se usa para verificar que una condicion es verdadera.
6. El ciclo ROJO → VERDE → REFACTOR es la base de _________.
7. El codigo HTTP _________ significa que la peticion fue exitosa.
8. La _________ mide que porcentaje del codigo se ejecuta durante los tests.

---

## Ejercicio 1. Agregar test de validacion de email

El endpoint `POST /users/register` actualmente no valida que el email tenga un formato valido. Pero los schemas de Pydantic incluyen validacion con `EmailStr` (si se agrega).

**Contexto:** Revisa el schema `UserCreate` en `app/schemas/user.py`. Si el campo `email` usara `EmailStr`, un email invalido como `"correo-invalido"` deberia retornar 422.

**Tarea:** Escribe un test que verifique que enviar un email invalido retorna 422.

```python
def test_register_invalid_email(client, test_user_data):
    # Modifica test_user_data para que tenga un email invalido
    # Envia la peticion a POST /users/register
    # Verifica que retorna 422
    ...
```

**Pista:** `test_user_data` es un diccionario. Puedes modificarlo antes de usarlo:
```python
invalid_data = {**test_user_data, "email": "correo-invalido"}
```

---

## Ejercicio 2. Escribir test completo de DELETE para admin

El endpoint `DELETE /courses/{course_id}` solo funciona si:
1. El usuario esta autenticado (tiene token)
2. El usuario tiene rol "admin"

**Tarea:** Escribe un test que verifique TODO el comportamiento de DELETE:

```python
def test_delete_course_full_scenario(
    client, auth_headers, admin_headers, course_data
):
    # 1. Crear un curso (como usuario autenticado)
    # 2. Verificar que el curso existe (GET /courses/{id} → 200)
    # 3. Intentar eliminar como estudiante → 403
    # 4. Verificar que el curso AUN existe
    # 5. Eliminar como admin → 200
    # 6. Verificar que el curso ya no existe (GET /courses/{id} → 404)
    ...
```

**Pista:** Usa `client.post()`, `client.get()`, `client.delete()` en secuencia. No olvides pasar los headers correspondientes.

---

## Ejercicio 3. Depurar test fallido

Observa este test:

```python
def test_crear_curso_sin_nombre(client, auth_headers):
    response = client.post(
        "/courses/",
        json={"credits": 4},
        headers=auth_headers,
    )
    assert response.status_code == 422
```

Cuando lo ejecutas, falla con:
```
FAILED test_courses.py::test_crear_curso_sin_nombre -
AssertionError: assert 201 == 422
```

**Preguntas:**
1. ¿Por que retorna 201 en lugar de 422?
2. ¿Que falta en el JSON enviado?
3. ¿El schema `CourseCreate` tiene el campo `name` como obligatorio?
4. **Solucion:** ¿Que debes corregir para que el test pase?

---

## Ejercicio 4. Escribir test unitario con mock

Los tests funcionales (los que usan TestClient) prueban el sistema completo. Pero a veces quieres probar una funcion de servicio de forma aislada, sin base de datos real.

**Tarea:** Escribe un test unitario para la funcion `create_user` del servicio `user_service.py` usando `unittest.mock.patch` para simular la base de datos.

```python
from unittest.mock import MagicMock, patch
from app.services.user_service import create_user
from app.schemas.user import UserCreate


def test_create_user_service():
    # 1. Crear un mock de la sesion de BD
    mock_db = MagicMock()

    # 2. Crear datos de usuario
    user_data = UserCreate(
        username="test",
        email="test@mail.com",
        password="123456",
    )

    # 3. Llamar a la funcion (sin BD real)
    # result = create_user(user_data, mock_db)

    # 4. Verificar que se llamo a mock_db.add() y mock_db.commit()
    ...
```

**Pista:** Un `MagicMock()` registra cada llamada que recibe. Puedes verificar con `mock_db.add.assert_called_once()`.

---

## Desafio extra (opcional)

**Objetivo:** Llevar la cobertura de tests a 95% o mas.

**Instrucciones:**

1. Ejecuta `pytest --cov=app --cov-report=term-missing` y anota el porcentaje actual y las lineas no cubiertas.

2. Identifica que codigo NO se esta probando (aparece en la columna `Missing`).

3. Escribe tests que cubran las lineas faltantes. Algunas ideas:
   - Probar que un usuario desactivado (`active=False`) no pueda hacer login
   - Probar el manejador de error 500 (Exception generica)
   - Probar que un `TrustedHostMiddleware` bloquea hosts no permitidos
   - Probar el escenario de token expirado

4. Vuelve a ejecutar la cobertura. Debes ver una mejora significativa.

**Meta:** `app/errors/handlers.py` suele tener lineas no cubiertas (el handler de 500). Escribe un test que fuerce una excepcion no controlada.
