# src/db/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .connection import Base

class CallCenterRecord(Base):
    __tablename__ = "call_center_records"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True)
    transcript = Column(Text)
    sentiment = Column(String(20))
    created_at = Column(DateTime)

class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String(50), unique=True, index=True)
    description = Column(Text)
    intent = Column(String(50))
    created_at = Column(DateTime)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event = Column(String(255))
    log_type = Column(String(50))
