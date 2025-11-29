from __future__ import annotations

from typing import Dict

from syntara.core.compliance_engine import ComplianceEngine, ComplianceRegistry
from syntara.tenancy.integration import apply_tenant_policy_to_context
from syntara.tenancy.policy import TenantPolicy, TenantPolicyStore


def test_apply_tenant_policy_default_does_not_change_context() -> None:
    # Ensure clean state
    TenantPolicyStore.set_default(TenantPolicy())
    TenantPolicyStore.clear_overrides()

    ctx: Dict[str, object] = {"risk_score": 0.20}
    new_ctx = apply_tenant_policy_to_context(ctx)

    # No tenant_id + no policy -> context should be unchanged
    assert new_ctx == ctx


def test_tenant_policy_risk_threshold_override_affects_compliance() -> None:
    # Reset policy store and registry
    TenantPolicyStore.set_default(TenantPolicy())
    TenantPolicyStore.clear_overrides()
    ComplianceRegistry.clear()

    # Default tenant — no override
    base_ctx: Dict[str, object] = {"risk_score": 0.20}
    default_ctx = apply_tenant_policy_to_context(base_ctx)

    engine_default = ComplianceEngine()
    result_default = engine_default.evaluate("proceed", default_ctx)

    # For the default tenant, this risk score should be allowed
    assert result_default.allowed is True

    # Strict tenant — override with a lower threshold
    TenantPolicyStore.set_override("strict", TenantPolicy(risk_threshold=0.10))

    strict_ctx = apply_tenant_policy_to_context(
        {"risk_score": 0.20, "tenant_id": "strict"}
    )

    ComplianceRegistry.clear()
    engine_strict = ComplianceEngine()
    result_strict = engine_strict.evaluate("proceed", strict_ctx)

    # For the strict tenant, the same risk score should be blocked
    assert result_strict.allowed is False

    # Cleanup for other tests
    TenantPolicyStore.set_default(TenantPolicy())
    TenantPolicyStore.clear_overrides()
    ComplianceRegistry.clear()
