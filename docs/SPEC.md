# SPEC — AprovechaElBug

> **Qué es este documento:** la versión refinada de la SPEC de clase.
> El primer commit de este archivo es la SPEC oficial recibida el 21/10/2026, sin modificar.
> Lo que sigue es su evolución: mismos requisitos, ambigüedades resueltas y decisiones
> incorporadas, cada una con su origen.

## 1. Identidad del producto

- **Nombre propio:** AprovechaElBug
- **Una línea:** para estudiantes que quieren aprender gratis · catálogo comunitario de
  cursos gratuitos validados y roadmaps personales de aprendizaje · evita perder tiempo
  entre ofertas dispersas y de calidad dudosa.

## 2. Problema

Los cursos gratuitos de calidad existen, pero están repartidos entre decenas de plataformas
(Udemy, Microsoft Learn, Platzi, entre otras) y mezclados con promociones temporales,
cursos desactualizados o contenido de baja calidad. Quien quiere aprender un tema tiene que
buscar plataforma por plataforma, sin saber si el curso sigue vigente, si entrega
certificado, si exige examen o si lo respalda alguna organización.

Hoy esto se resuelve con listas sueltas en foros o redes, marcadores personales o buscadores
generales. Ninguna de esas vías valida la información ni ayuda a ordenar el aprendizaje:
cada persona repite la misma búsqueda y descubre los mismos callejones sin salida.

Una comunidad cambia la ecuación: cada persona que descubre un curso útil lo aporta una
sola vez con sus datos concretos (incluyendo si realmente lo tomó) y una validación lo
deja disponible para todos. El esfuerzo de curar se reparte, y la información mejora con
cada aporte. Además, un roadmap personal convierte una lista de cursos en un plan de
aprendizaje con orden y seguimiento.

## 3. Visión

En su mejor versión, dentro de 12 meses, AprovechaElBug es el lugar de referencia de la
comunidad estudiantil para encontrar cursos gratuitos confiables: un catálogo amplio y
vigente, con información verificada por la comunidad, y roadmaps que los estudiantes
construyen, siguen y comparten para llegar a un objetivo de aprendizaje concreto.

## 4. Alcance

### Dentro

- Registro, login y cierre de sesión, con contraseñas cifradas con bcrypt.
- Rate limiting en el endpoint de login.
- Recuperación de contraseña con ciclo completo: solicitud, token y nueva contraseña.
- Aporte de cursos gratuitos con enlace activo y todos los datos exigidos por la SPEC.
- Declaración de si quien aporta tomó el curso.
- Validación de aportes por un moderador (aprobar o rechazar con motivo).
- Catálogo comunitario paginado, con búsqueda por texto y filtro por categoría.
- Roadmap personal: incluir cursos del catálogo, ordenarlos y marcar su avance.
- Interfaz mobile-first con mejora progresiva, menú sándwich y estética tipo Google.

### Fuera (out of scope explícito)

- Cursos de pago, y cualquier tipo de pasarela o cobro.
- Alojar o reproducir contenido de los cursos: solo se guarda el enlace externo.
- Verificación automática de enlaces o extracción (scraping) de datos de las plataformas.
- Valoraciones, comentarios o foros sobre los cursos.
- Roadmaps públicos o compartidos entre usuarios.
- Envío real de correos: en desarrollo el token de recuperación se registra en el log.
- Gestión de usuarios y roles desde la interfaz: el moderador se crea por seed.
- Edición de aportes ya enviados, y reenvío de aportes rechazados (se aporta uno nuevo).
- Inicio de sesión con redes sociales, app móvil nativa, internacionalización.

## 5. Reglas de producto clave

| # | Regla | Origen |
|---|-------|--------|
| BR-001 | Un curso aportado entra al sistema "en revisión" y solo llega al catálogo comunitario tras ser validado | SPEC clase ("cursos cargados y **validados** pasan al catálogo") |
| BR-002 | Quien aporta un curso declara si él o ella lo tomó | SPEC clase |
| BR-003 | El roadmap es personal: cada usuario ve y edita solo el suyo | decisión propia |
| BR-004 | Un mismo enlace de curso no puede existir dos veces en el sistema | decisión propia |
| BR-005 | Solo un usuario con rol moderador valida o rechaza aportes; el rechazo exige un motivo | decisión propia |

> El detalle completo de reglas vive en el PRD §7.


## 6. Stack registrado (versiones exactas con las que se va a desarrollar)

| Capa | Tecnología | Versión exacta instalada |
|------|------------|--------------------------|
| Frontend | React + Vite + pnpm | react 19.3.1 · vite 8.3.5 · pnpm 12.4.1 |
| Backend | FastAPI + uv | fastapi 0.161.1 · uv 0.13.5 |
| Base de datos | PostgreSQL | 18.6 |
| Infra (dev) | Docker + Docker Compose | docker 29.9.2 · compose 5.6.1 |

