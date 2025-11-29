# Observability & Explainability

This document describes how Syntara records decision traces without changing
core decision logic.

## 1. ExplainabilityEngine Events

The explainability layer records a list of `ExplanationStep` values:

```python
@dataclass
class ExplanationStep:
    event: str       # event kind
    details: Dict[str, Any]  # event payload

