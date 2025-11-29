from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from syntara.core.compliance_engine import ComplianceEngine, ComplianceResult
from syntara.core.explainability import ExplainabilityEngine


@dataclass
class Decision:
    action: str
    payload: Dict[str, Any]
    compliance: ComplianceResult
    explanation: Any


class DecisionEngine:
    """
    Routes signals into agent behaviors:
    - performs compliance checks
    - produces explainability traces
    """

    def __init__(
        self,
        compliance: Optional[ComplianceEngine] = None,
        explain: Optional[ExplainabilityEngine] = None,
    ) -> None:
        self.compliance = compliance or ComplianceEngine()
        self.explain = explain or ExplainabilityEngine()
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register(
        self,
        signal_name: str,
        handler: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> None:
        self._handlers[signal_name] = handler

    def handle(self, signal: str, ctx: Dict[str, Any]) -> Decision:
        handler = self._handlers.get(signal)
        if handler is None:
            self.explain.add("no_handler", {"signal": signal})
            comp = ComplianceResult(True, "no_checks_for_unknown_signal", {})
            return Decision("noop", {}, comp, self.explain.flush())

        payload = handler(ctx)
        action = payload.get("action", "noop")

        comp = self.compliance.evaluate(action, ctx)
        self.explain.add(
            "compliance_eval",
            {"allowed": comp.allowed, "reason": comp.reason},
        )

        if not comp.allowed:
            self.explain.add("blocked", {"action": action})
            return Decision(action, payload, comp, self.explain.flush())

        self.explain.add("executed", {"action": action})
        return Decision(action, payload, comp, self.explain.flush())
