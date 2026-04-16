import sqlite3
import os
import streamlit as st
from src.utils.logger import init_db  # reuse the same init logic

# Resolve the repo root (two levels up from utils)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Point to the backend database file
DB_PATH = os.path.join(BASE_DIR, "backend", "streamiq.db")

def _get_connection():
    """Ensure DB is initialized and return a connection."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("SELECT 1 FROM logs LIMIT 1;")
    except sqlite3.OperationalError:
        # Table doesn't exist → initialize
        init_db()
    return conn

def log_history(entry: str):
    """Insert a dashboard action into the unified logs table."""
    conn = _get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (timestamp, event, log_type) VALUES (datetime('now'), ?, ?)",
        (entry, "DASHBOARD"),
    )
    conn.commit()
    conn.close()

def show_history(limit: int = 50):
    """Display recent logs (backend + dashboard) in Streamlit."""
    conn = _get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT event, timestamp, log_type FROM logs ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = c.fetchall()
    conn.close()

    if rows:
        st.dataframe(
            [{"event": row[0], "timestamp": row[1], "log_type": row[2]} for row in rows]
        )
    else:
        st.info("No history available yet.")
