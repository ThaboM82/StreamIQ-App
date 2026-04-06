import streamlit as st

st.title("⚙️ Model Training Results")

st.write("Training progress and metrics for StreamIQ models.")

training_metrics = {
    "Epochs": 10,
    "Final Accuracy": "92%",
    "Loss": "0.08",
    "Engine": "HuggingFace"
}

for k, v in training_metrics.items():
    st.write(f"**{k}:** {v}")

st.info("Run `dvc repro --force` to retrain and refresh metrics.")

# Log into history
if "history" in st.session_state:
    st.session_state["history"].append("Viewed Training Results page")
