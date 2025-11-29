# ===============================================
# FILE: src/syntara/agents/lead_qualification_agent.py
# ===============================================

from __future__ import annotations

from typing import Dict, Any

from syntara.agents.base_agent import BaseAgent
from syntara.crm.models import Lead
from syntara.core.explainability import ExplainabilityEngine
from syntara.crm.adapter import CRMAdapter


class LeadQualificationAgent(BaseAgent):
    """
    Agent that evaluates lead quality and proposes an updated lead score
    and recommended next action.
    """

    @property
    def name(self) -> str:
        return "lead_qualification_agent"

    @property
    def description(self) -> str:
        return "Evaluates CRM leads and proposes qualification scores and next steps."

    @property
    def required_context_keys(self) -> list[str]:
        return ["lead_id"]

    def handle(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        self._ensure_required_keys(ctx)

        lead_id = str(ctx["lead_id"])
        lead = self.crm.get_lead(lead_id)
        if lead is None:
            self.explain.add(
                "lead_not_found",
                {"lead_id": lead_id, "agent": self.name},
            )
            return {"action": "noop", "reason": "lead_not_found"}

        base_score = float(lead.score or 0.0)
        risk_score = float(ctx.get("risk_score", 0.0))

        # Simple heuristic: lower risk increases qualification, high risk decreases.
        adjusted_score = max(0.0, min(1.0, base_score + (0.2 - risk_score * 0.3)))

        domain_bonus = 0.0
        if lead.email and lead.email.endswith("corp.com"):
            domain_bonus = 0.1

        final_score = max(0.0, min(1.0, adjusted_score + domain_bonus))

        if final_score >= 0.7:
            decision = "qualify"
            recommended_next_step = "assign_to_sales"
        elif final_score <= 0.3:
            decision = "disqualify"
            recommended_next_step = "nurture_campaign"
        else:
            decision = "review"
            recommended_next_step = "manual_review"

        updated_lead = Lead(
            id=lead.id,
            name=lead.name,
            email=lead.email,
            company=lead.company,
            score=final_score,
            metadata=(lead.metadata or {}) | {"decision": decision},
        )

        self.explain.add(
            "lead_qualification",
            {
                "lead_id": lead.id,
                "base_score": base_score,
                "risk_score": risk_score,
                "domain_bonus": domain_bonus,
                "final_score": final_score,
                "decision": decision,
                "recommended_next_step": recommended_next_step,
            },
        )

        return {
            "action": "update_lead",
            "lead": updated_lead,
            "decision": decision,
            "recommended_next_step": recommended_next_step,
        }
