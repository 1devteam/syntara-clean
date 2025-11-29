# ===============================================
# FILE: tests/test_agents_lead_qualification.py
# ===============================================

from syntara.crm.dummy_provider import DummyCRM
from syntara.core.decision_engine import DecisionEngine
from syntara.core.explainability import ExplainabilityEngine
from syntara.agents.lead_qualification_agent import LeadQualificationAgent


def test_lead_qualification_agent_basic():
    crm = DummyCRM()
    explain = ExplainabilityEngine()
    agent = LeadQualificationAgent(crm=crm, explain=explain)

    engine = DecisionEngine(compliance=None, explain=explain)
    engine.register("qualify_lead", agent.handle)

    ctx = {"lead_id": "l-001", "risk_score": 0.1}
    decision = engine.handle("qualify_lead", ctx)

    assert decision.action == "update_lead"
    assert decision.compliance.allowed is True
    assert decision.payload["decision"] in ("qualify", "review", "disqualify")
    assert decision.payload["lead"].score is not None
    assert len(decision.explanation) > 0

