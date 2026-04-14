import sqlite3
import os
from datetime import datetime

# Resolve the repo root (two levels up from utils)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Point to the backend database file
DB_FILE = os.path.join(BASE_DIR, "backend", "streamiq.db")

# -------------------------------
# Database Initialization
# -------------------------------
def init_db():
    """Initialize the SQLite database with logs table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event TEXT NOT NULL,
            log_type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -------------------------------
# Add Log Entry
# -------------------------------
def add_log(event: str, log_type: str = "BACKEND"):
    """
    Insert a new log entry into the database.
    Default log_type is 'BACKEND' to distinguish backend events.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (timestamp, event, log_type) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), event, log_type.upper())
    )
    conn.commit()
    conn.close()

# -------------------------------
# Get Logs
# -------------------------------
def get_logs(limit: int = 100):
    """Retrieve logs from the database, newest first."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, event, log_type FROM logs ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [{"timestamp": r[0], "event": r[1], "log_type": r[2]} for r in rows]

# -------------------------------
# Clear Logs (optional for demos)
# -------------------------------
def clear_logs():
    """Delete all logs from the database (useful for demo resets)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
