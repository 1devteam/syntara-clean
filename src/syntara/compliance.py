from __future__ import annotations

from typing import Any, Dict, List

from syntara.core.compliance_engine import (
    ComplianceEngine,
    ComplianceRegistry,
)
from syntara.compliance_rules import RiskRule, EthicsRule, PrivacyRule


class ComplianceWrapper:
    """
    Keeps the original public surface:
      - .governance_rules (dict)
      - .check_pre_execution(action, ctx) -> bool

    Internally delegates to the pluggable ComplianceEngine + rules.
    """

    def __init__(self) -> None:
        # Original tests expect this to be a dict, not a class.
        self.governance_rules: Dict[str, Any] = {
            "max_risk_score": 0.25,
            "ethical_review_needed": [
                "launch_experiment",
                "change_pricing",
            ],
            "data_privacy_required": True,
        }

        ComplianceRegistry.clear()
        ComplianceRegistry.register(RiskRule)
        ComplianceRegistry.register(EthicsRule)
        ComplianceRegistry.register(PrivacyRule)

        self._engine = ComplianceEngine()

    def _build_context(self, action: str, ctx: Dict[str, Any]) -> Dict[str, Any]:
        combined: Dict[str, Any] = dict(ctx)

        combined.setdefault("risk_threshold", self.governance_rules["max_risk_score"])

        ethical_actions: List[str] = self.governance_rules.get(
            "ethical_review_needed", []
        )
        if action in ethical_actions:
            combined.setdefault("ethical_review_required", True)

        if bool(self.governance_rules.get("data_privacy_required", False)):
            combined.setdefault("sensitive_data", True)

        return combined

    def check_pre_execution(self, action: str, ctx: Dict[str, Any]) -> bool:
        context = self._build_context(action, ctx)
        evaluation = self._engine.evaluate(action, context)
        return evaluation.allowed
