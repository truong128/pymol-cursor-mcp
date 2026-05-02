#!/usr/bin/env python3
"""Exit 0 if venv + pymol_mcp_server import + PyMOL XML-RPC work."""
import os
import subprocess
import sys
import xmlrpc.client

REPO = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.join(REPO, "venv", "bin", "python")
if sys.platform == "win32":
    VENV_PY = os.path.join(REPO, "venv", "Scripts", "python.exe")
RPC = os.environ.get("PYMOL_RPC_URL", "http://localhost:9123")


def main() -> int:
    if not os.path.isfile(VENV_PY):
        print("FAIL: venv python not found. Create venv in repo root:\n  python3 -m venv venv && ./venv/bin/pip install -r requirements.txt", file=sys.stderr)
        return 1
    r = subprocess.run(
        [VENV_PY, "-c", "import mcp; import pymol_mcp_server"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print("FAIL: MCP server import\n", r.stderr or r.stdout, file=sys.stderr)
        return 1
    try:
        p = xmlrpc.client.ServerProxy(RPC, allow_none=True)
        p.get_names()
    except Exception as e:
        print("FAIL: XML-RPC", RPC, "-", e, file=sys.stderr)
        print("Start PyMOL with XML-RPC (see README): pymol -R", file=sys.stderr)
        return 1
    print("OK: MCP import + PyMOL RPC at", RPC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
