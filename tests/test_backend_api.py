import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_security_headers():
    response = client.get("/health")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert response.headers.get("Strict-Transport-Security") is not None
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

def test_programs_api():
    response = client.get("/api/v1/programs/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 5
    assert any("Computer Science" in p["name"] for p in data["data"])

def test_schools_api():
    response = client.get("/api/v1/schools/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 5
    assert any(s["id"] == "set" for s in data["data"])

def test_admissions_api():
    response = client.get("/api/v1/admissions/scholarships")
    assert response.status_code == 200
    data = response.json()
    assert len(data["scholarships"]) >= 1

def test_lead_capture_and_scoring():
    payload = {
        "full_name": "Rohan Gupta",
        "phone": "+919876543210",
        "email": "rohan.gupta@example.com",
        "city": "Greater Noida",
        "state": "Uttar Pradesh",
        "interested_course": "B.Tech CSE AI/ML",
        "source": "ai_assistant",
        "consent": True
    }
    response = client.post("/api/v1/leads/capture", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    lead_info = data["data"]["lead"]
    assert lead_info["lead_intent_score"] >= 70
    assert lead_info["lead_priority"] in ["HOT", "WARM"]
    assert lead_info["compliance"]["dpdp_consent_given"] is True

def test_ai_chat_grounding():
    chat_payload = {
        "query": "What is the fee for B.Tech Computer Science at Sharda?",
        "conversation_history": []
    }
    response = client.post("/api/v1/ai/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "2,20,000" in data["answer"] or "Engineering" in data["answer"]
    assert data["lead_capture_recommended"] is True
