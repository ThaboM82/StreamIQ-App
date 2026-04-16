import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "StreamIQ backend" in data["message"]

def test_callcenter_post_and_get():
    payload = {"customer_id": "C123", "transcript": "Hello, I need help", "sentiment": "Positive"}
    r_post = requests.post(f"{BASE_URL}/callcenter", json=payload)
    assert r_post.status_code == 200
    assert r_post.json()["status"] == "recorded"

    r_get = requests.get(f"{BASE_URL}/callcenter")
    assert r_get.status_code == 200
    assert isinstance(r_get.json(), list)

def test_claims_post_and_get():
    payload = {"claim_id": "CL456", "description": "Car accident claim", "intent": "Pending"}
    r_post = requests.post(f"{BASE_URL}/claims", json=payload)
    assert r_post.status_code == 200
    assert r_post.json()["status"] == "recorded"

    r_get = requests.get(f"{BASE_URL}/claims")
    assert r_get.status_code == 200
    assert isinstance(r_get.json(), list)

def test_auditlog_post_and_get():
    payload = {"event": "pytest audit event", "log_type": "TEST"}
    r_post = requests.post(f"{BASE_URL}/auditlog", json=payload)
    assert r_post.status_code == 200
    assert r_post.json()["status"] == "logged"

    r_get = requests.get(f"{BASE_URL}/auditlog?limit=5")
    assert r_get.status_code == 200
    logs = r_get.json()
    assert isinstance(logs, list)
    assert any(log["event"] == "pytest audit event" for log in logs)

def test_bigdata_and_multilingual():
    r_bigdata = requests.get(f"{BASE_URL}/bigdata")
    assert r_bigdata.status_code == 200
    assert isinstance(r_bigdata.json(), list)

    r_multi = requests.get(f"{BASE_URL}/multilingual")
    assert r_multi.status_code == 200
    assert isinstance(r_multi.json(), list)

def test_mlflow_runs():
    r = requests.get(f"{BASE_URL}/mlflow?experiment_name=StreamlitPredictionDemo")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
