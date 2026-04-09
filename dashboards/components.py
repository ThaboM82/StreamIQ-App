import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# Initialize history tracker safely
def init_history():
    if "history" not in st.session_state:
        st.session_state["history"] = []

def render_sidebar_history():
    with st.sidebar.expander("🕒 Recent History", expanded=True):
        if st.session_state["history"]:
            for entry in st.session_state["history"][-5:]:
                if "filter applied" in entry.lower():
                    st.markdown(f"<span style='color:blue'>🔍 {entry}</span>", unsafe_allow_html=True)
                elif "viewed" in entry.lower():
                    st.markdown(f"<span style='color:green'>📄 {entry}</span>", unsafe_allow_html=True)
                elif "evaluation" in entry.lower():
                    st.markdown(f"<span style='color:purple'>📊 {entry}</span>", unsafe_allow_html=True)
                else:
                    st.write(f"📝 {entry}")
            if st.button("🗑️ Clear History (Sidebar)"):
                st.session_state["history"] = []
                st.success("History cleared successfully.")
        else:
            st.write("No actions logged yet.")

def render_pipeline_tab():
    st.header("Pipeline Status")
    st.write("✔️ NLP Engine initialized")
    st.write("⚠️ Topic Modeling pending")
    st.write("❌ Entity Extraction failed")

def render_call_center_tab():
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

    if sentiment_filter != "All" or segment_filter != "All":
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["history"].append(
            f"[{timestamp}] Call Center filter applied → Sentiment: {sentiment_filter}, Segment: {segment_filter}"
        )

    st.dataframe(filtered_call_df)
    st.download_button(
        label="⬇️ Download Call Center Data (CSV)",
        data=filtered_call_df.to_csv(index=False).encode("utf-8"),
        file_name="call_center_results.csv",
        mime="text/csv"
    )
    fig = px.histogram(filtered_call_df, x="Sentiment", color="Sentiment", title="Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)
    topic_counts = filtered_call_df["Topic"].value_counts().reset_index()
    topic_counts.columns = ["Topic", "Count"]
    fig2 = px.bar(topic_counts, x="Topic", y="Count", title="Topic Frequency")
    st.plotly_chart(fig2, use_container_width=True)

# Similarly, create render_insurance_tab(), render_history_tab(), render_settings_tab(), render_evaluation_tab()
