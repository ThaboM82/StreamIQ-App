# src/utils/loaders.py
import requests
import streamlit as st
import pandas as pd
from datetime import datetime

# ✅ Dummy datasets for fallback/demo mode
from src.db.dummy_data import (
    dummy_callcenter,
    dummy_claims,
    dummy_bigdata,
    dummy_multilingual,
    dummy_transcriptions,
    dummy_auditlogs,
    dummy_bank_records,
    dummy_insurance_records,
    dummy_callcenter_nlp,
)

# ✅ Import init_db directly from db, clear_logs from logger, reset_preferences from preferences
from src.db.init_db import init_db
from src.utils.logger import clear_logs
from src.utils.preferences import reset_preferences

# --- Global toggle ---
USE_DUMMY = True   # Set to False to use backend, True to force dummy datasets
BACKEND_URL = "http://127.0.0.1:8000"

def _fallback(dummy):
    """Helper to return dummy dataset with timestamp as DataFrame."""
    return pd.DataFrame(dummy), datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _wrap_response(resp_json):
    """Ensure backend JSON is converted to DataFrame with timestamp."""
    try:
        return pd.DataFrame(resp_json), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return pd.DataFrame(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_loader(fetch_fn, demo_data=None):
    """
    Wraps a backend fetch function with tuple return + demo fallback.
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        data = fetch_fn()
        if data:
            return pd.DataFrame(data), ts
        else:
            return pd.DataFrame(), ts
    except Exception:
        if demo_data is not None:
            return pd.DataFrame(demo_data), ts
        return pd.DataFrame(), ts

# --- Call Center Loader ---
@st.cache_data
def load_call_center(limit: int = 10):
    if USE_DUMMY:
        return _fallback(dummy_callcenter)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/callcenter?limit={limit}", timeout=10).json(),
                       demo_data=dummy_callcenter)

# --- Claims Loader ---
@st.cache_data
def load_claims(limit=10):
    if USE_DUMMY:
        return _fallback(dummy_claims)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/claims?limit={limit}", timeout=10).json(),
                       demo_data=dummy_claims)

# --- Big Data Loader ---
@st.cache_data
def load_bigdata(limit=10):
    if USE_DUMMY:
        return _fallback(dummy_bigdata)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/bigdata?limit={limit}", timeout=10).json(),
                       demo_data=dummy_bigdata)

# --- Multilingual Loader ---
@st.cache_data
def load_multilingual(limit=10):
    if USE_DUMMY:
        return _fallback(dummy_multilingual)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/multilingual?limit={limit}", timeout=10).json(),
                       demo_data=dummy_multilingual)

# --- Speech-to-Text Loader ---
@st.cache_data
def load_transcriptions():
    if USE_DUMMY:
        return _fallback(dummy_transcriptions)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/speechdemo", timeout=10).json(),
                       demo_data=dummy_transcriptions)

# --- Audit Logs Loader ---
@st.cache_data
def load_audit_logs(limit=50):
    if USE_DUMMY:
        return _fallback(dummy_auditlogs)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/auditlog?limit={limit}", timeout=10).json(),
                       demo_data=dummy_auditlogs)

# --- Banking Loader ---
@st.cache_data
def load_bank_records(limit=10):
    if USE_DUMMY:
        return _fallback(dummy_bank_records)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/banking?limit={limit}", timeout=10).json(),
                       demo_data=dummy_bank_records)

# --- Insurance Loader ---
@st.cache_data
def load_insurance_records(limit=10):
    if USE_DUMMY:
        return _fallback(dummy_insurance_records)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/insurance?limit={limit}", timeout=10).json(),
                       demo_data=dummy_insurance_records)

# --- Call Center NLP Loader ---
@st.cache_data
def load_callcenter_nlp(limit=10):
    if USE_DUMMY:
        return _fallback(dummy_callcenter_nlp)
    return safe_loader(lambda: requests.get(f"{BACKEND_URL}/callcenter_nlp?limit={limit}", timeout=10).json(),
                       demo_data=dummy_callcenter_nlp)

# -------------------------------
# Module Load Confirmation
# -------------------------------
from src.utils.branding import cli_confirm
cli_confirm("Loaders module loaded")




