# Syntara Refactor Roadmap (Stability-First)

This roadmap captures the next refactors with one rule: **stability before speed**.
Every change must keep tests green and be backed by new tests where behavior changes.

---

## Milestone 1 — Tenant Policy Integration (Risk Only, Fully Tested)

**Goal:** Use `TenantPolicyStore` to override risk thresholds per tenant without breaking current behavior.

**Steps:**

1. Add tests:
   - `tests/test_tenant_policy_risk_threshold.py`
     - default tenant uses existing `max_risk_score`.
     - a specific tenant (e.g. `"bank-x"`) uses a lower threshold.
2. Implement a small helper, e.g. `apply_tenant_policy(ctx)`, that:
   - reads `tenant_id` from `ctx`.
   - fetches policy via `TenantPolicyStore.get(tenant_id)`.
   - injects `ctx["risk_threshold"]` when policy defines one.
3. Call this helper in the composition layer (API/CLI/runtime), **not** inside core engines.
4. Keep all existing tests unchanged; add new ones for the tenant-specific behavior.

**Non-goals (for this milestone):**

- No rule enable/disable yet.
- No DB-backed policies; still in-memory.

---

## Milestone 2 — Rule Enable/Disable per Tenant (Feature Flags for Risk/Ethics/Privacy)

**Goal:** Allow tenants to opt in/out of specific rules (e.g. ethics checks) in a controlled way.

**Steps:**

1. Add tests:
   - A tenant where `enable_ethics=False`:
     - Ethics rule is not registered / not evaluated.
     - Other rules still apply.
   - A tenant where `enable_privacy=False`:
     - Privacy rule is skipped; document risk clearly.
2. Implement a rule-selection function that:
   - reads `TenantPolicy`,
   - decides which rule classes to register in `ComplianceRegistry`.
3. Wire rule selection into the place where we currently auto-register default rules.
4. Ensure default behavior (no tenant policy) keeps **all three rules enabled**.

**Non-goals:**

- No dynamic runtime reconfiguration yet (policies set at startup or test setup).

---

## Milestone 3 — Observability & Explainability Hardening

**Goal:** Make decisions easier to debug and audit without changing outcomes.

**Steps:**

1. Standardize `ExplainabilityEngine` events:
   - document event names and fields (e.g. `compliance_eval`, `blocked`, `executed`, `no_handler`).
2. Add unit tests that assert:
   - when a request is blocked by a rule, there is a matching explanation step.
   - when no handler exists, explanation clearly states that.
3. Introduce structured logging (logger adapter) that can emit:
   - tenant_id,
   - action,
   - rule that blocked (if any),
   - reason code.

**Non-goals:**

- No external log backend; just ensure logs exist and are testable.

---

## Milestone 4 — API & CLI Contract Hardening

**Goal:** Treat the API/CLI as stable contracts with clear error handling and schema.

**Steps:**

1. Tighten Pydantic models (e.g., enums for template types are already in place; document them).
2. Add tests:
   - invalid inputs (missing required fields, bad types) return clean 4xx responses.
   - CLI returns non-zero exit codes on failure, with reason printed once.
3. Document public API/CLI usage in `docs/usage.md`.
4. Ensure `tenant_id` handling is documented and consistent (header vs. flag).

**Non-goals:**

- No versioned API yet; focus is on correctness and clarity of the current one.

---

## Milestone 5 — Package, CI, and Release Discipline

**Goal:** Make it safe to evolve the codebase over time with automation backing it.

**Steps:**

1. Confirm:
   - `make lint`, `make test`, `make typecheck` all run locally and in CI.
2. Add CI rules:
   - pre-merge: `lint + typecheck + tests` must pass.
   - optional: require coverage above a minimal threshold for new code paths.
3. Define a simple versioning policy in `pyproject.toml` and `CHANGELOG`:
   - e.g. `0.x.y` while under heavy development.
4. Add `docs/release-process.md`:
   - how to cut a new version,
   - how to run smoke tests.

**Non-goals:**

- No heavy release machinery (no packages to PyPI yet) unless needed.

---

## General Principles (Apply to All Milestones)

- Add tests **before** or together with behavior changes.
- Keep core (`syntara.core.*`) independent of CRM, tenancy, and transports.
- Prefer small helpers and composition layers over pushing logic into engines.
- Any new behavior must have:
  - unit tests,
  - minimal docs update (architecture / tenancy / usage).

