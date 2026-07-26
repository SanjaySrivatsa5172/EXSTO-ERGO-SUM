#!/usr/bin/env bash
# Set up a Python environment with cnsplots for publication-ready scientific plots.
#
# Usage:
#   bash setup_env.sh [VENV_DIR]
#
# Creates (or reuses) a virtualenv at VENV_DIR (default: .venv-cnsplots in the
# current directory) and installs cnsplots into it. cnsplots pulls in matplotlib,
# seaborn, pandas, scanpy, lifelines and gseapy, so the first install takes a
# minute or two. On success it prints the path to the venv's python interpreter —
# use that interpreter to run make_figure.py / gallery_demo.py.
set -euo pipefail

VENV_DIR="${1:-.venv-cnsplots}"

# Prefer python3.10+ (cnsplots requires >=3.10).
PY="python3"
if ! "$PY" -c 'import sys; assert sys.version_info[:2] >= (3, 10)' 2>/dev/null; then
  echo "ERROR: python3 >= 3.10 is required for cnsplots (found: $("$PY" --version 2>&1))." >&2
  echo "Install a newer Python or point PATH at one, then re-run." >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo ">> Creating virtualenv at $VENV_DIR"
  "$PY" -m venv "$VENV_DIR"
fi

VENV_PY="$VENV_DIR/bin/python"
echo ">> Upgrading pip"
"$VENV_PY" -m pip install --quiet --upgrade pip

if "$VENV_PY" -c 'import cnsplots' 2>/dev/null; then
  echo ">> cnsplots already installed ($("$VENV_PY" -c 'import cnsplots; print(cnsplots.__version__)'))"
else
  echo ">> Installing cnsplots (this can take 1-2 minutes)"
  "$VENV_PY" -m pip install cnsplots
fi

echo ""
echo ">> Ready. Use this interpreter:"
echo "   $(cd "$(dirname "$VENV_PY")" && pwd)/$(basename "$VENV_PY")"
echo ""
echo ">> Example:"
echo "   $VENV_PY scripts/make_figure.py --self-test --out /tmp/cns_selftest.png"
