"""
CRM-agnostic data models for the Syntara OS CRM layer.
These allow all agents & decision engines to use a unified schema.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class Lead:
    id: str
    name: str
    email: Optional[str] = None
    company: Optional[str] = None
    score: Optional[float] = None
    metadata: Dict[str, Any] = None


@dataclass
class Opportunity:
    id: str
    name: str
    stage: str
    amount: Optional[float] = None
    probability: Optional[float] = None
    metadata: Dict[str, Any] = None


@dataclass
class CRMTask:
    id: str
    description: str
    due_date: Optional[str] = None
    owner: Optional[str] = None
    completed: bool = False
    metadata: Dict[str, Any] = None


@dataclass
class CRMUser:
    id: str
    email: str
    name: Optional[str] = None
    role: Optional[str] = None
    metadata: Dict[str, Any] = None
