"""
PyMOL MCP server (stdio) — exposes PyMOL XML-RPC as MCP tools for Cursor / Claude Code.

Upstream concept: https://github.com/nagarh/pymol-claude-code
Environment: set PYMOL_RPC_URL if PyMOL listens somewhere other than http://localhost:9123
"""
import os
import xmlrpc.client
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PyMOL")
_pymol_rpc_url = os.environ.get("PYMOL_RPC_URL", "http://localhost:9123")
pymol = xmlrpc.client.ServerProxy(_pymol_rpc_url)


@mcp.tool()
def run_command(command: str) -> str:
    """Run a single PyMOL command."""
    pymol.do(command)
    return "OK"


@mcp.tool()
def run_python(code: str) -> str:
    """Execute Python code inside PyMOL. Returns OK or ERROR: <message> directly."""
    import os as _os

    error_file = "/tmp/pymol_error.txt"
    if _os.path.exists(error_file):
        _os.remove(error_file)
    wrapped = f"""try:
{chr(10).join('    ' + line for line in code.strip().splitlines())}
except Exception as e:
    open('{error_file}', 'w').write('ERROR: ' + str(e))
"""
    pymol.do(f"python\n{wrapped}\npython end")
    try:
        with open(error_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "OK"


@mcp.tool()
def pymol_get(method: str, args: list = []) -> str:
    """Call any PyMOL XML-RPC method and return the result."""
    try:
        result = getattr(pymol, method)(*args)
        return str(result)
    except Exception as e:
        return f"ERROR: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
