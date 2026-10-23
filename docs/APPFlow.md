# APPFlow — Mapa del sitio y flujos de usuario — AprovechaElBug

> **Qué es:** el esqueleto de navegación: sitemap, rutas, ficha por pantalla y flujos de
> punta a punta. Une el [PRD](PRD.md) (qué quiere el usuario) con el
> [BackendSchema](BackendSchema.md) (qué API lo sostiene). Los componentes visuales están
> en [UX-UI](UX-UI.md).

## 1. Sitemap

```mermaid
flowchart TD
    HOME(["Home<br>/"]) --> CAT["Catálogo<br>/catalogo"]
    HOME --> LOGIN["Login<br>/login"]
    HOME --> REG["Registro<br>/registro"]
    MENU(["Menú principal<br>header o drawer"]) --> CAT
    MENU --> APORT["Aportar curso<br>/aportar"]
    MENU --> MIS["Mis aportes<br>/mis-aportes"]
    MENU --> ROAD["Mi roadmap<br>/roadmap"]
    MENU -->|solo moderador| VAL["Validación<br>/validar"]
    CAT --> DET["Detalle de curso<br>/catalogo/:id"]
    DET --> CAT
    REG -->|cuenta creada| LOGIN
    LOGIN -->|sesión iniciada| CAT
    LOGIN --> OLV["Olvidé mi contraseña<br>/olvide-password"]
    OLV -.->|enlace con token| REST["Restablecer contraseña<br>/restablecer-password/:token"]
    REST -->|contraseña cambiada| LOGIN
    APORT -->|aporte enviado| MIS
```

## 2. Rutas

| Ruta | Pantalla | Requiere login | Notas |
|------|----------|----------------|-------|
| `/` | Home | no | presenta la propuesta y lleva al catálogo; no consume API |
| `/catalogo` | Catálogo comunitario (paginado) | no | estado en la URL: `?q=`, `?categoria=`, `?page=` |
| `/catalogo/:id` | Detalle de curso | no | solo cursos publicados |
| `/registro` | Registro | no | si ya hay sesión, redirige a `/catalogo` |
| `/login` | Login | no | acepta `?volver=<ruta>` para regresar tras entrar |
| `/olvide-password` | Solicitud de recuperación | no | |
| `/restablecer-password/:token` | Nueva contraseña | no | el token viaja en la ruta |
| `/aportar` | Formulario de aporte | sí | |
| `/mis-aportes` | Estado de mis aportes (paginado) | sí | |
| `/validar` | Panel de validación (paginado) | sí, rol moderador | otro rol ve la pantalla "No tenés permiso" |
| `/roadmap` | Mi roadmap (paginado) | sí | redirige a `/login?volver=/roadmap` si no hay sesión |
| `*` | Página no encontrada | no | cualquier ruta inexistente |

## 3. Fichas de pantalla

> Todas las pantallas consumen además `GET /api/v1/auth/me` al cargar la app, para conocer
> la sesión y el rol del header.

### Pantalla: Home (`/`)

- **Objetivo del usuario:** entender qué es AprovechaElBug y entrar al catálogo.
- **Componentes (UX-UI):** header, título, dos botones (primario "Explorar catálogo", secundario "Aportar un curso") y tres pasos de "cómo funciona".
- **Estados:** `ok` (pantalla estática).
- **APIs que consume:** ninguna.
- **Navegación:** hacia `/catalogo`, `/aportar` (con login) y `/registro`.

### Pantalla: Catálogo comunitario (`/catalogo`)

- **Objetivo del usuario:** descubrir cursos publicados, buscarlos y agregarlos a su roadmap. Historias: US-001, US-007, US-006.
- **Componentes (UX-UI):** header, campo de búsqueda, select de categoría, grid de cards (§4.4), paginador, toast, skeleton, estado vacío.
- **Estados:** `loading` (skeleton) · `ok` · `vacío` (sin resultados, con "Limpiar filtros") · `error` (con "Reintentar").
- **APIs que consume:** `GET /api/v1/cursos?page=&page_size=&categoria=&q=` · `GET /api/v1/categorias` (opciones del filtro) · `POST /api/v1/roadmap/items` (botón "Agregar a mi roadmap").
- **Navegación:** al detalle del curso; el botón "Agregar" sin sesión lleva a `/login?volver=/catalogo`.

