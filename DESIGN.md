---
name: Dami Soporte
description: Mesa de ayuda para clientes externos; riel pizarra neutro, área de trabajo blanca fría y un solo acento verde azulado.
colors:
  rail: "oklch(0.28 0.015 235)"
  rail-hover: "oklch(0.33 0.016 235)"
  rail-active: "oklch(0.37 0.018 235)"
  rail-ink: "oklch(0.97 0.004 235)"
  rail-muted: "oklch(0.80 0.012 235)"
  rail-avatar: "oklch(0.42 0.018 235)"
  rail-glint: "oklch(0.82 0.10 180)"
  brand-mark: "oklch(0.70 0.11 180)"
  accent: "oklch(0.50 0.10 188)"
  accent-hover: "oklch(0.44 0.10 188)"
  accent-soft: "oklch(0.95 0.03 188)"
  accent-ink: "oklch(0.38 0.08 190)"
  focus: "oklch(0.62 0.13 188)"
  ground: "oklch(0.972 0.006 200)"
  surface: "oklch(1 0 0)"
  surface-2: "oklch(0.985 0.004 200)"
  ink: "oklch(0.25 0.02 225)"
  ink-2: "oklch(0.46 0.02 225)"
  ink-3: "oklch(0.56 0.015 225)"
  line: "oklch(0.91 0.008 210)"
  line-strong: "oklch(0.84 0.012 210)"
  status-blue: "oklch(0.50 0.14 255)"
  status-blue-bg: "oklch(0.955 0.025 255)"
  status-amber: "oklch(0.50 0.11 65)"
  status-amber-bg: "oklch(0.96 0.05 85)"
  status-green: "oklch(0.47 0.11 150)"
  status-green-bg: "oklch(0.955 0.04 150)"
  status-gray: "oklch(0.48 0.01 225)"
  status-gray-bg: "oklch(0.95 0.005 225)"
  danger-red: "oklch(0.52 0.17 25)"
  danger-red-bg: "oklch(0.96 0.025 25)"
typography:
  headline:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.625rem"
    fontWeight: 680
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  title:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.375rem"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "-0.015em"
  subtitle:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 650
    lineHeight: 1.25
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 600
    lineHeight: 1.5
  caption:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.5
  mono:
    fontFamily: "ui-monospace, Cascadia Mono, SF Mono, Consolas, monospace"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: "6px"
  md: "8px"
  lg: "12px"
  pill: "999px"
spacing:
  xs: "6px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "20px"
  2xl: "24px"
  3xl: "32px"
  page: "40px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "0 16px"
    height: "40px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0 16px"
    height: "40px"
  button-secondary-hover:
    backgroundColor: "{colors.surface-2}"
  button-ghost:
    textColor: "{colors.ink-2}"
    rounded: "{rounded.md}"
    padding: "0 16px"
    height: "40px"
  button-sm:
    typography: "{typography.label}"
    padding: "0 12px"
    height: "34px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "9px 12px"
    height: "40px"
  panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.lg}"
    padding: "24px"
  rail-nav-item:
    textColor: "{colors.rail-muted}"
    rounded: "{rounded.md}"
    padding: "9px 10px"
  rail-nav-item-active:
    backgroundColor: "{colors.rail-active}"
    textColor: "{colors.rail-ink}"
  pill-abierto:
    backgroundColor: "{colors.status-blue-bg}"
    textColor: "{colors.status-blue}"
    typography: "{typography.caption}"
    rounded: "{rounded.pill}"
    padding: "0 9px"
    height: "24px"
  pill-revision:
    backgroundColor: "{colors.status-amber-bg}"
    textColor: "{colors.status-amber}"
    rounded: "{rounded.pill}"
  pill-respondido:
    backgroundColor: "{colors.status-green-bg}"
    textColor: "{colors.status-green}"
    rounded: "{rounded.pill}"
  pill-cerrado:
    backgroundColor: "{colors.status-gray-bg}"
    textColor: "{colors.status-gray}"
    rounded: "{rounded.pill}"
  mailbox:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.mono}"
    rounded: "{rounded.md}"
    padding: "8px 8px 8px 12px"
  mailbox-lg:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "12px 12px 12px 16px"
---

# Design System: Dami Soporte

## Overview

**Creative North Star: "El mostrador en orden"**

Dami Soporte es una mesa de ayuda estándar ejecutada con precisión: un riel lateral gris pizarra neutro sostiene la marca y la navegación, y a su derecha un área de trabajo blanca y fría donde vive el trabajo real (tabla de tickets, formulario, detalle, confirmación). El sistema se mide contra Zendesk y Freshdesk: nada decorativo, todo legible, cada pantalla con un título, una acción primaria y un contenido.

