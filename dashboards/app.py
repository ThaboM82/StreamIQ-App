import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Import DB logging
from src.db.connection import get_db
from src.db.models import AuditLog

# --- Sidebar History Tracker ---
if "history" not in st.session_state:
    st.session_state["history"] = []

def log_action(action: str):
    """Log action to session and persist to DB."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"action": action, "timestamp": timestamp}
    st.session_state["history"].append(entry)

    # Persist to DB
    db = next(get_db())
    db_entry = AuditLog(action=action, timestamp=datetime.now())
    db.add(db_entry)
    db.commit()

def export_history_csv():
    df = pd.DataFrame(st.session_state["history"])
    return df.to_csv(index=False).encode("utf-8")

# --- Sidebar ---
st.sidebar.title("📜 Audit Trail")
for entry in st.session_state["history"]:
    st.sidebar.write(f"{entry['timestamp']} - {entry['action']}")

if st.sidebar.button("Clear History"):
    st.session_state["history"].clear()
    log_action("History cleared")

st.sidebar.download_button(
    label="⬇️ Export History CSV",
    data=export_history_csv(),
    file_name="audit_history.csv",
    mime="text/csv"
)

# --- Main Tabs ---
st.title("StreamIQ Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Pipeline", "Call Center", "Insurance Claims", "History", "Settings", "Evaluation"
])

with tab1:
    st.header("Pipeline Overview")
    log_action("Viewed Pipeline tab")
    st.write("This section shows the NLP pipeline stages.")

with tab2:
    st.header("Call Center Data")
    log_action("Viewed Call Center tab")
    df = pd.DataFrame({
        "CallID": [1, 2, 3],
        "Sentiment": ["Positive", "Negative", "Neutral"],
        "Duration": [300, 450, 200]
    })
    st.dataframe(df)
    st.download_button("⬇️ Export Call Center CSV", df.to_csv(index=False), "call_center.csv")

with tab3:
    st.header("Insurance Claims")
    log_action("Viewed Insurance Claims tab")
    claims = pd.DataFrame({
        "ClaimID": [101, 102, 103],
        "Status": ["Approved", "Pending", "Rejected"],
        "Amount": [5000, 12000, 3000]
    })
    st.dataframe(claims)
    st.download_button("⬇️ Export Claims CSV", claims.to_csv(index=False), "claims.csv")

with tab4:
    st.header("Audit History")
    log_action("Viewed History tab")
    st.dataframe(pd.DataFrame(st.session_state["history"]))

with tab5:
    st.header("Settings")
    log_action("Viewed Settings tab")
    st.write("Configuration options go here.")

with tab6:
    st.header("Evaluation Metrics")
    log_action("Viewed Evaluation tab")

    try:
        metrics = open("data/metrics.txt").read()
        st.text(metrics)
    except FileNotFoundError:
        st.warning("metrics.txt not found")

    try:
        cm = np.load("data/confusion_matrix.npy")
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        st.pyplot(fig)
    except FileNotFoundError:
        st.warning("confusion_matrix.npy not found")
