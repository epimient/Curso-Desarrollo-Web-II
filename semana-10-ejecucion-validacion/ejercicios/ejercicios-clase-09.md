# Ejercicios - Clase 09

> **Nota:** El ejercicio 0 es de calentamiento. Los ejercicios 1-5 construyen progresivamente sobre el ejemplo de autenticacion.

---

## Ejercicio 0. Emparejar terminos

Une cada termino de la izquierda con su descripcion a la derecha:

| Termino | Descripcion |
|---|---|
| 1. `hash_password()` | A. Codigo HTTP cuando no hay token o es invalido |
| 2. `verify_password()` | B. Codigo HTTP cuando el token no tiene permisos suficientes |
| 3. `create_access_token()` | C. Convierte una contraseña en un hash irreversible |
| 4. `get_current_user()` | D. Header donde se envia el JWT |
| 5. `Authorization: Bearer` | E. Compara una contraseña contra un hash |
| 6. 401 Unauthorized | F. Genera un JWT con datos del usuario + expiracion |
| 7. 403 Forbidden | G. Extrae y verifica el JWT, devuelve el usuario |
| 8. `OAuth2PasswordBearer` | H. Clase de FastAPI que extrae el token del header |

---

## Ejercicio 1. Implementar hash y verificacion

Sin mirar el ejemplo, escribe las funciones `hash_password()` y `verify_password()`:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Escribe aqui
    ...


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Escribe aqui
    ...
```

**Prueba:**
```python
h = hash_password("micontrasena")
assert verify_password("micontrasena", h) == True
assert verify_password("otra", h) == False
print("✓ Prueba pasada")
```

---

## Ejercicio 2. Endpoint /token

Completa el endpoint de login:

```python
@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # 1. Buscar usuario por form_data.username
    # 2. Verificar contraseña con verify_password()
    # 3. Si falla, lanzar HTTPException 401
    # 4. Crear access_token con {"sub": str(user.id), "role": user.role}
    # 5. Retornar Token(access_token=..., token_type="bearer")
    ...
```

**Verificacion desde Swagger UI:**
1. Abre `http://localhost:8000/docs`
2. Busca `POST /token` → "Try it out"
3. En los campos `form_data`, escribe `username: ana`, `password: 123456`
4. "Execute" → debe retornar `{"access_token": "eyJ...", "token_type": "bearer"}`

---

## Ejercicio 3. Proteger un endpoint existente

Protege el endpoint `POST /courses` para que solo usuarios autenticados puedan crear cursos:

```python
@router.post("/", response_model=CourseResponse, status_code=201)
def add_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ← Agrega esto
):
    return create_course(course_data, db)
```

**Verificacion desde Swagger UI:**
1. Abre `http://localhost:8000/docs`
2. Busca `POST /courses` → "Try it out"
3. Sin token aun, envia `{"name": "Fisica", "credits": 4}` → debe dar **401** "Not authenticated"
4. Ahora haz clic en **Authorize** 🔒, pega tu token como `Bearer <token>`, cierra
5. Vuelve a `POST /courses` → "Try it out" → mismo body → "Execute"
6. Ahora debe dar **201 Created** con los datos del curso

---

## Ejercicio 4. Endpoint solo para admin

Crea un endpoint que solo usuarios con `role="admin"` puedan ejecutar:

```python
@router.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Si el rol NO es "admin", lanzar HTTPException 403
    # Si es admin, ejecutar la eliminacion
    ...
```

**Pista:** Para hacer a un usuario admin, puedes modificar la BD directamente:

```bash
sqlite3 cursos.db "UPDATE users SET role='admin' WHERE username='ana';"
```

---

## Ejercicio 5. Depurar errores de autenticacion

Identifica la causa de cada error y escribe la solucion:

**Error A:** `GET /users/me` con **Authorize** vacio → `401 "Not authenticated"`
- **Causa:** No se envio el token.
- **Solucion:** Usa el boton **Authorize** 🔒 para pegar el token.

**Error B:** `POST /token` con contraseña incorrecta → `401 "Incorrect username or password"`
- **Causa:** La contraseña no coincide con el hash almacenado.
- **Solucion:** Usa la contraseña correcta o registra un nuevo usuario.

**Error C:** `DELETE /courses/{id}` con token de estudiante → `403 "Not enough permissions"`
- **Causa:** El usuario esta autenticado pero su rol no es "admin".
- **Solucion:** Cambia el rol a "admin" en la BD (`sqlite3 cursos.db "UPDATE users SET role='admin' WHERE username='ana';"`) o registra un usuario con role="admin".

**Error D:**
```python
# Al ejecutar uvicorn:
ModuleNotFoundError: No module named 'passlib'
```

**Error E:**
```python
# Al hacer login:
jose.exceptions.ExpiredSignatureError: Signature has expired
```

---

## Desafio extra (opcional)

Implementa `PUT /users/{user_id}/role` que permita a un admin cambiar el rol de otro usuario.

**Requisitos:**
1. Solo accesible por usuarios con `role="admin"`.
2. Recibe `{"role": "admin"}` o `{"role": "student"}` en el body.
3. Valida que el role sea valido.
4. No permite que un admin se quite su propio rol (opcional).

```python
class RoleUpdate(BaseModel):
    role: str = Field(pattern="^(admin|student)$")


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verificar que current_user es admin
    # Buscar user por user_id
    # Actualizar role
    # Guardar y retornar
    ...
```

**Verificacion desde Swagger UI:**
1. Con token de admin en **Authorize**, ejecuta `PUT /users/{user_id}/role` con `user_id: 2`, body `{"role": "admin"}` → debe dar **200 OK**
2. Haz **Logout** del Authorize, ingresa un token de estudiante, ejecuta el mismo endpoint → debe dar **403**