La densidad es media. Las superficies son planas con borde fino y una sombra apenas perceptible; el riel pizarra da la estructura oscura sin color de marca; el verde azulado vive solo en el acento (acciones primarias y selección) y en el cuadro de la marca; el resto del color son cuatro estados semánticos. El dato estrella del producto, el correo de seguimiento `@dami.lat`, se presenta siempre en monoespaciada dentro del bloque de buzón con su botón Copiar.

**Key Characteristics:**
- Riel lateral de 248px en gris pizarra neutro frío; en móvil se convierte en barra superior del mismo color.
- Fondo blanco frío, paneles blancos con borde de 1px y radio de 12px.
- El verde azulado aparece solo en el acento de acción, la selección y la marca; el resto del color es semántico.
- Pila tipográfica del sistema, pesos intermedios (550 a 680) y tracking negativo en títulos.
- Iconos Lucide en trazo de 2px, inline como `<symbol>` SVG.
- Monoespaciada solo para identificadores: folio y correo de seguimiento.

## Colors

Una paleta fría y contenida: pizarra neutra para la estructura, un único verde azulado para acción, selección y marca, y color saturado solo cuando significa algo.

### Primary
- **Verde Azulado Medio** (`accent`): fondo del botón primario, borde de foco de campos, cursor de texto, borde del buzón grande. Su versión `accent-hover` oscurece al pasar el puntero; `accent-soft` es el fondo de la opción seleccionada del control segmentado y del icono de estados vacíos; `accent-ink` es el color de enlaces y texto de acento sobre blanco.
- **Anillo de Foco** (`focus`): contorno de 2px en `:focus-visible` y halo de 3px al 22% en campos enfocados.

### Secondary
- **Riel Pizarra** (`rail`): gris pizarra neutro frío (croma 0.015) para el riel lateral, la barra móvil y la banda superior de 220px de las pantallas de acceso. `rail-hover` y `rail-active` son sus estados de navegación; `rail-ink` es el texto sobre el riel, `rail-muted` el texto inactivo y `rail-avatar` el círculo del usuario.
- **Destello Verde Azulado** (`rail-glint`): el único verde azulado sobre el riel; marca el icono del ítem activo (selección), el foco sobre el riel y el glifo de la marca en su variante oscura. `brand-mark` es el cuadro de la marca sobre el riel.

### Tertiary (estados semánticos)
- **Azul Abierto** (`status-blue` / `-bg`): estado Abierto y avisos informativos.
- **Ámbar En Revisión** (`status-amber` / `-bg`): estado En revisión.
- **Verde Respondido** (`status-green` / `-bg`): estado Respondido, avisos de éxito, círculo de confirmación, "Copiado".
- **Gris Cerrado** (`status-gray` / `-bg`): estado Cerrado.
- **Rojo Error** (`danger-red` / `-bg`): errores de campo, avisos de error, barras de prioridad Alta.

### Neutral
- **Suelo Frío** (`ground`): fondo de página detrás del área de trabajo.
- **Superficie** (`surface`) y **Superficie 2** (`surface-2`): paneles y tablas; `surface-2` para cabeceras de tabla, sufijos de campo y el buzón compacto.
- **Tinta** (`ink`, `ink-2`, `ink-3`): texto principal, secundario (subtítulos, etiquetas de metadatos, cabeceras de tabla) y terciario (placeholders, contadores).
- **Líneas** (`line`, `line-strong`): divisores y bordes de panel; `line-strong` para bordes de campos y botón secundario.

### Named Rules
**The One Action Color Rule.** El acento verde azulado medio pertenece a la acción primaria y a la selección. No se usa para decorar, ni para titulares, ni para fondos de sección.

**The Semantic Status Rule.** Azul, ámbar, verde y gris significan exclusivamente Abierto, En revisión, Respondido y Cerrado (rojo: error y prioridad Alta). Un color de estado nunca aparece como decoración.

**The Neutral Rail Rule.** El riel, la barra móvil y la banda de acceso son pizarra neutra; el verde azulado nunca rellena el riel, solo aparece en él como cuadro de marca, icono activo y foco. El área de trabajo permanece blanca y fría.

## Typography

**Display Font:** ninguna; la pila del sistema (system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial) cubre todos los roles.
**Body Font:** la misma pila del sistema.
**Label/Mono Font:** ui-monospace, Cascadia Mono, SF Mono, Consolas, para identificadores.

