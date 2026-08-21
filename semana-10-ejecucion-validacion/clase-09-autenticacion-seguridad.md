# Clase 09 - Autenticacion y seguridad con JWT

## 1. Identificacion de la clase

**Asignatura:** Desarrollo de Aplicaciones Web II  
**Enfoque del curso:** FastAPI como framework principal para aplicaciones web y APIs modernas.  
**Semana:** 9  
**Unidad:** Unidad 2 - Uso de un Framework Especifico  
**Duracion sugerida:** 3 horas de acompanamiento directo y 6 horas de trabajo independiente.  
**Resultado de aprendizaje asociado:**

- RA3: Desarrollar habilidades para la creacion y manejo de rutas y controladores dentro del framework mediante la implementacion de logica de negocio en controladores o equivalentes pedagogicos.
- RA4: Aplicar principios de diseno de APIs RESTful en la construccion de servicios web mediante la implementacion de endpoints que cumplan con los estandares de la arquitectura REST.
- RA6: Mostrar una actitud proactiva y etica al enfrentar desafios y tomar decisiones durante el desarrollo de la aplicacion web.

## 2. Proposito de la clase

Hasta ahora la API no tiene restricciones: cualquier persona puede crear, modificar o eliminar datos. En esta clase se incorpora **autenticacion** (quien eres) y **autorizacion** (que puedes hacer) mediante JSON Web Tokens (JWT) y OAuth2.

Los estudiantes aprenderan a:

- hashear contraseñas con bcrypt para no guardarlas en texto plano;
- crear un endpoint `/token` que verifique credenciales y devuelva un JWT;
- proteger endpoints con `Depends(get_current_user)`;
- diferenciar roles (admin, student) para controlar acceso.

## 3. Pregunta orientadora

**Como evitamos que cualquier persona pueda modificar datos en nuestra API sin identificarse?**

---

> **En español simple:** Hoy la API es como una tienda sin puerta: cualquiera entra, agarra productos y se va. La autenticacion agrega una puerta con cerradura. Solo quienes tengan llave (JWT) pueden entrar, y algunos tienen pase VIP (admin).

---

## 4. Conceptos previos requeridos

- Modelos SQLAlchemy (Clase 07).
- Inyeccion de dependencias con `Depends()` (Clase 05 + 07).
- Schemas Pydantic (Clase 06).
- Concepto basico de que es un hash (de lo contrario, leer seccion 6).

## 5. El problema: API sin proteccion

```python
@router.post("/courses", response_model=CourseResponse)
def add_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    return create_course(course_data, db)
```

Cualquier persona con acceso a la API puede crear cursos. Cualquiera puede modificar o eliminar datos. No hay forma de:

- saber quien creo un curso;
- evitar que un estudiante elimine cursos de otros;
- restringir ciertas acciones solo a administradores.

---

> **En español simple:** Falta un "carnet de identidad" digital. Sin el, la API no sabe si eres estudiante, profesor, admin o un robot malicioso.

---

## 6. Hash de contraseñas

> **En español simple:** Guardar la contraseña tal cual en la BD es como dejar la combinacion de la caja fuerte escrita en la puerta. Si alguien roba la BD, tiene todas las contraseñas. El hash convierte la contraseña en un codigo irreversible.

### 6.1 Instalacion

```bash
pip install "passlib[bcrypt]"
```

### 6.2 Hashear una contraseña

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

**Salida tipica de `hash_password("123456")`:**

```
$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Q8p9CwqJq5Y7X8Z9a0B1C2D3E4F
```

**Esto NO es la contraseña.** Es un hash. No puedes recuperar "123456" a partir de ese string.

### 6.3 Verificar una contraseña

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

```python
verify_password("123456", hash)  # → True
verify_password("incorrecta", hash)  # → False
```

**Analogia:** Hashear es como meter la contraseña en una licuadora y obtener un batido. No importa que tengas el batido, no puedes recuperar los ingredientes originales. Pero puedes hacer el mismo proceso con otra contraseña y comparar si los batidos son iguales.

---

## 7. JSON Web Token (JWT)

> **En español simple:** Un JWT es un carnet de identidad digital. Tiene tus datos (quien eres), cuando vence, y una firma que garantiza que no fue falsificado.

### 7.1 Instalacion

```bash
pip install "python-jose[cryptography]"
```

### 7.2 Estructura de un JWT

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Tres partes separadas por puntos:

| Parte | Contenido | Que es |
|---|---|---|
| Header | `{"alg": "HS256", "typ": "JWT"}` | Algoritmo de firma |
| Payload | `{"sub": "user_id", "exp": 1234567890}` | Datos del usuario + expiracion |
| Signature | Firma digital | Garantiza que no fue modificado |

### 7.3 Crear un token

