# ===============================================
# FILE: src/syntara/agents/deal_risk_agent.py
# ===============================================

from __future__ import annotations

from typing import Dict, Any, Optional

from syntara.agents.base_agent import BaseAgent
from syntara.crm.models import Opportunity
from syntara.core.explainability import ExplainabilityEngine
from syntara.crm.adapter import CRMAdapter


class DealRiskAgent(BaseAgent):
    """
    Agent that assesses the risk of a specific opportunity/deal and
    proposes whether it should be flagged for risk.
    """

    @property
    def name(self) -> str:
        return "deal_risk_agent"

    @property
    def description(self) -> str:
        return "Assesses deal risk and flags opportunities for review."

    @property
    def required_context_keys(self) -> list[str]:
        return ["opportunity_id"]

    def _find_opp(self, opp_id: str) -> Optional[Opportunity]:
        for opp in self.crm.get_opportunities(limit=100):
            if opp.id == opp_id:
                return opp
        return None

    def handle(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        self._ensure_required_keys(ctx)

        opp_id = str(ctx["opportunity_id"])
        opp = self._find_opp(opp_id)
        if opp is None:
            self.explain.add(
                "opportunity_not_found",
                {"opportunity_id": opp_id, "agent": self.name},
            )
            return {"action": "noop", "reason": "opportunity_not_found"}

        probability = float(opp.probability or 0.0)
        amount = float(opp.amount or 0.0)
        external_risk = float(ctx.get("risk_score", 0.0))

        # Simple heuristic: big deals with low probability or high external risk are risky.
        base_risk = external_risk
        if amount > 100000 and probability < 0.4:
            base_risk += 0.4
        elif amount > 50000 and probability < 0.3:
            base_risk += 0.3

        risk_score = max(0.0, min(1.0, base_risk))

        if risk_score >= 0.7:
            risk_level = "high"
            action = "flag_deal_risk"
        elif risk_score >= 0.4:
            risk_level = "medium"
            action = "monitor_deal_risk"
        else:
            risk_level = "low"
            action = "noop"

        self.explain.add(
            "deal_risk_assessment",
            {
                "opportunity_id": opp.id,
                "amount": amount,
                "probability": probability,
                "external_risk": external_risk,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "proposed_action": action,
            },
        )

        return {
            "action": action,
            "opportunity_id": opp.id,
            "risk_score": risk_score,
            "risk_level": risk_level,
        }

