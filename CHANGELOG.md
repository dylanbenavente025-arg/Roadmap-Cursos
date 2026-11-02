# Changelog

Todos los cambios relevantes de AprovechaElBug se registran en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto
usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Added
- Reglas de negocio del curso como funciones puras (validación del aporte, normalización de enlaces, transiciones de estado) con tests unitarios (ticket C27-T1).
- Reglas del roadmap personal como funciones puras (agregar solo cursos publicados y sin repetir, reordenar, quitar y cambiar el avance) con tests unitarios (ticket C27-T2).
- Reglas de validación de aportes como funciones puras (solo el moderador valida, solo aportes en revisión, motivo obligatorio al rechazar) con tests unitarios (ticket C27-T3).
- Dockerfile multi-stage del backend sobre `python:3.13-alpine`, con usuario no-root y healthcheck contra `/health` (ticket C27-T7).
- `.dockerignore` del backend y del frontend: el contexto de build excluye dependencias locales, cachés, tests y secretos (ticket C27-T8).
- Dockerfile multi-stage del frontend: build con `node:22-alpine` y runtime `nginx:alpine-slim`, con fallback de SPA, proxy de `/api/`, caché de assets y cabeceras de seguridad (ticket C27-T9). 

### Changed
- El año de edición de un curso no puede ser futuro (BR-012).
- `uvicorn[standard]` pasa a ser dependencia de desarrollo; la imagen usa `uvicorn` sin extras.
- En Docker Compose, el frontend se sirve con nginx en lugar del servidor de desarrollo de Vite.

## [v0.1.0] - 2026-10-29

### Added
- Estructura de carpetas por dominio según el TRD §3.2 y `.env.example`.
- Backend mínimo: FastAPI con `GET /health`, `GET /api/v1/cursos` paginado (datos de ejemplo en memoria), formato uniforme de errores y configuración de SQLAlchemy.
- Frontend mínimo: React + Vite con la pantalla de catálogo consumiendo `GET /api/v1/cursos`, estados de carga, error y vacío, y proxy de `/api` al backend.
- Docker Compose de desarrollo con PostgreSQL 18.6, backend y frontend.

### Changed
- Flujo de Git: de GitHub Flow a rama de integración `dev` con releases versionadas en `main` (ver `docs/GIT_WORKFLOW.md`).