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