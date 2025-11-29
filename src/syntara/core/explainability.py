from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ExplanationStep:
    event: str
    details: Dict[str, Any]


class ExplainabilityEngine:
    """
    Produces human-readable traces across:
    - compliance decisions
    - agent decisions
    - CRM interactions
    """

    def __init__(self) -> None:
        self._steps: List[ExplanationStep] = []

    def add(self, event: str, details: Dict[str, Any]) -> None:
        self._steps.append(ExplanationStep(event=event, details=details))

    def flush(self) -> List[ExplanationStep]:
        out = list(self._steps)
        self._steps.clear()
        return out
