import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import requests

# Import your NLP modules
from src.speech_to_text.transcriber import Transcriber
from src.satisfaction import SatisfactionPredictor
from src.nlp import analyze_sentiment, classify_intent
from src.utils.session_state_initializer import init_session_state

# -------------------------------
# Page setup (must be first)
# -------------------------------
st.set_page_config(page_title="StreamIQ Dashboard", layout="wide")
st.title("📊 StreamIQ Dashboard")

# -------------------------------
# Initialize session state
# -------------------------------
init_session_state()
if "history" not in st.session_state:
    st.session_state["history"] = []

# -------------------------------
# Sidebar History Widget
# -------------------------------
with st.sidebar.expander("🕒 Recent History", expanded=True):
    if st.session_state["history"]:
        for entry in st.session_state["history"][-5:]:
            st.write(f"📝 {entry}")
        if st.button("🗑️ Clear History (Sidebar)"):
            st.session_state["history"] = []
            st.success("History cleared successfully.")
    else:
        st.write("No actions logged yet.")

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Pipeline", "Call Center Results", "Insurance Claims Results",
    "History", "Settings", "Evaluation",
    "Transcription", "Satisfaction", "Audit Logs"
])

# --- Pipeline Tab ---
with tab1:
    st.header("Pipeline Status")
    st.write("✔️ NLP Engine initialized")
    st.write("⚠️ Topic Modeling pending")
    st.write("❌ Entity Extraction failed")

# --- Call Center Results Tab ---
with tab2:
    st.header("📂 Call Center Analysis")
    call_data = {
        "Call_ID": [1001, 1002, 1003, 1004, 1005],
        "Customer_Segment": ["Retail Banking", "Insurance Claims", "Corporate Client", "Retail Banking", "Insurance Claims"],
        "Transcript_Snippet": [
            "I can’t access my online account today.",
            "The agent helped me file quickly.",
            "Fees are higher than expected.",
            "Great service, very polite staff.",
            "Still waiting for my reimbursement."
        ],
        "Sentiment": ["Negative", "Positive", "Negative", "Positive", "Neutral"],
        "Topic": ["Account Access", "Claims Processing", "Pricing", "Customer Service", "Claims Delay"]
    }
    call_df = pd.DataFrame(call_data)

    sentiment_filter = st.selectbox("Filter by Sentiment", ["All"] + call_df["Sentiment"].unique().tolist())
    segment_filter = st.selectbox("Filter by Customer Segment", ["All"] + call_df["Customer_Segment"].unique().tolist())

    filtered_call_df = call_df.copy()
    if sentiment_filter != "All":
        filtered_call_df = filtered_call_df[filtered_call_df["Sentiment"] == sentiment_filter]
    if segment_filter != "All":
        filtered_call_df = filtered_call_df[filtered_call_df["Customer_Segment"] == segment_filter]

    st.dataframe(filtered_call_df)

    st.download_button(
        label="⬇️ Download Call Center Data (CSV)",
        data=filtered_call_df.to_csv(index=False).encode("utf-8"),
        file_name="call_center_results.csv",
        mime="text/csv"
    )

    fig = px.histogram(filtered_call_df, x="Sentiment", color="Sentiment", title="Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)

# --- Insurance Claims Results Tab ---
with tab3:
    st.header("📂 Insurance Claims Workflow")
    claims_data = {
        "Claim_ID": [2001, 2002, 2003, 2004, 2005],
        "Customer_Segment": ["Retail Customer", "Corporate Client", "Retail Customer", "Retail Customer", "Corporate Client"],
        "Claim_Type": ["Auto Accident", "Property Damage", "Health Insurance", "Auto Accident", "Liability Claim"],
        "Status": ["Approved", "Pending", "Rejected", "Approved", "Escalated"],
        "Sentiment": ["Positive", "Neutral", "Negative", "Positive", "Negative"],
        "Notes": [
            "Claim processed quickly, thank you.",
            "Still waiting for assessment report.",
            "Unfair denial, need explanation.",
            "Funds reimbursed within 3 days.",
            "Case dragged on too long."
        ]
    }
    claims_df = pd.DataFrame(claims_data)
    st.dataframe(claims_df)

# --- History Tab ---
with tab4:
    st.header("History Tracker")
    if st.session_state["history"]:
        for entry in st.session_state["history"]:
            st.write(entry)
    else:
        st.write("No filters applied yet.")

# --- Settings Tab ---
with tab5:
    st.header("Settings")
    st.selectbox("Choose NLP Engine", ["HuggingFace", "SparkNLP"])
    st.radio("Theme", ["Light", "Dark"])
    st.write("Version: 1.0.0")

# --- Evaluation Tab ---
with tab6:
    st.header("📊 Model Evaluation")
    metrics_path = "C:/StreamIQ App/data/metrics.txt"
    matrix_file = "C:/StreamIQ App/data/confusion_matrix.npy"
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            st.text(f.read())
    else:
        st.warning("Metrics file not found.")
    if os.path.exists(matrix_file):
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        cm = np.load(matrix_file)
        labels = [f"Class {i}" for i in range(cm.shape[0])]
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                    xticklabels=labels, yticklabels=labels)
        st.pyplot(fig)

# --- Transcription Tab ---
with tab7:
    st.header("Speech-to-Text Transcription")
    transcriber = Transcriber()
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    if audio_file is not None:
        text = transcriber.transcribe(audio_file.read())
        st.write("### Transcribed Text")
        st.write(text)
        st.session_state["history"].append(f"Transcribed audio → {text[:50]}...")

# --- Satisfaction Tab ---
with tab8:
    st.header("Customer Satisfaction Prediction")
    predictor = SatisfactionPredictor()
    demo_text = st.text_area("Enter transcript text")
    if st.button("Predict Satisfaction"):
        prediction = predictor.predict(demo_text)
        sentiment = analyze_sentiment(demo_text)
        intent = classify_intent(demo_text)
        st.write(f"Prediction: {prediction}")
        st.write(f"Sentiment: {sentiment}")
        st.write(f"Intent: {intent}")
        st.session_state["history"].append(f"Satisfaction predicted → {prediction}")

# --- Audit Logs Tab ---
with tab9:
    st.header("Audit Logs (via FastAPI)")
    try:
        response = requests.get("http://localhost:8000/logs")
        if response.status_code == 200:
            logs = response.json()
            if logs:
                df = pd.DataFrame(logs)
                st.dataframe(df)
            else:
                st.info("No audit logs found.")
        else:
            st.error(f"Failed to fetch logs. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
