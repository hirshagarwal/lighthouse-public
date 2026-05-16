import json
import os
from pathlib import Path

BASE_DIR = Path(os.environ.get("LIGHTHOUSE_BASE_DIR", "/home/ubuntu/lighthouse"))
CONTENT_DIR = BASE_DIR / "content"
INDEX_FILENAME = "index.json"


def clean_name(filename: str) -> str:
    if filename != os.path.basename(filename) or filename in {".", "..", INDEX_FILENAME}:
        raise ValueError("invalid filename")
    return filename


def content_path(filename: str) -> Path:
    return CONTENT_DIR / clean_name(filename)


def read_file(filename: str) -> str:
    return content_path(filename).read_text(encoding="utf-8")


def write_file(filename: str, content: bytes) -> None:
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    content_path(filename).write_bytes(content)


def build_index() -> dict[str, list[str]]:
    if not CONTENT_DIR.exists():
        return {"files": []}

    files = [
        path.name
        for path in CONTENT_DIR.iterdir()
        if path.is_file() and not path.name.startswith(".")
    ]
    return {"files": sorted(files)}


def build_index_json() -> str:
    return json.dumps(build_index(), indent=2) + "\n"
