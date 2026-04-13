import streamlit as st
import mlflow
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

def log_confusion_matrix(y_true, y_pred, labels, run_name="TrainingDemo"):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")

    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")
    plt.close()

def train_demo_model():
    # Demo dataset
    texts = ["billing issue", "technical problem", "account query",
             "billing error", "system crash", "account locked"]
    labels = ["billing", "technical", "account",
              "billing", "technical", "account"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)

    # Vectorize
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    # Predict
    y_pred = model.predict(X_test_vec)

    # Metrics
    accuracy = np.mean(y_pred == y_test)
    loss = 1 - accuracy  # simple proxy for demo

    # Log to MLflow
    with mlflow.start_run(run_name="TrainingDemo"):
        mlflow.log_param("algorithm", "LogisticRegression")
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("loss", loss)

        # Confusion matrix
        log_confusion_matrix(y_test, y_pred, labels=list(set(labels)))

    return accuracy, loss

def main():
    st.title("🛠️ Training Demo")
    st.write("Simulate a training run and log metrics + confusion matrix to MLflow.")

    if st.button("Run Training"):
        accuracy, loss = train_demo_model()
        st.success(f"Training complete! Accuracy: {accuracy:.2f}, Loss: {loss:.2f}")
        st.info("Metrics and confusion matrix logged to MLflow.")

if __name__ == "__main__":
    main()
