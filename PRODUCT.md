# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Flask (Python), pedido explícito del usuario. Plantillas Jinja, SQLite como almacenamiento local (delegado: elección por simplicidad para un primer prototipo).

## Users

Clientes externos de la empresa que necesitan reportar un problema con un producto o servicio y darle seguimiento. Llegan con un problema concreto, a menudo frustrados, y quieren saber que alguien lo recibió y cómo seguirlo.

## Product Purpose

Dami Soporte es una mesa de ayuda: el cliente se registra, inicia sesión, levanta un ticket describiendo su problema y recibe una dirección de correo de seguimiento única para ese ticket. Éxito: el cliente termina la solicitud sabiendo exactamente a dónde escribir si tiene dudas o quejas.

## Positioning

Cada ticket recibe su propio correo de seguimiento en el dominio dami.lat (aleatorio, editable después), de modo que la conversación sobre ese caso tiene una dirección dedicada.

## Capabilities and Constraints

- Registro, inicio y cierre de sesión.
- Crear ticket: asunto, categoría, prioridad, descripción del problema.
- Al crear el ticket se genera automáticamente un correo `<aleatorio>@dami.lat`; el usuario puede cambiar la parte local después.
- La pantalla de confirmación indica explícitamente que ese correo es el canal para dudas o quejas sobre el ticket.
- Por ahora el correo NO es funcional (no se envía ni recibe nada); es un identificador inventado.
- Idioma de la interfaz: español.

## Brand Commitments

Nombre: "Dami Soporte". Dominio: dami.lat.

## Evidence on Hand

No hay logotipo, testimonios ni datos reales. No inventar clientes, métricas ni tiempos de respuesta garantizados.

## Product Principles

1. El cliente nunca debe quedarse con la duda de si su solicitud llegó.
2. El correo de seguimiento es el dato más importante de la confirmación.
3. Formularios cortos: pedir solo lo necesario para atender el problema.
