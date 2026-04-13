# streamiq/mlflow_utils.py
import mlflow

def log_experiment(run_name: str, params: dict, metrics: dict):
    """
    Log parameters and metrics to MLflow.
    """
    with mlflow.start_run(run_name=run_name):
        for k, v in params.items():
            mlflow.log_param(k, v)
        for k, v in metrics.items():
            mlflow.log_metric(k, v)
