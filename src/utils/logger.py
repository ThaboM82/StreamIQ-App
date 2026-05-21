# src/utils/logger.py
import sqlite3
import os
from datetime import datetime
from src.utils.branding import cli_confirm

# Path to logs database
DB_PATH = os.path.join("src", "db", "logs.db")

def _init_logs():
    """Ensure logs table exists."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event TEXT,
            log_type TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_log(event: str, log_type: str = "INFO"):
    """Insert a new log entry."""
    _init_logs()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (timestamp, event, log_type) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), event, log_type)
    )
    conn.commit()
    conn.close()

def show_history(limit: int = 50):
    """Retrieve recent logs."""
    _init_logs()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT timestamp, event, log_type FROM logs ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def clear_logs():
    """Delete all logs."""
    _init_logs()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM logs")
    conn.commit()
    conn.close()

# -------------------------------
# Module Load Confirmation
# -------------------------------
cli_confirm("Logger module loaded")