```python
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "clave-super-secreta-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `to_encode = data.copy()` | Copia los datos del usuario (ej: `{"sub": "1", "role": "admin"}`) |
| `expire = datetime.utcnow() + timedelta(minutes=30)` | Fecha de expiracion: 30 minutos desde ahora |
| `to_encode.update({"exp": expire})` | Agrega la expiracion al payload |
| `jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)` | Crea el token firmado con la clave secreta |

### 7.4 Decodificar un token

```python
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
```

Si el token expiro o fue manipulado, `jwt.decode()` lanza error y devolvemos `None`.

---

## 8. Modelo User

```python
from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student")  # "admin" o "student"
    active = Column(Boolean, default=True)
```

**Nota:** `hashed_password` guarda el hash, NO la contraseña en texto plano.

---

## 9. Flujo de autenticacion completo

```
Cliente                    Servidor
   │                          │
   │  POST /token             │
   │  {"username": "ana",     │
   │   "password": "123456"}  │
   │─────────────────────────→│
   │                          │ 1. Buscar usuario en BD
   │                          │ 2. Verificar password con bcrypt
   │                          │ 3. Crear JWT con user_id + role
   │  {"access_token": "eyJ.  │
   │   "token_type": "bearer"}│
   │←─────────────────────────│
   │                          │
   │  GET /courses (protegido)│
   │  Authorization: Bearer   │
   │  eyJ...                  │
   │─────────────────────────→│
   │                          │ 4. Extraer JWT del header
   │                          │ 5. Decodificar y validar
   │                          │ 6. Obtener usuario
   │                          │ 7. Ejecutar endpoint
   │  {"courses": [...]}      │
   │←─────────────────────────│
```

---

## 10. Paso a paso en codigo

### 10.1 Dependencia OAuth2

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
```

Esto le dice a FastAPI: "la autenticacion se hace enviando un token en el header `Authorization: Bearer <token>`, y el endpoint para obtener el token es `/token`".

### 10.2 Endpoint `/token`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.hash import verify_password
from app.auth.jwt import create_access_token
from app.models.user import User

router = APIRouter(tags=["Auth"])


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `OAuth2PasswordRequestForm = Depends()` | Toma los campos `username` y `password` del body del formulario |
| `db.query(User).filter(User.username == form_data.username).first()` | Busca el usuario por nombre de usuario |
| `if not user or not verify_password(...)` | Si no existe o la contraseña no coincide → error 401 |
| `create_access_token(data={"sub": str(user.id), "role": user.role})` | Crea el JWT con el ID y rol del usuario |
| `return {"access_token": ..., "token_type": "bearer"}` | FastAPI espera esta estructura exacta |

### 10.3 Dependencia `get_current_user`

```python
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.active:
        raise credentials_exception

    return user
```

**Desglose:**

| Linea | Que hace |
|---|---|
| `token: str = Depends(oauth2_scheme)` | Extrae el JWT del header `Authorization` |
| `jwt.decode(token, settings.secret_key, ...)` | Verifica la firma y la expiracion |
| `payload.get("sub")` | Obtiene el ID del usuario del JWT |
| `db.query(User).filter(User.id == int(user_id)).first()` | Busca el usuario en BD |
| `if user is None or not user.active` | Rechaza si el usuario no existe o esta desactivado |
| `return user` | Devuelve el usuario para que el endpoint lo use |

### 10.4 Proteger un endpoint

```python
@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/courses", response_model=CourseResponse)
def add_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_course(course_data, db)
```

**Como se ve ahora:**

```python
# ❌ ANTES: cualquiera podia crear cursos
def add_course(course_data, db):
    ...

# ✅ DESPUES: solo usuarios autenticados
def add_course(course_data, db, current_user: User = Depends(get_current_user)):
    ...
```

> **Asi NO ❌ vs Asi SI ✅**
>
> ❌ **Sin proteccion:**
> ```python
> @router.delete("/courses/{id}")
> def delete_course(course_id: int, db: Session = Depends(get_db)):
>     # Cualquiera puede eliminar cualquier curso
> ```
>
> ✅ **Con proteccion y verificacion de rol:**
> ```python
> @router.delete("/courses/{id}")
> def delete_course(
>     course_id: int,
>     db: Session = Depends(get_db),
>     current_user: User = Depends(get_current_user),
> ):
>     if current_user.role != "admin":
>         raise HTTPException(status_code=403, detail="Not enough permissions")
>     # Solo admins pueden eliminar
> ```

---

## 11. Registrar usuario

