#!/usr/bin/env bash
set -euo pipefail
PY=${PYTHON:-python3}
${PY} -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
pip install -r requirements-dev.txt 2>/dev/null || true
pytest -q || true
