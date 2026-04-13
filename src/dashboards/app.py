import sys
import os

# Add project root (C:\StreamIQ App) to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import requests

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

st.sidebar.title("📂 StreamIQ Navigation")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "⚙️ Pipeline",
        "📞 Call Center Results",
        "📑 Insurance Claims Results",
        "🌍 Multilingual Processor",
        "📊 Mock Data Demo",
        "🧠 NLP Demo",
        "📝 Logs",
        "📜 History",
        "⚙️ Settings",
        "ℹ️ About"
    ]
)

# Sidebar polish sections
st.sidebar.markdown("### 🔎 Data Exploration")
st.sidebar.info("Explore datasets and Spark summaries.")
st.sidebar.markdown("- Call Center Results\n- Insurance Claims Results")

st.sidebar.markdown("### 🤖 NLP & Prediction")
st.sidebar.info("Run multilingual processing and NLP demos.")
st.sidebar.markdown("- Multilingual Processor\n- NLP Demo")

st.sidebar.markdown("### 📊 Mock Data")
st.sidebar.info("Explore multilingual mock datasets.")
st.sidebar.markdown("- Mock Data Demo")

st.sidebar.markdown("### 📈 Evaluation & Logs")
st.sidebar.info("View pipeline status and backend logs.")
st.sidebar.markdown("- Pipeline\n- Logs")

st.sidebar.markdown("### 📜 Audit Trail")
st.sidebar.info("View and export history.")
st.sidebar.markdown("- History")

st.sidebar.markdown("### ⚙️ Settings & Info")
st.sidebar.markdown("- Settings\n- About")

st.sidebar.markdown("---")
st.sidebar.success("Enterprise‑ready demo pipeline 🚀")

# -------------------------------
# Pages
# -------------------------------

if page == "Home":
    st.header("🏠 Welcome to StreamIQ")
    st.write("""
    This dashboard showcases the full StreamIQ demo pipeline:
    - 📊 Big Data exploration with Spark
    - 🤖 NLP intent prediction
    - 🛠️ Training simulation with MLflow logging
    - 📈 Evaluation with metrics and confusion matrix
    - 📜 Audit trail with exportable history
    """)
    query = st.text_input("Enter a query:")
    if st.button("Submit"):
        if validate_non_empty(query):
            add_log("User query submitted", log_type="ACTION")
            log_history(f"User query: {query}")
            st.success("Query logged successfully.")
        else:
            st.error("Please enter a valid query.")

elif page == "⚙️ Pipeline":
    st.header("⚙️ Pipeline Status")
    st.info("Pipeline running smoothly (demo placeholder).")
    add_log("Viewed Pipeline Status", log_type="INFO")

elif page == "📞 Call Center Results":
    st.header("📞 Call Center Analytics")
    df = pd.DataFrame({
        "Agent": ["Alice", "Bob", "Charlie"],
        "Calls": [120, 95, 110],
        "Satisfaction": [0.92, 0.85, 0.88]
    })
    st.dataframe(df)
    log_history("Viewed Call Center Results")
    add_log("Viewed Call Center Results", log_type="INFO")

elif page == "📑 Insurance Claims Results":
    st.header("📑 Insurance Claims Analytics")
    df = pd.DataFrame({
        "ClaimID": [101, 102, 103],
        "Amount": [5000, 12000, 7500],
        "Status": ["Approved", "Pending", "Rejected"]
    })
    st.dataframe(df)
    log_history("Viewed Insurance Claims Results")
    add_log("Viewed Insurance Claims Results", log_type="INFO")

elif page == "🌍 Multilingual Processor":
    st.header("🌍 Multilingual Processor")

    demo_texts = {
        "English": "Hello, how can I help you today?",
        "isiZulu": "Sawubona, ngingakusiza kanjani namuhla?",
        "Sepedi": "Dumela, nka go thuša bjang lehono?",
        "Xitsonga": "Xewani, ndzi nga ku pfuna njhani namuntlha?"
    }

    lang = st.selectbox("Select language", list(demo_texts.keys()))
    use_demo = st.checkbox("Use demo dataset text")

    if use_demo:
        text = demo_texts[lang]
        st.text_area("Demo text:", text, height=100, disabled=True)
    else:
        text = st.text_area("Enter text:")

    if st.button("Process"):
        if validate_non_empty(text) and validate_language(lang):
            payload = {"input": text, "lang": lang}
            response = requests.post(f"{BACKEND_URL}/process", json=payload)
            if response.ok:
                result = response.json()
                st.success(result["output"])
                log_history(f"Processed text in {lang}")
                add_log(f"Processed text in {lang}", log_type="ACTION")
            else:
                st.error("Backend error.")
                add_log("Backend error in Multilingual Processor", log_type="ERROR")
        else:
            st.error("Invalid input or language.")
            add_log("Invalid input or language in Multilingual Processor", log_type="ERROR")

