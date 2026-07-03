# Dudas frecuentes - Clase 09

> Aqui encontraras las preguntas mas comunes sobre autenticacion y seguridad con JWT en FastAPI.

---

## 1. ¿Que es un hash de contraseña? ¿Por que no guardar la contraseña directamente?

**Respuesta corta:** Un hash convierte la contraseña en un codigo irreversible. Nunca guardes la contraseña en texto plano.

**Respuesta larga:** Si guardas `password = "123456"` en la BD y alguien roba la base de datos, tiene TODAS las contraseñas de TODOS tus usuarios. Con hash, el atacante obtiene algo como `$2b$12$LJ3m4ys...` que no se puede convertir de vuelta a "123456".

**El hash es como una licuadora:** Metes la contraseña, obtienes un batido. No importa que tengas el batido, no puedes recuperar los ingredientes originales. Pero puedes meter otra contraseña, licuarla, y comparar si los dos batidos son iguales.

---

## 2. ¿Que es bcrypt?

**Respuesta corta:** Es un algoritmo de hash disenado especificamente para contraseñas. Es lento a proposito.

**Respuesta larga:** A diferencia de algoritmos como MD5 o SHA256 (que son rapidos), bcrypt es deliberadamente lento. Esto hace que si un atacante roba la BD, le tome mucho tiempo probar contraseñas.

- MD5: puede probar **miles de millones** de contraseñas por segundo.
- bcrypt: puede probar **miles** de contraseñas por segundo.

Esa lentitud es la que protege tus contraseñas.

---

## 3. ¿Que es JWT? ¿Que partes tiene?

**Respuesta corta:** JSON Web Token. Es un string con tres partes separadas por puntos: header, payload, signature.

**Respuesta larga:**

```text
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIn0.fake_signature
├── HEADER ─┤├─── PAYLOAD ─────────┤├─── SIGNATURE ──┤
```

| Parte | Contenido | Proposito |
|---|---|---|
| Header | Algoritmo de firma | Decir como se firmo el token |
| Payload | Datos del usuario + expiracion | "Soy el usuario 1, rol admin, hasta las 15:30" |
| Signature | Firma digital | Garantizar que nadie modifico el token |

**Analogia:** El JWT es un carnet de identidad. El header dice "este carnet es plastico", el payload tiene tu foto y nombre, la firma es el sello oficial que garantiza que no es falso.

---

## 4. ¿Donde se guarda el JWT en el cliente?

**Respuesta corta:** En memoria (variable JS), localStorage, o en una cookie httpOnly.

**Respuesta larga:** Donde lo guardes depende del tipo de aplicacion:

| Donde | Ventaja | Desventaja |
|---|---|---|
| Memoria (variable) | Seguro contra XSS | Se pierde al recargar pagina |
| localStorage | Persiste entre recargas | Vulnerable a XSS |
| Cookie httpOnly | Seguro contra XSS | Mas complejo de implementar |

Para el curso, asumimos que el cliente guarda el token en memoria o localStorage y lo envia en el header `Authorization`.

---

## 5. ¿Que es OAuth2? ¿FastAPI lo implementa completo?

**Respuesta corta:** OAuth2 es un estandar de autorizacion. FastAPI implementa el **Password flow**, no OAuth2 completo.

**Respuesta larga:** OAuth2 tiene varios "flows" (formas de obtener un token). FastAPI implementa el **Resource Owner Password Credentials flow** (a veces llamado "password flow"), donde el usuario envia su username+password y recibe un token. Es el mas simple y el que usamos en este curso.

OAuth2 completo incluye otros flows como:
- Authorization Code (el de "Login with Google")
- Client Credentials (maquina a maquina)
- Implicit (obsoleto)

---

## 6. ¿Que hace `OAuth2PasswordBearer`?

**Respuesta corta:** Extrae el token del header `Authorization: Bearer <token>`.

