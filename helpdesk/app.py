"""Helpdesk: ticket-based customer support app (Flask).

Run:  flask --app app run        (or  python app.py  for debug mode, local use only)

Two interfaces share one database:
  * Agent backend  (/helpdesk)  - Kanban board by stage, ticket form with chatter.
  * Customer portal (/my)       - customers open tickets and follow the conversation.
"""
import os
import re
import secrets
import sqlite3
from datetime import datetime, timedelta
from functools import wraps

from flask import (Flask, abort, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import seed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
    DATABASE=os.environ.get("DATABASE") or os.path.join(BASE_DIR, "helpdesk.db"),
)

STAGES = [("new", "New"), ("in_progress", "In Progress"), ("solved", "Solved"), ("cancelled", "Cancelled")]
STAGE_LABELS = dict(STAGES)
PRIORITIES = {0: "Low", 1: "Medium", 2: "High", 3: "Urgent"}
CHANNELS = ["Email", "Live Chat", "WhatsApp", "Website Form"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ROLES = {"admin": "Admin", "agent": "Agent", "customer": "Customer"}
STAFF_ROLES = ("admin", "agent")

# Role -> permission matrix shown on the Privileges page (and enforced by the route decorators).
PERMISSIONS = [
    ("Open tickets and follow their own conversations", True, True, True),
    ("Be assigned tickets and reply to them", True, True, True),
    ("See every ticket in the Kanban board and list", True, True, False),
    ("Change stages, assignee, team and priority", True, True, False),
    ("Write internal notes", True, True, False),
    ("Manage users and change roles", True, False, False),
    ("View settings and edit them", True, False, False),
    ("View demo account passwords", True, False, False),
]
SETTING_DEFAULTS = {
    "company_name": "Helpdesk",
    "support_email": "support@example.com",
    "allow_signup": "1",
    "default_priority": "1",
    "enabled_channels": ",".join(CHANNELS),
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    demo_password TEXT,  -- only for the fake demo accounts; real sign-ups stay hashed
    role TEXT NOT NULL DEFAULT 'customer',  -- admin | agent | customer
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES users(id),
    assignee_id INTEGER REFERENCES users(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    stage TEXT NOT NULL DEFAULT 'new',
    priority INTEGER NOT NULL DEFAULT 1,
    channel TEXT NOT NULL DEFAULT 'Website Form',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    closed_at TEXT
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id),
    author_id INTEGER NOT NULL REFERENCES users(id),
    kind TEXT NOT NULL DEFAULT 'message',  -- message (public) | note (internal) | log (history)
    body TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

TICKET_SQL = """
SELECT t.*, c.name AS customer_name, c.email AS customer_email,
       a.name AS assignee_name, tm.name AS team_name
FROM tickets t
JOIN users c ON c.id = t.customer_id
LEFT JOIN users a ON a.id = t.assignee_id
JOIN teams tm ON tm.id = t.team_id
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


SEED_VERSION = 7  # bump when the schema or demo data changes: the database is rebuilt


def init_db():
    with app.app_context():
        db = get_db()
        if db.execute("PRAGMA user_version").fetchone()[0] != SEED_VERSION:
            db.executescript("DROP TABLE IF EXISTS messages; DROP TABLE IF EXISTS tickets;"
                             " DROP TABLE IF EXISTS teams; DROP TABLE IF EXISTS users;"
                             " DROP TABLE IF EXISTS settings;")
            db.executescript(SCHEMA)
            seed.populate(db)
            db.execute(f"PRAGMA user_version = {SEED_VERSION}")
        else:
            db.executescript(SCHEMA)
        db.commit()


def now():
    return datetime.now().isoformat(timespec="seconds")


# ------------------------------------------------------------------ security
def csrf_token():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(32)
    return session["_csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def protect_forms():
    if request.method == "POST":
        sent = request.form.get("_csrf") or request.headers.get("X-CSRF-Token", "")
        if not sent or not secrets.compare_digest(sent, session.get("_csrf", "")):
            abort(400, "Your session expired. Reload the page and try again.")


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
            flash("Please sign in to continue.", "info")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def agent_required(view):
    """Agent backend: agents and admins."""
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if g.user["role"] not in STAFF_ROLES:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if g.user["role"] != "admin":
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def customer_required(view):
    """Portal: customers and admins (agents live in the backend)."""
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if g.user["role"] == "agent":
            return redirect(url_for("board"))
        return view(*args, **kwargs)
    return wrapped


def safe_next(target):
    return target if target and target.startswith("/") and not target.startswith("//") else None


def home_for(user):
    return url_for("board") if user["role"] == "agent" else url_for("my_tickets")


def get_settings():
    if "settings" not in g:
        stored = {r["key"]: r["value"] for r in get_db().execute("SELECT key, value FROM settings")}
        g.settings = {**SETTING_DEFAULTS, **stored}
        g.settings["channels"] = [c for c in g.settings["enabled_channels"].split(",") if c in CHANNELS]
    return g.settings


# ----------------------------------------------------------------- template
app.jinja_env.globals.update(STAGES=STAGES, STAGE_LABELS=STAGE_LABELS, PRIORITIES=PRIORITIES, CHANNELS=CHANNELS,
                             ROLES=ROLES)


@app.context_processor
def inject_settings():
    return {"settings": get_settings()}


@app.template_filter("role_label")
def role_label(role):
    return ROLES.get(role, role.title())


@app.template_filter("dt")
def fmt_dt(value):
    d = datetime.fromisoformat(value)
    return f"{d:%b} {d.day}, {d.year} {d:%H:%M}"


@app.template_filter("ago")
def ago(value):
    secs = int((datetime.now() - datetime.fromisoformat(value)).total_seconds())
    if secs < 60:
        return "just now"
    if secs < 3600:
        return f"{secs // 60} min ago"
    if secs < 86400:
        return f"{secs // 3600} h ago"
    if secs < 30 * 86400:
        return f"{secs // 86400} d ago"
    return fmt_dt(value)


@app.template_filter("ref")
def ref(ticket_id):
    return f"#{ticket_id:04d}"


# ------------------------------------------------------------------- auth
@app.route("/")
def index():
    return redirect(home_for(g.user) if g.user else url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(home_for(g.user))
    if get_settings()["allow_signup"] != "1":
        flash("Sign-ups are closed. Ask an administrator to create your account.", "info")
        return redirect(url_for("login"))
    errors, form = {}, {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ("name", "email")}
        form["email"] = form["email"].lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if len(form["name"]) < 2:
            errors["name"] = "Enter your name."
        if not EMAIL_RE.match(form["email"]):
            errors["email"] = "Enter a valid email, for example name@company.com."
        elif get_db().execute("SELECT 1 FROM users WHERE email = ?", (form["email"],)).fetchone():
            errors["email"] = "An account with this email already exists. Sign in instead."
        if len(password) < 8:
            errors["password"] = "Use at least 8 characters."
        elif password != confirm:
            errors["confirm"] = "Passwords do not match."
        if not errors:
            db = get_db()
            cur = db.execute(
                "INSERT INTO users (name, email, password_hash, role, created_at) VALUES (?, ?, ?, 'customer', ?)",
                (form["name"], form["email"], generate_password_hash(password), now()))
            db.commit()
            session.clear()
            session["user_id"] = cur.lastrowid
            flash(f"Account created. Welcome, {form['name'].split()[0]}.", "success")
            return redirect(url_for("my_tickets"))
    return render_template("register.html", errors=errors, form=form), (422 if errors else 200)


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(home_for(g.user))
    error, email = None, ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear()
            session["user_id"] = user["id"]
            return redirect(safe_next(request.args.get("next")) or home_for(user))
        error = "Email or password is incorrect. Check them and try again."
    return render_template("login.html", error=error, email=email), (401 if error else 200)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("login"))


# ---------------------------------------------------------------- shared helpers
def get_ticket(ticket_id, participant_id=None):
    """A ticket by id. With participant_id, only if that user requested it or is assigned to it."""
    sql = TICKET_SQL + " WHERE t.id = ?"
    params = [ticket_id]
    if participant_id is not None:
        sql += " AND (t.customer_id = ? OR t.assignee_id = ?)"
        params += [participant_id, participant_id]
    t = get_db().execute(sql, params).fetchone()
    if t is None:
        abort(404)
    return t


def get_messages(ticket_id, include_internal):
    sql = ("SELECT m.*, u.name AS author_name, u.role AS author_role FROM messages m "
           "JOIN users u ON u.id = m.author_id WHERE m.ticket_id = ?")
    if not include_internal:
        sql += " AND m.kind = 'message'"
    return get_db().execute(sql + " ORDER BY m.created_at, m.id", (ticket_id,)).fetchall()


def add_message(ticket_id, kind, body, author_id=None):
    db = get_db()
    ts = now()
    db.execute("INSERT INTO messages (ticket_id, author_id, kind, body, created_at) VALUES (?, ?, ?, ?, ?)",
               (ticket_id, author_id or g.user["id"], kind, body, ts))
    db.execute("UPDATE tickets SET updated_at = ? WHERE id = ?", (ts, ticket_id))


def set_stage(ticket, stage):
    """Change a ticket's stage and leave a history entry. Returns True if it changed."""
    if stage not in STAGE_LABELS or stage == ticket["stage"]:
        return False
    db = get_db()
    closed = now() if stage in ("solved", "cancelled") else None
    db.execute("UPDATE tickets SET stage = ?, closed_at = ? WHERE id = ?", (stage, closed, ticket["id"]))
    add_message(ticket["id"], "log", f"Stage: {STAGE_LABELS[ticket['stage']]} → {STAGE_LABELS[stage]}")
    return True


def people(exclude_id=None):
    """Everyone a ticket can be requested by or assigned to (agents first)."""
    rows = get_db().execute("SELECT id, name, role FROM users ORDER BY role, name").fetchall()
    return [p for p in rows if p["id"] != exclude_id]


def teams():
    return get_db().execute("SELECT id, name FROM teams ORDER BY id").fetchall()


# ---------------------------------------------------------------- agent backend
@app.route("/helpdesk")
@agent_required
def board():
    team = request.args.get("team", type=int)
    q = request.args.get("q", "").strip()
    mine = request.args.get("mine") == "1"
    view = request.args.get("view", "kanban")
    if view not in ("kanban", "list"):
        view = "kanban"

    where, params = [], []
    if team:
        where.append("t.team_id = ?")
        params.append(team)
    if mine:
        where.append("t.assignee_id = ?")
        params.append(g.user["id"])
    if q:
        where.append("(t.subject LIKE ? OR c.name LIKE ? OR c.email LIKE ? OR CAST(t.id AS TEXT) LIKE ?)")
        params += [f"%{q}%"] * 3 + [q.lstrip("#").lstrip("0") + "%"]
    sql = TICKET_SQL + (" WHERE " + " AND ".join(where) if where else "")
    rows = get_db().execute(sql + " ORDER BY t.priority DESC, t.updated_at DESC", params).fetchall()

    columns = {key: [] for key, _ in STAGES}
    for t in rows:
        columns[t["stage"]].append(t)

    week_ago = (datetime.now() - timedelta(days=7)).isoformat(timespec="seconds")
    open_rows = [t for t in rows if t["stage"] in ("new", "in_progress")]
    stats = {
        "open": len(open_rows),
        "unassigned": sum(1 for t in open_rows if t["assignee_id"] is None),
        "urgent": sum(1 for t in open_rows if t["priority"] == 3),
        "solved_week": sum(1 for t in rows if t["stage"] == "solved" and (t["closed_at"] or "") >= week_ago),
    }
    return render_template("agent/board.html", columns=columns, rows=rows, stats=stats, teams=teams(),
                           team=team, q=q, mine=mine, view=view)


@app.route("/helpdesk/tickets/<int:tid>")
@agent_required
def agent_ticket(tid):
    return render_template("agent/ticket.html", t=get_ticket(tid), messages=get_messages(tid, True),
                           people=people(), teams=teams())


@app.route("/helpdesk/new", methods=["GET", "POST"])
@agent_required
def agent_new_ticket():
    db = get_db()
    errors, form = {}, {"priority": "1", "channel": "Email", "assignee_id": str(g.user["id"])}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in
                ("subject", "customer_id", "team_id", "priority", "channel", "assignee_id", "description")}
        if len(form["subject"]) < 5:
            errors["subject"] = "Enter a subject (at least 5 characters)."
        if not db.execute("SELECT 1 FROM users WHERE id = ?", (form["customer_id"],)).fetchone():
            errors["customer_id"] = "Choose who is requesting this."
        if not db.execute("SELECT 1 FROM teams WHERE id = ?", (form["team_id"],)).fetchone():
            errors["team_id"] = "Choose a team."
        if form["priority"] not in {str(k) for k in PRIORITIES}:
            errors["priority"] = "Choose a priority."
        if form["channel"] not in get_settings()["channels"]:
            errors["channel"] = "Choose a channel."
        if len(form["description"]) < 10:
            errors["description"] = "Describe the issue (at least 10 characters)."
        if not errors:
            assignee = int(form["assignee_id"]) if form["assignee_id"].isdigit() and int(form["assignee_id"]) else None
            ts = now()
            cur = db.execute(
                "INSERT INTO tickets (subject, description, customer_id, assignee_id, team_id, stage, priority,"
                " channel, created_at, updated_at) VALUES (?, ?, ?, ?, ?, 'new', ?, ?, ?, ?)",
                (form["subject"], form["description"], form["customer_id"], assignee, form["team_id"],
                 int(form["priority"]), form["channel"], ts, ts))
            tid = cur.lastrowid
            db.execute("INSERT INTO messages (ticket_id, author_id, kind, body, created_at) VALUES (?, ?, 'message', ?, ?)",
                       (tid, form["customer_id"], form["description"], ts))
            db.commit()
            flash(f"Ticket {tid:04d} created.", "success")
            return redirect(url_for("agent_ticket", tid=tid))
    return render_template("agent/new.html", errors=errors, form=form, channels=get_settings()["channels"],
                           people=people(), teams=teams()), (422 if errors else 200)


@app.post("/helpdesk/tickets/<int:tid>/update")
@agent_required
def agent_update(tid):
    t = get_ticket(tid)
    db = get_db()
    changes = []
    assignee = request.form.get("assignee_id", "")
    new_assignee = int(assignee) if assignee.isdigit() and int(assignee) else None
    if new_assignee is not None and not db.execute(
            "SELECT 1 FROM users WHERE id = ?", (new_assignee,)).fetchone():
        abort(400, "Unknown user.")
    if new_assignee != t["assignee_id"]:
        new_name = db.execute("SELECT name FROM users WHERE id = ?", (new_assignee,)).fetchone()
        changes.append(f"Assigned to: {t['assignee_name'] or 'Unassigned'} → {new_name['name'] if new_name else 'Unassigned'}")
        db.execute("UPDATE tickets SET assignee_id = ? WHERE id = ?", (new_assignee, tid))
    team_id = request.form.get("team_id", type=int)
    new_team = db.execute("SELECT * FROM teams WHERE id = ?", (team_id,)).fetchone()
    if new_team and new_team["id"] != t["team_id"]:
        changes.append(f"Team: {t['team_name']} → {new_team['name']}")
        db.execute("UPDATE tickets SET team_id = ? WHERE id = ?", (new_team["id"], tid))
    priority = request.form.get("priority", type=int)
    if priority in PRIORITIES and priority != t["priority"]:
        changes.append(f"Priority: {PRIORITIES[t['priority']]} → {PRIORITIES[priority]}")
        db.execute("UPDATE tickets SET priority = ? WHERE id = ?", (priority, tid))
    for line in changes:
        add_message(tid, "log", line)
    db.commit()
    if changes:
        flash("Ticket saved.", "success")
    return redirect(url_for("agent_ticket", tid=tid))


@app.post("/helpdesk/tickets/<int:tid>/stage")
@agent_required
def agent_stage(tid):
    t = get_ticket(tid)
    stage = request.form.get("stage", "")
    if stage not in STAGE_LABELS:
        abort(400, "Unknown stage.")
    set_stage(t, stage)
    get_db().commit()
    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify(ok=True, stage=stage)
    return redirect(url_for("agent_ticket", tid=tid))


@app.post("/helpdesk/tickets/<int:tid>/message")
@agent_required
def agent_message(tid):
    t = get_ticket(tid)
    body = request.form.get("body", "").strip()
    kind = "note" if request.form.get("kind") == "note" else "message"
    if not body:
        flash("Write something before sending.", "error")
        return redirect(url_for("agent_ticket", tid=tid))
    db = get_db()
    add_message(tid, kind, body)
    if kind == "message":  # answering a new ticket picks it up
        if t["assignee_id"] is None:
            db.execute("UPDATE tickets SET assignee_id = ? WHERE id = ?", (g.user["id"], tid))
            add_message(tid, "log", f"Assigned to: Unassigned → {g.user['name']}")
        if t["stage"] == "new":
            set_stage(t, "in_progress")
    db.commit()
    flash("Message sent to the customer." if kind == "message" else "Internal note logged.", "success")
    return redirect(url_for("agent_ticket", tid=tid) + "#chatter-end")


# --------------------------------------------------------------- customer portal
@app.route("/my/tickets")
@customer_required
def my_tickets():
    uid = g.user["id"]
    rows = get_db().execute(
        TICKET_SQL + " WHERE t.customer_id = ? OR t.assignee_id = ? ORDER BY t.updated_at DESC", (uid, uid)).fetchall()
    requested = [t for t in rows if t["customer_id"] == uid]
    assigned = [t for t in rows if t["assignee_id"] == uid and t["customer_id"] != uid]
    return render_template("portal/list.html", requested=requested, assigned=assigned)


@app.route("/my/tickets/new", methods=["GET", "POST"])
@customer_required
def my_new_ticket():
    errors, form = {}, {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ("subject", "team_id", "assignee_id", "description")}
        db = get_db()
        assignee = None
        if len(form["subject"]) < 5:
            errors["subject"] = "Summarize the issue in a sentence (at least 5 characters)."
        if not db.execute("SELECT 1 FROM teams WHERE id = ?", (form["team_id"],)).fetchone():
            errors["team_id"] = "Choose the topic that best fits your request."
        if form["assignee_id"] not in ("", "0"):
            row = db.execute("SELECT id FROM users WHERE id = ? AND id != ?",
                             (form["assignee_id"], g.user["id"])).fetchone()
            if row is None:
                errors["assignee_id"] = "Choose someone from the list."
            else:
                assignee = row["id"]
        if len(form["description"]) < 20:
            errors["description"] = "Tell us a bit more: what happened, when, and what you expected."
        if not errors:
            ts = now()
            cur = db.execute(
                "INSERT INTO tickets (subject, description, customer_id, assignee_id, team_id, stage, priority,"
                " channel, created_at, updated_at) VALUES (?, ?, ?, ?, ?, 'new', ?, 'Website Form', ?, ?)",
                (form["subject"], form["description"], g.user["id"], assignee, form["team_id"],
                 int(get_settings()["default_priority"]), ts, ts))
            tid = cur.lastrowid
            add_message(tid, "message", form["description"])
            if assignee:
                who = db.execute("SELECT name FROM users WHERE id = ?", (assignee,)).fetchone()["name"]
                add_message(tid, "log", f"Assigned to: Unassigned → {who}")
            db.commit()
            flash("Your ticket was created and the person you chose can see it now."
                  if assignee else "Your ticket was created. Our team will reply here.", "success")
            return redirect(url_for("my_ticket", tid=tid))
    return render_template("portal/new.html", errors=errors, form=form, teams=teams(),
                           people=people(g.user["id"])), (422 if errors else 200)


@app.route("/my/tickets/<int:tid>")
@customer_required
def my_ticket(tid):
    t = get_ticket(tid, g.user["id"])
    return render_template("portal/ticket.html", t=t, messages=get_messages(tid, False))


@app.post("/my/tickets/<int:tid>/reply")
@customer_required
def my_reply(tid):
    t = get_ticket(tid, g.user["id"])
    body = request.form.get("body", "").strip()
    if not body:
        flash("Write a message before sending.", "error")
        return redirect(url_for("my_ticket", tid=tid))
    add_message(tid, "message", body)
    if t["stage"] in ("solved", "cancelled"):  # a reply reopens the ticket
        set_stage(t, "new")
    elif t["stage"] == "new" and t["assignee_id"] == g.user["id"]:  # the assignee picking it up
        set_stage(t, "in_progress")
    get_db().commit()
    flash("Message sent.", "success")
    return redirect(url_for("my_ticket", tid=tid) + "#chatter-end")


@app.post("/my/tickets/<int:tid>/stage")
@customer_required
def my_stage(tid):
    t = get_ticket(tid, g.user["id"])
    stage = request.form.get("stage", "")
    if t["assignee_id"] != g.user["id"] or stage not in ("in_progress", "solved"):
        abort(403)
    set_stage(t, stage)
    get_db().commit()
    flash("Ticket marked as done." if stage == "solved" else "Ticket is in progress.", "success")
    return redirect(url_for("my_ticket", tid=tid))


# ------------------------------------------------------------------- admin
@app.route("/admin")
@admin_required
def admin_home():
    return redirect(url_for("admin_users"))


@app.route("/admin/users")
@admin_required
def admin_users():
    rows = get_db().execute(
        "SELECT u.*, (SELECT COUNT(*) FROM tickets WHERE customer_id = u.id) AS requested,"
        " (SELECT COUNT(*) FROM tickets WHERE assignee_id = u.id) AS assigned"
        " FROM users u ORDER BY CASE u.role WHEN 'admin' THEN 0 WHEN 'agent' THEN 1 ELSE 2 END, u.name").fetchall()
    return render_template("admin/users.html", users=rows)


@app.post("/admin/users/<int:uid>/role")
@admin_required
def admin_set_role(uid):
    role = request.form.get("role", "")
    if role not in ROLES:
        abort(400, "Unknown role.")
    if uid == g.user["id"]:
        flash("You cannot change your own role.", "error")
        return redirect(url_for("admin_users"))
    db = get_db()
    user = db.execute("SELECT name FROM users WHERE id = ?", (uid,)).fetchone()
    if user is None:
        abort(404)
    db.execute("UPDATE users SET role = ? WHERE id = ?", (role, uid))
    db.commit()
    flash(f"{user['name']} is now {ROLES[role]}.", "success")
    return redirect(url_for("admin_users"))


@app.route("/admin/privileges")
@admin_required
def admin_privileges():
    counts = {r["role"]: r["n"] for r in get_db().execute("SELECT role, COUNT(*) AS n FROM users GROUP BY role")}
    return render_template("admin/privileges.html", permissions=PERMISSIONS, counts=counts)


@app.route("/admin/settings", methods=["GET", "POST"])
@admin_required
def admin_settings():
    errors = {}
    form = dict(get_settings())
    if request.method == "POST":
        form = {
            "company_name": request.form.get("company_name", "").strip(),
            "support_email": request.form.get("support_email", "").strip(),
            "allow_signup": "1" if request.form.get("allow_signup") else "0",
            "default_priority": request.form.get("default_priority", ""),
            "enabled_channels": ",".join(c for c in CHANNELS if c in request.form.getlist("channels")),
        }
        if not 2 <= len(form["company_name"]) <= 40:
            errors["company_name"] = "Use between 2 and 40 characters."
        if not EMAIL_RE.match(form["support_email"]):
            errors["support_email"] = "Enter a valid email address."
        if not form["default_priority"].isdigit() or int(form["default_priority"]) not in PRIORITIES:
            errors["default_priority"] = "Choose a priority."
        if not form["enabled_channels"]:
            errors["channels"] = "Keep at least one channel enabled."
        if not errors:
            db = get_db()
            for key, value in form.items():
                db.execute("INSERT INTO settings (key, value) VALUES (?, ?)"
                           " ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, value))
            db.commit()
            flash("Settings saved.", "success")
            return redirect(url_for("admin_settings"))
        form["channels"] = form["enabled_channels"].split(",")
    return render_template("admin/settings.html", errors=errors, form=form), (422 if errors else 200)


# ------------------------------------------------------------------ errors
@app.errorhandler(403)
def forbidden(_e):
    return render_template("error.html", code=403, title="Access denied",
                           message="You do not have access to this page."), 403


@app.errorhandler(404)
def not_found(_e):
    return render_template("error.html", code=404, title="Page not found",
                           message="The ticket or page you are looking for does not exist."), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template("error.html", code=400, title="We could not process that",
                           message=getattr(e, "description", "")), 400


init_db()

if __name__ == "__main__":
    app.run(debug=True)
