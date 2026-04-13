import streamlit as st
import mlflow
import pandas as pd

def fetch_runs(experiment_name: str):
    """
    Fetch MLflow runs for a given experiment.
    """
    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if not experiment:
        return pd.DataFrame()

    runs = client.search_runs([experiment.experiment_id])
    records = []
    for run in runs:
        record = {"run_id": run.info.run_id}
        record.update(run.data.params)
        record.update(run.data.metrics)
        records.append(record)
    return pd.DataFrame(records)

def main():
    st.title("📈 Model Evaluation")

    st.write("View metrics and parameters logged in MLflow experiments.")

    experiment_name = st.text_input("Experiment name:", "StreamlitPredictionDemo")

    if st.button("Load Metrics"):
        df = fetch_runs(experiment_name)
        if df.empty:
            st.warning("No runs found for this experiment.")
        else:
            st.write("### Experiment Runs")
            st.dataframe(df)

            # Show metrics summary
            metric_cols = [col for col in df.columns if col not in ["run_id"]]
            if metric_cols:
                st.write("### Metrics Overview")
                st.bar_chart(df[metric_cols])

if __name__ == "__main__":
    main()
