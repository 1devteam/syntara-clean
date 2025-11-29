# ===============================================
# FILE: tests/test_api.py
# ===============================================

from __future__ import annotations

from fastapi.testclient import TestClient

from syntara.api import create_app


def _client() -> TestClient:
    app = create_app()
    return TestClient(app)


def test_api_qualify_lead():
    client = _client()
    resp = client.post(
        "/decision/qualify-lead",
        json={"lead_id": "l-001", "risk_score": 0.2},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["action"] == "update_lead"
    assert "compliance" in data
    assert "explanation" in data


def test_api_outreach_blocked_without_consent():
    client = _client()
    resp = client.post(
        "/decision/outreach",
        json={"lead_id": "l-001", "template_type": "intro"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["action"] == "send_email"
    assert data["compliance"]["allowed"] is False


def test_api_outreach_allowed_with_consent_and_approval():
    client = _client()
    resp = client.post(
        "/decision/outreach",
        json={
            "lead_id": "l-001",
            "template_type": "intro",
            "user_consent": True,
            "ethical_approval": True,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["action"] == "send_email"
    assert data["compliance"]["allowed"] is True
    email = data["payload"]["email"]
    assert "@" in email["to"]
    assert email["subject"]
    assert email["body"]
