# Lighthouse File Server

A small, token-protected Flask file server plus an MCP Streamable HTTP service for a personal Lighthouse content directory.

The server exposes a flat `content/` directory as readable and writable files. The MCP service exposes the same store through tools so an MCP client can list, read, and update content.

## What Is Included

- `app.py` - Flask HTTP API for file access
- `lighthouse_mcp.py` - MCP Streamable HTTP app
- `content_store.py` - shared file validation and storage helpers
- `*.service` - optional Ubuntu `systemd` units for running both services
- `content/.gitkeep` - placeholder for local content; real content is ignored by git

## Requirements

- Python 3.10+
- `pip`
- Linux with `systemd` if you want to use the included service files

## Local Setup

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdir -p content
export LIGHTHOUSE_BASE_DIR="$PWD"
export DASHBOARD_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
```

Run the Flask file server:

```sh
python app.py
```

Run the MCP server in another shell:

```sh
. .venv/bin/activate
export LIGHTHOUSE_BASE_DIR="$PWD"
uvicorn lighthouse_mcp:app --host 0.0.0.0 --port 5002
```

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

## Endpoints

Flask API:

- `GET /index` - returns a JSON index of files in `content/`
- `GET /files/<filename>` - reads a file
- `POST /files/<filename>` - writes a file

MCP endpoint:

```text
http://YOUR_HOST:5002/mcp
```

## Authentication

Flask requests require `DASHBOARD_TOKEN`.

Preferred header:

```http
Authorization: Bearer $DASHBOARD_TOKEN
```

Fallback query parameter:

```text
?token=$DASHBOARD_TOKEN
```

The MCP service does not enforce `DASHBOARD_TOKEN` itself. Run it only on a trusted network, behind a private tunnel, or behind an authenticating reverse proxy if it is reachable outside the host.

## Public-Sharing Notes

Runtime content under `content/`, Python caches, virtual environments, `.env` files, and macOS metadata are ignored by git. Do not commit real notes, tokens, or production environment files.
