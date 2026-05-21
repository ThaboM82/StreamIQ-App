"""
StreamIQ Speech-to-Text Transcriber
-----------------------------------
Handles audio transcription, NLP tokenization, and resilient logging.
Designed for stakeholder demos with graceful fallbacks.
"""

import spacy
import speech_recognition as sr
import sqlite3
import os

# Path to local SQLite database for demo logs
DB_PATH = os.path.join(os.path.dirname(__file__), "streamiq_logs.db")


def add_log(event: str):
    """
    Insert a log entry into the demo database.
    Ensures the logs table exists before writing.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("INSERT INTO logs (event) VALUES (?)", (event,))
    conn.commit()
    conn.close()


class Transcriber:
    """
    Speech-to-Text engine with NLP tokenization.
    Provides resilience for stakeholder demos.
    """

    def __init__(self):
        # Attempt to load SpaCy model; fallback if unavailable
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            self.nlp = None

        # Initialize recognizer
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_bytes: bytes) -> str:
        """
        Convert audio bytes into text.
        Logs success or fallback events for demo resilience.
        """
        try:
            audio_data = sr.AudioData(audio_bytes, sample_rate=16000, sample_width=2)

            try:
                # Primary transcription via Google Speech Recognition
                text = self.recognizer.recognize_google(audio_data)
                add_log("Transcription succeeded")

                # Optional NLP tokenization
                if self.nlp:
                    doc = self.nlp(text)
                    text = " ".join([token.text for token in doc])

                return text

            except sr.UnknownValueError:
                add_log("Fallback: speech not understood")
                return "Audio received but speech was not understood."

            except sr.RequestError:
                add_log("Fallback: service unavailable")
                return "Speech recognition service unavailable. Please try again later."

        except Exception as e:
            add_log(f"Fallback: transcription failed ({e})")
            return f"Transcription failed gracefully: {e}"

