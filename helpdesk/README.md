# Helpdesk

Ticket-based customer support app built with Flask and SQLite. It has two interfaces on one database:

- **Agent backend** (`/helpdesk`): Kanban board by stage (drag cards to change stage), list view, filters, ticket form with conversation and internal notes.
- **Customer portal** (`/my/tickets`): open tickets, choose who they are assigned to, follow the conversation.
- **Admin** (`/admin`): users and roles, privileges matrix, settings.

On first start the database is filled with demo data (fake users, teams and about 45 tickets).

## Run locally

```powershell
cd helpdesk
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask --app app run
```

Open http://127.0.0.1:5000.

## Demo accounts

| Role | Email | Password |
|---|---|---|
| Admin (also a customer) | danna@nullzone.ai | 1234ABCD |
| Agent | danna@reimbursor.info | ASDFGHJK |

The other demo users are listed, with their fake passwords, under Admin > Users & passwords. These are demo credentials only.

## Deploy

`render.yaml` in the repository root deploys the app to Render (free plan). The free plan has an ephemeral disk, so the database is rebuilt with the demo data after each restart.
