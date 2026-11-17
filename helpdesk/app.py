"""Dami Soporte: mesa de ayuda en Flask.

Ejecutar:  python app.py   (o  flask --app app run --debug)
"""
import os
import re
import secrets
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
    DATABASE=os.environ.get("DATABASE") or os.path.join(BASE_DIR, "helpdesk.db"),
    # Dominio de los correos de seguimiento. Cámbialo aquí o con la variable de entorno.
    TRACKING_DOMAIN=os.environ.get("TRACKING_DOMAIN", "dami.lat"),
    # Dirección a la que se pide enviar el PDF en tickets de prioridad alta.
    SALES_EMAIL=os.environ.get("SALES_EMAIL", "danna@reimbursor.info"),
)

CATEGORIES = ["Cuenta y acceso", "Facturación y pagos", "Falla técnica", "Pedido o envío", "Otro"]
PRIORITIES = {"baja": "Baja", "media": "Media", "alta": "Alta"}
STATUSES = {
    "abierto": "Abierto",
    "revision": "En revisión",
    "respondido": "Respondido",
    "cerrado": "Cerrado",
}
LOCAL_PART_RE = re.compile(r"^[a-z0-9](?:[a-z0-9._-]{1,38}[a-z0-9])$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
# Sin caracteres ambiguos (0/o, 1/l/i) para que el correo sea fácil de dictar o copiar a mano.
TOKEN_ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    subject TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'abierto',
    tracking_email TEXT UNIQUE,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


# --------------------------------------------------------------------------- db
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        get_db().executescript(SCHEMA)


def now():
    return datetime.now().isoformat(timespec="seconds")


# ------------------------------------------------------------- tracking email
def random_tracking_email(ticket_id):
    """Correo de seguimiento inventado: caso-0042-k7m2qx@dami.lat (no es funcional todavía)."""
    db = get_db()
    domain = app.config["TRACKING_DOMAIN"]
    while True:
        token = "".join(secrets.choice(TOKEN_ALPHABET) for _ in range(6))
        email = f"caso-{ticket_id:04d}-{token}@{domain}"
        if not db.execute("SELECT 1 FROM tickets WHERE tracking_email = ?", (email,)).fetchone():
            return email


# ------------------------------------------------------------------ security
def csrf_token():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(32)
    return session["_csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def protect_forms():
    if request.method == "POST":
        sent = request.form.get("_csrf", "")
        if not sent or not secrets.compare_digest(sent, session.get("_csrf", "")):
            abort(400, "La sesión del formulario expiró. Recarga la página e inténtalo de nuevo.")


@app.before_request
def load_user():
    uid = session.get("user_id")
    g.user = None
    if uid is not None:
        g.user = get_db().execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
        if g.user is None:
            session.clear()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            flash("Inicia sesión para continuar.", "info")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def safe_next(target):
    return target if target and target.startswith("/") and not target.startswith("//") else None


# ----------------------------------------------------------------- template
# Globals (no context_processor) para que también las vean las macros importadas.
app.jinja_env.globals.update(STATUSES=STATUSES, PRIORITIES=PRIORITIES)


@app.context_processor
def inject_globals():
    return {"TRACKING_DOMAIN": app.config["TRACKING_DOMAIN"], "SALES_EMAIL": app.config["SALES_EMAIL"]}


@app.template_filter("fecha")
def fecha(value):
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    d = datetime.fromisoformat(value)
    return f"{d.day} {meses[d.month - 1]} {d.year}, {d:%H:%M}"


@app.template_filter("folio")
def folio(ticket_id):
    return f"#{ticket_id:04d}"


# ------------------------------------------------------------------- auth
@app.route("/")
def index():
    return redirect(url_for("tickets" if g.user else "login"))


@app.route("/registro", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(url_for("tickets"))
    errors, form = {}, {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ("name", "email")}
        form["email"] = form["email"].lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if len(form["name"]) < 2:
            errors["name"] = "Escribe tu nombre."
        if not EMAIL_RE.match(form["email"]):
            errors["email"] = "Escribe un correo válido, por ejemplo nombre@empresa.com."
        elif get_db().execute("SELECT 1 FROM users WHERE email = ?", (form["email"],)).fetchone():
            errors["email"] = "Ya existe una cuenta con este correo. Inicia sesión."
        if len(password) < 8:
            errors["password"] = "Usa al menos 8 caracteres."
        elif password != confirm:
            errors["confirm"] = "Las contraseñas no coinciden."
        if not errors:
            db = get_db()
            cur = db.execute(
                "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (form["name"], form["email"], generate_password_hash(password), now()),
            )
            db.commit()
            session.clear()
            session["user_id"] = cur.lastrowid
            flash(f"Cuenta creada. Hola, {form['name'].split()[0]}.", "success")
            return redirect(url_for("tickets"))
    return render_template("auth/register.html", errors=errors, form=form), (422 if errors else 200)


@app.route("/entrar", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for("tickets"))
    error, email = None, ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear()
            session["user_id"] = user["id"]
            return redirect(safe_next(request.args.get("next")) or url_for("tickets"))
        error = "El correo o la contraseña no coinciden. Revisa e inténtalo de nuevo."
    return render_template("auth/login.html", error=error, email=email), (401 if error else 200)


@app.route("/salir", methods=["POST"])
def logout():
    session.clear()
    flash("Cerraste sesión.", "info")
    return redirect(url_for("login"))


# ---------------------------------------------------------------- tickets
def own_ticket(ticket_id):
    t = get_db().execute(
        "SELECT * FROM tickets WHERE id = ? AND user_id = ?", (ticket_id, g.user["id"])
    ).fetchone()
    if t is None:
        abort(404)
    return t


@app.route("/tickets")
@login_required
def tickets():
    rows = get_db().execute(
        "SELECT * FROM tickets WHERE user_id = ? ORDER BY updated_at DESC", (g.user["id"],)
    ).fetchall()
    return render_template("tickets/list.html", tickets=rows)


@app.route("/tickets/nuevo", methods=["GET", "POST"])
@login_required
def new_ticket():
    errors, form = {}, {"priority": "media"}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ("subject", "category", "priority", "description")}
        if len(form["subject"]) < 5:
            errors["subject"] = "Resume el problema en una frase (mínimo 5 caracteres)."
        if form["category"] not in CATEGORIES:
            errors["category"] = "Elige la categoría que mejor describa el problema."
        if form["priority"] not in PRIORITIES:
            errors["priority"] = "Elige una prioridad."
        if len(form["description"]) < 20:
            errors["description"] = "Cuéntanos un poco más: qué pasó, cuándo y qué esperabas que pasara."
        if not errors:
            db = get_db()
            ts = now()
            cur = db.execute(
                "INSERT INTO tickets (user_id, subject, category, priority, description, created_at, updated_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (g.user["id"], form["subject"], form["category"], form["priority"], form["description"], ts, ts),
            )
            tid = cur.lastrowid
            db.execute("UPDATE tickets SET tracking_email = ? WHERE id = ?", (random_tracking_email(tid), tid))
            db.commit()
            return redirect(url_for("ticket_sent", ticket_id=tid))
    return render_template("tickets/new.html", errors=errors, form=form, categories=CATEGORIES), (422 if errors else 200)


@app.route("/tickets/<int:ticket_id>/enviado")
@login_required
def ticket_sent(ticket_id):
    return render_template("tickets/sent.html", t=own_ticket(ticket_id))


@app.route("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id):
    return render_template("tickets/detail.html", t=own_ticket(ticket_id), email_error=None)


@app.route("/tickets/<int:ticket_id>/correo", methods=["POST"])
@login_required
def change_tracking_email(ticket_id):
    t = own_ticket(ticket_id)
    local = request.form.get("local_part", "").strip().lower()
    error = None
    if not LOCAL_PART_RE.match(local):
        error = "Usa de 3 a 40 caracteres: letras minúsculas, números, punto, guion o guion bajo. Debe empezar y terminar con letra o número."
    else:
        email = f"{local}@{app.config['TRACKING_DOMAIN']}"
        if email == t["tracking_email"]:
            return redirect(url_for("ticket_detail", ticket_id=ticket_id))
        db = get_db()
        if db.execute("SELECT 1 FROM tickets WHERE tracking_email = ?", (email,)).fetchone():
            error = f"{email} ya está en uso. Prueba con otro nombre."
        else:
            db.execute("UPDATE tickets SET tracking_email = ?, updated_at = ? WHERE id = ?", (email, now(), ticket_id))
            db.commit()
            flash(f"Listo. El correo de seguimiento ahora es {email}.", "success")
            return redirect(url_for("ticket_detail", ticket_id=ticket_id))
    return render_template("tickets/detail.html", t=t, email_error=error, local_attempt=local), 422


@app.errorhandler(404)
def not_found(_e):
    return render_template("error.html", code=404, title="No encontramos esta página",
                           message="El ticket o la página que buscas no existe o no es tuyo."), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template("error.html", code=400, title="No pudimos procesar el formulario",
                           message=getattr(e, "description", "")), 400


init_db()

if __name__ == "__main__":
    app.run(debug=True)
