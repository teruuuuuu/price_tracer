#!/bin/bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/app/src"
export LOG_DIR="$ROOT_DIR/logs"
export PYTHONPATH="$PYTHONPATH:$SRC_DIR"

source "$ROOT_DIR/.venv/bin/activate"
echo "Starting FastAPI application..."
uvicorn app.src.main:app --reload
