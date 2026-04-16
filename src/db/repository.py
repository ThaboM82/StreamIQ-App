import pandas as pd
from src.db.init_db import insert_audit_log, fetch_audit_logs

# -------------------------------
# Audit Log
# -------------------------------
def add_audit_log(event: str, log_type: str = "API"):
    """Insert an audit log entry."""
    insert_audit_log(event, log_type)

class AuditLogRecord:
    def __init__(self, id, timestamp, event, log_type):
        self.id = id
        self.timestamp = timestamp
        self.event = event
        self.log_type = log_type

def get_audit_logs(limit=50):
    """Fetch audit logs as objects."""
    rows = fetch_audit_logs(limit)
    return [AuditLogRecord(id=r[0], timestamp=r[1], event=r[2], log_type=r[3]) for r in rows]

# -------------------------------
# Call Center Records
# -------------------------------
def get_call_center_records(limit=50):
    """Return demo call center records as a DataFrame."""
    return pd.DataFrame({
        "Agent": ["Alice", "Bob", "Charlie"],
        "Calls": [120, 95, 110],
        "Satisfaction": [0.92, 0.85, 0.88]
    })

def add_call_center_record(customer_id: str, transcript: str, sentiment: str):
    """Demo: pretend to add a call center record, return dict."""
    return {
        "customer_id": customer_id,
        "transcript": transcript,
        "sentiment": sentiment,
        "status": "added"
    }

# -------------------------------
# Insurance Claims
# -------------------------------
def get_insurance_claims(limit=50):
    """Return demo insurance claims as a DataFrame."""
    return pd.DataFrame({
        "ClaimID": [101, 102, 103],
        "Amount": [5000, 12000, 7500],
        "Status": ["Approved", "Pending", "Rejected"]
    })

def add_insurance_claim(claim_id: str, description: str, intent: str):
    """Demo: pretend to add an insurance claim, return dict."""
    return {
        "claim_id": claim_id,
        "description": description,
        "intent": intent,
        "status": "added"
    }

# -------------------------------
# Big Data Demo
# -------------------------------
def get_big_data_demo(limit=50):
    """Return demo big data records as a DataFrame."""
    return pd.DataFrame({
        "RecordID": range(1, 6),
        "Category": ["Banking", "Insurance", "Call Center", "Banking", "Insurance"],
        "Value": [1000, 2500, 300, 1500, 4000]
    })

# -------------------------------
# Multilingual Samples
# -------------------------------
def get_multilingual_samples(limit=50):
    """Return demo multilingual text samples."""
    return {
        "English": "Hello, how can I help you today?",
        "isiZulu": "Sawubona, ngingakusiza kanjani namuhla?",
        "Sepedi": "Dumela, nka go thuša bjang lehono?",
        "Xitsonga": "Xewani, ndzi nga ku pfuna njhani namuntlha?"
    }
