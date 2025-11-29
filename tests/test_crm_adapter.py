from syntara.crm.dummy_provider import DummyCRM
from syntara.crm.models import Lead

def test_dummy_crm_leads_basic():
    crm = DummyCRM()
    leads = crm.get_leads()
    assert len(leads) >= 2
    assert isinstance(leads[0], Lead)

def test_update_lead():
    crm = DummyCRM()
    lead = crm.get_lead("l-001")
    lead.score = 0.9
    updated = crm.update_lead(lead)
    assert updated is True
    assert crm.get_lead("l-001").score == 0.9

def test_raw_call():
    crm = DummyCRM()
    r = crm.raw("/test")
    assert r["provider"] == "dummy-crm"
