from __future__ import annotations

from typing import List, Type

from syntara.core.compliance_engine import ComplianceRule
from syntara.tenancy.policy import TenantPolicy


def _rule_name(rule_cls: Type[ComplianceRule]) -> str:
    """
    Extract a canonical name for the rule.

    We prefer the explicit `name` attribute if present; otherwise fall back
    to the class name in lowercase. This keeps behavior stable even if rules
    are refactored slightly.
    """
    return getattr(rule_cls, "name", rule_cls.__name__.lower())


def get_effective_rules_for_policy(
    policy: TenantPolicy,
    all_rules: List[Type[ComplianceRule]],
) -> List[Type[ComplianceRule]]:
    """
    Return the list of rule classes that should be active under the given policy.

    Semantics:
    - If policy.enable_* is None  -> treat as "enabled" (do not filter).
    - If policy.enable_* is False -> drop the corresponding rule type.
    - If policy.enable_* is True  -> keep it (assuming it is present in all_rules).

    This function does NOT touch any global registry or engine; it is pure and
    can be unit-tested independently.
    """
    effective: List[Type[ComplianceRule]] = []

    for rule_cls in all_rules:
        name = _rule_name(rule_cls)

        if name == "risk_rule" and policy.enable_risk is False:
            continue
        if name == "ethics_rule" and policy.enable_ethics is False:
            continue
        if name == "privacy_rule" and policy.enable_privacy is False:
            continue

        effective.append(rule_cls)

    return effective
