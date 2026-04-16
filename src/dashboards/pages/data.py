# src/dashboards/pages/data.py

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def run():
    st.title("📊 Audit Log Viewer")

    # --- Add a new log entry ---
    with st.form("add_log_form"):
        event = st.text_input("Event description")
        log_type = st.selectbox("Log type", ["DASHBOARD", "SYSTEM", "API"])
        submitted = st.form_submit_button("Add Log")

        if submitted and event.strip():
            resp = requests.post(
                f"{API_URL}/auditlog",
                params={"event": event, "log_type": log_type}
            )
            if resp.status_code == 200:
                st.success(f"Log added: {event} ({log_type})")
            else:
                st.error("Failed to add log")

    # --- Show recent logs ---
    st.subheader("Recent Logs")
    resp = requests.get(f"{API_URL}/auditlog", params={"limit": 50})
    if resp.status_code == 200 and resp.json():
        logs = resp.json()
        st.dataframe(logs)
    else:
        st.info("No logs available yet.")
