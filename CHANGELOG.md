# Changelog

Todos los cambios relevantes de AprovechaElBug se registran en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto
usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [v0.1.0] - 2026-10-29

### Added
- Estructura de carpetas por dominio según el TRD §3.2 y `.env.example`.
- Backend mínimo: FastAPI con `GET /health`, `GET /api/v1/cursos` paginado (datos de ejemplo en memoria), formato uniforme de errores y configuración de SQLAlchemy.
- Frontend mínimo: React + Vite con la pantalla de catálogo consumiendo `GET /api/v1/cursos`, estados de carga, error y vacío, y proxy de `/api` al backend.
- Docker Compose de desarrollo con PostgreSQL 18.6, backend y frontend.

### Changed
- Flujo de Git: de GitHub Flow a rama de integración `dev` con releases versionadas en `main` (ver `docs/GIT_WORKFLOW.md`).