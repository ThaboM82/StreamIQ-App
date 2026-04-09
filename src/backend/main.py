# src/backend/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import numpy as np

from src.db.connection import get_db
from src.db.models import AuditLog, User

app = FastAPI(title="StreamIQ Backend", version="1.0.0")

# -------------------------------
# Audit Logs Endpoints
# -------------------------------
@app.get("/logs")
def read_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).all()
    return [log.as_dict() for log in logs]

@app.post("/logs/add")
def add_log(action: str, timestamp: str, db: Session = Depends(get_db)):
    try:
        ts = datetime.fromisoformat(timestamp)
    except ValueError:
        return {"error": "Invalid timestamp format. Use YYYY-MM-DD HH:MM:SS"}

    log = AuditLog(action=action, timestamp=ts)
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"message": "Log added successfully", "log": log.as_dict()}

# -------------------------------
# Users Endpoints
# -------------------------------
@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [user.as_dict() for user in users]

@app.post("/users/add")
def add_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User added successfully", "user": user.as_dict()}

# -------------------------------
# Metrics Endpoint with Confusion Matrix
# -------------------------------
@app.get("/metrics")
def get_metrics():
    # Example static metrics for demo purposes
    accuracy = 0.91
    precision = 0.89
    recall = 0.87
    f1_score = 0.88

    # Example confusion matrix (multi-class: Satisfied, Neutral, Dissatisfied)
    # Rows = actual, Columns = predicted
    confusion_matrix = np.array([
        [45, 3, 2],   # Actual Satisfied
        [4, 30, 6],   # Actual Neutral
        [2, 5, 40]    # Actual Dissatisfied
    ]).tolist()

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "confusion_matrix": confusion_matrix,
        "labels": ["Satisfied", "Neutral", "Dissatisfied"]
    }
