## 1. ¿Que diferencia hay entre middleware y dependency injection?

**Respuesta corta:** El middleware se ejecuta para TODAS las rutas. La dependency injection se ejecuta solo para las rutas que la usan.

**Respuesta larga:** El middleware es como un seguridad en la puerta del edificio que revisa a TODOS los que entran. La dependency injection es como un traductor que solo esta presente en ciertas oficinas. El middleware no sabe a que endpoint vas (solo ve la request), mientras que `Depends()` se ejecuta dentro del contexto del endpoint y puede acceder a sus parametros.

**Analogia:** Middleware = filtro de agua en la entrada del edificio (toda el agua pasa por ahi). Dependency injection = filtro de agua en una canilla especifica (solo esa canilla lo tiene).

---

## 2. ¿Por que mi frontend recibe error CORS si la API funciona en Postman?

**Respuesta corta:** Porque CORS es una restriccion del navegador. Postman no lo implementa.

**Respuesta larga:** CORS es un mecanismo de seguridad del navegador. Cuando haces una request desde Postman, no hay navegador de por medio, por lo que CORS no se aplica. Cuando haces la misma request desde un frontend en React, el navegador la intercepta y verifica los headers CORS. Si el backend no los envia, el navegador bloquea la respuesta.

**Analogia:** Es como si Postman fuera un mensajero que entra por la puerta de servicio (sin seguridad), mientras que el navegador es un visitante que pasa por la puerta principal con seguridad. El mensajero pasa siempre, el visitante solo si tiene permiso.

---

## 3. ¿Que es una preflight request (OPTIONS)?

**Respuesta corta:** Es una request "de prueba" que el navegador envia antes de la request real para preguntar si el backend acepta el metodo y los headers.

**Respuesta larga:** Cuando el frontend quiere hacer una request "no simple" (con headers custom como `Authorization`, o metodo `DELETE`, o content-type `application/json`), el navegador primero envia un `OPTIONS` al mismo endpoint. Si el backend responde con los headers CORS correctos, el navegador procede con la request real. Si no, la bloquea.

**Analogia:** Es como llamar por telefono antes de ir a una fiesta: "¿Puedo ir? ¿Aceptan invitados?" (OPTIONS). Si te dicen que si, vas (request real). Si te dicen que no, te quedas en casa.

---

## 4. ¿Puedo tener multiples middlewares? ¿En que orden se ejecutan?

**Respuesta corta:** Si. Se ejecutan en el orden en que los agregaste (el primero en la lista es el primero en recibir la request).

**Respuesta larga:** Los middlewares funcionan como capas de cebolla. El primer middleware agregado es la capa mas externa: recibe la request primero y la respuesta ultimo. El ultimo middleware agregado es la capa mas interna: recibe la request ultimo y la respuesta primero.

```python
app.add_middleware(A)  # ← primero en recibir request, ultimo en recibir response
app.add_middleware(B)  # ← segundo
app.add_middleware(C)  # ← ultimo en recibir request, primero en recibir response
```

**Analogia:** Es como ponerse ropa en invierno: primero la camiseta, luego el buzo, luego la campera. La campera (primer middleware) ve la lluvia primero, pero tambien sale al exterior ultima.

---

## 5. ¿Cuando usar `@app.middleware("http")` vs `app.add_middleware()`?

**Respuesta corta:** Usa `add_middleware()` para middlewares empaquetados (CORS, TrustedHost). Usa `@app.middleware("http")` para middlewares personalizados simples.

**Respuesta larga:** `add_middleware()` acepta clases ASGI y es la forma estandar de integrar middlewares de terceros. `@app.middleware("http")` es un atajo para funciones asincronas simples. La principal diferencia practica es que `add_middleware()` permite pasar configuracion en el constructor, mientras que `@app.middleware()` solo recibe `request` y `call_next`.

**Analogia:** `add_middleware()` es como instalar un electrodomestico ya fabricado (solo lo conectas y configuras). `@app.middleware("http")` es como construir tu propio dispositivo desde cero.

---

## 6. ¿Como devuelvo un error 500 con mensaje personalizado?

**Respuesta corta:** Registra un handler para `Exception` con `@app.exception_handler(Exception)`.

**Respuesta larga:** Cualquier error no capturado que ocurra en tu app (excepcion no manejada, error de sintaxis, error de BD) se convierte en un 500. Sin un handler personalizado, FastAPI devuelve un JSON generico. Con el handler, puedes controlar el mensaje y loguear el error real sin exponerlo al cliente.

```python
@app.exception_handler(Exception)
async def handler(request: Request, exc: Exception):
    logger.error(f"Error interno: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": True, "mensaje": "Error interno del servidor"},
    )
```

**Advertencia:** Nunca devuelvas `str(exc)` al cliente en produccion. Loguealo internamente pero responde con un mensaje generico.

---

## 7. ¿Que es `RequestValidationError` y en que se diferencia de `HTTPException`?

**Respuesta corta:** `RequestValidationError` ocurre cuando los datos de entrada no pasan la validacion de Pydantic (error 422). `HTTPException` la lanzas manualmente para errores logicos (404, 401, 403, 400).

