import streamlit as st
import os

st.set_page_config(page_title="StreamIQ Evaluation Dashboard", layout="wide")

st.title("📊 StreamIQ Model Evaluation Dashboard")

# --- Metrics Section ---
st.header("Evaluation Metrics")
metrics_path = "C:/StreamIQ App/data/metrics.txt"

if os.path.exists(metrics_path):
    with open(metrics_path, "r") as f:
        metrics_text = f.read()
    st.text(metrics_text)
else:
    st.warning("⚠️ Metrics file not found. Run evaluation to generate metrics.")

# --- Confusion Matrix Heatmap Section ---
st.header("Confusion Matrix Heatmap")
cm_img_path = "C:/StreamIQ App/data/confusion_matrix.png"

if os.path.exists(cm_img_path):
    st.image(cm_img_path, caption="Confusion Matrix", use_column_width=True)
else:
    st.warning("⚠️ Confusion matrix image not found. Run evaluation to generate the heatmap.")

# --- Optional polish: Add sidebar info ---
st.sidebar.title("Pipeline Status")
st.sidebar.info(
    "This dashboard displays the latest evaluation results.\n\n"
    "Run `dvc repro --force` to refresh metrics and visuals."
)
