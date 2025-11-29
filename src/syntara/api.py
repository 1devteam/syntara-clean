from __future__ import annotations

from typing import Any, Dict, Optional

from dataclasses import asdict, is_dataclass

from fastapi import FastAPI, Header
from pydantic import BaseModel

from syntara.runtime import build_engine
from syntara.tenancy.integration import apply_tenant_policy_to_context


def _serialize(obj: Any) -> Any:
    if is_dataclass(obj):
        return {k: _serialize(v) for k, v in asdict(obj).items()}
    if isinstance(obj, list):
        return [_serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


ENGINE = build_engine()


class QualifyLeadRequest(BaseModel):
    lead_id: str
    risk_score: Optional[float] = None


class DealRiskRequest(BaseModel):
    opportunity_id: str
    risk_score: Optional[float] = None


class OutreachRequest(BaseModel):
    lead_id: str
    template_type: str
    user_consent: bool = False
    ethical_approval: bool = False


def create_app() -> FastAPI:
    app = FastAPI(title="Syntara OS Demo API", version="0.0.1")

    @app.post("/decision/qualify-lead")
    def qualify_lead(
        req: QualifyLeadRequest,
        tenant_id: Optional[str] = Header(default=None, alias="X-Tenant-ID"),
    ) -> Dict[str, Any]:
        ctx: Dict[str, Any] = {"lead_id": req.lead_id}
        if req.risk_score is not None:
            ctx["risk_score"] = req.risk_score
        if tenant_id is not None:
            ctx["tenant_id"] = tenant_id

        ctx = apply_tenant_policy_to_context(ctx)
        decision = ENGINE.handle("qualify_lead", ctx)

        return {
            "action": decision.action,
            "payload": _serialize(decision.payload),
            "compliance": _serialize(decision.compliance),
            "explanation": _serialize(decision.explanation),
        }

    @app.post("/decision/deal-risk")
    def deal_risk(
        req: DealRiskRequest,
        tenant_id: Optional[str] = Header(default=None, alias="X-Tenant-ID"),
    ) -> Dict[str, Any]:
        ctx: Dict[str, Any] = {"opportunity_id": req.opportunity_id}
        if req.risk_score is not None:
            ctx["risk_score"] = req.risk_score
        if tenant_id is not None:
            ctx["tenant_id"] = tenant_id

        ctx = apply_tenant_policy_to_context(ctx)
        decision = ENGINE.handle("assess_deal_risk", ctx)

        return {
            "action": decision.action,
            "payload": _serialize(decision.payload),
            "compliance": _serialize(decision.compliance),
            "explanation": _serialize(decision.explanation),
        }

    @app.post("/decision/outreach")
    def outreach(
        req: OutreachRequest,
        tenant_id: Optional[str] = Header(default=None, alias="X-Tenant-ID"),
    ) -> Dict[str, Any]:
        ctx: Dict[str, Any] = {
            "lead_id": req.lead_id,
            "template_type": req.template_type,
            "user_consent": req.user_consent,
        }
        if req.ethical_approval:
            ctx["ethical_approval"] = True
        if tenant_id is not None:
            ctx["tenant_id"] = tenant_id

        ctx = apply_tenant_policy_to_context(ctx)
        decision = ENGINE.handle("draft_outreach_email", ctx)

        return {
            "action": decision.action,
            "payload": _serialize(decision.payload),
            "compliance": _serialize(decision.compliance),
            "explanation": _serialize(decision.explanation),
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("syntara.api:app", host="0.0.0.0", port=8000, reload=True)
