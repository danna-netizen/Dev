---
version: 1
slug: "helpdesk-templates"
primary_target: "helpdesk/templates"
related_targets: []
---

## Scope

Aplicación Flask completa de Dami Soporte (registro, inicio de sesión, lista de tickets, nuevo ticket, confirmación y detalle). Modo: Operate.

## Audience and task

Clientes externos que reportan un problema y necesitan saber que se recibió y a dónde escribir para seguimiento. La confirmación debe dejar claro el correo de seguimiento @dami.lat.

## Direction contract

THESIS: Helpdesk estándar ejecutado con precisión (barra lateral + área de trabajo, a la altura de Zendesk o Freshdesk). Rechaza el portal genérico de tarjetas iguales y el formulario suelto sin contexto.
OWN-WORLD: Fondo blanco frío; riel lateral, barra móvil y banda de acceso en gris pizarra neutro frío (elección del usuario: "Gris pizarra neutro"); un solo acento verde azulado para acciones primarias, selección y la marca; colores de estado semánticos (azul abierto, ámbar en revisión, verde respondido, gris cerrado). Pila tipográfica del sistema, escala 1.2, iconos Lucide en trazo de 2px.
STORY: El cliente entra, levanta su ticket en un formulario corto, y la confirmación le entrega su correo de seguimiento como dato principal, con instrucción explícita de escribir ahí dudas o quejas.
FIRST VIEWPORT: Barra lateral izquierda de 240px (marca, Mis tickets, Nuevo ticket, usuario y Salir abajo); área principal con título de página, acción primaria arriba a la derecha y tabla de tickets o formulario. En la confirmación, el bloque del correo con botón Copiar ocupa el centro de atención.
FORM: Canon (salida estándar elegida por el usuario), seed: none (canon chosen) sobre seed:28a62392a3d050c3. Referencias de oficio: Zendesk, Freshdesk.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
