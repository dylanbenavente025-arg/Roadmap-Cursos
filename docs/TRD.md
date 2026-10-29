# TRD — Technical Requirements Document — AprovechaElBug

> **Qué es:** el CÓMO técnico de AprovechaElBug: stack, decisiones de arquitectura,
> estructura de carpetas y convenciones. El producto está en el [PRD](PRD.md); el orden de
> construcción, en el [Implementation Plan](IMPLEMENTATION_PLAN.md).

## 1. Stack y versiones exactas

Versiones verificadas el 23/10/2026 (ver [SPEC §6](SPEC.md)).

| Capa | Elección | Versión exacta | Por qué |
|------|----------|----------------|---------|
| Frontend | React + Vite + pnpm sobre Node | react 19.3.1 · vite 8.3.5 · pnpm 12.4.1 · node 22.17.1 | fijado por la SPEC; Vite da un servidor de desarrollo rápido y un proxy simple hacia la API |
| Backend | FastAPI + uv sobre Python | fastapi 0.161.1 · uv 0.13.5 · python 3.13.5 | fijado por la SPEC; validación y documentación OpenAPI automáticas |
| Validación | Pydantic (dependencia de FastAPI) | pydantic 2.14.1 | contratos de entrada y salida tipados |
| ORM / driver | SQLAlchemy 2 + psycopg 3 + Alembic | se fija en `uv.lock` al instalar (Instancia B) | modelo explícito, migraciones versionadas y repositorios simples |
| Seguridad | bcrypt (paquete `bcrypt`) y PyJWT | se fija en `uv.lock` al instalar | bcrypt exigido por la SPEC; JWT para la sesión (TD-001) |
| BD | PostgreSQL | 18.6 | fijado por la SPEC |
| Infra (dev) | Docker + Docker Compose | docker 29.9.2 · compose 5.6.1 | fijado por la SPEC |

> Los lockfiles (`uv.lock`, `pnpm-lock.yaml`) se versionan en la Instancia B y pasan a ser
> la fuente exacta de versiones de las librerías de aplicación.

## 2. Decisiones técnicas

| # | Decisión | Alternativas consideradas | Elegida | Por qué |
|---|----------|---------------------------|---------|---------|
| TD-001 | Autenticación y sesión | JWT en header `Authorization` guardado en `localStorage` · sesión en servidor · JWT en cookie HttpOnly | JWT (HS256) en cookie HttpOnly `SameSite=Lax`, expira a los 60 min, sin refresh. El token lleva `sub` y `rol` | La cookie HttpOnly no es legible desde JavaScript (mitiga robo por XSS). Como el frontend consume la API por el mismo origen (proxy de Vite), no hace falta CORS con credenciales. Sin refresh simplifica el MVP |
| TD-002 | Paginación | offset + total · cursor | offset + total: `page` (desde 1) y `page_size` (20 por defecto, máximo 50) | El paginador estilo Google necesita ir a una página concreta y conocer el total; los volúmenes del MVP no justifican cursores |
| TD-003 | Formato de errores de la API | envelope propio · RFC 7807 (`problem+json`) | Envelope propio `{ "error": { "code", "message", "details" } }` | Más simple de consumir desde el frontend y de testear; el `code` estable permite traducir mensajes sin depender del texto |
| TD-004 | Cómo modelar "mi roadmap" | tabla intermedia usuario-curso con orden y estado · lista dentro del usuario · tabla `roadmaps` con ítems (varios roadmaps por usuario) | Tabla `roadmap_items` (usuario, curso, orden, estado de avance) con restricción única por usuario y curso | Cubre BR-003 y BR-007 con una restricción de base de datos; un roadmap por usuario alcanza para el MVP |
| TD-005 | Rate limiting del login (BR-009) | `slowapi` · tabla en PostgreSQL · Redis · implementación propia en memoria | Implementación propia en memoria: contador de fallos por clave `IP + email` en ventana deslizante de 15 min, máximo 5; responde 429 con `Retry-After` | Un solo proceso en desarrollo, sin servicios nuevos, y la lógica queda como función pura con reloj inyectable, testeable el 27/10. Se pierde al reiniciar el backend (riesgo aceptado, ver §6) |
| TD-006 | Recuperación de contraseña (BR-008) | SMTP real · MailHog · registro en el log | Token aleatorio (`secrets.token_urlsafe(32)`); se guarda solo su hash SHA-256 con vencimiento a 1 h y marca de uso. El enlace de restablecimiento se escribe en el log del backend | Sin servidor de correo en desarrollo. Guardar solo el hash evita que una filtración de la base entregue tokens usables |
| TD-007 | Datos iniciales | cargar a mano · migración de datos · script de seed | Script `seed` idempotente que crea categorías, el moderador (credenciales desde variables de entorno) y cursos de prueba para el catálogo | Reproducible en una máquina limpia (RNF-009) y permite medir RNF-007 con datos |


