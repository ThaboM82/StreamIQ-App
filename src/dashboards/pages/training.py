import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import time

def run():
    st.title("🧪 Training Demo")
    st.write("Simulated training progress with seeded demo metrics.")

    epochs = list(range(1, 21))
    train_loss = [1.0/(e**0.5) + np.random.uniform(-0.05, 0.05) for e in epochs]
    val_loss = [1.2/(e**0.5) + np.random.uniform(-0.05, 0.05) for e in epochs]
    train_acc = [min(0.5 + 0.03*e + np.random.uniform(-0.02, 0.02), 1.0) for e in epochs]
    val_acc = [min(0.45 + 0.03*e + np.random.uniform(-0.02, 0.02), 1.0) for e in epochs]

    df = pd.DataFrame({
        "Epoch": epochs,
        "Train Loss": train_loss,
        "Validation Loss": val_loss,
        "Train Accuracy": train_acc,
        "Validation Accuracy": val_acc
    })

    st.subheader("Training Progress (Demo)")
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(len(epochs)):
        progress_bar.progress(int((i+1)/len(epochs)*100))
        status_text.text(f"Epoch {i+1}/{len(epochs)} - Train Loss: {train_loss[i]:.3f}, Train Acc: {train_acc[i]:.3f}")
        time.sleep(0.1)

    st.subheader("Loss Curves")
    loss_chart = alt.Chart(df).transform_fold(
        ["Train Loss", "Validation Loss"],
        as_=["Metric", "Value"]
    ).mark_line().encode(
        x="Epoch",
        y="Value",
        color="Metric"
    ).properties(title="Training vs Validation Loss")
    st.altair_chart(loss_chart, use_container_width=True)

    st.subheader("Accuracy Curves")
    acc_chart = alt.Chart(df).transform_fold(
        ["Train Accuracy", "Validation Accuracy"],
        as_=["Metric", "Value"]
    ).mark_line().encode(
        x="Epoch",
        y="Value",
        color="Metric"
    ).properties(title="Training vs Validation Accuracy")
    st.altair_chart(acc_chart, use_container_width=True)

    st.subheader("Final Metrics (Demo)")
    st.write({
        "Final Train Loss": round(train_loss[-1], 3),
        "Final Validation Loss": round(val_loss[-1], 3),
        "Final Train Accuracy": round(train_acc[-1], 3),
        "Final Validation Accuracy": round(val_acc[-1], 3)
    })

    st.download_button(
        label="⬇️ Export Training Metrics (CSV)",
        data=df.to_csv(index=False),
        file_name="training_metrics.csv",
        mime="text/csv"
    )

    # -------------------------------
    # Confusion Matrix Demo
    # -------------------------------
    st.subheader("Confusion Matrix (Demo)")
    conf_matrix = pd.DataFrame(
        [[45, 10], [8, 37]],
        columns=["Predicted Positive", "Predicted Negative"],
        index=["Actual Positive", "Actual Negative"]
    )
    st.dataframe(conf_matrix)

    # -------------------------------
    # ROC Curve Demo
    # -------------------------------
    st.subheader("ROC Curve (Demo)")
    roc_data = pd.DataFrame({
        "False Positive Rate": [0.0, 0.1, 0.2, 0.3, 1.0],
        "True Positive Rate": [0.0, 0.65, 0.78, 0.88, 1.0]
    })
    roc_chart = alt.Chart(roc_data).mark_line(color="green").encode(
        x="False Positive Rate",
        y="True Positive Rate"
    ).properties(title="ROC Curve (Demo)")
    st.altair_chart(roc_chart, use_container_width=True)
