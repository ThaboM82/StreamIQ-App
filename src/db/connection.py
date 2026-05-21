# src/db/connection.py
import os, sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Ensure project root is on Python path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DB_PATH = os.path.join(PROJECT_ROOT, "data", "streamiq.db")

# --- SQLAlchemy setup ---
Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

# --- ORM model ---
class ProcessedTranscript(Base):
    __tablename__ = "processed_transcripts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

# --- DB init ---
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)

# --- Insert single record ---
def insert_transcript(text: str, sentiment: str):
    with SessionLocal() as session:
        transcript = ProcessedTranscript(text=text, sentiment=sentiment)
        session.add(transcript)
        session.commit()
        return transcript.id

# --- Insert batch ---
def insert_transcripts_batch(records):
    """records = [(text, sentiment), ...]"""
    with SessionLocal() as session:
        objs = [ProcessedTranscript(text=t, sentiment=s) for t, s in records]
        session.add_all(objs)
        session.commit()
        return [obj.id for obj in objs]

# --- Query counts ---
def get_sentiment_counts():
    with SessionLocal() as session:
        results = (
            session.query(ProcessedTranscript.sentiment, func.count(ProcessedTranscript.id))
            .group_by(ProcessedTranscript.sentiment)
            .all()
        )
        return [{"category": s, "value": c} for s, c in results]

def reset_db():
    """Delete all transcripts from the database."""
    with SessionLocal() as session:
        session.query(ProcessedTranscript).delete()
        session.commit()
