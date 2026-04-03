"""
Database Models
===============

Defines SQLAlchemy ORM models for StreamIQ.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class CustomerInteraction(Base):
    __tablename__ = "customer_interactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(50), nullable=False)
    transcript = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to sentiment results
    sentiment_results = relationship("SentimentResult", back_populates="interaction")

class SentimentResult(Base):
    __tablename__ = "sentiment_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interaction_id = Column(Integer, ForeignKey("customer_interactions.id"), nullable=False)
    sentiment = Column(String(20), nullable=False)   # e.g., "positive", "negative", "neutral"
    satisfaction_score = Column(Float, nullable=False)
    analyzed_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to interaction
    interaction = relationship("CustomerInteraction", back_populates="sentiment_results")
