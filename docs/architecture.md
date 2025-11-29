# Syntara Architecture Overview

## 1. Goals

- Compliance-first decision engine for CRM / sales / outreach.
- Modular, pluggable rules (risk, ethics, privacy).
- Clean separation of concerns (core engine vs. adapters vs. API/CLI).
- Strong typing (mypy), consistent styling (ruff, black).
- Easy to extend with new domains (finance, health, security) and tenants.

Python version: **3.12**  
Layout: **strict src/** package (`src/syntara`).

---

## 2. High-Level Layers

```text
CLI / API (FastAPI)
        |
        v
   Decision Engine
        |
        v
   Agents Layer
        |
        v
    CRM Layer
        |
        v
 Compliance Engine  -> Explainability Engine (trace)


