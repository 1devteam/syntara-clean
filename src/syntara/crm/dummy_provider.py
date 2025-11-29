"""
Dummy CRM provider used during development.

This allows Syntara to develop all pipeline, compliance, explainability,
and agent logic without relying on Salesforce/HubSpot API latency or quotas.

This provider simulates CRM behavior deterministically.
"""

from __future__ import annotations
from typing import List, Optional
from uuid import uuid4

from .adapter import CRMAdapter
from .models import Lead, Opportunity, CRMTask, CRMUser


class DummyCRM(CRMAdapter):

    def __init__(self):
        self._user = CRMUser(
            id="u-001",
            email="syntara.dev@example.com",
            name="Syntara Dev",
            role="developer"
        )

        self._leads = [
            Lead(id="l-001", name="Alice Johnson", email="alice@corp.com", company="Corp LLC", score=0.4),
            Lead(id="l-002", name="Bob Smith", email="bob@startup.ai", company="StartupAI", score=0.2),
        ]

        self._opps = [
            Opportunity(id="o-001", name="Corporate Expansion", stage="Qualification", amount=50000, probability=0.3),
        ]

        self._tasks = []

    def name(self) -> str:
        return "dummy-crm"

    # -------------------------------
    # Lead API
    # -------------------------------
    def get_leads(self, limit: int = 50) -> List[Lead]:
        return self._leads[:limit]

    def get_lead(self, lead_id: str) -> Optional[Lead]:
        return next((l for l in self._leads if l.id == lead_id), None)

    def update_lead(self, lead: Lead) -> bool:
        for idx, existing in enumerate(self._leads):
            if existing.id == lead.id:
                self._leads[idx] = lead
                return True
        return False

    # -------------------------------
    # Opportunities
    # -------------------------------
    def get_opportunities(self, limit: int = 50) -> List[Opportunity]:
        return self._opps[:limit]

    def update_opportunity(self, opp: Opportunity) -> bool:
        for idx, existing in enumerate(self._opps):
            if existing.id == opp.id:
                self._opps[idx] = opp
                return True
        return False

    # -------------------------------
    # Tasks
    # -------------------------------
    def create_task(self, task: CRMTask) -> str:
        tid = f"t-{uuid4()}"
        task.id = tid
        self._tasks.append(task)
        return tid

    def get_tasks(self, owner_id: Optional[str] = None) -> List[CRMTask]:
        if owner_id is None:
            return self._tasks
        return [t for t in self._tasks if t.owner == owner_id]

    # -------------------------------
    # Users
    # -------------------------------
    def get_current_user(self) -> CRMUser:
        return self._user

    # -------------------------------
    # Raw low-level hook
    # -------------------------------
    def raw(self, path: str, params=None):
        return {"path": path, "params": params, "provider": self.name()}
