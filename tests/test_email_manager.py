"""Unit and API route tests for Smart Email Manager."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from fastapi.testclient import TestClient

from domain.models import CleanupAction
from main import app
from utils.text_helpers import normalize_subject, truncate_preview


def test_text_helpers_normalize_and_truncate() -> None:
    """Verify subject prefix stripping and bounded preview truncation."""
    assert normalize_subject("Re: Fwd:   Q4 Budget Review  ") == "Q4 Budget Review"
    short_text = "Short body"
    assert truncate_preview(short_text, max_length=50) == "Short body"
    long_text = "A" * 40
    assert truncate_preview(long_text, max_length=15) == "AAAAAAAAAAAA..."


def test_health_endpoint() -> None:
    """Verify GET /api/health returns service status ok."""
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "email-manager"}


def test_analyze_emails_day_zero_empty_inbox() -> None:
    """Verify POST /api/emails/analyze handles Day-0 empty inbox cleanly."""
    client = TestClient(app)
    response = client.post("/api/emails/analyze", json={"messages": []})
    assert response.status_code == 200
    data = response.json()
    assert data["total_analyzed"] == 0
    assert data["useless_count"] == 0
    assert data["items"] == []
    assert data["topic_clusters"] == []


def test_analyze_emails_groups_by_topic_and_flags_useless_emails() -> None:
    """Verify AGY container analysis groups topics and recommends deleting stale promos."""
    client = TestClient(app)
    payload = {
        "messages": [
            {
                "message_id": "msg-1",
                "sender": "deals@store.example.com",
                "subject": "Flash Sale: 50% discount newsletter",
                "body": "Click here to unsubscribe from future promo offers.",
                "age_days": 45,
                "is_unread": False,
            },
            {
                "message_id": "msg-2",
                "sender": "pm@lumenconsultancy.ae",
                "subject": "Re: Sprint review and client deployment deadline",
                "body": "Let us finalize the release milestone before Friday.",
                "age_days": 2,
                "is_unread": True,
            },
            {
                "message_id": "msg-3",
                "sender": "billing@cloud.example.com",
                "subject": "Monthly invoice and payment receipt",
                "body": "Attached is your billing statement for November.",
                "age_days": 5,
                "is_unread": True,
            },
        ]
    }
    response = client.post("/api/emails/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_analyzed"] == 3
    assert data["useless_count"] == 1
    by_id = {item["message_id"]: item for item in data["items"]}
    assert by_id["msg-1"]["cleanup_action"] == CleanupAction.DELETE.value
    assert by_id["msg-1"]["topic"] == "Promotions & Newsletters"
    assert by_id["msg-2"]["cleanup_action"] == CleanupAction.KEEP.value
    assert by_id["msg-2"]["topic"] == "Work & Projects"
    assert by_id["msg-3"]["topic"] == "Finance & Billing"
    topics = {cluster["topic"] for cluster in data["topic_clusters"]}
    assert topics == {"Promotions & Newsletters", "Work & Projects", "Finance & Billing"}