## 3. Arquitectura

### 3.1 Patrón y capas

Screaming Architecture + arquitectura en capas:

```mermaid
flowchart LR
    HTTP[Router - HTTP] --> SVC[Service - reglas de negocio]
    SVC --> REPO[Repository - acceso a datos]
    REPO --> DB[(PostgreSQL)]
    SVC --> MODELS[Models - entidades]
```

- **Router:** recibe HTTP, valida con los schemas, delega al service y traduce el resultado. Sin lógica de negocio.
- **Service:** reglas de negocio (BR-001 a BR-011). Funciones testeables sin base de datos ni HTTP; el reloj y el generador de tokens se inyectan.
- **Repository:** única puerta a la base de datos. Sin reglas de negocio.
- **La estructura de carpetas habla del dominio**, no del framework: `identidad`, `categorias`, `cursos`, `aportes`, `roadmap`.

### 3.2 Estructura de carpetas (la que se crea en la Instancia B)

```text
roadmap-cursos/
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── migrations/
│   ├── app/
│   │   ├── main.py                 # app FastAPI, routers y handlers de errores
│   │   ├── config.py               # variables de entorno
│   │   ├── database.py             # engine y sesión
│   │   ├── errores.py              # envelope de errores (TD-003)
│   │   ├── paginacion.py           # parámetros y respuesta paginada (TD-002)
│   │   ├── seed.py                 # datos iniciales (TD-007)
│   │   ├── identidad/              # registro, login, sesión, recuperación, rate limit
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── categorias/             # lista cerrada de categorías
│   │   ├── cursos/                 # catálogo comunitario (solo publicados)
│   │   ├── aportes/                # aportar, mis aportes y validación del moderador
│   │   └── roadmap/                # roadmap personal
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── vite.config.js              # incluye el proxy de /api
│   ├── Dockerfile
│   └── src/
│       ├── main.jsx
│       ├── app/                    # shell, router, header con menú sándwich
│       ├── features/
│       │   ├── identidad/          # registro, login, recuperación
│       │   ├── catalogo/           # listado, detalle, búsqueda y filtros
│       │   ├── aportes/            # formulario, mis aportes, panel de validación
│       │   └── roadmap/            # mi roadmap
│       │       ├── components/
│       │       ├── hooks/
│       │       └── api.js
│       ├── compartido/             # paginador, botones, cliente HTTP, toasts
│       └── styles/                 # tokens globales (UX-UI)
├── docker-compose.yml
├── .env.example
└── docs/
```

Los módulos `categorias`, `cursos`, `aportes` y `roadmap` repiten la estructura de `identidad` (router, service, repository, models, schemas). `aportes` y `cursos` comparten la entidad `Curso`, definida en `cursos/models.py`.

### 3.3 Servicios Docker (entorno de desarrollo)

| Servicio | Imagen / base | Puerto | Rol |
|----------|---------------|--------|-----|
| postgres | postgres:18.6 | 5432 | base de datos, con volumen y healthcheck |
| backend | python:3.13-slim + uv | 8000 | API FastAPI (modo desarrollo) |
| frontend | node:22-alpine + pnpm | 5173 | SPA Vite (servidor de desarrollo) |

```mermaid
flowchart LR
    BROWSER[Navegador :5173] --> FE[frontend Vite]
    FE -- "/api/*" --> BE[backend FastAPI :8000]
    BE --> PG[(postgres :5432)]
```

- El navegador solo habla con el frontend; Vite reenvía `/api/*` al backend (proxy con `xfwd` para conservar la IP del cliente, necesaria para el rate limiting).
- El backend arranca después de que PostgreSQL pasa su healthcheck, ejecuta las migraciones y el seed, y recién entonces levanta la API.
- El volumen de PostgreSQL se monta según indica la documentación de la imagen 18 (verificar el punto de montaje al escribir el `docker-compose.yml`).

> En la clase del 27/10 los Dockerfiles evolucionan a multi-stage. Por ahora, lo mínimo que levanta.


## 4. Convenciones