**Character:** Tipografía de herramienta, no de marca: nítida, nativa de cada plataforma y con pesos intermedios (650 a 680) que dan autoridad a los títulos sin gritar.

### Hierarchy
- **Headline** (680, 1.625rem, 1.25, -0.02em): título de página ("Mis tickets") y titular de la confirmación.
- **Title** (650 a 680, 1.375rem, 1.25, -0.015em): título del panel de acceso y de estados vacíos o de error.
- **Subtitle** (650, 1.0625rem): encabezados internos ("Tu correo de seguimiento"), nombre de la marca, correo del buzón grande (600).
- **Body** (400, 0.9375rem, 1.5): texto corriente; la descripción del ticket usa 1.65 de interlineado y máximo 72ch; subtítulos de página a 62ch.
- **Label** (600, 0.8125rem): etiquetas de campo, títulos de panel (650 en `ink-2`), avisos, texto de tabla.
- **Caption** (600, 0.75rem): cabeceras de tabla, pills de estado, términos de metadatos, contadores.
- **Mono** (400, 0.8125rem): folio `#0001`, correo de seguimiento, sufijo `@dami.lat`.

### Named Rules
**The Identifier Mono Rule.** La monoespaciada se reserva a identificadores que el cliente copia o cita (folio y correo). Nunca para texto corriente ni etiquetas.

**The Tabular Numbers Rule.** Folios y cifras usan `font-variant-numeric: tabular-nums` (clase `num`).

## Layout

Rejilla de dos columnas: riel fijo de 248px a la izquierda (sticky, alto completo) y área principal `minmax(0, 1fr)`. El contenido principal se centra con máximo 1120px y relleno de 40px (64px abajo); los formularios limitan sus hijos a 680px. El detalle de ticket usa dos columnas (`1fr` + lateral de 340px, separación 20px) que colapsan a una bajo 960px.

La cabecera de página alinea título y subtítulo a la izquierda y la acción primaria abajo a la derecha, con 24px de separación inferior. El ritmo vertical se construye en pasos de 4: 6, 8, 12, 16, 20, 24, 28, 32 y 40px; 20px es el espacio estándar entre campos y paneles.

Responsivo: bajo 760px el riel pasa a barra superior horizontal (marca solo con glifo, navegación en fila, sin avatar ni nombre), el relleno baja a 24px/16px, las filas de formulario y la rejilla de metadatos colapsan a una columna, las tablas ocultan columnas secundarias y el botón Copiar del buzón ocupa el ancho completo. Las pantallas de acceso usan una columna centrada de 420px sobre la banda del riel.

## Elevation & Depth

Sistema plano con borde: la profundidad viene del contraste entre el suelo frío y la superficie blanca, más un borde de 1px. Las sombras son ambientales y casi invisibles; solo crecen en los dos momentos que piden foco (la confirmación y el panel de acceso).

### Shadow Vocabulary
- **Reposo** (`--shadow-sm`): paneles, tablas, botón secundario.
- **Elevada** (`--shadow-md`): tarjeta de confirmación.
- **Acceso** (sombra doble con 12px/32px al 10%): panel de inicio de sesión y registro sobre la banda del riel.
- **Acento** (sombra de 2px/8px teñida de verde azulado): buzón grande y botón primario.

### Named Rules
**The Border-First Rule.** Todo contenedor se define primero por su borde de 1px (`line`); la sombra solo acompaña, nunca sustituye al borde.

## Shapes

Esquinas suavemente redondeadas en tres pasos: 6px para elementos internos (opciones del control segmentado, enlace de salto), 8px para controles (botones, campos, buzón, ítems del riel, avisos) y 12px para contenedores (paneles, tabla, estados vacíos, confirmación). Pills de estado y avatar son completamente redondos. Los estados vacíos usan borde discontinuo para distinguirse de los paneles con contenido.

## Components

### Buttons
Firmes y compactos.
- **Shape:** esquinas suaves (8px), alto de 40px, peso 600, icono de 17px con 8px de separación.
- **Primary:** fondo `accent`, texto casi blanco, sombra teñida mínima; oscurece a `accent-hover` y a un tono más profundo al presionar.
- **Secondary:** superficie blanca con borde `line-strong` y sombra de reposo; al pasar, `surface-2` y borde más oscuro.
- **Ghost:** transparente en `ink-2`; al pasar, fondo gris frío y texto `ink`.
- **Small:** 34px de alto, 12px de relleno, texto label.
- **Busy:** al enviar, el texto se oculta y aparece un spinner circular de 16px (700ms); el botón queda deshabilitado.
- Todas las transiciones duran 160ms con la curva `--ease`.

