import streamlit as st
import pandas as pd
import requests
from src.utils.helpers import log_history, show_history
from src.utils.session_state_initializer import init_session_state
from src.utils.validators import validate_language, validate_non_empty, validate_domain
from src.utils.logger import init_db

# -------------------------------
# Initialization
# -------------------------------
init_session_state()
init_db()

# Backend URL (Flask)
BACKEND_URL = "http://127.0.0.1:8000"

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("StreamIQ Dashboard")
page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Pipeline",
        "Call Center Results",
        "Insurance Claims Results",
        "Multilingual Processor",
        "Mock Data Demo",
        "NLP Demo",
        "Logs",
        "History",
        "Settings",
        "About"
    ]
)

# -------------------------------
# Pages
# -------------------------------

if page == "Home":
    st.header("🏠 Welcome to StreamIQ")
    query = st.text_input("Enter a query:")
    if st.button("Submit"):
        if validate_non_empty(query):
            log_history(f"User query: {query}")
            st.success("Query logged successfully.")
        else:
            st.error("Please enter a valid query.")

elif page == "Pipeline":
    st.header("⚙️ Pipeline Status")
    st.info("Pipeline running smoothly (demo placeholder).")

elif page == "Call Center Results":
    st.header("📞 Call Center Analytics")
    df = pd.DataFrame({
        "Agent": ["Alice", "Bob", "Charlie"],
        "Calls": [120, 95, 110],
        "Satisfaction": [0.92, 0.85, 0.88]
    })
    st.dataframe(df)
    log_history("Viewed Call Center Results")

elif page == "Insurance Claims Results":
    st.header("📑 Insurance Claims Analytics")
    df = pd.DataFrame({
        "ClaimID": [101, 102, 103],
        "Amount": [5000, 12000, 7500],
        "Status": ["Approved", "Pending", "Rejected"]
    })
    st.dataframe(df)
    log_history("Viewed Insurance Claims Results")

elif page == "Multilingual Processor":
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
            else:
                st.error("Backend error.")
        else:
            st.error("Invalid input or language.")

elif page == "Mock Data Demo":
    st.header("📊 Multilingual Mock Data Demo")

    demo_queries = {
        "English": "What is my account balance?",
        "isiZulu": "Iyini ibhalansi yami ye-akhawunti?",
        "Sepedi": "Ke bokae tšhelete ye e šetšego ka akhaonteng ya ka?",
        "Xitsonga": "Xana mali ya mina ya akhawunti i njhani?"
    }

    lang = st.selectbox("Select language", list(demo_queries.keys()))
    query = demo_queries[lang]

    st.markdown("### Demo Query")
    st.write(f"**{lang}:** {query}")

    if st.button("Run Demo Query"):
        payload = {"input": query, "lang": lang}
        response = requests.post(f"{BACKEND_URL}/process", json=payload)
        if response.ok:
            result = response.json()
            st.success(f"Processed Output → {result['output']}")
            log_history(f"Demo query processed in {lang}")
        else:
            st.error("Backend error.")

    st.markdown("### All Demo Queries")
    df = pd.DataFrame(list(demo_queries.items()), columns=["Language", "Query"])
    st.dataframe(df)

elif page == "NLP Demo":
    st.header("🧠 NLP Demo")
    text = st.text_area("Enter text for NLP demo:")
    lang = st.selectbox("Select language", ["English", "isiZulu", "Sepedi", "Xitsonga"])
    if st.button("Run NLP"):
        if validate_non_empty(text) and validate_language(lang):
            payload = {"input": text, "lang": lang}
            response = requests.post(f"{BACKEND_URL}/process", json=payload)
            if response.ok:
                result = response.json()
                st.success(f"NLP Output → {result['output']}")
                log_history(f"NLP Demo run in {lang}")
            else:
                st.error("Backend error.")
        else:
            st.error("Invalid input or language.")

elif page == "Logs":
    st.header("📝 Backend Logs")
    response = requests.get(f"{BACKEND_URL}/logs")
    if response.ok:
        logs = response.json()["logs"]
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df)
        else:
            st.info("No logs available yet.")
        log_history("Viewed Backend Logs")
    else:
        st.error("Failed to fetch logs.")

elif page == "History":
    st.header("📜 History")
    show_history()

elif page == "Settings":
    st.header("⚙️ Settings")
    st.info("Settings placeholder.")

elif page == "About":
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
