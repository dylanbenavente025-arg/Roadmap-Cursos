# AprovechaElBug

> WebApp de gestión de comunidad de cursos: catálogo comunitario de cursos gratuitos
> aportados y validados por los usuarios, más roadmaps personales de aprendizaje.
>
> **Estado:** Instancia B en desarrollo — release v0.2.0 (tests, catálogo en PostgreSQL y Docker multi-stage).

**Stack:** React 19 + Vite + pnpm · FastAPI + uv · PostgreSQL 18.6 · Docker Compose (dev)

**Autor:** Benavente, Dylan — Legajo 29176 · Materia: Desarrollo de Software, Comisión S34, 2026

---

## Cómo levantar

Requisitos: Git y Docker Desktop (incluye Docker Compose).

```bash
git clone https://github.com/dylanbenavente025-arg/Roadmap-Cursos.git
cd Roadmap-Cursos
cp .env.example .env
docker compose up --build
```

| Qué | URL |
|-----|-----|
| Frontend | http://localhost:5173 |
| Backend (health) | http://localhost:8000/health |
| API del catálogo | http://localhost:8000/api/v1/cursos |
| Documentación de la API | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 (credenciales en `.env`) |

- Detener: `Ctrl+C` y luego `docker compose down`. Borrar también la base: `docker compose down -v`.
- Si un puerto está ocupado, cambiá `POSTGRES_PORT`, `BACKEND_PORT` o `FRONTEND_PORT` en `.env`.
- Las imágenes copian el código: después de cambiarlo, volvé a correr `docker compose up --build`.

## Cómo correr los tests

**Backend** (los tests de integración necesitan PostgreSQL levantado):

```bash
docker compose up -d postgres --wait
cd backend
uv run pytest --cov=app --cov-report=term-missing
```

**Frontend:**

```bash
cd frontend
pnpm test
```

> Con Docker Compose, el frontend se sirve con nginx (versión de producción). Para desarrollar
> con recarga automática: `docker compose up -d postgres --wait`, después `uv run uvicorn app.main:app --reload`
> en `backend` y `pnpm dev` en `frontend`.

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
| A — Documentación | repo + 7 documentos | Aprobada |
| B — Desarrollo del MVP | ejecución del Implementation Plan | En desarrollo — v0.1.0 (29/10) y v0.2.0 (02/11) publicadas |
| Clase 27/10 | testing, Docker multi-stage, gestión del cambio | Hecha fuera de término: 10 de 11 tickets; C27-T5 pendiente |

## Versionado

- **Flujo de Git:** rama de integración `dev`; ramas `feat/T{N}-…` y `fix/…` que nacen de `dev` y vuelven a `dev`; `main` solo recibe releases con tag `vX.Y.Z` y su entrada en [CHANGELOG.md](CHANGELOG.md). Detalle en [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md).
- **Convención de commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `docker:`), incluidos merges y releases.

## Ciclo de la clase del 27/10

Realizado fuera de término (del 29/10 al 02/11), sobre la v0.1.0. Publicado como **v0.2.0**.

| Ticket | Qué hace | Rama | Estado |
|--------|----------|------|--------|
| C27-T1 | Tests unitarios de las reglas del curso | `test/C27-T1-reglas-curso` | Hecho |
| C27-T2 | Tests unitarios de las reglas del roadmap | `test/C27-T2-reglas-roadmap` | Hecho |
| C27-T3 | Tests unitarios de la validación de aportes | `test/C27-T3-validacion-aportes` | Hecho |
| C27-T4 | Tests de integración del `CursoRepository` (y catálogo en PostgreSQL) | `test/C27-T4-repository-cursos` | Hecho |
| C27-T5 | Tests de integración del flujo aporte → validación | — | **Pendiente**: necesita login y roles (401 y 403), todavía no construidos |
| C27-T6 | Tests del hook `useCursos` con Vitest | `test/C27-T6-hook-cursos` | Hecho |
| C27-T7 | Dockerfile multi-stage del backend | `docker/C27-T7-backend-multistage` | Hecho |
| C27-T8 | `.dockerignore` del backend y del frontend | `docker/C27-T8-dockerignore` | Hecho |
| C27-T9 | Dockerfile multi-stage del frontend con nginx | `docker/C27-T9-frontend-nginx` | Hecho |
| C27-T10 | Healthchecks y arranque en cascada en Compose | `docker/C27-T10-compose-healthchecks` | Hecho |
| C27-T11 | Cierre: CHANGELOG, retrospectiva y release | `docs/C27-T11-cierre` | Hecho |

### Resultados frente a los criterios de la clase

| Criterio | Mínimo | Resultado |
|----------|--------|-----------|
| Tests pasando | 0 failed, 0 skipped | backend 129 passed · frontend 11 passed |
| Cobertura del backend (unit + integración) | ≥ 85 % | 98 % |
| Imagen del backend (multi-stage) | < 100 MB | ~93 MB (`python:3.13-alpine`) |
| Imagen del frontend (multi-stage + nginx) | < 30 MB | 15,2 MB (`nginx:alpine-slim`) |
| Docker Compose | 3/3 healthy | 3/3 healthy |
| Commits | 100 % Conventional Commits | 100 %, salvo una excepción documentada (ver retrospectiva) |
| Gestión del cambio | rama por ticket, merges según el flujo, CHANGELOG | una rama por ticket, `merge --no-ff` a `dev`, CHANGELOG por release |

### Retrospectiva

1. **Funcionó:** una rama por ticket con `merge --no-ff` y mensaje convencional; `git log --graph` muestra cada ticket como un bloque auditable de punta a punta.
2. **Funcionó:** escribir primero el test que falla y commitearlo antes del código dejó la evidencia de TDD en el historial; con las reglas de negocio como funciones puras, la cobertura llegó al 98 %.
3. **Cambié sobre la marcha:** el flujo pasó de GitHub Flow a `dev` + releases (27/10), y sumé prefijos `test/`, `docker/` y `docs/` con `C27-T{N}` para no confundir estos tickets con los T1 a T5 del scaffold; lo documenté en `GIT_WORKFLOW.md` antes de usarlo.
4. **Cambié sobre la marcha:** las imágenes del ticket (`slim`, `nginx:alpine`, `node:20`) no cumplían los objetivos de tamaño ni el TRD; usé `alpine` y `alpine-slim` y lo justifiqué en el TRD. T5 quedó pendiente porque el login todavía no existe.
5. **A mejorar:** el único commit no convencional (`Merge pull request #1`) se hizo con el botón de PR de GitHub en la Instancia A; desde entonces todos los merges se hacen por consola con `-m`. No reescribí la historia para no alterar commits ni tags ya publicados.