import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="StreamIQ Dashboard", layout="wide")
st.title("📊 StreamIQ Dashboard")

# Initialize history tracker
if "history" not in st.session_state:
    st.session_state["history"] = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Pipeline", "Call Center Results", "Insurance Claims Results", "History", "Settings"
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

    # Multi-filter: sentiment + customer segment
    sentiment_filter = st.selectbox("Filter by Sentiment", ["All"] + call_df["Sentiment"].unique().tolist())
    segment_filter = st.selectbox("Filter by Customer Segment", ["All"] + call_df["Customer_Segment"].unique().tolist())

    filtered_call_df = call_df.copy()
    if sentiment_filter != "All":
        filtered_call_df = filtered_call_df[filtered_call_df["Sentiment"] == sentiment_filter]
    if segment_filter != "All":
        filtered_call_df = filtered_call_df[filtered_call_df["Customer_Segment"] == segment_filter]

    # Log filter selection
    if sentiment_filter != "All" or segment_filter != "All":
        st.session_state["history"].append(
            f"Call Center filter applied → Sentiment: {sentiment_filter}, Segment: {segment_filter}"
        )

    st.dataframe(filtered_call_df)

    # Export button
    st.download_button(
        label="⬇️ Download Call Center Data (CSV)",
        data=filtered_call_df.to_csv(index=False).encode("utf-8"),
        file_name="call_center_results.csv",
        mime="text/csv"
    )

    # Charts
    fig = px.histogram(filtered_call_df, x="Sentiment", color="Sentiment", title="Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)

    topic_counts = filtered_call_df["Topic"].value_counts().reset_index()
    topic_counts.columns = ["Topic", "Count"]
    fig2 = px.bar(topic_counts, x="Topic", y="Count", title="Topic Frequency")
    st.plotly_chart(fig2, use_container_width=True)

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

    # Multi-filter: claim status + customer segment
    status_filter = st.selectbox("Filter by Claim Status", ["All"] + claims_df["Status"].unique().tolist())
    segment_filter_claims = st.selectbox("Filter by Customer Segment", ["All"] + claims_df["Customer_Segment"].unique().tolist())

    filtered_claims_df = claims_df.copy()
    if status_filter != "All":
        filtered_claims_df = filtered_claims_df[filtered_claims_df["Status"] == status_filter]
    if segment_filter_claims != "All":
        filtered_claims_df = filtered_claims_df[filtered_claims_df["Customer_Segment"] == segment_filter_claims]

    # Log filter selection
    if status_filter != "All" or segment_filter_claims != "All":
        st.session_state["history"].append(
            f"Claims filter applied → Status: {status_filter}, Segment: {segment_filter_claims}"
        )

    st.dataframe(filtered_claims_df)

    # Export button
    st.download_button(
        label="⬇️ Download Claims Data (CSV)",
        data=filtered_claims_df.to_csv(index=False).encode("utf-8"),
        file_name="insurance_claims_results.csv",
        mime="text/csv"
    )

    # Charts
    fig = px.histogram(filtered_claims_df, x="Status", color="Status", title="Claims Status Distribution")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.pie(filtered_claims_df, names="Sentiment", title="Customer Sentiment on Claims")
    st.plotly_chart(fig2, use_container_width=True)

# --- History Tab ---
with tab4:
    st.header("History Tracker")

    if st.session_state["history"]:
        for entry in st.session_state["history"]:
            st.write(f"- {entry}")
    else:
        st.write("No filters applied yet.")

    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state["history"] = []
        st.success("History cleared successfully.")

# --- Settings Tab ---
with tab5:
    st.header("Settings")
    st.selectbox("Choose NLP Engine", ["HuggingFace", "SparkNLP"])
    st.radio("Theme", ["Light", "Dark"])
    st.write("Version: 1.0.0")
