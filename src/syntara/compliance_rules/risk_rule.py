from typing import Dict

from syntara.core.compliance_engine import ComplianceResult


class RiskRule:
    name = "risk_rule"
    description = "Blocks actions above configured risk threshold."

    def check(self, context: Dict) -> ComplianceResult:
        risk = float(context.get("risk_score", 0.0))
        threshold = float(context.get("risk_threshold", 0.25))
        if risk > threshold:
            return ComplianceResult.block(
                rule=self.name,
                reason=f"Risk {risk} exceeds threshold {threshold}",
            )
        return ComplianceResult.allow(rule=self.name)
