# Changelog

Todos los cambios relevantes de AprovechaElBug se registran en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto
usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [v0.2.0] - 2026-11-02

Ciclo de la clase del 27/10 (tickets C27-T1 a C27-T11) sobre la v0.1.0: reglas de negocio con
tests, catálogo persistido en PostgreSQL, imágenes multi-stage y arranque con healthchecks.
El ticket C27-T5 (integración del flujo aporte → validación) queda pendiente: necesita el login
y los roles, que todavía no están construidos (tareas 1.x y 3.x del Implementation Plan).

### Added
- Reglas de negocio del curso como funciones puras (validación del aporte, normalización de enlaces, transiciones de estado) con tests unitarios (C27-T1).
- Reglas del roadmap personal como funciones puras (agregar solo cursos publicados y sin repetir, reordenar, quitar y cambiar el avance) con tests unitarios (C27-T2).
- Reglas de validación de aportes como funciones puras (solo el moderador valida, solo aportes en revisión, motivo obligatorio al rechazar) con tests unitarios (C27-T3).
- Modelos de SQLAlchemy para `usuarios`, `categorias` y `cursos`, `CursoRepository` con paginación y filtros, y datos iniciales (C27-T4).
- `GET /api/v1/cursos` acepta los filtros `q` (título y tema) y `categoria` (C27-T4).
- Tests de integración contra PostgreSQL del repository, del endpoint del catálogo y del seed (C27-T4).
- `useCursos` soporta paginación (`setPage`), filtros (`setFiltros`, que vuelve a la página 1) y `refetch`, con tests de Vitest y Testing Library (C27-T6).
- Dockerfile multi-stage del backend sobre `python:3.13-alpine`, con usuario no-root y healthcheck contra `/health` (C27-T7).
- `.dockerignore` del backend y del frontend: el contexto de build excluye dependencias locales, cachés, tests y secretos (C27-T8).
- Dockerfile multi-stage del frontend: build con `node:22-alpine` y runtime `nginx:alpine-slim`, con fallback de SPA, proxy de `/api/`, caché de assets y cabeceras de seguridad (C27-T9).
- Healthcheck de PostgreSQL con `pg_isready` y arranque en cascada en Docker Compose (C27-T10).
- Cierre del ciclo en el README: tickets, resultados y retrospectiva (C27-T11).

### Changed
- El año de edición de un curso no puede ser futuro (BR-012).
- El catálogo se lee de PostgreSQL en lugar de una lista en memoria; el backend crea las tablas y carga los datos iniciales al arrancar.
- `uvicorn[standard]` pasa a ser dependencia de desarrollo; la imagen usa `uvicorn` sin extras.
- En Docker Compose, el frontend se sirve con nginx en lugar del servidor de desarrollo de Vite.
- Flujo de Git: prefijos de rama `test/`, `docker/` y `docs/` con `C27-T{N}` para los tickets de la clase, y `feat/M{n}` para los módulos del plan.

## [v0.1.0] - 2026-10-29

### Added
- Estructura de carpetas por dominio según el TRD §3.2 y `.env.example`.
- Backend mínimo: FastAPI con `GET /health`, `GET /api/v1/cursos` paginado (datos de ejemplo en memoria), formato uniforme de errores y configuración de SQLAlchemy.
- Frontend mínimo: React + Vite con la pantalla de catálogo consumiendo `GET /api/v1/cursos`, estados de carga, error y vacío, y proxy de `/api` al backend.
- Docker Compose de desarrollo con PostgreSQL 18.6, backend y frontend.

### Changed
- Flujo de Git: de GitHub Flow a rama de integración `dev` con releases versionadas en `main` (ver `docs/GIT_WORKFLOW.md`).