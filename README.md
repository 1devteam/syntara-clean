<div align="center">

<svg width="100%" height="180" viewBox="0 0 1200 180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="1200" height="180" fill="#020617"/>
  <rect width="1200" height="180" fill="url(#grid)">
    <animateTransform attributeName="transform" type="translate"
      from="0 0" to="40 40" dur="6s" repeatCount="indefinite"/>
  </rect>
  <text x="50%" y="55%" text-anchor="middle"
        font-size="48" fill="#e5e7eb" font-family="monospace">
    SYNTARA CLEAN
  </text>
  <text x="50%" y="75%" text-anchor="middle"
        font-size="18" fill="#94a3b8" font-family="monospace">
    Compliance-Aware Intelligence Runtime
  </text>
</svg>

</div>

---

## 🚀 Overview

**Syntara Clean** is a deterministic, explainable, compliance-aware intelligence system designed for CRM decisioning, policy enforcement, and multi-agent reasoning.

It combines:
- Explicit compliance rules
- Tenant-scoped policy enforcement
- Deterministic agent pipelines
- Full explainability for every decision

No black boxes. No hidden state.

---

## ✨ Core Capabilities

| Capability | Description |
|----------|-------------|
| 🧠 Agents | Lead qualification, deal risk, outreach |
| 🛡 Compliance | Risk, ethics, privacy rules |
| 🧾 Explainability | Every decision is traceable |
| 🏢 Tenancy | Per-tenant policy overrides |
| 🔌 CRM | Adapter-based CRM abstraction |
| ⚙️ Deterministic | Pure, testable execution paths |

---

## 📦 Installation

```bash
git clone https://github.com/1devteam/syntara-clean
cd syntara-clean
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

