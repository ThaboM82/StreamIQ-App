"""
Database Package
================

Provides database connection utilities and models for StreamIQ.
"""

# Expose the main connection function at package level
from .connection import get_db_connection

__all__ = [
    "get_db_connection",
]
