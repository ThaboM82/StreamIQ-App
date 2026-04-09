# src/utils/session_state_initializer.py

import streamlit as st

def init_session_state():
    """
    Initialize all StreamIQ session state keys with safe defaults.
    Call this once at the top of each Streamlit page.
    """

    defaults = {
        "history": [],             # interaction log
        "filters": {},             # active filters for dashboard views
        "audit_log": [],           # local audit trail before DB commit
        "user_id": None,           # current user identifier
        "transcriptions": [],      # speech-to-text results
        "predictions": [],         # satisfaction model outputs
        "sentiments": [],          # sentiment analysis results
        "intents": [],             # intent classification results
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
