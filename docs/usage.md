# Syntara Usage Guide

This repo is a small, stability-first core for Syntara:
- strict `src/` layout
- decision + compliance + explainability engines
- Dummy CRM + agents
- CLI + FastAPI entrypoints
- multi-tenant risk thresholds (opt-in)

This document shows how to run it locally.

---

## 1. Setup

### 1.1 Clone + venv

```bash
git clone git@github.com:1devteam/syntara-clean.git
cd syntara-clean

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -U pip wheel setuptools
pip install -e ".[dev]"

