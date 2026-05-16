import hmac
import os
from pathlib import Path

from flask import Flask, Response, abort, request, send_from_directory
from flask_cors import CORS

from content_store import CONTENT_DIR, build_index_json, clean_name, write_file

TOKEN_ENV = "DASHBOARD_TOKEN"
app = Flask(__name__)
CORS(app)

@app.before_request
def require_token():
    if request.method == "OPTIONS":
        return None

    token = os.environ.get(TOKEN_ENV, "")
    header = request.headers.get("Authorization", "")
    prefix = "Bearer "
    supplied = request.args.get("token", "")

    if header.startswith(prefix):
        supplied = header[len(prefix) :]
    if not token or not supplied:
        abort(401)

    if not hmac.compare_digest(supplied, token):
        abort(401)

def request_file(filename):
    try:
        return clean_name(filename)
    except ValueError:
        abort(404)

@app.get("/index")
def index():
    return Response(build_index_json(), mimetype="application/json")

@app.get("/files/<filename>")
def get_file(filename):
    filename = request_file(filename)
    mimetype = {
        ".json": "application/json",
        ".md": "text/markdown",
        ".markdown": "text/markdown",
    }.get(Path(filename).suffix, "text/plain")
    return send_from_directory(CONTENT_DIR, filename, mimetype=mimetype)

@app.post("/files/<filename>")
def put_file(filename):
    filename = request_file(filename)
    write_file(filename, request.get_data())
    return Response(status=204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
