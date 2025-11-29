from typing import Dict

from syntara.core.compliance_engine import ComplianceResult


class EthicsRule:
    name = "ethics_rule"
    description = "Requires ethical approval when flagged as required."

    def check(self, context: Dict) -> ComplianceResult:
        requires = bool(context.get("ethical_review_required", False))
        approved = bool(context.get("ethical_approval", False))

        if requires and not approved:
            return ComplianceResult.block(
                rule=self.name,
                reason="Ethical approval is required but missing.",
            )
        return ComplianceResult.allow(self.name)
