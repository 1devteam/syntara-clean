# ===============================================
# FILE: src/syntara/agents/base_agent.py
# ===============================================

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any, List

from syntara.crm.adapter import CRMAdapter
from syntara.core.explainability import ExplainabilityEngine


class BaseAgent(ABC):
    """
    Base class for all Syntara agents.
    Agents operate against a CRMAdapter and feed explanations into the
    shared ExplainabilityEngine.
    """

    def __init__(self, crm: CRMAdapter, explain: ExplainabilityEngine):
        self.crm = crm
        self.explain = explain

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    def required_context_keys(self) -> List[str]:
        return []

    @abstractmethod
    def handle(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process context and return a payload dict.
        Must include an 'action' key for downstream compliance routing.
        """
        raise NotImplementedError

    def _ensure_required_keys(self, ctx: Dict[str, Any]) -> None:
        missing = [k for k in self.required_context_keys if k not in ctx]
        if missing:
            self.explain.add(
                "missing_context_keys",
                {"agent": self.name, "missing": missing},
            )
            raise ValueError(f"Missing required context keys for {self.name}: {missing}")