### Pantalla: Detalle de curso (`/catalogo/:id`)

- **Objetivo del usuario:** ver todos los datos de un curso y decidir si lo agrega o lo toma. Historias: US-001, US-006.
- **Componentes (UX-UI):** header, datos del curso, badges, botón "Ir al curso" (enlace externo con `rel="noopener noreferrer"`), botón "Agregar a mi roadmap".
- **Estados:** `loading` · `ok` · `no encontrado` (curso inexistente o no publicado) · `error`.
- **APIs que consume:** `GET /api/v1/cursos/{id}` · `POST /api/v1/roadmap/items`.
- **Navegación:** vuelve al catálogo conservando los filtros.

### Pantalla: Registro (`/registro`)

- **Objetivo del usuario:** crear una cuenta. Historia: US-002.
- **Componentes (UX-UI):** campos nombre, email, contraseña y repetir contraseña (esta última se compara solo en el frontend), botón primario, enlace a login.
- **Estados:** `default` · `error de campo` · `enviando` · éxito (redirige a `/login` con toast).
- **APIs que consume:** `POST /api/v1/auth/registro`.
- **Navegación:** hacia `/login`.

### Pantalla: Login (`/login`)

- **Objetivo del usuario:** iniciar sesión. Historia: US-003.
- **Componentes (UX-UI):** campos email y contraseña, botón primario, enlaces a registro y a "Olvidé mi contraseña".
- **Estados:** `default` · `error` (mensaje genérico) · `bloqueado` (mensaje con el tiempo de espera, tomado de `retry_after_seconds`) · `enviando`.
- **APIs que consume:** `POST /api/v1/auth/login`.
- **Navegación:** a la ruta de `?volver=` o, si no hay, a `/catalogo`.

### Pantalla: Olvidé mi contraseña (`/olvide-password`)

- **Objetivo del usuario:** pedir el enlace de recuperación. Historia: US-008.
- **Componentes (UX-UI):** campo email, botón primario, mensaje de confirmación.
- **Estados:** `default` · `enviando` · `confirmación` (mismo mensaje exista o no la cuenta, BR-008).
- **APIs que consume:** `POST /api/v1/auth/recuperar`.
- **Navegación:** vuelve a `/login`.

### Pantalla: Restablecer contraseña (`/restablecer-password/:token`)

- **Objetivo del usuario:** definir una nueva contraseña con el enlace recibido. Historia: US-008.
- **Componentes (UX-UI):** campos nueva contraseña y repetirla, botón primario.
- **Estados:** `default` · `error de campo` · `token inválido o vencido` (mensaje y enlace a `/olvide-password`) · éxito (redirige a `/login` con toast).
- **APIs que consume:** `POST /api/v1/auth/restablecer`.
- **Navegación:** hacia `/login`.

### Pantalla: Aportar curso (`/aportar`)

- **Objetivo del usuario:** cargar un curso gratuito al catálogo. Historia: US-004.
- **Componentes (UX-UI):** formulario de aporte (§4.3), select de categoría, casillas, grupo de radios "¿Tomaste este curso?", toast.
- **Estados:** `loading` (carga de categorías) · `default` · `error de campo` · `enviando` · `error de red` (toast y los datos se conservan).
- **APIs que consume:** `GET /api/v1/categorias` · `POST /api/v1/aportes`.
- **Navegación:** al enviar con éxito, a `/mis-aportes` con toast.

### Pantalla: Mis aportes (`/mis-aportes`)

- **Objetivo del usuario:** saber si sus aportes fueron aprobados o rechazados y por qué. Historia: US-009.
- **Componentes (UX-UI):** tabla o cards (§4.6), badge de estado (§4.5), paginador.
- **Estados:** `loading` · `ok` · `vacío` (con botón "Aportar el primero") · `error`.
- **APIs que consume:** `GET /api/v1/aportes/mios?page=&page_size=`.
- **Navegación:** hacia `/aportar`; los aportes publicados enlazan a su detalle.

### Pantalla: Validación (`/validar`)