```python
from app.auth.hash import hash_password


def create_user(user_data: UserCreate, db: Session) -> User:
    existing = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="student",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

**Schema `UserCreate`:**

```python
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=6, max_length=100)
```

---

## 12. Errores comunes y troubleshooting

### 12.1 `401 Unauthorized` al llamar un endpoint protegido

**Causa 1:** No enviaste el header `Authorization`.  
**Solucion:** Agrega `Authorization: Bearer <token>`.

**Causa 2:** El token expiro (por defecto 30 min).  
**Solucion:** Obten un token nuevo en `/token`.

**Causa 3:** El token fue manipulado.  
**Solucion:** Verifica que el `SECRET_KEY` coincida entre creacion y verificacion.

### 12.2 `403 Forbidden` al intentar una accion de admin

**Causa:** Tu usuario tiene `role="student"` y el endpoint requiere `role="admin"`.  
**Solucion:** Cambia el rol del usuario en BD o usa un usuario con rol admin.

### 12.3 Error: `"detail": "Could not validate credentials"`

**Causa:** El JWT no se pudo decodificar (invalido, expirado, o firma incorrecta).  
**Solucion:** Revisa que el token sea valido en https://jwt.io.

### 12.4 `NotImplementedError: bcrypt`

**Causa:** No instalaste `bcrypt`.  
**Solucion:** `pip install "passlib[bcrypt]"`.

### 12.5 El hash cambia cada vez para la misma contraseña

**No es un error.** bcrypt usa un "salt" (valor aleatorio) cada vez, por lo que el hash es diferente aunque la contraseña sea la misma. `verify_password()` funciona correctamente porque el salt esta incluido en el hash.

---

## 13. Configuracion: variables sensibles

Agrega a `app/core/config.py`:

```python
class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"
    secret_key: str = "cambiar-en-produccion-por-clave-segura"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
```

> **Importante:** En produccion, `secret_key` debe ser una clave larga y aleatoria, no un texto fijo. Se recomienda usar variables de entorno.

---

## 14. Actividad central de clase

Agregar autenticacion completa al proyecto de cursos.

**Pasos:**
1. Instalar `passlib[bcrypt]` y `python-jose[cryptography]`.
2. Crear modelo `User` con username, email, hashed_password, role, active.
3. Implementar `hash_password()` y `verify_password()`.
4. Implementar `create_access_token()`.
5. Crear endpoint `POST /token` (login).
6. Implementar `get_current_user` como dependencia.
7. Proteger `POST /courses` (solo autenticados).
8. Proteger `DELETE /courses/{id}` (solo admin).
9. Crear endpoint `POST /users/register` (cualquiera puede registrarse).
10. Probar flujo completo: register → login → acceder a endpoint protegido.

## 15. Producto de clase — Checklist de verificacion

- [ ] `requirements.txt` incluye `passlib[bcrypt]` y `python-jose[cryptography]`
- [ ] Modelo `User` con `hashed_password` (nunca texto plano)
- [ ] Funcion `hash_password()` en `app/auth/hash.py`
- [ ] Funcion `verify_password()` en `app/auth/hash.py`
- [ ] Funcion `create_access_token()` en `app/auth/jwt.py`
- [ ] `POST /token` devuelve `{"access_token": "...", "token_type": "bearer"}`
- [ ] `get_current_user` en `app/auth/dependencies.py`
- [ ] `POST /courses` protegido con `Depends(get_current_user)`
- [ ] `DELETE /courses/{id}` solo accesible por admin (403 si no lo es)
- [ ] `POST /users/register` crea usuario con contraseña hasheada
- [ ] Probar flujo completo desde Swagger UI (/docs)
- [ ] `GET /users/me` devuelve el usuario del token actual

---

## 16. Cierre conceptual

La autenticacion con JWT es el estandar de facto en APIs REST modernas. FastAPI provee las herramientas (`OAuth2PasswordBearer`, `Depends`) para implementarla de forma limpia y reutilizable. El patron aprendido (hash → token → dependencia → endpoint protegido) se repite en practicamente cualquier API profesional.

---

## 17. Trabajo independiente

1. Agregar campo `created_by` (FK a User) en el modelo `Course`.
2. Modificar `create_course()` para que asocie el curso al usuario autenticado.
3. Crear endpoint `GET /users/me/courses` que retorne solo los cursos del usuario actual.
4. Crear un endpoint `PUT /users/{id}/role` que solo un admin pueda ejecutar.
5. Investigar como leer `SECRET_KEY` desde una variable de entorno en lugar de hardcodearlo.

---

## 18. Bibliografia y referencias utiles

- FastAPI. (s. f.). *Security*. https://fastapi.tiangolo.com/tutorial/security/
- FastAPI. (s. f.). *OAuth2 with Password (and hashing)*. https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- JWT. (s. f.). *Introduction to JSON Web Tokens*. https://jwt.io/introduction
- passlib. (s. f.). *CryptContext*. https://passlib.readthedocs.io/en/stable/
