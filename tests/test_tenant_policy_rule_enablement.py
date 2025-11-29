from __future__ import annotations

from typing import List, Type

from syntara.compliance_rules.ethics_rule import EthicsRule
from syntara.compliance_rules.privacy_rule import PrivacyRule
from syntara.compliance_rules.risk_rule import RiskRule
from syntara.core.compliance_engine import ComplianceRule
from syntara.tenancy.policy import TenantPolicy
from syntara.tenancy.rules import get_effective_rules_for_policy


def _names(rules: List[Type[ComplianceRule]]) -> set[str]:
    return {getattr(r, "name", r.__name__.lower()) for r in rules}


def test_default_policy_keeps_all_rules_enabled() -> None:
    all_rules: List[Type[ComplianceRule]] = [RiskRule, EthicsRule, PrivacyRule]
    policy = TenantPolicy()  # all enable_* = None

    effective = get_effective_rules_for_policy(policy, all_rules)

    assert set(all_rules) == set(effective)
    assert _names(effective) == {"risk_rule", "ethics_rule", "privacy_rule"}


def test_disable_ethics_rule_for_specific_policy() -> None:
    all_rules: List[Type[ComplianceRule]] = [RiskRule, EthicsRule, PrivacyRule]
    policy = TenantPolicy(enable_ethics=False)

    effective = get_effective_rules_for_policy(policy, all_rules)
    names = _names(effective)

    assert "risk_rule" in names
    assert "privacy_rule" in names
    assert "ethics_rule" not in names


def test_disable_privacy_rule_for_specific_policy() -> None:
    all_rules: List[Type[ComplianceRule]] = [RiskRule, EthicsRule, PrivacyRule]
    policy = TenantPolicy(enable_privacy=False)

    effective = get_effective_rules_for_policy(policy, all_rules)
    names = _names(effective)

    assert "risk_rule" in names
    assert "ethics_rule" in names
    assert "privacy_rule" not in names


def test_disable_all_rules_for_extreme_policy() -> None:
    all_rules: List[Type[ComplianceRule]] = [RiskRule, EthicsRule, PrivacyRule]
    policy = TenantPolicy(
        enable_risk=False,
        enable_ethics=False,
        enable_privacy=False,
    )

    effective = get_effective_rules_for_policy(policy, all_rules)

    assert effective == []
