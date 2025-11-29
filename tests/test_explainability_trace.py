from __future__ import annotations

from typing import Dict, Any

from syntara.core.compliance_engine import ComplianceEngine
from syntara.core.decision_engine import DecisionEngine
from syntara.core.explainability import ExplainabilityEngine


def _events(decision) -> list[str]:
    # decision.explanation is a list[ExplanationStep]
    return [step.event for step in decision.explanation]


def test_blocked_decision_has_compliance_and_blocked_events() -> None:
    """
    If compliance blocks an action, we expect:
    - at least one compliance_eval event
    - at least one blocked event
    """
    explain = ExplainabilityEngine()
    comp = ComplianceEngine()
    engine = DecisionEngine(compliance=comp, explain=explain)

    # Handler that triggers privacy block: uses personal data without consent.
    def handler(ctx: Dict[str, Any]) -> Dict[str, Any]:
        return {"action": "use_personal_data", "ctx": ctx}

    engine.register("use_personal_data_signal", handler)

    ctx: Dict[str, Any] = {"user_consent": False}
    decision = engine.handle("use_personal_data_signal", ctx)

    assert decision.compliance.allowed is False

    events = _events(decision)
    assert "compliance_eval" in events
    assert "blocked" in events


def test_happy_path_has_executed_event() -> None:
    """
    When an action is allowed, we expect:
    - a compliance_eval event
    - an executed event
    - no blocked event
    """
    explain = ExplainabilityEngine()
    comp = ComplianceEngine()
    engine = DecisionEngine(compliance=comp, explain=explain)

    def handler(ctx: Dict[str, Any]) -> Dict[str, Any]:
        # Same action as above, but with consent -> allowed.
        return {"action": "use_personal_data", "ctx": ctx}

    engine.register("use_personal_data_signal", handler)

    ctx: Dict[str, Any] = {"user_consent": True}
    decision = engine.handle("use_personal_data_signal", ctx)

    assert decision.compliance.allowed is True

    events = _events(decision)
    assert "compliance_eval" in events
    assert "executed" in events
    assert "blocked" not in events


def test_no_handler_produces_no_handler_event() -> None:
    """
    If there is no handler for a signal, we expect a no_handler event.
    """
    explain = ExplainabilityEngine()
    comp = ComplianceEngine()
    engine = DecisionEngine(compliance=comp, explain=explain)

    decision = engine.handle("nonexistent_signal", {})

    events = _events(decision)
    assert "no_handler" in events
