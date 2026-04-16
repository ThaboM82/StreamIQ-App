import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../streamiq.db")

# -------------------------------
# Database Initialization
# -------------------------------
def init_db():
    """Initialize SQLite database with demo tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # AuditLog table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event TEXT,
            log_type TEXT
        )
    """)

    # Call Center table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS call_center (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            transcript TEXT,
            sentiment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insurance Claims table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insurance_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim_id TEXT,
            description TEXT,
            intent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# -------------------------------
# AuditLog helpers
# -------------------------------
def insert_audit_log(event: str, log_type: str = "SYSTEM"):
    """Insert a new audit log entry."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audit_log (event, log_type) VALUES (?, ?)", (event, log_type))
    conn.commit()
    conn.close()

def fetch_audit_logs(limit=50):
    """Fetch audit logs from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, event, log_type FROM audit_log ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------
# Call Center helpers
# -------------------------------
def insert_call_center_record(customer_id: str, transcript: str, sentiment: str):
    """Insert a new call center record into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO call_center (customer_id, transcript, sentiment)
        VALUES (?, ?, ?)
    """, (customer_id, transcript, sentiment))
    conn.commit()
    conn.close()

def fetch_call_center_records(limit=50):
    """Fetch call center records from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer_id, transcript, sentiment, created_at FROM call_center ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------
# Insurance Claims helpers
# -------------------------------
def insert_insurance_claim(claim_id: str, description: str, intent: str):
    """Insert a new insurance claim into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO insurance_claims (claim_id, description, intent)
        VALUES (?, ?, ?)
    """, (claim_id, description, intent))
    conn.commit()
    conn.close()

def fetch_insurance_claims(limit=50):
    """Fetch insurance claims from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, claim_id, description, intent, created_at FROM insurance_claims ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows
