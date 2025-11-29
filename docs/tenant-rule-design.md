# Tenant-Based Rule Enable/Disable (Design Only)

Status: DESIGN ONLY — no implementation yet.  
Goal: Allow tenants to opt in/out of Risk, Ethics, Privacy rules in a
controlled, test-driven way.

---

## 1. Problem

We already support per-tenant risk thresholds via `TenantPolicy.risk_threshold`
and `apply_tenant_policy_to_context(ctx)`. All rules (Risk, Ethics, Privacy)
are still enabled for all tenants.

We want:

- Some tenants to **disable** specific rules:
  - Example: a pilot tenant that only uses risk checks, not ethics or privacy.
- Other tenants to **enable** all rules:
  - Example: compliance-heavy customers.

We must:

- Avoid pushing tenancy logic into core rule code (`RiskRule`, `EthicsRule`, etc.).
- Avoid changing behavior for tenants that do not define enable flags.
- Keep behavior stable and covered by tests.

---

## 2. Design Options (High Level)

### Option A — Rule Checks Inside Rules (REJECTED)

Each rule queries `TenantPolicyStore` and checks `enable_*` flags:

```python
if not TenantPolicyStore.get(ctx.get("tenant_id")).enable_risk:
    return ComplianceResult.allow(...)

