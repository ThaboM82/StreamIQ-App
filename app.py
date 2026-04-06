import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# Page setup
st.set_page_config(page_title="StreamIQ Dashboard", layout="wide")
st.title("📊 StreamIQ Dashboard")

# Initialize history tracker
if "history" not in st.session_state:
    st.session_state["history"] = []

# Sidebar History Widget (styled)
with st.sidebar.expander("🕒 Recent History", expanded=True):
    if "history" in st.session_state and st.session_state["history"]:
        # Show last 5 entries with icons + colors
        for entry in st.session_state["history"][-5:]:
            if "filter applied" in entry.lower():
                st.markdown(f"<span style='color:blue'>🔍 {entry}</span>", unsafe_allow_html=True)
            elif "viewed" in entry.lower():
                st.markdown(f"<span style='color:green'>📄 {entry}</span>", unsafe_allow_html=True)
            elif "evaluation" in entry.lower():
                st.markdown(f"<span style='color:purple'>📊 {entry}</span>", unsafe_allow_html=True)
            else:
                st.write(f"📝 {entry}")

        # Clear history button in sidebar
        if st.button("🗑️ Clear History (Sidebar)"):
            st.session_state["history"] = []
            st.success("History cleared successfully.")
    else:
        st.write("No actions logged yet.")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Pipeline", "Call Center Results", "Insurance Claims Results", "History", "Settings", "Evaluation"
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["history"].append(
            f"[{timestamp}] Call Center filter applied → Sentiment: {sentiment_filter}, Segment: {segment_filter}"
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
        "Customer_Segment": [
            "Retail Customer", "Corporate Client", "Retail Customer", "Retail Customer", "Corporate Client"
        ],
        "Claim_Type": [
            "Auto Accident", "Property Damage", "Health Insurance", "Auto Accident", "Liability Claim"
        ],
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["history"].append(
            f"[{timestamp}] Claims filter applied → Status: {status_filter}, Segment: {segment_filter_claims}"
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
            st.write(entry)

        # Export full history as CSV
        history_df = pd.DataFrame(st.session_state["history"], columns=["Action Log"])
        st.download_button(
            label="⬇️ Download Full History (CSV)",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="history_log.csv",
            mime="text/csv"
        )
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

# --- Evaluation Tab ---
with tab6:
    st.header("📊 Model Evaluation")

    metrics_path = "C:/StreamIQ App/data/metrics.txt"
    cm_img_path = "C:/StreamIQ App/data/confusion_matrix.png"
    matrix_file = "C:/StreamIQ App/data/confusion_matrix.npy"

    # Show metrics
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            st.text(f.read())
    else:
        st.warning("Metrics file not found. Run evaluation to generate metrics.")

    # Interactive confusion matrix
    st.header("Confusion Matrix Heatmap")

    if os.path.exists(matrix_file):
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np

        cm = np.load(matrix_file)

        # Dropdown to select which labels to highlight
        labels = [f"Class {i}" for i in range(cm.shape[0])]
        selected_labels = st.multiselect("Highlight labels", labels, default=Here’s the **final full `app.py`** with *all the changes integrated* — including the styled sidebar widget, timestamps, CSV export, and all six tabs polished for demo use. This is your enterprise‑ready StreamIQ dashboard code.

---

### ✅ Final `app.py`

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# Page setup
st.set_page_config(page_title="StreamIQ Dashboard", layout="wide")
st.title("📊 StreamIQ Dashboard")

# Initialize history tracker
if "history" not in st.session_state:
    st.session_state["history"] = []

# Sidebar History Widget (styled + collapsible)
with st.sidebar.expander("🕒 Recent History", expanded=True):
    if st.session_state["history"]:
        # Show last 5 entries with icons + colors
        for entry in st.session_state["history"][-5:]:
            if "filter applied" in entry.lower():
                st.markdown(f"<span style='color:blue'>🔍 {entry}</span>", unsafe_allow_html=True)
            elif "viewed" in entry.lower():
                st.markdown(f"<span style='color:green'>📄 {entry}</span>", unsafe_allow_html=True)
            elif "evaluation" in entry.lower():
                st.markdown(f"<span style='color:purple'>📊 {entry}</span>", unsafe_allow_html=True)
            else:
                st.write(f"📝 {entry}")

        # Clear history button in sidebar
        if st.button("🗑️ Clear History (Sidebar)"):
            st.session_state["history"] = []
            st.success("History cleared successfully.")
    else:
        st.write("No actions logged yet.")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Pipeline", "Call Center Results", "Insurance Claims Results", "History", "Settings", "Evaluation"
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

    status_filter = st.selectbox("Filter by Claim Status", ["All"] + claims_df["Status"].unique().tolist())
    segment_filter_claims = st.selectbox("Filter by Customer Segment", ["All"] + claims_df["Customer_Segment"].unique().tolist())

    filtered_claims_df = claims_df.copy()
    if status_filter != "All":
        filtered_claims_df = filtered_claims_df[claims_df["Status"] == status_filter]
    if segment_filter_claims != "All":
        filtered_claims_df = filtered_claims_df[claims_df["Customer_Segment"] == segment_filter_claims]

    if status_filter != "All" or segment_filter_claims != "All":
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["history"].append(
            f"[{timestamp}] Claims filter applied → Status: {status_filter}, Segment: {segment_filter_claims}"
        )

    st.dataframe(filtered_claims_df)

    st.download_button(
        label="⬇️ Download Claims Data (CSV)",
        data=filtered_claims_df.to_csv(index=False).encode("utf-8"),
        file_name="insurance_claims_results.csv",
        mime="text/csv"
    )

    fig = px.histogram(filtered_claims_df, x="Status", color="Status", title="Claims Status Distribution")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.pie(filtered_claims_df, names="Sentiment", title="Customer Sentiment on Claims")
    st.plotly_chart(fig2, use_container_width=True)

# --- History Tab ---
with tab4:
    st.header("History Tracker")

    if st.session_state["history"]:
        for entry in st.session_state["history"]:
            st.write(entry)

        history_df = pd.DataFrame(st.session_state["history"], columns=["Action Log"])
        st.download_button(
            label="⬇️ Download Full History (CSV)",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="history_log.csv",
            mime="text/csv"
        )
    else:
        st.write("No filters applied yet.")

    if st.button("🗑️ Clear History"):
        st.session_state["history"] = []
        st.success("History cleared successfully.")

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
    cm_img_path = "C:/StreamIQ App/data/confusion_matrix.png"
    matrix_file = "C:/StreamIQ App/data/confusion_matrix.npy"

    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            st.text(f.read())
    else:
        st.warning("Metrics file not found. Run evaluation to generate metrics.")

    st.header("Confusion Matrix Heatmap")

    if os.path.exists(matrix_file):
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np

        cm = np.load(matrix_file)
        labels = [f"Class {i}" for i in range(cm.shape[0])]
        selected_labels = st.multiselect("Highlight labels", labels, default=labels)

        mask = np.ones_like(cm, dtype=bool)
        for idx, lbl in enumerate(labels):
            if lbl in selected_labels:
                mask[idx, :] = False
                mask[:, idx] = False

        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", mask=mask, ax=ax,
                    xticklabels=labels, yticklabels=labels)
        st.pyplot(fig)