elif page == "📊 Mock Data Demo":
    st.header("📊 Multilingual Mock Data Demo")

    st.markdown("### Banking Queries")
    banking_data = pd.DataFrame({
        "Language": ["English", "isiZulu", "Sepedi", "Xitsonga"],
        "Query": [
            "What is my account balance?",
            "Iyini ibhalansi yami ye-akhawunti?",
            "Ke bokae tšhelete ye e šetšego ka akhaonteng ya ka?",
            "Xana mali ya mina ya akhawunti i njhani?"
        ]
    })
    st.dataframe(banking_data)

    st.markdown("### Insurance Claims")
    insurance_data = pd.DataFrame({
        "Language": ["English", "isiZulu", "Sepedi", "Xitsonga"],
        "Query": [
            "How do I submit a claim?",
            "Ngiyifaka kanjani isimangalo sami?",
            "Ke romela bjang kgopelo ya tshenyo?",
            "Ndzi endla njhani xikombelo xa xihlawulo?"
        ]
    })
    st.dataframe(insurance_data)

    st.markdown("### Call Center Phrases")
    callcenter_data = pd.DataFrame({
        "Language": ["English", "isiZulu", "Sepedi", "Xitsonga"],
        "Phrase": [
            "Please hold while I transfer your call.",
            "Ngicela ubambe ngizodlulisa ucingo lwakho.",
            "Ke kgopela o emele ge ke fetisetsa moletšo wa gago.",
            "Ndzi kombela u yimela loko ndzi hundzisa riqingho ra wena."
        ]
    })
    st.dataframe(callcenter_data)

    log_history("Viewed Multilingual Mock Data Demo")
    add_log("Viewed Multilingual Mock Data Demo", log_type="INFO")

elif page == "🧠 NLP Demo":
    st.header("🧠 NLP Demo")
    text = st.text_area("Enter text for NLP demo:")
    lang = st.selectbox("Select language", ["English", "isiZulu", "Sepedi", "Xitsonga"])
    if st.button("Run NLP"):
        if validate_non_empty(text) and validate_language(lang):
            st.success(f"NLP Demo processed ({lang}): {text}")
            log_history(f"NLP Demo run in {lang}")
            add_log(f"NLP Demo run in {lang}", log_type="ACTION")
        else:
            st.error("Invalid input or language.")
            add_log("Invalid input or language in NLP Demo", log_type="ERROR")

elif page == "📝 Logs":
    st.header("📝 Backend Logs")
    response = requests.get(f"{BACKEND_URL}/logs")
    if response.ok:
        logs = response.json()["logs"]
        for log in logs:
            st.write(f"- {log['event']}")
        log_history("Viewed Backend Logs")
        add_log("Viewed Backend Logs", log_type="INFO")
    else:
        st.error("Failed to fetch logs.")
        add_log("Failed to fetch backend logs", log_type="ERROR")

elif page == "📜 History":
    st.header("📜 History")
    show_history()

    # Advanced filters
    st.subheader("Filter Logs")
    start_date = st.date_input("Start date", value=datetime.today())
    end_date = st.date_input("End date", value=datetime.today())
    keyword = st.text_input("Keyword search")
    log_type = st.selectbox("Log type", ["All", "INFO", "ERROR", "ACTION"])

    logs = get_logs(limit=500)
    if logs:
        df = pd.DataFrame(logs)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Apply filters
        mask = (df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)
        filtered_df = df.loc[mask]

        if keyword:
            filtered_df = filtered_df[filtered_df["event"].str.contains(keyword, case=False, na=False)]
        if log_type != "All":
            filtered_df = filtered_df[filtered_df["event"].str.upper().str.startswith(log_type)]

        st.dataframe(filtered_df)

        # Export buttons
        if not filtered_df.empty:
            st.download_button(
                label="⬇️ Download as CSV",
                data=filtered_df.to_csv(index=False).encode("utf-8"),
                file_name="audit_log.csv",
                mime="text/csv"
            )
            st.download_button(
                label="⬇️ Download as JSON",
                data=filtered_df.to_json(orient="records", indent=2).encode("utf-8"),
                file_name="audit_log.json",
                mime="application/json"
            )

            # Visual analytics
            st.subheader("📈 Log Analytics")

            # Logs by type
            type_counts = filtered_df["event"].str.split(":").str[0].value_counts()
            st.bar_chart(type_counts)

            # Logs by day
            daily_counts = filtered_df.groupby(filtered_df["timestamp"].dt.date).size()
            st.line_chart(daily_counts)

            # Clear history button
            if st.button("🗑️ Clear History"):
                clear_logs()
                st.success("History cleared successfully.")

        else:
            st.info("No logs found for the selected filters.")
    else:
        st.info("No history available yet.")

elif page == "⚙️ Settings":
    st.header("⚙️ Settings")
    st.info("Settings placeholder. Configure StreamIQ options here.")

elif page == "ℹ️ About":
    st.header("ℹ️ About StreamIQ Demo")
    st.markdown("""
    **StreamIQ** is an enterprise-ready NLP demo platform.

    - **Frontend:** Streamlit multi-page dashboard with modular navigation  
    - **Backend:** Flask API running on `http://localhost:8000`  
    - **Features:**  
        - Multilingual text processing (English, isiZulu, Sepedi, Xitsonga)  
        - Call center and insurance claims analytics  
        - Mock datasets for banking, insurance, and call centers  
        - Persistent history logging with SQLite  
        - Exportable logs and audit trail  

    This demo is designed for **stakeholder presentations** and **enterprise polish**.
    """)
