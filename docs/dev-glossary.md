# Developer Glossary

Shared vocabulary for the Syntara codebase. Stability-first: these terms are
used consistently across code, tests, and docs.

---

## Engine

**DecisionEngine** (`syntara.core.decision_engine`)

- Orchestrates handlers (agents, workflows).
- Input:
  - `signal: str` — what we are trying to do (e.g. `"qualify_lead"`, `"draft_outreach_email"`).
  - `context: Dict[str, Any]` — all the data needed for the decision.
- Output:
  - `Decision` dataclass:
    - `action: str`
    - `payload: Dict[str, Any]`
    - `compliance` (result from ComplianceEngine)
    - `explanation` (list of ExplanationStep)

**ComplianceEngine** (`syntara.core.compliance_engine`)

- Runs a pipeline of compliance rules against the context.
- Uses `ComplianceRegistry` to know which rules to run.
- Returns `ComplianceEvaluation` (allowed, reason, traces).

**ExplainabilityEngine** (`syntara.core.explainability`)

- Records a sequence of `ExplanationStep` events describing what happened.
- Used by DecisionEngine to trace:
  - missing handlers,
  - compliance evaluations,
  - blocked decisions,
  - successful executions.

---

## Agent

**Agents** (`syntara.agents.*`)

- Encapsulate domain logic like:
  - lead qualification,
  - deal risk,
  - outreach email drafting.
- Typically:
  - Take a context dict,
  - Call CRM adapters or other services,
  - Return structured payloads (scores, decisions, content).

**BaseAgent**

- Common interface / base class for agents.
- Makes it easier to:
  - register agents,
  - unit-test behaviors,
  - swap implementations later.

---

## Adapter

**CRM Adapter** (`syntara.crm.adapter`)

- Boundary between Syntara and external CRMs.
- Provides methods like:
  - `get_lead(lead_id)`,
  - `get_opportunity(opportunity_id)`,
  - `update_lead(...)`, etc.
- Implementation example:
  - `DummyCRM` in `syntara.crm.dummy_provider`.

Key rule:
- Core engines do NOT import CRM.
- CRM adapters + agents use the core, not the other way around.

---

## Rule, Registry, and Result

**Rule** (`ComplianceRule`)

- A single compliance check.
- Implements:
  - `check(context: Dict[str, Any]) -> ComplianceResult`
- Examples:
  - `RiskRule` — risk score threshold.
  - `EthicsRule` — ethical review / approval.
  - `PrivacyRule` — consent for user-related data.

**ComplianceRegistry**

- Global registry of rule classes.
- `register(rule_cls)` — add a rule.
- `get_rules()` — list all rules.
- `clear()` — reset registry (used in tests).

**ComplianceResult**

- The result of a single rule:
  - `allowed: bool`
  - `reason: str` (code, not a sentence; e.g. `"privacy_consent_missing"`)
  - `rule: str` (rule name).

**ComplianceEvaluation**

- Aggregated result from ComplianceEngine:
  - `allowed: bool` — overall decision.
  - `reason: str` — first blocking reason or empty if allowed.
  - `traces: List[ComplianceTrace]` — per-rule results.

---

## Tenancy

**Tenant ID**

- A string that identifies a customer / workspace / environment.
- Provided:
  - via HTTP header `X-Tenant-ID` in the API,
  - via CLI flag `--tenant-id` in demo commands.
- Propagated into the decision context as `context["tenant_id"]`.

**TenantPolicy** (`syntara.tenancy.policy`)

- Immutable config for one tenant:
  - `tenant_id: Optional[str]`
  - `risk_threshold: Optional[float]`
  - `enable_risk: Optional[bool]`
  - `enable_ethics: Optional[bool]`
  - `enable_privacy: Optional[bool]`
- Defaults to `None` for all fields; meaning “use global behavior”.

**TenantPolicyStore**

- In-memory store for tenant policies:
  - `set_default(policy)`
  - `set_override(tenant_id, policy)`
  - `clear_overrides()`
  - `get(tenant_id) -> TenantPolicy`
- Used by `apply_tenant_policy_to_context(ctx)` to derive effective context.

**apply_tenant_policy_to_context**

- Function in `syntara.tenancy.integration`.
- Given a context (with optional `tenant_id`), returns a new context where:
  - `risk_threshold` may be injected from tenant policy if not already present.
- Core rules (e.g., RiskRule) are unchanged; they just read context.

---

## Explainability Events

Event names used in `ExplanationStep.event`:

- `no_handler` — no handler registered for the signal.
- `compliance_eval` — result from compliance engine.
- `blocked` — decision blocked by compliance.
- `executed` — decision allowed and considered executed.

These are treated as a stable contract and are now covered by tests in
`tests/test_explainability_trace.py`.

---

## Context

**Context dict**

- Central concept: `Dict[str, Any]` passed into DecisionEngine and rules.
- Contains:
  - domain fields (lead_id, risk_score, template_type, etc.),
  - governance fields (ethical_approval, user_consent, risk_threshold),
  - cross-cutting fields (tenant_id).
- Engines do not make assumptions about the presence of a particular key
  beyond what is validated in tests and documented in docs.

