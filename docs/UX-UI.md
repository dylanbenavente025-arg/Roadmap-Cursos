# UX-UI — Guía visual de estilos — AprovechaElBug

> **Qué es:** la gramática visual de la interfaz: tokens, componentes, estados y
> accesibilidad. Se define **antes** de escribir CSS. La navegación entre pantallas vive en
> el [APPFlow](APPFlow.md).
> **Inspiración fijada por la SPEC:** apariencia y experiencia similares a Google (estética
> Material: limpieza, espacio en blanco, azul primario, sombras sutiles, radios amplios).
> Los contrastes de esta guía fueron calculados con la fórmula WCAG 2.x el 23/10/2026.

## 1. Principios

1. **Mobile primero:** el layout base se diseña para 360 px y se mejora hacia arriba; nunca se repara con media queries.
2. **Una acción principal por pantalla:** el azul primario marca lo que se puede hacer; el resto es neutro.
3. **Los estados son parte del diseño:** carga, vacío y error se definen antes que el caso feliz.
4. **Nada depende solo del color:** estado, error y selección llevan además icono o texto.
5. **Espacio en blanco como herramienta:** el aire agrupa mejor que las cajas.

## 2. Design tokens

### 2.1 Paleta de colores

| Token | Valor | Uso | Contraste (calculado) |
|-------|-------|-----|-----------------------|
| `--color-primary` | `#1a73e8` | botones rellenos, foco, iconos | vs blanco 4,51:1 ✓ AA |
| `--color-primary-dark` | `#1557b0` | **texto y links azules**, hover del primario | vs blanco 6,95:1 · vs fondo 6,59:1 ✓ |
| `--color-primary-container` | `#e8f0fe` | chip de categoría, ítem activo del menú, página actual | texto `#174ea6` encima: 6,85:1 ✓ |
| `--color-on-primary` | `#ffffff` | texto sobre primario | vs `#1a73e8` 4,51:1 ✓ · vs `#1557b0` 6,95:1 ✓ |
| `--color-surface` | `#ffffff` | cards, header, modal, drawer | — |
| `--color-background` | `#f8f9fa` | fondo de página | — |
| `--color-text` | `#202124` | texto principal | vs surface 16,10:1 · vs fondo 15,27:1 ✓ |
| `--color-text-muted` | `#5f6368` | metadatos, ayudas, placeholders | vs surface 6,05:1 · vs fondo 5,74:1 ✓ |
| `--color-border` | `#dadce0` | **solo** divisores y bordes de cards | 1,37:1: decorativo, nunca borde de control |
| `--color-border-strong` | `#80868b` | borde de inputs, selects y checkboxes | vs surface 3,68:1 · vs fondo 3,49:1 ✓ (≥ 3:1) |
| `--color-hover-grey` | `#f1f3f4` | hover de filas y botones secundarios, input deshabilitado | muted encima: 5,44:1 ✓ |
| `--color-success` | `#188038` | icono y texto de éxito | vs surface 5,02:1 ✓ |
| `--color-success-container` | `#e6f4ea` | fondo de badge "publicado" | texto `#137333` encima: 5,24:1 ✓ |
| `--color-warning` | `#f9ab00` | **solo** icono y borde de aviso, nunca texto | vs blanco 1,93:1 ✗ como texto |
| `--color-warning-container` | `#fef7e0` | fondo de badge "en revisión" | texto `#7a4100` encima: 7,58:1 ✓ |
| `--color-error` | `#d93025` | texto de error, borde de campo inválido, botón peligro | vs surface 4,77:1 · vs fondo 4,53:1 ✓ |
| `--color-error-container` | `#fce8e6` | fondo de badge "rechazado" | texto `#b3261e` encima: 5,55:1 ✓ (con `#d93025` sería 4,05:1 ✗) |
| `--color-snackbar` | `#323232` | fondo de toast | texto blanco 12,82:1 · acción `#8ab4f8` 6,08:1 ✓ |