**Respuesta larga:**

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
```

Esto crea una dependencia que:
1. Revisa el header `Authorization` en cada request.
2. Si no existe, responde con 401 automaticamente.
3. Si existe, extrae el token (la parte despues de "Bearer ").
4. El parametro `tokenUrl="/token"` solo es informativo (para la documentacion de `/docs`).

**No verifica el token.** Solo lo extrae. La verificacion la haces tu en `get_current_user()`.

---

## 7. ¿Que diferencia hay entre 401 Unauthorized y 403 Forbidden?

**Respuesta corta:** 401 = no estás autenticado (no tienes token). 403 = estás autenticado pero no tienes permiso.

**Respuesta larga:**

| Codigo | Significado | Ejemplo |
|---|---|---|
| 401 Unauthorized | No hay token, o el token es invalido/expirado | Llamar a `/users/me` sin header Authorization |
| 403 Forbidden | El token es valido, pero no tienes permisos | Un `student` intentando eliminar un curso (solo admin) |

**Analogia:** 401 es "la puerta del edificio esta cerrada y no tienes llave". 403 es "tienes llave para entrar al edificio, pero no para la oficina del director".

---

## 8. ¿Que pasa si el token expira?

**Respuesta corta:** El endpoint devuelve 401. El cliente debe obtener un token nuevo.

**Respuesta larga:** El token tiene una `exp` (expiration) en el payload. Cuando `jwt.decode()` encuentra un token expirado, lanza `ExpiredSignatureError`. Tu codigo lo captura y devuelve 401.

Para obtener un token nuevo, el cliente debe llamar a `/token` de nuevo con username+password.

**En aplicaciones reales** se usan **refresh tokens**: un token de larga duracion que permite obtener nuevos access tokens sin pedir la contraseña otra vez. No lo cubrimos en este curso.

---

## 9. ¿Como manejo roles?

**Respuesta corta:** Guarda el rol en el JWT y verificalo en cada endpoint protegido.

**Respuesta larga:** Cuando creas el token, incluyes el rol:

```python
create_access_token(data={"sub": str(user.id), "role": user.role})
```

Luego, en el endpoint, verificas:

```python
if current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Not enough permissions")
```

**Para simplificar,** puedes crear una dependencia reutilizable:

```python
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return current_user


@router.delete("/courses/{id}")
def delete_course(
    ...,
    admin: User = Depends(require_admin),
):
    ...
```

---

## 10. ¿Debo almacenar el token en localStorage o en cookie?

**Respuesta corta:** Para este curso, asumimos que el cliente lo guarda en memoria/localStorage.

**Respuesta larga:**

| Opcion | Seguridad | Facilidad |
|---|---|---|
| localStorage | Medio (vulnerable a XSS) | Facil |
| Cookie httpOnly | Alta (no accesible desde JS) | Media |
| Memoria (variable) | Alta (se pierde al recargar) | Facil |

Para prototipos y proyectos de curso, localStorage es aceptable. Para produccion, se recomienda cookie httpOnly con CSRF protection.

---

## 11. ¿Que es `python-jose`?

**Respuesta corta:** Es la libreria para crear y verificar JWT en Python.

**Respuesta larga:** Jose significa "JSON Object Signing and Encryption". `python-jose` permite:
- Firmar tokens con HMAC (HS256) o RSA (RS256)
- Verificar la firma
- Decodificar el payload

```python
from jose import jwt

# Crear
token = jwt.encode({"sub": "1"}, "clave_secreta", algorithm="HS256")

# Verificar
payload = jwt.decode(token, "clave_secreta", algorithms=["HS256"])
```

La razon de instalar `python-jose[cryptography]` (con el extra `cryptography`) es para tener soporte completo de algoritmos de firma.

---

## 12. ¿Que es `SECRET_KEY` y por que es importante?

**Respuesta corta:** Es la clave que firma los JWT. Si alguien la obtiene, puede falsificar tokens.

**Respuesta larga:** La `SECRET_KEY` se usa para:
- **Firmar** tokens al crearlos (`jwt.encode`)
- **Verificar** tokens al recibirlos (`jwt.decode`)

Si un atacante obtiene la `SECRET_KEY`, puede:
1. Crear tokens falsos con cualquier usuario y rol.
2. Acceder a endpoints protegidos como si fuera admin.

**Por eso NUNCA debes:**
- Hardcodearla en el codigo (usar variables de entorno).
- Subirla a Git.
- Compartirla.
- Usar claves debiles como "12345" o "secret".

En produccion, genera una clave con:
```bash
openssl rand -hex 32
```
