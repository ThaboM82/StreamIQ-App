"""
NLP Package
===========

Provides natural language processing utilities for StreamIQ,
including sentiment analysis and text preprocessing.
"""

# Expose the main sentiment analysis function at package level
from .sentiment import analyze_sentiment

__all__ = [
    "analyze_sentiment",
]
