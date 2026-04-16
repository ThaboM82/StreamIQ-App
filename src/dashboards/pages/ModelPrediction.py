import streamlit as st
from streamiq.model_utils import predict_intent
from streamiq.mlflow_utils import log_experiment

def run():
    """Entry point for Streamlit sidebar navigation."""
    st.title("🤖 Model Prediction Demo")
    user_text = st.text_area(
        "Enter text:",
        placeholder="e.g. billing issue, technical problem, account query"
    )

    if st.button("Predict"):
        if user_text.strip():
            prediction = predict_intent(user_text)
            st.success(f"Predicted intent: **{prediction}**")

            # Log prediction to MLflow
            log_experiment(
                run_name="StreamlitPredictionDemo",
                params={"text": user_text},
                metrics={"prediction": prediction}
            )
            st.info("Prediction logged to MLflow.")
        else:
            st.warning("Please enter some text before predicting.")
