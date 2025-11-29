"""
Compliance rule pack for Syntara.

Rules live in individual modules and are registered with ComplianceRegistry
by tests, CLI, or application startup code.
"""

from syntara.compliance_rules.risk_rule import RiskRule
from syntara.compliance_rules.ethics_rule import EthicsRule
from syntara.compliance_rules.privacy_rule import PrivacyRule

__all__ = [
    "RiskRule",
    "EthicsRule",
    "PrivacyRule",
]
