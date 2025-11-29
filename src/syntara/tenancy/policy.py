from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Optional


@dataclass(frozen=True)
class TenantPolicy:
    """
    Basic per-tenant knobs.

    All fields are optional so the engine can fall back to global defaults.
    """

    tenant_id: Optional[str] = None
    risk_threshold: Optional[float] = None
    enable_risk: Optional[bool] = None
    enable_ethics: Optional[bool] = None
    enable_privacy: Optional[bool] = None


class TenantPolicyStore:
    """
    In-memory policy store.

    WHY: Gives a single place to look up per-tenant policies without hard-coding
    multi-tenant logic inside the core compliance or decision engines.
    """

    _default_policy: TenantPolicy = TenantPolicy()
    _overrides: Dict[str, TenantPolicy] = {}

    @classmethod
    def set_default(cls, policy: TenantPolicy) -> None:
        cls._default_policy = replace(policy, tenant_id=None)

    @classmethod
    def set_override(cls, tenant_id: str, policy: TenantPolicy) -> None:
        cls._overrides[tenant_id] = replace(policy, tenant_id=tenant_id)

    @classmethod
    def clear_overrides(cls) -> None:
        cls._overrides.clear()

    @classmethod
    def get(cls, tenant_id: Optional[str]) -> TenantPolicy:
        if tenant_id is None:
            return cls._default_policy
        return cls._overrides.get(tenant_id, cls._default_policy)
