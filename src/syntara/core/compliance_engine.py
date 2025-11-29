from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, List, Dict, Type


@dataclass
class ComplianceResult:
    allowed: bool
    reason: str
    rule: str

    @staticmethod
    def allow(rule: str) -> "ComplianceResult":
        return ComplianceResult(True, "", rule)

    @staticmethod
    def block(rule: str, reason: str) -> "ComplianceResult":
        return ComplianceResult(False, reason, rule)


class ComplianceRule(Protocol):
    name: str
    description: str

    def check(self, context: Dict) -> ComplianceResult:  # pragma: no cover - protocol
        ...


class ComplianceRegistry:
    _rules: List[Type[ComplianceRule]] = []

    @classmethod
    def register(cls, rule_cls: Type[ComplianceRule]) -> None:
        cls._rules.append(rule_cls)

    @classmethod
    def get_rules(cls) -> List[Type[ComplianceRule]]:
        return list(cls._rules)

    @classmethod
    def clear(cls) -> None:
        cls._rules.clear()


@dataclass
class ComplianceTrace:
    rule: str
    allowed: bool
    reason: str


@dataclass
class ComplianceEvaluation:
    allowed: bool
    reason: str
    traces: List[ComplianceTrace]


class ComplianceEngine:
    """Runs all registered compliance rules in order and accumulates traces."""

    def __init__(self, auto_register_defaults: bool = True) -> None:
        # Auto-wire core rules if nothing has been registered yet.
        if auto_register_defaults and not ComplianceRegistry.get_rules():
            from syntara.compliance_rules import RiskRule, EthicsRule, PrivacyRule

            ComplianceRegistry.register(RiskRule)
            ComplianceRegistry.register(EthicsRule)
            ComplianceRegistry.register(PrivacyRule)

    def evaluate(self, action: str, context: Dict) -> ComplianceEvaluation:
        traces: List[ComplianceTrace] = []

        for rule_cls in ComplianceRegistry.get_rules():
            rule = rule_cls()
            result = rule.check(context)
            traces.append(
                ComplianceTrace(
                    rule=result.rule,
                    allowed=result.allowed,
                    reason=result.reason,
                )
            )

            if not result.allowed:
                return ComplianceEvaluation(
                    allowed=False,
                    reason=result.reason,
                    traces=traces,
                )

        return ComplianceEvaluation(
            allowed=True,
            reason="",
            traces=traces,
        )
