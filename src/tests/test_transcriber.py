import pytest
from src.speech_to_text.transcriber import Transcriber

def test_transcriber_returns_string():
    transcriber = Transcriber()
    audio_sample = b"fake audio bytes"
    result = transcriber.transcribe(audio_sample)
    assert isinstance(result, str)
    assert len(result) > 0

def test_transcriber_handles_empty_input():
    transcriber = Transcriber()
    result = transcriber.transcribe(b"")
    assert isinstance(result, str)
