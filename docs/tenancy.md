# Tenancy Model (Current + Planned)

## 1. Current State

### 1.1 Tenant Identifier

- API:
  - An optional HTTP header `X-Tenant-ID` is accepted by the FastAPI endpoints.
  - If present, it is attached to the decision context as `context["tenant_id"]`.
- CLI:
  - Each demo command accepts an optional `--tenant-id`.
  - If present, it is attached to the decision context as `context["tenant_id"]`.

### 1.2 Core Engines

- `DecisionEngine`:
  - Accepts `context: Dict[str, Any]`.
  - Does not inspect or branch on `tenant_id` directly.
- `ComplianceEngine` + `ComplianceRegistry`:
  - Use the same rules (Risk, Ethics, Privacy) for all tenants.
  - Risk thresholds can now be influenced through tenant policy, but the rule
    code itself is unchanged.

---

## 2. TenantPolicy and TenantPolicyStore

**Location:**

- `src/syntara/tenancy/policy.py`
- `src/syntara/tenancy/integration.py`

### 2.1 TenantPolicy

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class TenantPolicy:
    tenant_id: Optional[str] = None
    risk_threshold: Optional[float] = None
    enable_risk: Optional[bool] = None
    enable_ethics: Optional[bool] = None
    enable_privacy: Optional[bool] = None

