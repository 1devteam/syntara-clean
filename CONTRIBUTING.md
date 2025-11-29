# Contributing to Syntara

## Setup
1. `make setup` (creates venv, installs dev deps)
2. `pre-commit install` (enforce formatting/lint on commit)

## Workflow
- Branch from `main`, use feature branches: `feat/...`, `fix/...`, `chore/...`.
- Ensure `make lint` and `make test` pass before pushing.

## Commit style
- Conventional commits preferred: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`.

## PR checklist
- [ ] CI green (lint, format-check, mypy, tests)
- [ ] Added/updated tests
- [ ] Updated docs if needed
