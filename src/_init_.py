"""
StreamIQ Core Package
=====================

This package contains the core modules for StreamIQ:
- API (Flask routes)
- Database (SQLAlchemy models + connection)
- Speech-to-Text (audio transcription)
- NLP (sentiment + intent classification)
- Satisfaction prediction
- Utilities (logging, helpers)

Convenience imports are provided so you can do:
    from src import create_app, analyze_sentiment, classify_intent, predict_satisfaction
instead of deep paths.
"""

# Expose key functions and classes at package level
from .app import create_app
from .nlp.sentiment import analyze_sentiment
from .nlp.intent import classify_intent
from .satisfaction.predictor import predict_satisfaction

__all__ = [
    "create_app",
    "analyze_sentiment",
    "classify_intent",
    "predict_satisfaction",
]
