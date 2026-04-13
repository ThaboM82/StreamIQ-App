import streamlit as st

def init_session_state():
    """Initialize Streamlit session state keys."""
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "language" not in st.session_state:
        st.session_state["language"] = "English"
