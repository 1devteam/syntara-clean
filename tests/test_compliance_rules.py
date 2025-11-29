from syntara.core.compliance_engine import (
    ComplianceRegistry,
    ComplianceEngine,
)
from syntara.compliance_rules.risk_rule import RiskRule
from syntara.compliance_rules.ethics_rule import EthicsRule
from syntara.compliance_rules.privacy_rule import PrivacyRule


def setup_module(module) -> None:  # type: ignore[override]
    ComplianceRegistry.clear()
    ComplianceRegistry.register(RiskRule)
    ComplianceRegistry.register(EthicsRule)
    ComplianceRegistry.register(PrivacyRule)


def test_risk_rule_blocks() -> None:
    eng = ComplianceEngine()
    result = eng.evaluate("any", {"risk_score": 0.9, "risk_threshold": 0.5})
    assert not result.allowed
    assert "Risk" in result.reason


def test_ethics_rule_blocks() -> None:
    eng = ComplianceEngine()
    result = eng.evaluate("any", {"ethical_review_required": True, "ethical_approval": False})
    assert not result.allowed
    assert "Ethical" in result.reason


def test_privacy_rule_blocks() -> None:
    eng = ComplianceEngine()
    result = eng.evaluate("any", {"sensitive_data": True, "user_consent": False})
    assert not result.allowed
    assert "consent" in result.reason.lower()


def test_passes_when_all_good() -> None:
    eng = ComplianceEngine()
    result = eng.evaluate(
        "any",
        {
            "risk_score": 0.0,
            "risk_threshold": 0.5,
            "ethical_review_required": False,
            "ethical_approval": True,
            "sensitive_data": False,
            "user_consent": True,
        },
    )
    assert result.allowed
