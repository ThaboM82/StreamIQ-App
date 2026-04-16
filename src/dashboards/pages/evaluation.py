# src/dashboards/pages/evaluate.py
import streamlit as st
import requests
import pandas as pd

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
