import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

EXPERIMENT_NAME = "StreamIQ-NLP"

def init_experiment():
    """Ensure experiment exists and return its ID."""
    mlflow.set_experiment(EXPERIMENT_NAME)
    client = MlflowClient()
    exp = client.get_experiment_by_name(EXPERIMENT_NAME)
    return exp.experiment_id

def log_sentiment_model(model, X_train, y_train, X_test, y_test):
    """Train and log a sentiment model with MLflow."""
    exp_id = init_experiment()

    with mlflow.start_run(experiment_id=exp_id, run_name="sentiment_model_v1"):
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)

        mlflow.log_param("model_type", type(model).__name__)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "sentiment_model")

        print(f"Logged sentiment model with accuracy: {accuracy:.3f}")

def get_best_run(metric="accuracy"):
    """Retrieve best run by metric from MLflow."""
    client = MlflowClient()
    exp = client.get_experiment_by_name(EXPERIMENT_NAME)
    runs = client.search_runs(
        experiment_ids=[exp.experiment_id],
        order_by=[f"metrics.{metric} DESC"]
    )
    return runs[0] if runs else None
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

EXPERIMENT_NAME = "StreamIQ-NLP"

def init_experiment():
    """Ensure experiment exists and return its ID."""
    mlflow.set_experiment(EXPERIMENT_NAME)
    client = MlflowClient()
    exp = client.get_experiment_by_name(EXPERIMENT_NAME)
    return exp.experiment_id

def log_sentiment_model(model, X_train, y_train, X_test, y_test):
    """Train and log a sentiment model with MLflow."""
    exp_id = init_experiment()

    with mlflow.start_run(experiment_id=exp_id, run_name="sentiment_model_v1"):
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)

        mlflow.log_param("model_type", type(model).__name__)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "sentiment_model")

        print(f"Logged sentiment model with accuracy: {accuracy:.3f}")

def get_best_run(metric="accuracy"):
    """Retrieve best run by metric from MLflow."""
    client = MlflowClient()
    exp = client.get_experiment_by_name(EXPERIMENT_NAME)
    runs = client.search_runs(
        experiment_ids=[exp.experiment_id],
        order_by=[f"metrics.{metric} DESC"]
    )
    return runs[0] if runs else None
