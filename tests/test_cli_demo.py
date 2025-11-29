# ===============================================
# FILE: tests/test_cli_demo.py
# ===============================================

from __future__ import annotations

import json

from syntara import cli


def test_cli_qualify_lead_demo(capsys):
    code = cli.main(["demo", "qualify-lead", "--lead-id", "l-001", "--risk-score", "0.2"])
    assert code == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["action"] == "update_lead"
    assert "compliance" in data
    assert "explanation" in data
    assert isinstance(data["explanation"], list)


def test_cli_outreach_blocked_without_consent(capsys):
    code = cli.main(
        [
            "demo",
            "outreach",
            "--lead-id",
            "l-001",
            "--template-type",
            "intro",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    # Compliance engine should block send_email without consent
    assert data["action"] == "send_email"
    assert data["compliance"]["allowed"] is False


def test_cli_outreach_allowed_with_consent_and_approval(capsys):
    code = cli.main(
        [
            "demo",
            "outreach",
            "--lead-id",
            "l-001",
            "--template-type",
            "intro",
            "--user-consent",
            "--ethical-approval",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["action"] == "send_email"
    assert data["compliance"]["allowed"] is True
    email = data["payload"]["email"]
    assert "@" in email["to"]
    assert email["subject"]
    assert email["body"]

