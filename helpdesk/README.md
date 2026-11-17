# Dami Soporte

Mesa de ayuda en Flask: registro, inicio de sesión, levantamiento de tickets y un correo de seguimiento `@dami.lat` generado al azar para cada ticket.

## Ejecutar

```powershell
cd helpdesk
.venv\Scripts\activate          # o: python -m venv .venv  y  pip install -r requirements.txt
python app.py
```

Abre http://127.0.0.1:5000. La base de datos SQLite (`helpdesk.db`) se crea sola.

## Flujo

1. **/registro**: nombre, correo y contraseña (mínimo 8 caracteres, guardada con hash).
2. **/entrar**: inicio de sesión. **Salir** cierra la sesión (POST).
3. **/tickets/nuevo**: asunto, categoría, prioridad y descripción.
4. Al enviar, se genera el correo de seguimiento (`caso-0042-k7m2qx@dami.lat`) y la pantalla de confirmación le indica al usuario que ahí puede escribir dudas o quejas sobre ese ticket.
5. **/tickets/&lt;id&gt;**: detalle; desde ahí se puede **cambiar la dirección** (la parte antes de la @).

## Correo de seguimiento

- **No es funcional**: no envía ni recibe nada; solo es un identificador inventado.
- Para cambiar el dominio de todos los correos nuevos: variable de entorno `TRACKING_DOMAIN` o `app.config["TRACKING_DOMAIN"]` en `app.py`.
- El formato aleatorio vive en `random_tracking_email()` dentro de `app.py`.

## Configuración

| Variable | Uso | Por defecto |
|---|---|---|
| `SECRET_KEY` | Firma de sesiones. **Defínela en producción** (si no, las sesiones se pierden al reiniciar). | aleatoria |
| `DATABASE` | Ruta del archivo SQLite | `helpdesk.db` |
| `TRACKING_DOMAIN` | Dominio del correo de seguimiento | `dami.lat` |

## Pendiente (no incluido)

- Panel de agentes para responder tickets y cambiar el estado (hoy los estados existen: Abierto, En revisión, Respondido, Cerrado, pero solo se cambian en la base de datos).
- Recepción real de correo en las direcciones de seguimiento.