- **Objetivo del usuario (moderador):** revisar aportes pendientes y aprobarlos o rechazarlos. Historia: US-005.
- **Componentes (UX-UI):** tabla o cards con todos los datos del aporte, botones "Aprobar" y "Rechazar", modal de rechazo con motivo obligatorio (§4.9), paginador, toast.
- **Estados:** `loading` · `ok` · `vacío` ("No hay aportes pendientes") · `error` · `sin permiso` (usuario sin rol moderador).
- **APIs que consume:** `GET /api/v1/aportes/pendientes?page=&page_size=` · `POST /api/v1/aportes/{id}/validar`.
- **Navegación:** solo desde el menú, visible solo para el moderador.

### Pantalla: Mi roadmap (`/roadmap`)

- **Objetivo del usuario:** ver y mantener su plan de aprendizaje. Historias: US-006, US-010.
- **Componentes (UX-UI):** tabla o cards, select de estado de avance, botones Subir y Bajar, botón Quitar con modal de confirmación (§4.12), paginador.
- **Estados:** `loading` · `ok` · `vacío` (con acceso al catálogo) · `error`.
- **APIs que consume:** `GET /api/v1/roadmap?page=&page_size=` · `PATCH /api/v1/roadmap/items/{id}` · `POST /api/v1/roadmap/items/{id}/mover` · `DELETE /api/v1/roadmap/items/{id}`.
- **Navegación:** hacia el catálogo y hacia el detalle de cada curso.


## 4. Flujos de usuario

### Flujo 1 — Aportar un curso al catálogo

1. Un usuario con sesión elige "Aportar curso" en el menú y llega a `/aportar`.
2. La pantalla carga las categorías (`GET /categorias`) y muestra el formulario: enlace, categoría, tema, título, versión, año de edición, docentes, casillas (cuestionarios, examen, certificado), organización que lo avala (opcional) y "¿Tomaste este curso?".
3. Validación en línea: obligatorios, enlace con formato `http` o `https`, año numérico, declaración elegida.
4. Al enviar: `POST /aportes`. Respuesta 201 con estado `en_revision`.
5. Toast "Tu aporte quedó en revisión" y redirección a `/mis-aportes`.
6. **Ramas de error:**
   - 422: se marcan los campos inválidos y no se pierde nada de lo escrito.
   - 409: el campo enlace muestra "Este curso ya fue aportado".
   - 401 (sesión vencida): toast, redirección a `/login?volver=/aportar`.
   - Error de red: toast de error con reintento; los datos se conservan.

### Flujo 2 — Descubrir un curso y agregarlo al roadmap

1. Cualquier persona entra a `/catalogo` y ve la primera página de cursos publicados.
2. Escribe un texto y elige una categoría; la URL se actualiza y la lista se recarga (`GET /cursos?q=&categoria=`).
3. Abre un curso (`/catalogo/:id`) y lee sus datos; "Ir al curso" abre el enlace externo en otra pestaña.
4. Presiona "Agregar a mi roadmap".
5. **Sin sesión:** va a `/login?volver=/catalogo/:id` y, al entrar, vuelve al curso para repetir la acción.
6. **Con sesión:** `POST /roadmap/items`. Respuesta 201, toast "Agregado a tu roadmap" y la card pasa a "En tu roadmap".
7. **Ramas alternativas:** 409 (ya estaba) muestra el estado "En tu roadmap"; 404 (el curso ya no está publicado) muestra un toast de error y recarga la lista.
8. Desde el menú, "Mi roadmap" muestra el curso agregado.

### Flujo 3 — Validación de un aporte (moderador)

1. El moderador inicia sesión y ve la opción "Validar" en el menú.
2. En `/validar` aparece la lista paginada de aportes en revisión, los más antiguos primero (`GET /aportes/pendientes`).
3. Revisa los datos del aporte y abre el enlace del curso.
4. **Aprobar:** `POST /aportes/{id}/validar` con `aprobado: true`. El aporte sale de la lista y pasa a publicado.
5. **Rechazar:** abre el modal, escribe el motivo (obligatorio) y confirma; mismo endpoint con `aprobado: false` y `motivo`.
6. Toast de resultado y recarga de la lista; si la página quedó vacía, se retrocede a la anterior.
7. **Ramas de error:** 409 (otra decisión ya fue tomada) muestra un toast y recarga; 422 (motivo vacío) bloquea el botón y marca el campo; 403 (usuario sin rol) muestra "No tenés permiso".

