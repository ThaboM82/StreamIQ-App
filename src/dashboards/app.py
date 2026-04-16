import sys
import os
import streamlit as st
import pandas as pd
import requests
import altair as alt
from datetime import datetime

# Add project root (C:\StreamIQ App) to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# imports from src.utils
from src.utils.helpers import log_history, show_history
from src.utils.session_state_initializer import init_session_state
from src.utils.validators import validate_language, validate_non_empty, validate_domain
from src.utils.logger import init_db, add_log, get_logs, clear_logs

# -------------------------------
# Initialization
# -------------------------------
init_session_state()
init_db()

# Backend URL (Flask)
BACKEND_URL = "http://127.0.0.1:8000"

# -------------------------------
# Page Config & Sidebar
# -------------------------------
st.set_page_config(
    page_title="StreamIQ Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Branding
st.sidebar.image("assets/streamiq_logo.png", use_column_width=True)
st.sidebar.markdown("### StreamIQ")
st.sidebar.caption("Enterprise NLP Demo")

# Theme Toggle
theme = st.sidebar.radio("Theme", ["🌞 Light", "🌙 Dark"], index=0)

if theme == "🌞 Light":
    primary_color = "#0078D4"
    secondary_color = "#00B294"
    background_color = "#F5F5F5"
    text_color = "#2B2B2B"
    grid_color = "#E0E0E0"
    row_even = "#FFFFFF"
    row_odd = "#F0F0F0"
else:
    primary_color = "#00B294"
    secondary_color = "#0078D4"
    background_color = "#1E1E1E"
    text_color = "#FFFFFF"
    grid_color = "#444444"
    row_even = "#2B2B2B"
    row_odd = "#1E1E1E"

# Apply theme styling
st.markdown(
    f"""
    <style>
        .main {{
            background-color: {background_color};
            color: {text_color};
        }}
        .stButton>button {{
            background-color: {primary_color};
            color: white;
            border-radius: 4px;
            border: none;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Backend Health Check
try:
    response = requests.get(f"{BACKEND_URL}/")
    if response.status_code == 200:
        st.sidebar.success("✅ Backend is running")
        st.sidebar.caption(f"Last checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.sidebar.error("❌ Backend not responding")
except Exception:
    st.sidebar.error("❌ Backend unreachable")

# Sleek two-level navigation
category = st.sidebar.selectbox(
    "Category",
    ["🏠 Home", "📊 Data", "🤖 NLP", "🎓 Training", "📈 Logs", "⚙️ Settings & ℹ️ Info"]
)

if category == "🏠 Home":
    page = "Home"
elif category == "📊 Data":
    page = st.sidebar.radio("Navigate", ["⚙️ Pipeline", "📞 Call Center Results", "📑 Insurance Claims Results", "📊 Big Data Demo"])
elif category == "🤖 NLP":
    page = st.sidebar.radio("Navigate", ["🌍 Multilingual Processor", "📊 Mock Data Demo", "🧠 NLP Demo", "🎯 Model Prediction"])
elif category == "🎓 Training":
    page = st.sidebar.radio("Navigate", ["🧪 Training Demo", "📈 Model Evaluation"])
elif category == "📈 Logs":
    page = st.sidebar.radio("Navigate", ["📝 Backend Logs", "📜 History"])
elif category == "⚙️ Settings & ℹ️ Info":
    page = st.sidebar.radio("Navigate", ["⚙️ Settings", "ℹ️ About"])
else:
    page = "Home"

st.sidebar.markdown("---")
st.sidebar.success("Enterprise‑ready demo pipeline 🚀")

# -------------------------------
# Pages
# -------------------------------

if page == "Home":
    st.header("🏠 Welcome to StreamIQ")
    st.write("""
    StreamIQ is an enterprise-ready NLP demo platform.
    Use the sidebar to explore:
    - 📊 Data exploration
    - 🤖 NLP prediction
    - 🎓 Training simulation
    - 📈 Evaluation metrics
    - 📜 Audit trail
    """)

elif page == "⚙️ Pipeline":
    st.header("⚙️ Pipeline Status")
    st.info("Pipeline running smoothly (demo placeholder).")
    add_log("Viewed Pipeline Status", log_type="INFO")

elif page == "📞 Call Center Results":
    st.header("📞 Call Center Analytics")

    # --- Form to add new record ---
    with st.form("callcenter_form"):
        customer_id = st.text_input("Customer ID")
        transcript = st.text_area("Transcript")
        sentiment = st.selectbox("Sentiment", ["Positive", "Neutral", "Negative"])
        submitted = st.form_submit_button("Add Record")

        if submitted:
            payload = {"customer_id": customer_id, "transcript": transcript, "sentiment": sentiment}
            response = requests.post(f"{BACKEND_URL}/callcenter", json=payload)
            if response.ok:
                st.success("Record added successfully!")
                log_history(f"Added Call Center Record for {customer_id}")
                add_log("Added Call Center Record", log_type="ACTION")
            else:
                st.error("Failed to add record.")

    # --- Display records ---
    try:
        response = requests.get(f"{BACKEND_URL}/callcenter?limit=50")
        if response.ok:
            df = pd.DataFrame(response.json())
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download Data (CSV)", df.to_csv(index=False), "call_center_results.csv")
        else:
            st.error("Failed to fetch records.")
    except Exception as e:
        st.error(f"Error fetching records: {e}")

elif page == "📑 Insurance Claims Results":
    st.header("📑 Insurance Claims Analytics")

    # --- Form to add new claim ---
    with st.form("claims_form"):
        claim_id = st.text_input("Claim ID")
        description = st.text_area("Description")
        intent = st.selectbox("Intent", ["Approval", "Rejection", "Pending"])
        submitted = st.form_submit_button("Add Claim")

        if submitted:
            payload = {"claim_id": claim_id, "description": description, "intent": intent}
            response = requests.post(f"{BACKEND_URL}/claims", json=payload)
            if response.ok:
                st.success("Claim added successfully!")
                log_history(f"Added Insurance Claim {claim_id}")
                add_log("Added Insurance Claim", log_type="ACTION")
            else:
                st.error("Failed to add claim.")

    # --- Display claims ---
    try:
        response = requests.get(f"{BACKEND_URL}/claims?limit=50")
        if response.ok:
            df = pd.DataFrame(response.json())
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download Claims (CSV)", df.to_csv(index=False), "insurance_claims.csv")
        else:
            st.error("Failed to fetch claims.")
    except Exception as e:
        st.error(f"Error fetching claims: {e}")

elif page == "📊 Big Data Demo":
    st.header("📊 Big Data Demo")
    try:
        response = requests.get(f"{BACKEND_URL}/bigdata?limit=50")
        if response.ok:
            df = pd.DataFrame(response.json())
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download Big Data (CSV)", df.to_csv(index=False), "big_data_demo.csv")
        else:
            st.error("Failed to fetch Big Data Demo records.")
    except Exception as e:
        st.error(f"Error fetching Big Data Demo: {e}")

elif page == "🌍 Multilingual Processor":
    st.header("🌍 Multilingual Processor")

    text = st.text_area("Enter text:")
    lang = st.selectbox("Select language", ["English", "isiZulu", "Sepedi", "Xitsonga"])
    if st.button("Process Text"):
        payload = {"input": text, "lang": lang}
        response = requests.post(f"{BACKEND_URL}/process", json=payload)
        if response.ok:
            result = response.json()
            st.success(result.get("output", "No output returned"))
            log_history(f"Processed text in {lang}")
            add_log(f"Processed text in {lang}", log_type="ACTION")
        else:
            st.error("Failed to process text.")

elif page == "📊 Mock Data Demo":
    st.header("📊 Mock Data Demo")
    st.info("Placeholder for mock data demo.")

elif page == "🧠 NLP Demo":
    st.header("🧠 NLP Demo")
    st.info("Placeholder for NLP demo.")

elif page == "🎯 Model Prediction":
    from src.dashboards.pages import ModelPrediction
    ModelPrediction.run()

elif page == "🧪 Training Demo":
    from src.dashboards.pages import training
    training.run()

elif page == "📈 Model Evaluation":
    from src.dashboards.pages import evaluate
    evaluate.run()

elif page == "📝 Backend Logs":
    st.header("📝 Backend Logs")
    try:
        response = requests.get(f"{BACKEND_URL}/auditlog?limit=50")
        if response.ok:
            logs = response.json()
            df = pd.DataFrame(logs)
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download Logs (CSV)", df.to_csv(index=False), "backend_logs.csv")
            log_history("Viewed Backend Logs")
            add_log("Viewed Backend Logs", log_type="INFO")
        else:
            st.error("Failed to fetch logs.")
    except Exception as e:
        st.error(f"Error fetching logs: {e}")

elif page == "📜 History":
    st.header("📜 History")
    show_history()
    st.info("Audit trail of user actions and backend events.")
    # Optional: add export
    st.download_button("⬇️ Export History (CSV)", pd.DataFrame(get_logs()).to_csv(index=False), "history.csv")

elif page == "⚙️ Settings":
    st.header("⚙️ Settings")
    theme_choice = st.selectbox("Theme Preference", ["Light", "Dark"])
    st.success(f"Theme set to {theme_choice}")
    st.info("Additional configuration options can be added here.")

elif page == "ℹ️ About":
    st.header("ℹ️ About StreamIQ Demo")
    st.markdown("""
    **StreamIQ** is an enterprise-ready NLP demo platform.

    - **Frontend:** Streamlit multi-page dashboard with modular navigation  
    - **Backend:** Flask API running on `http://localhost:8000`  
    - **Features:**  
        - Multilingual text processing (English, isiZulu, Sepedi, Xitsonga)  
        - Call center and insurance claims analytics  
        - Big Data demo integration  
        - Persistent history logging with SQLite  
        - Exportable logs and audit trail  

    Designed for **stakeholder presentations** and **enterprise polish**.
    """)
