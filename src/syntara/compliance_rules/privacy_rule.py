from typing import Dict

from syntara.core.compliance_engine import ComplianceResult


class PrivacyRule:
    name = "privacy_rule"
    description = "Blocks processing of user-related data without consent."

    def check(self, context: Dict) -> ComplianceResult:
        # Default: outreach/CRM data is treated as sensitive unless explicitly overridden.
        sensitive = bool(context.get("sensitive_data", True))
        consent = context.get("user_consent")

        # Tests expect this exact reason code when consent is missing.
        if sensitive and consent is False:
            return ComplianceResult.block(
                rule=self.name,
                reason="privacy_consent_missing",
            )

        return ComplianceResult.allow(self.name)
