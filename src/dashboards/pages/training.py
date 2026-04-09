import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
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

st.title("📈 Training Metrics")
log_action("Viewed Training Metrics page")

epochs = np.arange(1, 11)
accuracy = np.linspace(0.6, 0.95, 10)

fig, ax = plt.subplots()
ax.plot(epochs, accuracy, marker="o")
ax.set_xlabel("Epoch")
ax.set_ylabel("Accuracy")
ax.set_title("Model Training Accuracy")

st.pyplot(fig)
