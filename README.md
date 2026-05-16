# Lighthouse

Personal AI knowledge infrastructure. A flat directory of markdown files exposed over HTTP and MCP so an AI agent can read and write persistent context across sessions.

Context compounds over time. The agent reads what's relevant, updates what changed, and it's there next session without re-explaining. Files are plain markdown — readable and editable directly.

---

## Contents

| File | Purpose |
|---|---|
| `app.py` | Flask HTTP API |
| `lighthouse_mcp.py` | MCP Streamable HTTP server |
| `content_store.py` | File validation and storage helpers |
| `*.service` | systemd units for Ubuntu |
| `content/.gitkeep` | Placeholder — real content is gitignored |

---

## Quickstart

**Requirements:** Python 3.10+

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

```
GET  /index              List all files in content/
GET  /files/<filename>   Read a file
POST /files/<filename>   Write a file
```

---

## Auth and Deployment

The Flask API uses bearer token auth on every request:

```http
Authorization: Bearer $DASHBOARD_TOKEN
```

Or via query param:

```
?token=$DASHBOARD_TOKEN
```

The MCP server has no built-in auth. It should not be exposed directly. Put it behind NGINX with basic auth or mutual TLS if accessible outside localhost:

```nginx
location /mcp {
    auth_basic "Lighthouse";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://127.0.0.1:5002;
}
```

---

## Ubuntu Systemd Install

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

- `content/`, `.env`, virtualenvs, and Python caches are gitignored
- Content directory is intentionally flat
- Do not commit tokens or credentials
