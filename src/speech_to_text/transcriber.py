from flask import Flask, request, jsonify
import sqlite3
import os
import spacy

# Import your Transcriber
from transcriber import Transcriber

# -------------------------------
# Flask App Initialization
# -------------------------------
app = Flask(__name__)
transcriber = Transcriber()

# -------------------------------
# Database Setup (SQLite)
# -------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "streamiq_logs.db")

def init_db():
    """Initialize SQLite database if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_log(event: str):
    """Insert a log entry into SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (event) VALUES (?)", (event,))
    conn.commit()
    conn.close()

def get_all_logs():
    """Retrieve all logs from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT event, timestamp FROM logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"event": row[0], "timestamp": row[1]} for row in rows]

# Initialize DB at startup
init_db()
add_log("Backend started (Flask)")

# -------------------------------
# NLP Pipelines
# -------------------------------
nlp_en = spacy.load("en_core_web_sm")

def process_english(text):
    doc = nlp_en(text)
    tokens = [token.text for token in doc]
    return f"English tokens: {tokens}"

def process_isizulu(text):
    tokens = text.split()
    if "Sawubona" in tokens:
        return "isiZulu greeting detected"
    return f"isiZulu tokens: {tokens}"

def process_sepedi(text):
    tokens = text.split()
    if "Dumela" in tokens:
        return "Sepedi greeting detected"
    return f"Sepedi tokens: {tokens}"

def process_xitsonga(text):
    tokens = text.split()
    if "Xewani" in tokens:
        return "Xitsonga greeting detected"
    return f"Xitsonga tokens: {tokens}"

# -------------------------------
# Endpoints
# -------------------------------
@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "StreamIQ Backend (Flask) is running"})

@app.route("/process", methods=["POST"])
def process_text():
    data = request.get_json(force=True)
    text = data.get("input", "")
    lang = data.get("lang", "English")

    if not text:
        return jsonify({"error": "Input text is required"}), 400

    if lang == "English":
        output = process_english(text)
    elif lang == "isiZulu":
        output = process_isizulu(text)
    elif lang == "Sepedi":
        output = process_sepedi(text)
    elif lang == "Xitsonga":
        output = process_xitsonga(text)
    else:
        return jsonify({"error": "Unsupported language"}), 400

    add_log(f"Processed text in {lang}")
    return jsonify({"output": output})

@app.route("/logs", methods=["GET"])
def logs():
    logs = get_all_logs()
    return jsonify({"logs": logs})

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    """
    Accept raw audio bytes (wav/mp3) and return transcription.
    """
    if "file" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["file"]
    audio_bytes = audio_file.read()
    result = transcriber.transcribe(audio_bytes)

    add_log("Transcribed audio file")
    return jsonify({"transcription": result})

# -------------------------------
# Run Backend Directly
# -------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
