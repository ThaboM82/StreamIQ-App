from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "streamiq.db")

# --- Initialize SQLite database ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT,
            lang TEXT,
            output TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            log_type TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Helper: add log ---
def add_log(event, log_type="INFO"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (event, log_type, timestamp) VALUES (?, ?, ?)",
        (event, log_type, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

# --- Simple multilingual processor ---
def process_text(input_text, lang):
    translations = {
        "en": f"Processed English: {input_text}",
        "af": f"Verwerk Afrikaans: {input_text}",
        "zu": f"Ukucubungula isiZulu: {input_text}",
        "nso": f"Tshekatsheko Sepedi: {input_text}",
        "ts": f"Ku tirhisa Xitsonga: {input_text}",
    }
    return translations.get(lang, f"[Unsupported language] {input_text}")

# --- API route: process text ---
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    input_text = data.get("input", "")
    lang = data.get("lang", "en")

    output = process_text(input_text, lang)
    timestamp = datetime.utcnow().isoformat()

    # Save to history
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (input, lang, output, timestamp) VALUES (?, ?, ?, ?)",
        (input_text, lang, output, timestamp)
    )
    conn.commit()
    conn.close()

    # Log event
    add_log(f"Processed text in {lang}", log_type="ACTION")

    return jsonify({"output": output, "timestamp": timestamp})

# --- API route: fetch history ---
@app.route("/history", methods=["GET"])
def history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, input, lang, output, timestamp FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    history_data = [
        {"id": row[0], "input": row[1], "lang": row[2], "output": row[3], "timestamp": row[4]}
        for row in rows
    ]
    return jsonify(history_data)

# --- API route: clear history ---
@app.route("/history", methods=["DELETE"])
def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    add_log("Cleared history table", log_type="ACTION")
    return jsonify({"message": "All history cleared successfully."})

# --- API route: fetch logs ---
@app.route("/logs", methods=["GET"])
def logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, event, log_type, timestamp FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    logs_data = [
        {"id": row[0], "event": row[1], "log_type": row[2], "timestamp": row[3]}
        for row in rows
    ]
    return jsonify({"logs": logs_data})

# --- API route: clear logs ---
@app.route("/logs", methods=["DELETE"])
def clear_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
    return jsonify({"message": "All logs cleared successfully."})

# --- Entry point ---
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)
