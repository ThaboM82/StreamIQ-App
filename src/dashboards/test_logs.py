import streamlit as st
from src.utils.helpers import log_history, show_history
from src.utils.logger import clear_logs  # make sure clear_logs exists in your logger

st.title("StreamIQ Log Test")

# Button to add a test entry
if st.button("Add Test Log"):
    log_history("Test entry from dashboard")
    st.success("Log entry added!")

# Button to clear all logs
if st.button("Clear Logs"):
    clear_logs()
    st.warning("All logs have been cleared.")

# Show recent history
st.subheader("Recent Logs")
show_history(limit=10)
