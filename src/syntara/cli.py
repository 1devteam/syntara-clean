from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List, Optional

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


def _inject_tenant(ctx: Dict[str, Any], args: argparse.Namespace) -> None:
    tenant_id = getattr(args, "tenant_id", None)
    if tenant_id:
        ctx["tenant_id"] = tenant_id


def _run_qualify_lead(args: argparse.Namespace) -> int:
    engine = build_engine()
    ctx: Dict[str, Any] = {"lead_id": args.lead_id}
    if args.risk_score is not None:
        ctx["risk_score"] = args.risk_score
    _inject_tenant(ctx, args)
    ctx = apply_tenant_policy_to_context(ctx)

    decision = engine.handle("qualify_lead", ctx)
    out = {
        "action": decision.action,
        "payload": _serialize(decision.payload),
        "compliance": _serialize(decision.compliance),
        "explanation": _serialize(decision.explanation),
    }
    print(json.dumps(out, indent=2))
    return 0


def _run_deal_risk(args: argparse.Namespace) -> int:
    engine = build_engine()
    ctx: Dict[str, Any] = {"opportunity_id": args.opportunity_id}
    if args.risk_score is not None:
        ctx["risk_score"] = args.risk_score
    _inject_tenant(ctx, args)
    ctx = apply_tenant_policy_to_context(ctx)

    decision = engine.handle("assess_deal_risk", ctx)
    out = {
        "action": decision.action,
        "payload": _serialize(decision.payload),
        "compliance": _serialize(decision.compliance),
        "explanation": _serialize(decision.explanation),
    }
    print(json.dumps(out, indent=2))
    return 0


def _run_outreach(args: argparse.Namespace) -> int:
    engine = build_engine()
    ctx: Dict[str, Any] = {
        "lead_id": args.lead_id,
        "template_type": args.template_type,
        "user_consent": args.user_consent,
    }
    if args.ethical_approval:
        ctx["ethical_approval"] = True
    _inject_tenant(ctx, args)
    ctx = apply_tenant_policy_to_context(ctx)

    decision = engine.handle("draft_outreach_email", ctx)
    out = {
        "action": decision.action,
        "payload": _serialize(decision.payload),
        "compliance": _serialize(decision.compliance),
        "explanation": _serialize(decision.explanation),
    }
    print(json.dumps(out, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="syntara",
        description="Syntara OS demo CLI (DummyCRM, agents, compliance, explainability).",
    )
    subparsers = parser.add_subparsers(dest="command")

    demo = subparsers.add_parser("demo", help="Run demo agent flows against DummyCRM.")
    demo_sub = demo.add_subparsers(dest="demo_command")

    # qualify-lead
    p_ql = demo_sub.add_parser("qualify-lead", help="Qualify a lead.")
    p_ql.add_argument("--lead-id", required=True, help="Lead ID in DummyCRM (e.g. l-001).")
    p_ql.add_argument(
        "--risk-score",
        type=float,
        default=None,
        help="Optional external risk score (0.0–1.0).",
    )
    p_ql.add_argument(
        "--tenant-id",
        default=None,
        help="Tenant identifier for multi-tenant routing.",
    )
    p_ql.set_defaults(func=_run_qualify_lead)

    # deal-risk
    p_dr = demo_sub.add_parser("deal-risk", help="Assess deal risk.")
    p_dr.add_argument(
        "--opportunity-id",
        required=True,
        help="Opportunity ID in DummyCRM (e.g. o-001).",
    )
    p_dr.add_argument(
        "--risk-score",
        type=float,
        default=None,
        help="External risk score (0.0–1.0).",
    )
    p_dr.add_argument(
        "--tenant-id",
        default=None,
        help="Tenant identifier for multi-tenant routing.",
    )
    p_dr.set_defaults(func=_run_deal_risk)

    # outreach
    p_or = demo_sub.add_parser("outreach", help="Draft an outreach email.")
    p_or.add_argument("--lead-id", required=True, help="Lead ID in DummyCRM.")
    p_or.add_argument(
        "--template-type",
        required=True,
        choices=["intro", "followup", "generic"],
        help="Email template type.",
    )
    p_or.add_argument(
        "--user-consent",
        action="store_true",
        help="Include this flag to indicate user consent is present.",
    )
    p_or.add_argument(
        "--ethical-approval",
        action="store_true",
        help="Include this flag to indicate ethical review has been approved.",
    )
    p_or.add_argument(
        "--tenant-id",
        default=None,
        help="Tenant identifier for multi-tenant routing.",
    )
    p_or.set_defaults(func=_run_outreach)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)

    if ns.command != "demo" or not hasattr(ns, "func"):
        parser.print_help()
        return 1

    return ns.func(ns)


if __name__ == "__main__":
    raise SystemExit(main())
