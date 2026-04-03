"""
Speech-to-Text Transcriber
==========================

Provides a simple interface for converting audio files
into text for downstream NLP analysis in StreamIQ.
"""

import speech_recognition as sr

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file into text.

    Parameters
    ----------
    file_path : str
        Path to the audio file (e.g., .wav, .mp3).

    Returns
    -------
    str
        Transcribed text from the audio.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            # Using Google's free API for demo purposes
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "[Unintelligible audio]"
    except sr.RequestError as e:
        return f"[API error: {e}]"
    except Exception as e:
        return f"[Transcription failed: {e}]"
