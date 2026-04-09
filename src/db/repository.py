# src/db/repository.py
from sqlalchemy.orm import Session
from . import models

# --- Call Center Records ---
def get_call_center_records(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.CallCenterRecord).offset(skip).limit(limit).all()

def create_call_center_record(db: Session, record: dict):
    new_record = models.CallCenterRecord(**record)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# --- Insurance Claims ---
def get_insurance_claims(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.InsuranceClaim).offset(skip).limit(limit).all()

def create_insurance_claim(db: Session, claim: dict):
    new_claim = models.InsuranceClaim(**claim)
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim
