import streamlit as st
from datetime import datetime
from src.db.connection import get_db
from src.db.models import AuditLog

def log_action(action: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"action": action, "timestamp": timestamp}
    if "history" not in st.session_state:
        st.session_state["history"] = []
    st.session_state["history"].append(entry)

    db = next(get_db())
    db_entry = AuditLog(action=action, timestamp=datetime.now())
    db.add(db_entry)
    db.commit()

st.title("🎬 Demo Visualization")
log_action("Viewed Demo Visualization page")

st.write("This page can showcase demo predictions or speech-to-text outputs.")
st.success("Demo: Satisfaction score predicted as 0.87")
