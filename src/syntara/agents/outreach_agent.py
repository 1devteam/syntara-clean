# ===============================================
# FILE: src/syntara/agents/outreach_agent.py
# ===============================================

from __future__ import annotations

from typing import Dict, Any

from syntara.agents.base_agent import BaseAgent
from syntara.crm.models import Lead
from syntara.core.explainability import ExplainabilityEngine
from syntara.crm.adapter import CRMAdapter


class OutreachAgent(BaseAgent):
    """
    Agent that drafts outreach emails for leads, leaving sending decisions
    to higher layers and compliance.
    """

    @property
    def name(self) -> str:
        return "outreach_agent"

    @property
    def description(self) -> str:
        return "Drafts compliant outreach emails for CRM leads."

    @property
    def required_context_keys(self) -> list[str]:
        return ["lead_id", "template_type"]

    def handle(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        self._ensure_required_keys(ctx)

        lead_id = str(ctx["lead_id"])
        template_type = str(ctx["template_type"])

        lead = self.crm.get_lead(lead_id)
        if lead is None:
            self.explain.add(
                "lead_not_found_for_outreach",
                {"lead_id": lead_id, "agent": self.name},
            )
            return {"action": "noop", "reason": "lead_not_found"}

        user_consent = bool(ctx.get("user_consent", False))

        subject, body = self._build_email(lead, template_type)

        self.explain.add(
            "outreach_draft_created",
            {
                "lead_id": lead.id,
                "template_type": template_type,
                "user_consent": user_consent,
            },
        )

        email_payload = {
            "to": lead.email,
            "subject": subject,
            "body": body,
        }

        return {
            "action": "send_email",  # compliance will enforce consent
            "email": email_payload,
            "lead_id": lead.id,
            "template_type": template_type,
        }

    def _build_email(self, lead: Lead, template_type: str) -> tuple[str, str]:
        name = lead.name or "there"
        if template_type == "intro":
            subject = f"Quick intro, {name}"
            body = (
                f"Hi {name},\n\n"
                "I wanted to reach out with a brief introduction and see if it "
                "makes sense to schedule a short conversation.\n\n"
                "Best,\nSyntara Agent"
            )
        elif template_type == "followup":
            subject = f"Following up, {name}"
            body = (
                f"Hi {name},\n\n"
                "Just following up on my previous message and checking if you "
                "had a chance to review it.\n\n"
                "Best,\nSyntara Agent"
            )
        else:
            subject = f"Hello {name}"
            body = (
                f"Hi {name},\n\n"
                "Reaching out to see if now is a good time to connect.\n\n"
                "Best,\nSyntara Agent"
            )
        return subject, body