- **Commits:** Conventional Commits (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `docker`).
- **Flujo de Git:** rama de integración `dev`, ramas `feat/T{N}-…` y `fix/…` que nacen de `dev`, y releases con tag `vX.Y.Z` en `main` (hasta el 23/10 se usó GitHub Flow). Detalle en [GIT_WORKFLOW.md](GIT_WORKFLOW.md).
- **Errores de API (TD-003):** toda respuesta de error usa este formato, con `code` estable en mayúsculas:

  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Hay campos inválidos",
      "details": [
        { "field": "email", "message": "El email ya está registrado" }
      ]
    }
  }
  ```

  | Código HTTP | `code` | Cuándo |
  |-------------|--------|--------|
  | 401 | `UNAUTHENTICATED` | sin sesión o sesión vencida; credenciales inválidas |
  | 403 | `FORBIDDEN` | sesión válida sin el rol necesario |
  | 404 | `NOT_FOUND` | recurso inexistente o no visible para el usuario |
  | 409 | `CONFLICT` | email o enlace duplicado; curso ya incluido en el roadmap |
  | 422 | `VALIDATION_ERROR` | datos inválidos |
  | 429 | `RATE_LIMITED` | login bloqueado; incluye el encabezado `Retry-After` |
  | 500 | `INTERNAL_ERROR` | error inesperado, sin detalles internos |

- **Variables de entorno** (el repo incluye `.env.example`; el `.env` real no se versiona):

  | Variable | Ejemplo | Obligatoria | Descripción |
  |----------|---------|-------------|-------------|
  | `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | `aprovecha` / `cambiar` / `aprovechaelbug` | sí | credenciales del contenedor de PostgreSQL |
  | `DATABASE_URL` | `postgresql+psycopg://aprovecha:cambiar@postgres:5432/aprovechaelbug` | sí | conexión del backend |
  | `JWT_SECRET` | cadena larga aleatoria | sí | firma del token |
  | `JWT_EXPIRES_MINUTES` | `60` | no | vida de la sesión |
  | `COOKIE_SECURE` | `false` | no | `true` en producción (HTTPS) |
  | `LOGIN_MAX_ATTEMPTS` / `LOGIN_WINDOW_MINUTES` | `5` / `15` | no | rate limiting del login |
  | `RESET_TOKEN_TTL_MINUTES` | `60` | no | vencimiento del token de recuperación |
  | `FRONTEND_BASE_URL` | `http://localhost:5173` | sí | base del enlace de restablecimiento |
  | `MODERADOR_EMAIL` / `MODERADOR_PASSWORD` | datos de prueba | sí | usuario moderador creado por el seed |

- **Logging y excepciones:** `logging` estándar de Python con nivel INFO y formato de una línea (fecha, nivel, módulo, mensaje). Nunca se registran contraseñas ni tokens de sesión; la única excepción deliberada es el enlace de recuperación en desarrollo (TD-006). Las reglas de negocio lanzan excepciones de dominio que un handler global traduce al envelope de errores; cualquier otra excepción se registra con su traza y responde `INTERNAL_ERROR`.

## 5. Requisitos no funcionales técnicos (traducción de las restricciones)

| Restricción | Cómo se cumple | Dónde se verifica |
|-------------|----------------|-------------------|
| Paginación de listados | TD-002: `page` y `page_size` en todos los GET de listado | `GET /api/v1/cursos?page=…&page_size=…` y demás listados del BackendSchema |
| Mobile-first con mejora progresiva | tokens y breakpoints de UX-UI §3, sin media queries en la base | componentes críticos: header, catálogo, formulario de aporte |
| Menú sándwich | componente de header con panel lateral y ARIA | APPFlow §3 y UX-UI §4.5 |
| Screaming Architecture | árbol de §3.2 | revisión del repositorio |
| Apariencia tipo Google | tokens concretos en UX-UI §2 | revisión visual contra UX-UI |
| bcrypt (RNF-006) | paquete `bcrypt` con costo 12, sin librerías intermedias | test unitario del service de identidad (clase del 27/10) |
| Rate limiting (BR-009) | TD-005 | test unitario de la función de límite con reloj inyectado |
| `docker compose up` completo (RNF-009) | §3.3 y TD-007 | verificación en máquina limpia al cierre de la Instancia B |

## 6. Riesgos técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| El rate limiting en memoria se pierde al reiniciar el backend y no escala a varios procesos | alta | bajo | aceptado en el MVP (un solo proceso); documentado; migrar a tabla o Redis si hubiera varios procesos |
| El backend ve la IP del contenedor y no la del cliente, y el límite pierde sentido | media | medio | proxy de Vite con `xfwd` y lectura de `X-Forwarded-For`; verificar en la Instancia B |
| Las migraciones con Alembic llevan más tiempo del estimado | media | medio | primera migración generada desde los modelos; el Plan reserva una tarea específica |
| Cookie `HttpOnly` con `SameSite=Lax` y falta de protección CSRF explícita | baja | medio | solo se aceptan peticiones JSON, y `SameSite=Lax` bloquea envíos entre sitios con métodos que modifican datos; revisar si se agregan formularios clásicos |
| El punto de montaje del volumen de PostgreSQL 18 cambió respecto de versiones anteriores | media | bajo | consultar la documentación de la imagen al escribir el `docker-compose.yml`, y probar `down` y `up` conservando datos |
| El formulario de aporte tiene muchos campos y su validación consume más tiempo | media | medio | un único schema de validación por campo en backend y reglas equivalentes en frontend |

---

**Referencia:**
- Design Docs at Google: https://www.industrialempathy.com/posts/design-docs-at-google/