### Flujo 4 — Registro e inicio de sesión

1. La persona abre `/registro`, completa nombre, email y contraseña (de 8 a 72 caracteres) y envía (`POST /auth/registro`).
2. Éxito: redirección a `/login` con toast "Cuenta creada, ya podés iniciar sesión".
3. En `/login` envía sus credenciales (`POST /auth/login`); el backend responde con la sesión en una cookie.
4. Redirección a la ruta de `?volver=` o a `/catalogo`; el header muestra su nombre.
5. **Ramas de error:**
   - Registro 409: "Ese email ya está registrado".
   - Login 401: mensaje genérico, sin indicar si falló el email o la contraseña.
   - Login 429 (más de 5 fallos en 15 minutos): el formulario se bloquea y muestra cuánto esperar.
6. Para salir, "Cerrar sesión" en el menú (`POST /auth/logout`) y vuelta a `/catalogo`.

### Flujo 5 — Recuperar la contraseña

1. En `/login`, el enlace "Olvidé mi contraseña" lleva a `/olvide-password`.
2. La persona ingresa su email y envía (`POST /auth/recuperar`); siempre ve el mismo mensaje de confirmación.
3. En desarrollo el enlace de restablecimiento se escribe en el log del backend (TD-006).
4. Abre `/restablecer-password/:token`, define la nueva contraseña y envía (`POST /auth/restablecer`).
5. Éxito: redirección a `/login` con toast.
6. **Rama de error:** token vencido o ya usado (422): mensaje claro y enlace para pedir otro.

## 5. Estados globales de la app

| Situación | Comportamiento |
|-----------|----------------|
| Sin sesión y ruta protegida | redirección a `/login?volver=<ruta original>` |
| Sesión vencida (cualquier llamada con respuesta 401 estando logueado) | toast "Tu sesión venció", se limpia el estado de sesión y se redirige a `/login?volver=<ruta actual>` |
| Usuario sin rol en `/validar` | pantalla "No tenés permiso" con enlace al catálogo |
| Ruta inexistente | pantalla "Página no encontrada" con enlace al catálogo |
| Error de red en un listado | estado de error del listado con botón "Reintentar" |
| Error de red en una acción | toast de error; los datos del formulario se conservan |
| Error 500 | toast genérico "Algo salió mal"; sin detalles técnicos |

## 6. Matriz de coherencia (historia → pantalla → endpoint)

| Historia | Pantallas | Endpoints |
|----------|-----------|-----------|
| US-001 | Catálogo, Detalle | `GET /cursos`, `GET /cursos/{id}` |
| US-002 | Registro | `POST /auth/registro` |
| US-003 | Login, header | `POST /auth/login`, `POST /auth/logout`, `GET /auth/me` |
| US-004 | Aportar | `GET /categorias`, `POST /aportes` |
| US-005 | Validación | `GET /aportes/pendientes`, `POST /aportes/{id}/validar` |
| US-006 | Catálogo, Detalle, Mi roadmap | `POST /roadmap/items`, `GET /roadmap` |
| US-007 | Catálogo | `GET /cursos` (`q`, `categoria`), `GET /categorias` |
| US-008 | Olvidé, Restablecer | `POST /auth/recuperar`, `POST /auth/restablecer` |
| US-009 | Mis aportes | `GET /aportes/mios` |
| US-010 | Mi roadmap | `PATCH /roadmap/items/{id}`, `POST /roadmap/items/{id}/mover`, `DELETE /roadmap/items/{id}` |

> Todos los endpoints llevan el prefijo `/api/v1`. Los 18 endpoints del BackendSchema
> aparecen en esta matriz: ninguno queda sin pantalla y ninguna pantalla consume una API inexistente.

---

**Referencias:**
- NN/g — Information Architecture vs. Sitemaps: https://www.nngroup.com/articles/information-architecture-sitemaps/
- NN/g — User Journeys vs. User Flows: https://www.nngroup.com/articles/user-journeys-vs-user-flows/