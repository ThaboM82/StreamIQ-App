"""
API Package
===========

This package defines the REST API routes for StreamIQ.
It exposes endpoints for:
- Health checks
- Speech-to-Text transcription
- NLP sentiment and intent analysis
- Satisfaction prediction
"""

# Expose the API blueprint at package level
from .routes import api_blueprint

__all__ = [
    "api_blueprint",
]
