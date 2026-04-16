from flask import Flask, request, jsonify
from src.db.init_db import init_db
from src.db.repository import (
    get_call_center_records,
    add_call_center_record,
    get_insurance_claims,
    add_insurance_claim,
    get_big_data_demo,
    get_multilingual_samples,
    add_audit_log,
    get_audit_logs
)

import mlflow

app = Flask(__name__)

# --- Startup: initialize DB ---
with app.app_context():
    init_db()
    add_audit_log("Backend service started", "SYSTEM")

# --- Health check ---
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "StreamIQ backend (Flask + SQLite) is running"})

# --- AuditLog endpoints ---
@app.route("/auditlog", methods=["POST"])
def create_audit_log():
    data = request.json or {}
    event = data.get("event")
    log_type = data.get("log_type", "API")
    add_audit_log(event, log_type)
    return jsonify({"status": "logged", "event": event, "log_type": log_type})

@app.route("/auditlog", methods=["GET"])
def list_audit_logs():
    limit = int(request.args.get("limit", 50))
    logs = get_audit_logs(limit=limit)
    return jsonify([
        {"id": log.id, "timestamp": str(log.timestamp), "event": log.event, "log_type": log.log_type}
        for log in logs
    ])

# --- CallCenterRecord endpoints ---
@app.route("/callcenter", methods=["POST"])
def create_call_center_record():
    data = request.json or {}
    customer_id = data.get("customer_id")
    transcript = data.get("transcript")
    sentiment = data.get("sentiment")
    add_call_center_record(customer_id, transcript, sentiment)
    return jsonify({"status": "recorded", "customer_id": customer_id})

@app.route("/callcenter", methods=["GET"])
def list_call_center_records():
    limit = int(request.args.get("limit", 50))
    records = get_call_center_records(limit=limit)
    return jsonify([
        {"id": r.id, "customer_id": r.customer_id, "transcript": r.transcript,
         "sentiment": r.sentiment, "created_at": str(r.created_at)}
        for r in records
    ])

# --- InsuranceClaim endpoints ---
@app.route("/claims", methods=["POST"])
def create_insurance_claim():
    data = request.json or {}
    claim_id = data.get("claim_id")
    description = data.get("description")
    intent = data.get("intent")
    add_insurance_claim(claim_id, description, intent)
    return jsonify({"status": "recorded", "claim_id": claim_id})

@app.route("/claims", methods=["GET"])
def list_insurance_claims():
    limit = int(request.args.get("limit", 50))
    claims = get_insurance_claims(limit=limit)
    return jsonify([
        {"id": c.id, "claim_id": c.claim_id, "description": c.description,
         "intent": c.intent, "created_at": str(c.created_at)}
        for c in claims
    ])

# --- Big Data Demo endpoint ---
@app.route("/bigdata", methods=["GET"])
def list_big_data_demo():
    limit = int(request.args.get("limit", 50))
    records = get_big_data_demo(limit=limit)
    return jsonify([
        {"id": r.id, "dataset": r.dataset, "value": r.value, "created_at": str(r.created_at)}
        for r in records
    ])

# --- Multilingual Samples endpoint ---
@app.route("/multilingual", methods=["GET"])
def list_multilingual_samples():
    limit = int(request.args.get("limit", 50))
    samples = get_multilingual_samples(limit=limit)
    return jsonify([
        {"id": s.id, "lang": s.lang, "text": s.text, "created_at": str(s.created_at)}
        for s in samples
    ])

# --- MLflow helpers ---
def fetch_runs(experiment_name: str):
    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if not experiment:
        return []

    runs = client.search_runs([experiment.experiment_id])
    records = []
    for run in runs:
        record = {"run_id": run.info.run_id}
        record.update(run.data.params)
        record.update(run.data.metrics)
        records.append(record)
    return records

# --- MLflow endpoint ---
@app.route("/mlflow", methods=["GET"])
def list_mlflow_runs():
    experiment_name = request.args.get("experiment_name", "StreamlitPredictionDemo")
    runs = fetch_runs(experiment_name)
    return jsonify(runs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
