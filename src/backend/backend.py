import sys, os, datetime
from flask import Flask, request, jsonify
import mlflow

# --- Import DB + Repository ---
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

# --- Import Dummy Data + Toggle ---
from src.db.dummy_data import (
    dummy_callcenter,
    dummy_claims,
    dummy_bigdata,
    dummy_multilingual,
    dummy_transcriptions,
    dummy_auditlogs,
    dummy_bank_records,
    dummy_insurance_records,
    dummy_callcenter_nlp,
)
USE_DUMMY = True   # Global toggle (aligns with loaders.py)

# --- Import Transcriber ---
from src.speech_to_text import Transcriber
transcriber = Transcriber()

# -- project root to sys.path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

app = Flask(__name__)

# --- Startup: initialize DB and preload demo records ---
with app.app_context():
    init_db()
    add_audit_log("Backend service started", "SYSTEM")

    if not USE_DUMMY:
        _cached_callcenter = get_call_center_records(limit=50)
        _cached_claims = get_insurance_claims(limit=50)
        _cached_bigdata = get_big_data_demo(limit=50)
    else:
        _cached_callcenter = dummy_callcenter
        _cached_claims = dummy_claims
        _cached_bigdata = dummy_bigdata

    _cache_last_refresh = datetime.datetime.now()

# --- Health checks ---
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "Flask server is alive"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "StreamIQ backend health endpoint is alive"})

@app.route("/", methods=["GET"])
def root_health_check():
    return jsonify({"status": "ok", "message": "StreamIQ backend (Flask + SQLite) is running"})

@app.route("/auditlog/health", methods=["GET"])
def auditlog_health():
    try:
        if USE_DUMMY:
            count = len(dummy_auditlogs)
        else:
            logs = get_audit_logs(limit=1)
            count = len(logs)
        return jsonify({"status": "ok", "message": f"AuditLog reachable, {count} record(s) found"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"AuditLog check failed: {str(e)}"}), 500

# --- AuditLog endpoints ---
@app.route("/auditlog", methods=["GET"])
def list_audit_logs():
    limit = int(request.args.get("limit", 50))
    if USE_DUMMY:
        return jsonify(dummy_auditlogs[:limit])
    logs = get_audit_logs(limit=limit)
    return jsonify([
        {"id": log.id, "timestamp": str(log.timestamp), "event": log.event, "log_type": log.log_type}
        for log in logs
    ])

@app.route("/auditlog", methods=["POST"])
def create_audit_log():
    data = request.json or {}
    event = data.get("event")
    log_type = data.get("log_type", "API")
    add_audit_log(event, log_type)
    return jsonify({"status": "logged", "event": event, "log_type": log_type})

# --- CallCenter endpoints ---
@app.route("/callcenter", methods=["GET"])
def list_call_center_records():
    limit = int(request.args.get("limit", 50))
    return jsonify(_cached_callcenter[:limit])

@app.route("/callcenter", methods=["POST"])
def create_call_center_record():
    data = request.json or {}
    customer_id = data.get("customer_id")
    transcript = data.get("transcript")
    sentiment = data.get("sentiment")
    add_call_center_record(customer_id, transcript, sentiment)
    return jsonify({"status": "recorded", "customer_id": customer_id})

# --- Claims endpoints ---
@app.route("/claims", methods=["GET"])
def list_insurance_claims():
    limit = int(request.args.get("limit", 50))
    return jsonify(_cached_claims[:limit])

@app.route("/claims", methods=["POST"])
def create_insurance_claim():
    data = request.json or {}
    claim_id = data.get("claim_id")
    description = data.get("description")
    intent = data.get("intent")
    add_insurance_claim(claim_id, description, intent)
    return jsonify({"status": "recorded", "claim_id": claim_id})

# --- Big Data endpoint ---
@app.route("/bigdata", methods=["GET"])
def list_big_data_demo():
    limit = int(request.args.get("limit", 50))
    return jsonify(_cached_bigdata[:limit])

# --- Multilingual endpoint ---
@app.route("/multilingual", methods=["GET"])
def list_multilingual_samples():
    limit = int(request.args.get("limit", 50))
    if USE_DUMMY:
        return jsonify(dummy_multilingual[:limit])
    samples = get_multilingual_samples(limit=limit)
    return jsonify([
        {"id": s.id, "lang": s.lang, "text": s.text, "created_at": str(s.created_at)}
        for s in samples
    ])

# --- Speech-to-Text endpoints ---
@app.route("/speechdemo", methods=["GET"])
def list_transcriptions():
    if USE_DUMMY:
        return jsonify(dummy_transcriptions)
    return jsonify([])

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    audio_file = request.files["file"]
    audio_bytes = audio_file.read()
    result = transcriber.transcribe(audio_bytes)
    add_audit_log("Transcribed audio file", "API")
    return jsonify({"transcription": result})

@app.route("/reset_transcription", methods=["POST"])
def reset_transcription_logs():
    import sqlite3
    try:
        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "../speech_to_text/streamiq_logs.db"))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM logs WHERE event LIKE 'Transcription%' OR event LIKE 'Fallback:%'")
        conn.commit()
        conn.close()
        add_audit_log("Transcription logs reset", "SYSTEM")
        return jsonify({"status": "ok", "message": "Transcription logs cleared"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Reset failed: {str(e)}"}), 500

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

@app.route("/mlflow", methods=["GET"])
def list_mlflow_runs():
    experiment_name = request.args.get("experiment_name", "StreamlitPredictionDemo")
    runs = fetch_runs(experiment_name)
    return jsonify(runs)

# --- Reset Demo endpoint ---
@app.route("/reset_demo", methods=["POST"])
def reset_demo():
    try:
        init_db()
        add_audit_log("Demo data reset", "SYSTEM")

        global _cached_callcenter, _cached_claims, _cached_bigdata, _cache_last_refresh
        if USE_DUMMY:
            _cached_callcenter = dummy_callcenter
            _cached_claims = dummy_claims
            _cached_bigdata = dummy_bigdata
        else:
            _cached_callcenter = get_call_center_records(limit=50)
            _cached_claims = get_insurance_claims(limit=50)
            _cached_bigdata = get_big_data_demo(limit=50)

        _cache_last_refresh = datetime.datetime.now()

        return jsonify({"status": "ok", "message": "Demo data reset successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Reset failed: {str(e)}"}), 500

# --- Demo Status endpoint ---
@app.route("/demo_status", methods=["GET"])
def demo_status():
    return jsonify({
        "mode": "Dummy" if USE_DUMMY else "Backend",
        "callcenter_cached": len(_cached_callcenter),
        "claims_cached": len(_cached_claims),
        "bigdata_cached": len(_cached_bigdata),
        "last_refresh": _cache_last_refresh.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
