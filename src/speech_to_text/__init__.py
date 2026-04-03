"""
Speech-to-Text Package
======================

This package handles audio transcription for StreamIQ.
It provides utilities to convert customer call recordings
into text for downstream NLP and satisfaction prediction.
"""

# Expose main transcription function(s) at package level
from .transcriber import transcribe_audio

__all__ = [
    "transcribe_audio",
]
