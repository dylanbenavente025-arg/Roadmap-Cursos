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