> Regla de uso: sobre fondos de color (`*-container`) se usa el texto oscuro indicado en la
> tabla, nunca el color base. El anillo de foco usa `--color-primary`: 4,27:1 sobre el fondo,
> suficiente para elementos no textuales (≥ 3:1).

### 2.2 Tipografía

| Token | Familia | Tamaño / line-height | Uso |
|-------|---------|----------------------|-----|
| `--font-family-base` | Roboto, `system-ui`, sans-serif | — | todo el texto |
| `--text-sm` | | 14px / 20px | metadatos, badges, tablas, botones |
| `--text-base` | | 16px / 24px | cuerpo y campos de formulario |
| `--text-lg` | | 18px / 24px | títulos de card |
| `--text-xl` | | 22px / 28px | títulos de pantalla |
| `--text-2xl` | | 28px / 36px | título de Home (solo desde 768 px) |

Pesos: 400 (cuerpo) y 500 (títulos y botones). Roboto se sirve desde el propio proyecto
(paquete `@fontsource/roboto`, pesos 400 y 500) con `font-display: swap`, sin depender de CDN.
El tamaño mínimo de texto es 14 px.

### 2.3 Espaciado, radios, sombras y capas

| Token | Valor | Uso |
|-------|-------|-----|
| `--space-1` … `--space-8` | 4, 8, 12, 16, 24, 32, 40, 48 px | ritmo de 4 px en todo |
| `--radius-input` | 8px | inputs, selects, toasts |
| `--radius-card` | 12px | cards de curso |
| `--radius-button` | 20px | botones (forma de píldora) |
| `--radius-modal` | 28px | modales |
| `--shadow-1` | `0 1px 2px rgba(60, 64, 67, .1), 0 1px 3px 1px rgba(60, 64, 67, .15)` | reposo de cards, header al hacer scroll |
| `--shadow-2` | `0 1px 2px rgba(60, 64, 67, .1), 0 2px 6px 2px rgba(60, 64, 67, .15)` | hover de card, drawer, modal |
| `--z-header` / `--z-drawer` / `--z-modal` / `--z-toast` | 100 / 200 / 250 / 300 | orden de capas |

### 2.4 Bloque de variables listo para copiar

```css
:root {
  --color-primary: #1a73e8;
  --color-primary-dark: #1557b0;
  --color-primary-container: #e8f0fe;
  --color-on-primary: #ffffff;
  --color-surface: #ffffff;
  --color-background: #f8f9fa;
  --color-text: #202124;
  --color-text-muted: #5f6368;
  --color-border: #dadce0;
  --color-border-strong: #80868b;
  --color-hover-grey: #f1f3f4;
  --color-success: #188038;
  --color-success-container: #e6f4ea;
  --color-warning: #f9ab00;
  --color-warning-container: #fef7e0;
  --color-error: #d93025;
  --color-error-container: #fce8e6;
  --color-snackbar: #323232;

  --font-family-base: "Roboto", system-ui, sans-serif;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.375rem;
  --text-2xl: 1.75rem;

  --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-7: 40px; --space-8: 48px;

  --radius-input: 8px;
  --radius-card: 12px;
  --radius-button: 20px;
  --radius-modal: 28px;

  --shadow-1: 0 1px 2px rgba(60, 64, 67, .1), 0 1px 3px 1px rgba(60, 64, 67, .15);
  --shadow-2: 0 1px 2px rgba(60, 64, 67, .1), 0 2px 6px 2px rgba(60, 64, 67, .15);

  --z-header: 100;
  --z-drawer: 200;
  --z-modal: 250;
  --z-toast: 300;
}
```

## 3. Estrategia mobile-first con mejora progresiva

> Obligatorio según la SPEC. **Prohibido** usar media queries para "arreglar" el layout base:
> solo para agregar o mejorar a medida que la pantalla crece.

