"""
Speech-to-Text Transcriber Module
=================================

Provides a simple wrapper for speech-to-text transcription.
"""

import speech_recognition as sr

class Transcriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio from raw bytes.

        Parameters
        ----------
        audio_bytes : bytes
            Audio file content (wav/mp3).

        Returns
        -------
        str
            Transcribed text.
        """
        try:
            # Convert bytes to AudioData
            import io
            audio_file = sr.AudioFile(io.BytesIO(audio_bytes))
            with audio_file as source:
                audio = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio)
        except Exception as e:
            return f"Transcription failed: {e}"
