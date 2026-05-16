from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from content_store import build_index_json, clean_name, read_file, write_file

mcp = FastMCP(
    "lighthouse",
    host="0.0.0.0",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False)
)


@mcp.tool()
def get_index() -> str:
    return build_index_json()


@mcp.tool()
def get_file(filename: str) -> str:
    return read_file(filename)


@mcp.tool()
def update_file(filename: str, content: str) -> str:
    filename = clean_name(filename)
    write_file(filename, content.encode("utf-8"))
    return "ok"


app = mcp.streamable_http_app()