| Capa | Dónde aplica | Qué define |
|------|--------------|------------|
| **Base (sin media queries)** | todos los viewports, diseñado para 360 px | una columna; header con hamburguesa; catálogo como cards apiladas; tablas como cards; botones de ancho completo en formularios y modales; targets táctiles de al menos 44 px |
| `@media (min-width: 768px)` | tablet | catálogo en 2 columnas; tablas como tabla real; formulario de aporte en 2 columnas; paginador con números; botones de ancho automático |
| `@media (min-width: 1024px)` | desktop | catálogo en 3 columnas; navegación horizontal en el header y hamburguesa oculta; contenedor con ancho máximo |

Patrón obligatorio de escritura del CSS:

```css
.catalogo-grid { display: grid; gap: var(--space-4); }                 /* base: 1 columna */
@media (min-width: 768px)  { .catalogo-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .catalogo-grid { grid-template-columns: repeat(3, 1fr); } }
```

## 4. Componentes (anatomía y estados)

### 4.1 Botón

- **Primario:** fondo `--color-primary`, texto `--color-on-primary`, `--radius-button`, alto mínimo 44 px, padding horizontal 24 px, Roboto 500 14 px. Hover: fondo `--color-primary-dark` y `--shadow-1`.
- **Secundario:** sin relleno, borde 1 px `--color-border-strong`, texto `--color-primary-dark`. Hover: fondo `--color-hover-grey`.
- **Peligro:** fondo `--color-error`, texto `--color-on-primary`. Siempre con confirmación previa (modal).
- Estados de todos: `default`, `hover`, `focus-visible` (anillo de 2 px `--color-primary` con separación de 2 px), `active`, `disabled` (opacidad .38, sin puntero, atributo `disabled`), `loading` (spinner, `aria-busy="true"`, deshabilitado).
- Un botón que solo tiene icono lleva `aria-label`.

### 4.2 Campo de formulario (input, select, textarea, casillas)

- Anatomía: `label` **siempre visible** encima, campo de 48 px de alto con borde 1 px `--color-border-strong` y `--radius-input`, texto de ayuda opcional debajo.
- Estados: `default` · `hover` (borde `--color-text`) · `focus` (borde 2 px `--color-primary`) · `filled` · `error` (borde 2 px `--color-error`, icono y mensaje en `--color-error`, `aria-invalid="true"` y `aria-describedby` apuntando al mensaje) · `disabled` (fondo `--color-hover-grey`).
- Casillas y radios: control de 24 px con área táctil de 44 px; el texto de la opción forma parte del `label`.
- Los campos obligatorios se marcan con texto ("obligatorio"), no solo con asterisco de color.

### 4.3 Formulario de aporte

- Secciones en una columna (base) y dos columnas desde 768 px:
  1. **Enlace del curso** (URL).
  2. **Datos:** categoría (select con la lista cerrada), tema, título, versión, año de edición, docentes o disertantes.
  3. **Características:** casillas "Tiene cuestionarios", "Requiere examen", "Extiende certificado", y campo opcional "Organización que lo avala".
  4. **Declaración:** grupo de radios "¿Tomaste este curso?" (Sí / No), obligatorio y sin valor preseleccionado (BR-002).
- Validación en línea al salir de cada campo y al enviar; el foco pasa al primer campo con error; **nunca se pierde lo escrito**.
- Envío: botón primario "Aportar curso" en estado `loading`; éxito con toast y redirección a "Mis aportes".

### 4.4 Card de curso

- Superficie `--color-surface`, `--radius-card`, `--shadow-1`, padding `--space-4`.
- Contenido, de arriba abajo: título (`--text-lg`, máximo 2 líneas), chip de categoría (`--color-primary-container`, texto `#174ea6`), docentes y "versión · año" (`--text-sm`, `--color-text-muted`), fila de badges con icono y texto (Certificado, Examen, Cuestionarios, Avalado), dominio del enlace y la marca "Quien lo aportó lo tomó" según BR-002, y la acción.
- Acción: "Agregar a mi roadmap" (secundario) o, si ya está, el texto "En tu roadmap" con icono de check.
- Estados: `default` · `hover` (`--shadow-2`) · `focus-visible` (anillo en el enlace del título) · `en mi roadmap` (borde 2 px `--color-primary` + icono + texto, nunca solo color) · `loading` (skeleton).

