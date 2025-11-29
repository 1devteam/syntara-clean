# Syntara Starter (WSL-safe)
![Coverage](coverage-badges/coverage.svg)


## Quickstart
```bash
cd ~/syntara
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements-dev.txt 2>/dev/null || true
pytest -q
```

Install in editable mode with dev extras:

```bash
pip install -e ".[dev]"

# syntara
