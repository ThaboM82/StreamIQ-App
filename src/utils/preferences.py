# src/utils/preferences.py
import sqlite3
import os
import warnings
import pandas as pd
from src.utils.validators import SUPPORTED_THEMES, SUPPORTED_SIDEBAR_STATES, SUPPORTED_PAGES
from src.utils.branding import (
    export_csv_with_branding,
    export_excel_with_branding,
    export_pdf_with_logo,
    cli_confirm
)

warnings.filterwarnings("ignore", category=RuntimeWarning)

# Path to preferences database
DB_PATH = os.path.join("src", "db", "preferences.db")

def _init_db():
    """Ensure preferences table exists."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

def set_preference(key: str, value: str):
    """Set a preference value with validation."""
    _init_db()
    if key == "theme" and value not in SUPPORTED_THEMES:
        raise ValueError(f"Unsupported theme: {value}")
    if key == "sidebar_state" and value not in SUPPORTED_SIDEBAR_STATES:
        raise ValueError(f"Unsupported sidebar state: {value}")
    if key == "last_page" and value not in SUPPORTED_PAGES:
        raise ValueError(f"Unsupported page: {value}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("REPLACE INTO preferences (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_preference(key: str, default: str = None):
    """Retrieve a preference value, fallback to default if not set."""
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT value FROM preferences WHERE key=?", (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default

# --- Theme Preferences ---
def get_theme_preference():
    return get_preference("theme", "light")

def set_theme_preference(theme: str):
    set_preference("theme", theme)

# --- Sidebar Preferences ---
def get_sidebar_state():
    return get_preference("sidebar_state", "expanded")

def set_sidebar_state(state: str):
    set_preference("sidebar_state", state)

# --- Last Page Preferences ---
def get_last_page():
    return get_preference("last_page", "Home")

def set_last_page(page: str):
    set_preference("last_page", page)

# --- Reset Preferences ---
def reset_preferences():
    """Clear all preferences back to defaults."""
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM preferences")
    conn.commit()
    conn.close()

# --- Export Preferences Snapshot ---
def export_preferences(base_filename: str = "preferences"):
    """Export preferences to PDF, Excel, and CSV with branding + summary."""
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM preferences")
    rows = cur.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=["Key", "Value"])
    summary = {"Total Preferences": len(df)}

    pdf_file = f"{base_filename}.pdf"
    xlsx_file = f"{base_filename}.xlsx"
    csv_file = f"{base_filename}.csv"

    export_pdf_with_logo(pdf_file, title="StreamIQ Preferences", df=df, summary=summary)
    export_excel_with_branding(df, xlsx_file, summary=summary, dataset_sheet="Preferences")
    export_csv_with_branding(df, csv_file, summary=summary)

    return {"pdf": pdf_file, "excel": xlsx_file, "csv": csv_file}

# -------------------------------
# Module Load Confirmation
# -------------------------------
cli_confirm("Preferences module loaded")