### 4.5 Badge de estado del aporte

| Estado | Fondo | Texto | Icono |
|--------|-------|-------|-------|
| en revisión | `--color-warning-container` | `#7a4100` | reloj |
| publicado | `--color-success-container` | `#137333` | check |
| rechazado | `--color-error-container` | `#b3261e` | cancelar |

Siempre con icono **y** texto.

### 4.6 Lista y tabla paginada

Aplica a: catálogo (grid de cards), mis aportes, panel de validación y mi roadmap.

- Desde 768 px: tabla real, encabezados con `scope="col"`, filas con divisor `--color-border` y hover `--color-hover-grey`.
- En la base (< 768 px): las mismas filas como cards apiladas, con la misma información y sin scroll horizontal.
- Debajo de cada listado va el paginador (§4.7).
- Estados: `loading` (skeleton), `ok`, `vacío` (empty state con acción) y `error` (mensaje y botón "Reintentar").

### 4.7 Paginador

- Elemento `nav` con `aria-label="Paginación"`.
- Base: botones "Anterior" y "Siguiente" y el texto "Página X de Y".
- Desde 768 px: además números de página con puntos suspensivos; la página actual con `aria-current="page"` y fondo `--color-primary-container` con texto `#174ea6`.
- "Anterior" se deshabilita en la primera página y "Siguiente" en la última. El tamaño de página es fijo (20), sin selector.

### 4.8 Menú sándwich (drawer)

- Se muestra por debajo de 1024 px: botón de 48 × 48 px en el extremo izquierdo del header, con `aria-label="Abrir menú"`, `aria-expanded` y `aria-controls`.
- Panel: ancho 280 px (máximo 85 % del ancho de pantalla), fondo `--color-surface`, `--shadow-2`, overlay `rgba(32, 33, 36, .6)` y bloqueo del scroll del fondo.
- Contenido: logo, enlaces según sesión y rol (Catálogo, Aportar, Mis aportes, Mi roadmap y, solo para el moderador, Validar), separador y zona de sesión (Ingresar y Registrarme, o el nombre y Cerrar sesión).
- Ítems de 48 px de alto; el activo con fondo `--color-primary-container`, texto `#174ea6` y `aria-current="page"`.
- Estados: cerrado y abierto. Cierre: toque en un enlace, botón X, tecla `ESC` o clic en el overlay.
- ARIA y foco: `role="dialog"`, `aria-modal="true"`, foco atrapado dentro del panel y devuelto al botón al cerrar.

### 4.9 Modal

- Usos: confirmar quitar un curso del roadmap; rechazar un aporte (con campo de motivo obligatorio).
- Superficie `--color-surface`, `--radius-modal`, `--shadow-2`, overlay igual al del drawer.
- `role="dialog"`, `aria-modal="true"`, título con `aria-labelledby`, foco atrapado, cierre con `ESC` y botón X; el clic en el overlay no cierra mientras se envía.
- Acciones: Cancelar (secundario) y la acción principal (primario o peligro). En la base van apiladas a ancho completo; desde 768 px, alineadas a la derecha.

### 4.10 Toast

- Fondo `--color-snackbar`, texto blanco, `--radius-input`, ancho mínimo 288 px.
- Posición: inferior centrado en la base; inferior izquierda desde 768 px.
- Tipos: éxito (icono de check), error (icono de alerta), info. Éxito e info duran 5 s; el error permanece 8 s y tiene botón de cierre. El tiempo se pausa con hover o foco.
- Accesibilidad: `role="status"` para éxito e info, `role="alert"` para error.

