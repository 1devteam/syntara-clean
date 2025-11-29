from __future__ import annotations

from typing import Any, Dict

from syntara.tenancy.policy import TenantPolicyStore


def apply_tenant_policy_to_context(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new context with tenant policy applied.

    Currently:
    - If a TenantPolicy exists for the given tenant_id and defines
      risk_threshold, and the context does *not* already specify
      risk_threshold, we inject it into the context.
    - Otherwise, the context is returned unchanged.

    This keeps behavior for tenants without explicit policy identical
    to the current global behavior.
    """
    new_ctx: Dict[str, Any] = dict(ctx)

    tenant_id = new_ctx.get("tenant_id")
    policy = TenantPolicyStore.get(tenant_id)

    if policy.risk_threshold is not None and "risk_threshold" not in new_ctx:
        new_ctx["risk_threshold"] = policy.risk_threshold

    return new_ctx
