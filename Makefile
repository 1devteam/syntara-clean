PY=python3
VENV=.venv

.PHONY: setup install test lint lint-fix fmt typecheck clean

setup: $(VENV)/bin/activate install
	@echo "✅ setup complete"

$(VENV)/bin/activate:
	@test -d $(VENV) || $(PY) -m venv $(VENV)
	@. $(VENV)/bin/activate; python -m pip install -U pip wheel setuptools

install:
	@. $(VENV)/bin/activate; pip install -e ".[dev]"

test:
	@. $(VENV)/bin/activate; pytest

lint:
	@. $(VENV)/bin/activate; ruff check . && black --check . && mypy --config-file mypy.ini .

lint-fix:
	@. $(VENV)/bin/activate; ruff check --fix . && ruff format . && black .

fmt:
	@. $(VENV)/bin/activate; ruff format . && black .

typecheck:
	@. $(VENV)/bin/activate; mypy --config-file mypy.ini .

clean:
	@rm -rf $(VENV) dist build .pytest_cache .ruff_cache .mypy_cache **/__pycache__