**Respuesta larga:** FastAPI lanza `RequestValidationError` automaticamente cuando Pydantic rechaza los datos de entrada (campo faltante, tipo incorrecto, validacion personalizada fallida). Tu nunca lanzas `RequestValidationError` directamente. `HTTPException`, en cambio, la lanzas manualmente en tu codigo cuando detectas una condicion de error (recurso no encontrado, sin permisos, regla de negocio violada).

**Analogia:** `RequestValidationError` = el portero automatico que revisa que tu DNI tenga foto y firma (si falta algo, no te deja entrar). `HTTPException` = el gerente que decide si puedes pasar a la sala VIP segun tu rol (decision humana/logica).

---

## 8. ¿`lifespan` es obligatorio? ¿Que pasa si no lo uso?

**Respuesta corta:** No es obligatorio. Si no lo usas, la app funciona igual pero sin tareas de inicializacion/limpieza.

**Respuesta larga:** `lifespan` es opcional. Si tu app solo necesita arrancar y servir requests sin configuracion previa, no lo necesitas. La mayoria de las apps simples funcionan sin el. Sin embargo, si necesitas crear tablas de BD al iniciar, conectar un cliente de Redis, o cargar un modelo ML, necesitas `lifespan`. La alternativa `@app.on_event("startup")` y `@app.on_event("shutdown")` esta deprecada en FastAPI moderno.

**Analogia:** `lifespan` es como la rutina de apertura y cierre de un local comercial. Si tienes un kiosco automatico 24h, no necesitas abrir/cerrar. Si tienes un restaurante con cocina, necesitas encender las hornallas al llegar y apagarlas al irte.

---

## 9. ¿`TrustedHostMiddleware` es obligatorio en produccion?

**Respuesta corta:** No es obligatorio, pero es altamente recomendado por seguridad.

**Respuesta larga:** `TrustedHostMiddleware` protege contra ataques de "Host Header Injection", donde un atacante envia una request con un header `Host` modificado para redirigir a los usuarios a un sitio malicioso. Sin este middleware, cualquier host es aceptado. Con el, solo los hosts en `allowed_hosts` son validos. Es una capa de seguridad simple pero efectiva.

**Analogia:** Es como tener un seguridad que revisa que la persona que llama al timbre tenga el apellido correcto. Si alguien dice ser "Perez" pero no esta en la lista, no le abres.

---

## 10. ¿Como hago para que ciertas rutas NO pasen por un middleware?

**Respuesta corta:** Revisa el `request.url.path` dentro del middleware y decide si ejecutar la logica o solo pasar la request.

**Respuesta larga:** No hay una forma declarativa de excluir rutas de un middleware. Debes hacerlo manualmente dentro del middleware:

```python
@app.middleware("http")
async def mi_middleware(request: Request, call_next):
    if request.url.path.startswith("/health"):
        # Saltar middleware para health checks
        return await call_next(request)
    # Logica del middleware aqui
    response = await call_next(request)
    return response
```

**Analogia:** Es como un filtro de agua que tiene una valvula de bypass para cuando solo quieres agua sin filtrar (ej: para el jardin). El agua sigue pasando, pero sin pasar por el filtro.

---

## 11. ¿Puedo modificar el body del request desde un middleware?

**Respuesta corta:** Teoricamente si, pero es complejo y no recomendado. Mejor modifica los datos en un `Depends()`.

**Respuesta larga:** El body de una request es un stream que solo se puede leer una vez. Si lo lees en un middleware, el endpoint ya no podra leerlo. Para modificarlo, necesitas leer el body completo, modificarlo, y crear un nuevo `Request` con el body modificado — lo cual es tedioso. La forma correcta es usar un middleware solo para tareas globales (logging, CORS, seguridad) y dejar la transformacion de datos a las dependencies.

**Analogia:** Es como abrir una carta, modificarla, y volver a cerrar el sobre. Es posible, pero es mas facil pedirle al destinatario que haga los cambios el mismo.

---

## 12. ¿Que es `request.state` y para que sirve?

**Respuesta corta:** Es un diccionario asociado a la request que permite compartir datos entre middleware, dependencies y endpoints.

**Respuesta larga:** `request.state` es un objeto donde puedes guardar informacion que se genera en un middleware y se consume en un endpoint. Por ejemplo, en un middleware puedes decodificar un token JWT y guardar el usuario en `request.state.user`, y luego en el endpoint accedes a `request.state.user` sin necesidad de otra dependency.

```python
# middleware
@app.middleware("http")
async def set_user(request: Request, call_next):
    request.state.user = None
    token = request.headers.get("Authorization")
    if token:
        request.state.user = decode_token(token)
    return await call_next(request)

# endpoint
@app.get("/me")
def read_me(request: Request):
    if request.state.user is None:
        raise HTTPException(status_code=401)
    return request.state.user
```

**Analogia:** `request.state` es como la bandeja de entrada de un hotel. El botones (middleware) deja las valijas (datos) ahi, y el huesped (endpoint) las recibe cuando llega a la habitacion.
