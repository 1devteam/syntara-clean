import importlib


def _load():
    mod = importlib.import_module("syntara")
    assert hasattr(mod, "ComplianceWrapper")
    return mod


def test_risk_above_threshold_is_rejected():
    mod = _load()
    cw = mod.ComplianceWrapper()
    ctx = {"risk_score": cw.governance_rules["max_risk_score"] + 0.1}
    assert cw.check_pre_execution("proceed", ctx) is False


def test_ethics_required_without_approval_is_rejected():
    mod = _load()
    cw = mod.ComplianceWrapper()
    action = cw.governance_rules["ethical_review_needed"][0]
    assert cw.check_pre_execution(action, {"risk_score": 0.0, "ethical_approval": False}) is False


def test_privacy_required_without_consent_is_rejected():
    mod = _load()
    cw = mod.ComplianceWrapper()
    if cw.governance_rules.get("data_privacy_required"):
        assert (
            cw.check_pre_execution("proceed", {"risk_score": 0.0, "user_consent": False}) is False
        )


def test_happy_path_is_allowed():
    mod = _load()
    cw = mod.ComplianceWrapper()
    ctx = {"risk_score": 0.0, "ethical_approval": True, "user_consent": True}
    assert cw.check_pre_execution("proceed", ctx) is True
