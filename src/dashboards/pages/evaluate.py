import streamlit as st
import requests
import pandas as pd
import altair as alt

API_URL = "http://127.0.0.1:8000"

def run():
    """Entry point for Streamlit sidebar navigation."""
    st.title("📈 Model Evaluation")
    st.write("View metrics and parameters logged in MLflow experiments.")

    # Input for experiment name
    experiment_name = st.text_input("Experiment name:", "StreamlitPredictionDemo")

    if st.button("Load Metrics"):
        # Call Flask backend API
        resp = requests.get(f"{API_URL}/mlflow", params={"experiment_name": experiment_name})

        if resp.status_code == 200 and resp.json():
            runs = resp.json()
            df = pd.DataFrame(runs)

            st.write("### Experiment Runs")
            st.dataframe(df)

            # Show metrics overview if numeric columns exist
            metric_cols = [
                col for col in df.columns
                if col not in ["run_id"] and pd.api.types.is_numeric_dtype(df[col])
            ]
            if metric_cols:
                st.write("### Metrics Overview")
                st.bar_chart(df[metric_cols])
        else:
            st.warning("No runs found for this experiment.")

    # -------------------------------
    # Seeded Demo Metrics (always shown for stakeholder polish)
    # -------------------------------
    demo_metrics = pd.DataFrame({
        "Model": [
            "Call Center Sentiment",
            "Insurance Claim Intent",
            "Big Data Risk Scoring",
            "Multilingual Classifier"
        ],
        "Accuracy": [0.91, 0.87, 0.89, 0.93],
        "Precision": [0.90, 0.85, 0.88, 0.92],
        "Recall": [0.89, 0.86, 0.87, 0.91],
        "F1 Score": [0.90, 0.85, 0.88, 0.92]
    })
    st.write("### Seeded Demo Metrics")
    st.dataframe(demo_metrics)

    # Export seeded metrics
    csv = demo_metrics.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Demo Metrics (CSV)", csv, "demo_metrics.csv", "text/csv")

    # -------------------------------
    # Confusion Matrix Demo
    # -------------------------------
    st.write("### Confusion Matrix (Demo)")
    conf_matrix = pd.DataFrame(
        [[50, 5], [7, 38]],
        columns=["Predicted Positive", "Predicted Negative"],
        index=["Actual Positive", "Actual Negative"]
    )
    st.dataframe(conf_matrix)

    # -------------------------------
    # ROC Curve Demo
    # -------------------------------
    st.write("### ROC Curve (Demo)")
    roc_data = pd.DataFrame({
        "False Positive Rate": [0.0, 0.1, 0.2, 0.3, 1.0],
        "True Positive Rate": [0.0, 0.6, 0.75, 0.85, 1.0]
    })
    roc_chart = alt.Chart(roc_data).mark_line(color="blue").encode(
        x="False Positive Rate",
        y="True Positive Rate"
    ).properties(title="ROC Curve (Demo)")
    st.altair_chart(roc_chart, use_container_width=True)