> Versiones verificadas el 23/10/2026 con `pnpm view`, `uv`, `docker --version` y
> `docker compose version`. La SPEC oficial referencia FastAPI 0.158.2 (21/10/2026).

## 7. Restricciones técnicas heredadas de la SPEC de clase

| # | Restricción | Cómo la vamos a cumplir |
|---|-------------|-------------------------|
| 1 | Mobile-first con mejora progresiva: base sin media queries; `@media (min-width: …)` solo para agregar o mejorar | CSS base de una columna sin media queries; `min-width: 768px` y `1024px` solo suman (UX-UI §3) |
| 2 | Paginación de todas las consultas de listado y de sus tablas | Paginación por offset con total (`page`, `page_size`; 20 por defecto, máximo 50) en catálogo, mis aportes, roadmap y panel de validación (TRD TD-002) |
| 3 | Menú sándwich en mobile | Header con botón hamburguesa y panel lateral por debajo de 1024px, con ARIA (UX-UI §4.5) |
| 4 | Screaming Architecture | Carpetas por dominio: `identidad`, `categorias`, `cursos`, `aportes`, `roadmap` (TRD §3.2) |
| 5 | Apariencia y experiencia inspiradas en Google | Tokens concretos: azul `#1a73e8`, sombras sutiles, radios amplios y estados definidos (UX-UI §2) |

> La consigna del docente habla de 4 prácticas, pero la SPEC oficial lista 5 en
> "Indicaciones técnicas". Se registran las 5.


## 8. Vacíos de la SPEC de clase y decisiones tomadas

| # | Vacío detectado en la SPEC | Opciones consideradas | Decisión | Dónde se desarrolla |
|---|----------------------------|-----------------------|----------|---------------------|
| 1 | ¿Quién valida los cursos aportados? | autovalidación comunitaria · validación docente · moderador | Un rol moderador aprueba o rechaza (con motivo) | PRD BR-005 |
| 2 | ¿Hay roles? | solo usuarios · usuario + moderador · roles configurables | Dos roles: usuario y moderador; el moderador se crea por seed, sin gestión desde la UI | PRD §8 · TRD TD-001 |
| 3 | ¿Qué es "incluir en mi catálogo / roadmap"? | lista simple · lista con orden y estado de avance | Un solo concepto: ítem de roadmap con orden y estado (pendiente, en curso, completado) | PRD BR-006, BR-007 · TRD TD-004 |
| 4 | ¿Cómo se busca en el catálogo? | solo texto · solo filtros · ambos | Texto libre (título y tema) y filtro por categoría, combinables | PRD US-007 |
| 5 | ¿Quién define las categorías? | lista cerrada por seed · alta libre por usuarios | Lista cerrada cargada por seed | BackendSchema §3.5 |
| 6 | ¿Qué estados tiene un curso aportado? | con borrador · sin borrador | Tres estados: en_revision, publicado, rechazado | BackendSchema §2 |
| 7 | ¿Qué pasa con un aporte rechazado? | editar y reenviar · definitivo | Queda rechazado con su motivo; para insistir se aporta uno nuevo | PRD §8 |
| 8 | ¿Qué es un duplicado? | mismo título · mismo enlace | Mismo enlace normalizado, en cualquier estado | PRD BR-004 |
| 9 | ¿Cómo llega el token de recuperación sin servidor de correo? | SMTP real · MailHog · registro en el log | En desarrollo se registra en el log del backend; token de un solo uso con expiración | PRD BR-008 · TRD TD-006 |
| 10 | ¿Cómo se aplica el rate limiting del login? | por IP · por email · ambos | Por combinación IP + email, con límite de intentos fallidos en una ventana de tiempo | PRD BR-009 · TRD TD-005 |
| 11 | ¿Cómo se mantiene la sesión? | JWT · sesión en servidor | JWT de acceso con expiración | TRD TD-001 |

## 9. Historia de la SPEC (autoregistro de cambios)

| Fecha | Cambio | Por qué |
|-------|--------|---------|
| 20/10/2026 | SPEC borrador escrita en el aula | — |
| 21/10/2026 | SPEC oficial recibida; precisa recuperación de contraseña, rate limiting y la versión de FastAPI (0.158.2) | corrección del docente |
| 23/10/2026 | Primer commit: SPEC oficial tal cual | regla de la consigna |
| 23/10/2026 | Refinamiento: identidad, alcance, reglas, stack y decisiones sobre vacíos (§1 a §8) | completar lo que la SPEC dejó abierto |