#!/usr/bin/env bash
# Start PyMOL with XML-RPC (default port 9123) for MCP clients.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

: "${PYMOL_BIN:=}"

if [[ -z "${PYMOL_BIN}" ]]; then
  if [[ -x "${HOME}/anaconda3/envs/pymol_mcp/bin/pymol" ]]; then
    PYMOL_BIN="${HOME}/anaconda3/envs/pymol_mcp/bin/pymol"
  elif [[ -x "${HOME}/miniconda3/envs/pymol_mcp/bin/pymol" ]]; then
    PYMOL_BIN="${HOME}/miniconda3/envs/pymol_mcp/bin/pymol"
  elif command -v pymol >/dev/null 2>&1; then
    PYMOL_BIN="$(command -v pymol)"
  fi
fi

if [[ -z "${PYMOL_BIN}" || ! -x "${PYMOL_BIN}" ]]; then
  echo "PyMOL executable not found." >&2
  echo "Install conda-forge PyMOL (recommended), e.g.:" >&2
  echo "  mamba create -y -n pymol_mcp -c conda-forge python=3.11 pymol-open-source glew libnetcdf netcdf4" >&2
  echo "Then: conda activate pymol_mcp" >&2
  echo "Or set: export PYMOL_BIN=/full/path/to/pymol" >&2
  exit 1
fi

echo "Using PyMOL: ${PYMOL_BIN}" >&2
echo "Repo (for reference): ${REPO_ROOT}" >&2
exec "${PYMOL_BIN}" -R "$@"
