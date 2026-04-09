import streamlit as st
import pandas as pd
from datetime import datetime
from src.db.connection import get_db
from src.db.models import AuditLog

# --- Logging helper ---
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

# --- Page content ---
st.title("📊 Data Overview")
log_action("Viewed Data Overview page")

df = pd.DataFrame({
    "CallID": [1, 2, 3],
    "Sentiment": ["Positive", "Negative", "Neutral"],
    "Duration": [300, 450, 200]
})

st.write("Here’s a sample of call center data:")
st.dataframe(df)

st.download_button("⬇️ Export Data CSV", df.to_csv(index=False), "data_overview.csv")
