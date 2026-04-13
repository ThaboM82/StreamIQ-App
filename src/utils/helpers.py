import sqlite3
import os
import streamlit as st

# Use the same DB path as backend
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "streamiq", "streamiq_logs.db")

def log_history(entry: str):
    """Insert a dashboard action into the unified logs table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logs (event) VALUES (?)", (entry,))
    conn.commit()
    conn.close()

def show_history(limit: int = 50):
    """Display recent logs (backend + dashboard) in Streamlit."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT event, timestamp FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()

    if rows:
        st.dataframe([{"event": row[0], "timestamp": row[1]} for row in rows])
    else:
        st.info("No history available yet.")

