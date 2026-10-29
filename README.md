# AprovechaElBug

> WebApp de gestión de comunidad de cursos: catálogo comunitario de cursos gratuitos
> aportados y validados por los usuarios, más roadmaps personales de aprendizaje.
>
> **Estado:** Documentación (Instancia A) enviada a aprobación el 23/10/2026. Desarrollo pendiente de aprobación docente.

**Stack:** React 19 + Vite + pnpm · FastAPI + uv · PostgreSQL 18.6 · Docker Compose (dev)

**Autor:** Benavente, Dylan — Legajo 29176 · Materia: Desarrollo de Software, Comisión S34, 2026

---

## Cómo levantar

> En construcción: se completa en el ticket T4.

Requisitos: Git y Docker Desktop (incluye Docker Compose).

## Qué hace

Cualquier persona registrada puede aportar un curso gratuito de cualquier plataforma
(Udemy, Microsoft, Platzi, etc.) cargando su enlace y sus datos. Un moderador valida el
aporte y, una vez publicado, entra al catálogo comunitario. Desde ahí, cada usuario
arma su roadmap personal de aprendizaje.

## Documentación

| Documento | Responde la pregunta | Link |
|-----------|----------------------|------|
| SPEC | ¿Qué nos pidieron construir y qué decidimos nosotros? | [docs/SPEC.md](docs/SPEC.md) |
| PRD | ¿Para quién, qué problema resuelve, qué hace y qué NO hace? | [docs/PRD.md](docs/PRD.md) |
| TRD | ¿Cómo lo construimos técnicamente y por qué? | [docs/TRD.md](docs/TRD.md) |
| UX-UI | ¿Cómo se ve, se siente y se comporta? | [docs/UX-UI.md](docs/UX-UI.md) |
| APPFlow | ¿Qué pantallas hay y cómo se navega? | [docs/APPFlow.md](docs/APPFlow.md) |
| BackendSchema | ¿Qué datos persistimos y qué API expone? | [docs/BackendSchema.md](docs/BackendSchema.md) |
| Implementation Plan | ¿En qué orden construimos y qué significa "hecho"? | [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) |
| Flujo de Git | ¿Cómo se versiona este repo? | [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) |

## Cómo revisar este repo

- Los `.md` se renderizan solos en GitHub, incluidos los diagramas Mermaid.
- La historia de `docs/SPEC.md` muestra la SPEC de clase original (primer commit)
  y luego su refinamiento.

## Estado del trabajo

| Instancia | Contenido | Estado |
|-----------|-----------|--------|
| A — Documentación | repo + 7 documentos | Enviada a aprobación el 23/10/2026 |
| B — Desarrollo del MVP | ejecución del Implementation Plan | Pendiente de aprobación |
| Clase 27/10 | testing, Docker multi-stage, gestión del cambio | Pendiente |

## Versionado

- **Flujo de Git:** rama de integración `dev`; ramas `feat/T{N}-…` y `fix/…` que nacen de `dev` y vuelven a `dev`; `main` solo recibe releases con tag `vX.Y.Z` y su entrada en [CHANGELOG.md](CHANGELOG.md). Detalle en [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md).
- **Convención de commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `docker:`), incluidos merges y releases.