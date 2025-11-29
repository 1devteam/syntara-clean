# ===============================================
# FILE: tests/test_agents_deal_risk.py
# ===============================================

from syntara.crm.dummy_provider import DummyCRM
from syntara.core.decision_engine import DecisionEngine
from syntara.core.explainability import ExplainabilityEngine
from syntara.agents.deal_risk_agent import DealRiskAgent


def test_deal_risk_agent_basic():
    crm = DummyCRM()
    explain = ExplainabilityEngine()
    agent = DealRiskAgent(crm=crm, explain=explain)

    engine = DecisionEngine(compliance=None, explain=explain)
    engine.register("assess_deal_risk", agent.handle)

    ctx = {"opportunity_id": "o-001", "risk_score": 0.5}
    decision = engine.handle("assess_deal_risk", ctx)

    assert "risk_score" in decision.payload
    assert decision.payload["risk_level"] in ("low", "medium", "high")
    assert len(decision.explanation) > 0
