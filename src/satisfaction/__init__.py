"""
Satisfaction Package
====================

Provides customer satisfaction scoring utilities for StreamIQ.
"""

# Expose the main scoring function at package level
from .scorer import calculate_satisfaction_score

__all__ = [
    "calculate_satisfaction_score",
]