### 4.11 Skeleton, estado vacío y estado de error

- **Skeleton:** bloques `--color-hover-grey` con brillo animado, con la forma de la card o fila que reemplazan.
- **Vacío:** icono grande en `--color-text-muted`, título (`--text-lg`), una línea de explicación y una acción. Ejemplo: "Todavía no hay cursos en esta categoría. Aportá el primero".
- **Error:** mensaje claro, botón "Reintentar" y, si corresponde, enlace de salida.

### 4.12 Controles del roadmap

- **Estado de avance:** `select` nativo con Pendiente, En curso y Completado.
- **Orden:** botones "Subir" y "Bajar" con `aria-label` que incluye el título del curso. No hay arrastrar y soltar en el MVP, para que sea accesible por teclado.
- **Quitar:** botón de texto con icono que abre el modal de confirmación (§4.9).

## 5. Layout y navegación

- **Header:** sticky (`--z-header`), fondo `--color-surface`, alto 56 px en la base y 64 px desde 768 px. Base: hamburguesa, logo y zona de sesión compacta. Desde 1024 px: logo, navegación horizontal y acciones de sesión. Aparece `--shadow-1` al hacer scroll.
- **Contenedor:** ancho máximo 1140 px centrado; padding lateral `--space-4` en la base y `--space-5` desde 768 px.
- **Pantallas** (el detalle de navegación y estados vive en el [APPFlow](APPFlow.md)): Home, Catálogo, Detalle de curso, Registro, Login, Olvidé mi contraseña, Restablecer contraseña, Aportar curso, Mis aportes, Validación (moderador) y Mi roadmap.

## 6. Accesibilidad mínima (no negociable)

- [x] Texto con contraste AA (≥ 4,5:1): `#202124` 16,10:1, `#5f6368` 6,05:1, links `#1557b0` 6,95:1, error `#d93025` 4,77:1
- [x] Botón primario con texto blanco sobre `#1a73e8`: 4,51:1
- [x] Bordes de controles ≥ 3:1: `#80868b` 3,68:1 sobre blanco (el `#dadce0` es solo decorativo)
- [x] El color nunca es el único indicador: estado, error y selección llevan icono o texto
- [ ] `:focus-visible` visible en todo elemento interactivo (anillo de 2 px)
- [ ] Menú sándwich con `aria-expanded`, `aria-controls`, foco atrapado y devuelto al cerrar
- [ ] Modales con `role="dialog"`, `aria-modal`, foco atrapado y cierre con `ESC`
- [ ] Errores de formulario asociados al campo con `aria-describedby` y `aria-invalid`
- [ ] `prefers-reduced-motion: reduce` desactiva el brillo del skeleton y las transiciones
- [ ] Iconos decorativos con `aria-hidden="true"`; iconos de acción con `aria-label`
- [ ] Todo se puede operar con teclado, incluido el reordenamiento del roadmap

> Los ítems sin tildar se verifican durante la construcción (Instancia B).

## 7. Iconografía y assets

- **Set:** Material Symbols (el set de Google), servido desde el propio proyecto con el paquete npm `material-symbols`, sin CDN. Se fija la versión en el lockfile.
- **Por qué:** coincide con la inspiración fijada por la SPEC y evita depender de servicios externos.
- **Tamaños y color:** 20 px dentro de botones, 24 px en listas y menú; el icono hereda el color del texto.
- **Imágenes:** sin fotos decorativas. Los estados vacíos usan iconos grandes en `--color-text-muted`.
- **Fuera de alcance de esta guía:** modo oscuro.

---

**Referencias:**
- NN/g — Front-End Style-Guides: https://www.nngroup.com/articles/front-end-style-guides/
- NN/g — Design Systems 101: https://www.nngroup.com/articles/design-systems-101/
- WebAIM — Contrast Checker: https://webaim.org/resources/contrastchecker/