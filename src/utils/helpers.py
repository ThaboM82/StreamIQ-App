import sqlite3
import os
import streamlit as st
import warnings
import pandas as pd
import src.utils.loaders as loaders
from src.db.init_db import init_db          # ✅ import from db, not logger
from src.utils.logger import clear_logs, reset_preferences
from src.utils.branding import (
    export_csv_with_branding,
    export_excel_with_branding,
    export_pdf_with_logo
)

# Suppress RuntimeWarning about re-importing helpers
warnings.filterwarnings(
    "ignore",
    message=".*src.utils.helpers.*",
    category=RuntimeWarning
)

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

# -------------------------------
# Logging Helpers
# -------------------------------
def log_event(event: str, log_type: str = "DASHBOARD"):
    """Insert an event into the unified logs table."""
    conn = _get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (timestamp, event, log_type) VALUES (datetime('now'), ?, ?)",
        (event, log_type),
    )
    conn.commit()
    conn.close()

def log_history(entry: str):
    """Legacy alias for dashboard logging."""
    log_event(entry, log_type="DASHBOARD")

# -------------------------------
# History Retrieval
# -------------------------------
def show_history(limit: int = 50):
    """
    Fetch recent logs (backend + dashboard).
    Returns list of dicts for reuse in Streamlit or backend.
    """
    # Dummy mode fallback
    if loaders.USE_DUMMY:
        return [
            {"event": "Dummy log entry", "timestamp": "2026-04-29 10:00:00", "log_type": "DUMMY"},
            {"event": "Viewed Call Center Demo", "timestamp": "2026-04-29 10:05:00", "log_type": "INFO"},
            {"event": "Ran Feedback Analysis", "timestamp": "2026-04-29 10:10:00", "log_type": "INFO"},
        ]

    conn = _get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT event, timestamp, log_type FROM logs ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = c.fetchall()
    conn.close()

    return [{"event": row[0], "timestamp": row[1], "log_type": row[2]} for row in rows]

# -------------------------------
# Reset Helpers
# -------------------------------
def reset_history_and_preferences():
    """Clear all logs and reset preferences in one call."""
    clear_logs()
    reset_preferences()

# -------------------------------
# Export Helpers
# -------------------------------
def export_history(base_filename: str = "history", limit: int = 50):
    """
    Export history logs with branding in CSV, Excel, and PDF formats.
    Returns dictionary of filenames.
    """
    logs = show_history(limit=limit)
    df = pd.DataFrame(logs)

    summary = {
        "Total Logs": len(df),
        "Log Types": df["log_type"].nunique() if not df.empty else 0,
        "Last Event": df["event"].iloc[0] if not df.empty else "None"
    }

    pdf_file = f"{base_filename}.pdf"
    xlsx_file = f"{base_filename}.xlsx"
    csv_file = f"{base_filename}.csv"

    export_pdf_with_logo(pdf_file, title="StreamIQ Log History", df=df, summary=summary)
    export_excel_with_branding(df, xlsx_file, summary=summary, dataset_sheet="Logs")
    export_csv_with_branding(df, csv_file, summary=summary)

    return {"pdf": pdf_file, "excel": xlsx_file, "csv": csv_file}

# -------------------------------
# CLI Entry Point
# -------------------------------
if __name__ == "__main__":
    print("Resetting history and preferences...")
    reset_history_and_preferences()
    print("Done.")

# -------------------------------
# Module Load Confirmation
# -------------------------------
from src.utils.branding import cli_confirm
cli_confirm("Logger module loaded")
