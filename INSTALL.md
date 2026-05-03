# Installation guide (Cursor + PyMOL MCP)

Follow **either** the short path or the detailed sections below.

See also **`flow.svg`** in the repo root (animated SVG): **You → Cursor → MCP server → tools → PyMOL (XML-RPC :9123)** — same idea as [upstream](https://github.com/nagarh/pymol-claude-code/blob/main/flow.svg), styled for Cursor.

## 1. Prerequisites

| Component | Notes |
|-----------|--------|
| **Python** | 3.10+ |
| **PyMOL** | Use **conda-forge** `pymol-open-source` (recommended). Pip-only PyMOL on conda **base** often misses native libs (`GLEW`, `NetCDF`, …). |
| **Cursor** | Current Cursor Desktop with MCP support. |

## 2. Clone this repository

```bash
git clone https://github.com/truong128/pymol-cursor-mcp.git
cd pymol-cursor-mcp
```

## 3. Create the MCP server virtual environment (repo root)

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
deactivate
```

**Windows (cmd)**

```cmd
py -3 -m venv venv
venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
deactivate
```

This `venv` is **only** for the MCP server (`mcp` package + `pymol_mcp_server.py`). It is **not** the same as your PyMOL installation.

## 4. PyMOL with XML‑RPC (required)

The MCP server talks to PyMOL over **XML‑RPC** (default **port 9123**).

**Recommended:** dedicated conda environment with PyMOL from **conda-forge**:

```bash
mamba create -y -n pymol_mcp -c conda-forge python=3.11 pymol-open-source glew libnetcdf netcdf4
conda activate pymol_mcp
pymol -R
```

Leave PyMOL running. The `-R` flag enables the RPC server.

**Helper script** (macOS/Linux; uses `PYMOL_BIN` or common conda paths):

```bash
chmod +x scripts/start_pymol_for_mcp.sh
./scripts/start_pymol_for_mcp.sh
```

## 5. Cursor: open this folder as the workspace

In Cursor: **File → Open Folder** → select the **`pymol-cursor-mcp`** directory (the repo root that contains `pymol_mcp_server.py` and `.cursor/mcp.json`).

## 6. MCP configuration

This repo ships **`.cursor/mcp.json`** using `${workspaceFolder}`:

- **macOS / Linux:** `venv/bin/python` + `pymol_mcp_server.py`
- **Windows:** copy `.cursor/mcp.json.windows.example` to `.cursor/mcp.json` (adjust if your paths differ), or edit `command` to `venv\\Scripts\\python.exe`.

Optional **global** MCP (all projects): merge the same `pymol` entry into `~/.cursor/mcp.json` using **absolute paths** to this clone.

Restart Cursor after changing MCP config.

### Non‑default RPC URL

If PyMOL listens elsewhere, add to the `pymol` server in `mcp.json`:

```json
"env": {
  "PYMOL_RPC_URL": "http://localhost:<PORT>"
}
```

Match SSH tunnels / HPC setups accordingly.

## 7. Verify

With PyMOL running (`pymol -R`):

```bash
python3 verify_stack.py
```

Expect: `OK: MCP import + PyMOL RPC at http://localhost:9123`

## 8. Optional: fewer MCP approval prompts

Enable Agent **auto-run** in Cursor settings. Optionally use `~/.cursor/permissions.json`:

```json
{
  "mcpAllowlist": ["pymol:*"]
}
```

See [Cursor permissions](https://cursor.com/docs/reference/permissions). Adding only `pymol:*` **replaces** the in-app MCP allowlist for that list — add other `server:*` entries if you need them.

## 9. Troubleshooting

| Problem | What to try |
|---------|-------------|
| MCP server failed | **Output → MCP / MCP Logs** in Cursor. Confirm `venv` exists and `pip install -r requirements.txt` succeeded. |
| XML-RPC errors | PyMOL must be running with **`-R`**. Check port: `lsof -i :9123` (macOS/Linux). |
| Wrong Python in MCP | Open the **repo root** as workspace so `${workspaceFolder}` resolves correctly. |
| PyMOL import errors (GLEW, NetCDF, …) | Install PyMOL from **conda-forge** into a clean env; avoid broken pip PyMOL on conda base. |

## 10. Usage in Cursor

1. Start PyMOL with RPC (`pymol -R` or the helper script).  
2. Open Chat or **Agent** in this workspace.  
3. Prompt in natural language, e.g. “Fetch 1hho, cartoon, color by secondary structure.”

Tools exposed: `run_command`, `run_python`, `pymol_get`.

---

## Claude Code (optional)

If you use Anthropic’s CLI instead of Cursor:

```bash
claude mcp add pymol "$(pwd)/venv/bin/python" "$(pwd)/pymol_mcp_server.py"
```

(`claude mcp list` should show `pymol` connected.)
