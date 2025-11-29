# ===============================================
# FILE: src/syntara/runtime.py
# Shared engine wiring for CLI + API.
# ===============================================

from __future__ import annotations

from syntara.crm.dummy_provider import DummyCRM
from syntara.core.compliance_engine import ComplianceEngine
from syntara.core.decision_engine import DecisionEngine
from syntara.core.explainability import ExplainabilityEngine
from syntara.agents.lead_qualification_agent import LeadQualificationAgent
from syntara.agents.deal_risk_agent import DealRiskAgent
from syntara.agents.outreach_agent import OutreachAgent


def build_engine() -> DecisionEngine:
    explain = ExplainabilityEngine()
    compliance = ComplianceEngine()
    crm = DummyCRM()
    engine = DecisionEngine(compliance=compliance, explain=explain)

    lead_agent = LeadQualificationAgent(crm=crm, explain=explain)
    deal_agent = DealRiskAgent(crm=crm, explain=explain)
    outreach_agent = OutreachAgent(crm=crm, explain=explain)

    engine.register("qualify_lead", lead_agent.handle)
    engine.register("assess_deal_risk", deal_agent.handle)
    engine.register("draft_outreach_email", outreach_agent.handle)

    return engine

