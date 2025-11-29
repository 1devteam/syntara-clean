"""
Universal CRM Adapter Interface for Syntara OS.
This abstraction decouples agents from CRM vendor APIs.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from .models import Lead, Opportunity, CRMTask, CRMUser


class CRMAdapter(ABC):
    """Base class for CRM integrations."""

    @abstractmethod
    def name(self) -> str:
        """Return the provider name, e.g. 'salesforce' or 'hubspot'."""
        raise NotImplementedError

    # -------------------------------
    # Lead API
    # -------------------------------
    @abstractmethod
    def get_leads(self, limit: int = 50) -> List[Lead]:
        """Retrieve recent leads."""
        raise NotImplementedError

    @abstractmethod
    def get_lead(self, lead_id: str) -> Optional[Lead]:
        """Retrieve one lead."""
        raise NotImplementedError

    @abstractmethod
    def update_lead(self, lead: Lead) -> bool:
        """Update an existing lead."""
        raise NotImplementedError

    # -------------------------------
    # Opportunities
    # -------------------------------
    @abstractmethod
    def get_opportunities(self, limit: int = 50) -> List[Opportunity]:
        raise NotImplementedError

    @abstractmethod
    def update_opportunity(self, opp: Opportunity) -> bool:
        raise NotImplementedError

    # -------------------------------
    # Tasks
    # -------------------------------
    @abstractmethod
    def create_task(self, task: CRMTask) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_tasks(self, owner_id: Optional[str] = None) -> List[CRMTask]:
        raise NotImplementedError

    # -------------------------------
    # Users
    # -------------------------------
    @abstractmethod
    def get_current_user(self) -> CRMUser:
        raise NotImplementedError

    # -------------------------------
    # Generic Data Hooks
    # -------------------------------
    @abstractmethod
    def raw(self, path: str, params: Dict[str, Any] | None = None) -> Any:
        """Low-level access. Each provider may override."""
        raise NotImplementedError