### Chips (pills de estado)
- **Style:** pill de 24px, fondo `-bg` del estado y texto del color del estado, con un punto de 6px en `currentColor`.
- **State:** cuatro variantes fijas (Abierto, En revisión, Respondido, Cerrado); no son interactivas.

### Cards / Containers
- **Corner Style:** 12px.
- **Background:** `surface` sobre `ground`.
- **Shadow Strategy:** reposo; elevada solo en la confirmación (ver Elevation & Depth).
- **Border:** 1px `line`.
- **Internal Padding:** 24px (20px en móvil); confirmación y acceso 32px.

### Inputs / Fields
- **Style:** fondo blanco, borde 1px `line-strong`, radio 8px, 40px de alto mínimo, cursor de texto en acento; etiqueta label encima a 6px; textarea de 160px mínimo con contador abajo a la derecha.
- **Focus:** el borde pasa a `accent` con halo de 3px del color de foco al 22%.
- **Error:** borde `danger-red` y halo rojo; mensaje en rojo con icono de alerta de 15px bajo el campo.
- **Select:** flecha Lucide en línea a 10px del borde derecho.
- **Affix:** campo con sufijo fijo (`@dami.lat`) en monoespaciada sobre `surface-2`, separado por un divisor.

### Navigation
- **Style:** ítems del riel con icono de 18px, peso 500, relleno 9px/10px, radio 8px, texto `rail-muted`.
- **Hover:** fondo `rail-hover` y texto `rail-ink`.
- **Active:** fondo `rail-active`, texto `rail-ink`, hairline interior blanca al 6% e icono en `rail-glint`.
- **Pie:** avatar circular de 32px, nombre y correo truncados, botón de salir solo icono; separado por una línea blanca al 10%.
- **Mobile:** barra horizontal superior del mismo color, ítems en fila con texto label.

### Segmented Control
Selector de prioridad en tres opciones iguales sobre una bandeja gris fría de 3px de relleno; la opción marcada toma `accent-soft`, texto `accent-ink`, peso 650 y un contorno de 1px verde azulado.

### Priority Bars
Tres barras verticales de 3px (5, 8 y 12px de alto) junto al texto de prioridad: Baja llena una barra en `ink-2`, Media dos, Alta las tres en `danger-red`.

### Tracking Mailbox (componente firma)
El bloque del correo de seguimiento: icono de sobre en `accent-ink`, dirección en monoespaciada seleccionable completa, botón secundario pequeño "Copiar" que cambia a "Copiado" en verde durante 2 segundos. Variante grande en la confirmación: superficie blanca, borde de 1.5px en `accent`, sombra de acento y dirección en subtitle. Variante compacta en el lateral del detalle: dirección truncada y botón solo icono de 34px.

### Notices
Aviso de ancho completo con icono de 17px, borde de 1px y fondo del color semántico (éxito, información, error), texto label; entra con un desplazamiento de 4px hacia abajo en 260ms.

## Do's and Don'ts

### Do:
- **Do** mantener el pizarra neutro (`rail`) en el riel, la barra móvil y la banda de acceso, y el área de trabajo en `ground`/`surface`.
- **Do** dar a cada pantalla un solo botón primario (`accent`), colocado arriba a la derecha de la cabecera o al final del formulario.
- **Do** presentar el correo de seguimiento siempre en el bloque de buzón, en monoespaciada y con su botón Copiar.
- **Do** usar iconos Lucide en trazo de 2px como `<symbol>` SVG inline, a 16-18px junto a texto.
- **Do** animar estados en 160ms con `cubic-bezier(0.16, 1, 0.3, 1)` y respetar `prefers-reduced-motion`.
- **Do** definir contenedores con borde de 1px `line` y radio de 12px.

### Don't:
- **Don't** rellenar el riel, la barra móvil o la banda de acceso con verde azulado.
- **Don't** usar el acento verde azulado ni los colores de estado como decoración, fondo de sección o color de titular.
- **Don't** construir portales de tarjetas iguales en rejilla para la navegación; el riel y la tabla son la estructura.
- **Don't** presentar un formulario suelto sin riel, título de página ni contexto.
- **Don't** usar la monoespaciada fuera de folios y correos.
- **Don't** sustituir el borde de un contenedor por sombra sola ni añadir sombras fuertes o desplazadas.
