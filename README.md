# Lighthouse

A personal AI knowledge infrastructure layer. Structured markdown files that an AI agent can read, write, and build on over time — so context compounds instead of evaporating between sessions.

The core insight: AI agents are only as good as the context they're grounded in. Most people give them none. Lighthouse is a persistent, human-readable knowledge store that lives alongside your agent and grows with it.

---

## What It Does

Lighthouse runs a lightweight server exposing a flat `content/` directory of markdown files. An AI agent (via MCP) can list, read, and update those files during a session. You can also read and edit them directly — they're just text.

Over time the directory becomes a structured external memory: preferences, decisions, ongoing projects, domain knowledge, anything the agent should carry forward. The agent reads what it needs, updates what changed, and the context is there next time without you having to re-explain it.

This is the personal, single-user version. One server, one content directory, one agent with persistent context.

---

## Why It Works

Standard AI sessions are stateless. You rebuild context every time, or you paste in notes, or you just accept that the agent doesn't know what it should. Lighthouse makes context durable without requiring a database, a vector store, or a retrieval pipeline. Markdown files are readable by humans and machines. They version cleanly in git. They're editable in any text editor. The simplicity is load-bearing.

---

## Contents

| File | Purpose |
|---|---|
| `app.py` | Flask HTTP API for file access |
| `lighthouse_mcp.py` | MCP Streamable HTTP server |
| `content_store.py` | Shared file validation and storage helpers |
| `*.service` | systemd units for running both services on Ubuntu |
| `content/.gitkeep` | Placeholder — real content is gitignored |

---

## Quickstart

**Requirements:** Python 3.10+, Linux with systemd (optional but recommended for always-on use)

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdir -p content
export LIGHTHOUSE_BASE_DIR="$PWD"
export DASHBOARD_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
```

Run the file server:

```sh
python app.py
```

Run the MCP server (separate shell):

```sh
. .venv/bin/activate
export LIGHTHOUSE_BASE_DIR="$PWD"
uvicorn lighthouse_mcp:app --host 0.0.0.0 --port 5002
```

---

## API

**Flask endpoints** (require `Authorization: Bearer $DASHBOARD_TOKEN`):

```
GET  /index              List all files in content/
GET  /files/<filename>   Read a file
POST /files/<filename>   Write a file
```

**MCP endpoint:**

```
http://YOUR_HOST:5002/mcp
```

The MCP service does not enforce token auth itself. Run it on a trusted network or behind an authenticating reverse proxy if exposed externally.

---

## Ubuntu Systemd Install (Always-On)

```sh
sudo mkdir -p /opt/dashboard-file-server /home/ubuntu/lighthouse/content
sudo cp app.py content_store.py lighthouse_mcp.py requirements.txt /opt/dashboard-file-server/
sudo python3 -m venv /opt/dashboard-file-server/.venv
sudo /opt/dashboard-file-server/.venv/bin/pip install -r /opt/dashboard-file-server/requirements.txt
echo "DASHBOARD_TOKEN=$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')" | sudo tee /etc/dashboard-file-server.env
sudo cp dashboard-file-server.service lighthouse-mcp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now dashboard-file-server lighthouse-mcp
```

---

## Notes

- Content files, `.env` files, virtual environments, and Python caches are gitignored by default
- Do not commit real notes, tokens, or production credentials
- The content directory is intentionally flat — simplicity over hierarchy
