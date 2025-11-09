#!/bin/bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/app/src"
export PYTHONPATH="$PYTHONPATH:$SRC_DIR"

source "$ROOT_DIR/.venv/bin/activate"
echo "Starting JupyterLab..."
jupyter lab --notebook-dir="$ROOT_DIR/notebook_dir" --ip=0.0.0.0 --port=8888 --no-browser
#
