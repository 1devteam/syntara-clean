# ===============================================
# FILE: tests/test_agents_outreach.py
# ===============================================

from syntara.crm.dummy_provider import DummyCRM
from syntara.core.decision_engine import DecisionEngine
from syntara.core.explainability import ExplainabilityEngine
from syntara.core.compliance_engine import ComplianceEngine
from syntara.agents.outreach_agent import OutreachAgent


def test_outreach_agent_blocked_without_consent():
    crm = DummyCRM()
    explain = ExplainabilityEngine()
    comp = ComplianceEngine()
    agent = OutreachAgent(crm=crm, explain=explain)

    engine = DecisionEngine(compliance=comp, explain=explain)
    engine.register("draft_outreach_email", agent.handle)

    ctx = {"lead_id": "l-001", "template_type": "intro", "user_consent": False}
    decision = engine.handle("draft_outreach_email", ctx)

    # Compliance engine should block sending email without consent for send_email action
    assert decision.action == "send_email"
    assert decision.compliance.allowed is False
    assert decision.compliance.reason in ("privacy_consent_missing", "ethical_review_missing")


def test_outreach_agent_allowed_with_consent():
    crm = DummyCRM()
    explain = ExplainabilityEngine()
    comp = ComplianceEngine()
    agent = OutreachAgent(crm=crm, explain=explain)

    engine = DecisionEngine(compliance=comp, explain=explain)
    engine.register("draft_outreach_email", agent.handle)

    ctx = {"lead_id": "l-001", "template_type": "intro", "user_consent": True, "ethical_approval": True}
    decision = engine.handle("draft_outreach_email", ctx)

    assert decision.action == "send_email"
    assert decision.compliance.allowed is True
    email = decision.payload["email"]
    assert "@" in email["to"]
    assert email["subject"]
    assert email["body"]
    assert len(decision.explanation) > 0
