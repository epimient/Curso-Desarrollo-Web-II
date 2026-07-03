# Ejemplo guiado - Autenticacion JWT en FastAPI

## Objetivo

Agregar autenticacion completa al proyecto de cursos: registro de usuarios, login con JWT, endpoints protegidos y control por roles.

---

## Requisitos

- Proyecto de Clase 08 funcionando (o al menos proyecto-con-bd de Clase 07).
- `pip install "passlib[bcrypt]" "python-jose[cryptography]"`

---

## Paso 1. Instalar dependencias

En `requirements.txt`:

```
fastapi[standard]
sqlalchemy
passlib[bcrypt]
python-jose[cryptography]
```

```bash
pip install -r requirements.txt
```

---

## Paso 2. Agregar configuracion de seguridad

En `app/core/config.py`, agrega:

```python
class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"
    secret_key: str = "supersecretkey1234567890"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
```

---

## Paso 3. Crear `app/auth/hash.py`

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**Prueba rapida:**
```python
h = hash_password("123456")
print(h)                    # → $2b$12$... (hash diferente cada vez)
print(verify_password("123456", h))  # → True
print(verify_password("otra", h))    # → False
```

---

## Paso 4. Crear `app/auth/jwt.py`

```python
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None
```

---

## Paso 5. Crear modelo User

`app/models/user.py`:

```python
from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student")
    active = Column(Boolean, default=True)
```

---

## Paso 6. Crear schemas de usuario

`app/schemas/user.py`:

```python
from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str
    active: bool
```

`app/schemas/token.py`:

```python
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
    role: str | None = None
```

---

## Paso 7. Crear `app/auth/dependencies.py`

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

---

## Paso 8. Crear servicio de usuarios

`app/services/user_service.py`:

```python
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.hash import hash_password


def create_user(user_data: UserCreate, db: Session) -> User:
    existing = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Username or email already exists"
        )

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


def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## Paso 9. Crear router de autenticacion

`app/routers/auth.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.auth.hash import verify_password
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_user
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_user_by_id

router = APIRouter(tags=["Auth"])


@router.post("/token", response_model=Token)
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
    return Token(access_token=access_token, token_type="bearer")


@router.post("/users/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_data, db)


@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## Paso 10. Proteger endpoints existentes

Modifica `app/routers/courses.py`:

```python
from app.auth.dependencies import get_current_user
from app.models.user import User


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ← NUEVO
):
    return create_course(course_data, db)


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    # ... logica de eliminacion (implementar en servicio)
    return {"detail": "Course deleted"}
```

---

## Paso 11. Actualizar `main.py`

```python
from app.routers import courses, health, auth

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health.router)
app.include_router(auth.router)      # ← NUEVO
app.include_router(courses.router)
```

---

## Paso 12. Probar el flujo completo desde Swagger UI

Abre `http://localhost:8000/docs` y ejecuta cada paso:

### 1. Registrar un usuario
- Busca `POST /users/register` → "Try it out"
- Ingresa en el Request body:
  ```json
  {"username": "ana", "email": "ana@mail.com", "password": "123456"}
  ```
- Haz clic en "Execute"
- **Respuesta esperada:** `201` con `{"id": 1, "username": "ana", "email": "ana@mail.com", "role": "student", "active": true}`

### 2. Hacer login (obtener token)
- Busca `POST /token` → "Try it out"
- En `form_data` (los campos aparecen separados):
  - `username`: `ana`
  - `password`: `123456`
- Haz clic en "Execute"
- **Respuesta esperada:** `{"access_token": "eyJ...", "token_type": "bearer"}`
- **Copia el token** (el texto largo que empieza con `eyJ`)

### 3. Autorizar Swagger con el token
- Haz clic en el boton **Authorize** 🔒 (arriba a la derecha)
- En el campo `Value`, pega: `Bearer <token_copiado>`
- Haz clic en "Authorize" → la ventana se cierra y el candado se bloquea
- Ahora todos los endpoints protegidos pueden ejecutarse sin pegar el token cada vez

### 4. Ver mi usuario (endpoint protegido)
- Busca `GET /users/me` → "Try it out" → "Execute"
- **Respuesta esperada:** `{"id": 1, "username": "ana", ...}`

### 5. Crear curso (autenticado)
- Busca `POST /courses` → "Try it out"
- Request body: `{"name": "Fisica", "credits": 4}`
- "Execute" → **Status 201**

### 6. Intentar crear curso SIN token
- Haz clic en el boton **Authorize** 🔒 → "Logout" (para desautorizar)
- Busca `POST /courses` → "Try it out" → mismo body que antes
- "Execute" → **Status 401** `{"detail": "Not authenticated"}`
- Vuelve a **Authorize** con tu token para restaurar el acceso

### 7. Eliminar curso falla (estudiante no tiene permiso)
- Busca `DELETE /courses/{course_id}` → "Try it out"
- `course_id`: `1`
- "Execute" → **Status 403** `{"detail": "Not enough permissions"}`
- Esto es correcto: ana es "student", no "admin"

---

## Paso 13. ¿Que pasaria si...?

Puedes probar todos estos escenarios directamente desde Swagger UI:

| Escenario | Como probarlo | Respuesta esperada |
|---|---|---|
| **Token expirado** | Modifica `ACCESS_TOKEN_EXPIRE_MINUTES` a `1` en `auth/jwt.py`, espera 1 minuto, y ejecuta `GET /users/me` | `401` "Could not validate credentials" |
| **Contraseña incorrecta** | En `POST /token`, usa `password: incorrecta` | `401` "Incorrect username or password" |
| **Usuario sin permisos de admin** | Con token de estudiante, ejecuta `DELETE /courses/{id}` | `403` "Not enough permissions" |
| **Usuario duplicado** | Ejecuta `POST /users/register` con un username que ya existe | `400` "Username or email already exists" |

> **Nota:** En el escenario de token expirado, despues de probarlo, restaura `ACCESS_TOKEN_EXPIRE_MINUTES` a `30` para no tener que refrescar el token constantemente durante el desarrollo.

---

## Resumen de archivos nuevos

| Archivo | Contenido |
|---|---|
| `app/auth/__init__.py` | Paquete de autenticacion |
| `app/auth/hash.py` | `hash_password()` y `verify_password()` con bcrypt |
| `app/auth/jwt.py` | `create_access_token()` y `decode_token()` |
| `app/auth/dependencies.py` | `get_current_user()` (extrae y verifica JWT) |
| `app/models/user.py` | Modelo User con `hashed_password` y `role` |
| `app/schemas/user.py` | `UserCreate` y `UserResponse` |
| `app/schemas/token.py` | `Token` y `TokenData` |
| `app/services/user_service.py` | `create_user()` y `get_user_by_id()` |
| `app/routers/auth.py` | `POST /token`, `POST /users/register`, `GET /users/me` |
| `app/core/config.py` | + `secret_key`, `algorithm`, `access_token_expire_minutes` |

---

## Cierre

La API ahora tiene puerta con cerradura. Los usuarios se registran, obtienen un JWT, y lo usan para acceder a endpoints protegidos. Los admins tienen permisos adicionales. Este patron (hash → token → dependencia → endpoint protegido) es el estandar en APIs REST modernas.
