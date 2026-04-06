import streamlit as st
import pandas as pd

st.title("📂 Data Overview")

st.write("Quick look at the datasets powering StreamIQ.")

data = {
    "Source": ["Call Center", "Insurance Claims", "Retail Banking"],
    "Records": [5000, 3200, 2100],
    "Last Updated": ["2026-04-01", "2026-04-02", "2026-04-03"]
}
df = pd.DataFrame(data)

st.dataframe(df)

# Export
st.download_button(
    label="⬇️ Download Data Summary (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="data_summary.csv",
    mime="text/csv"
)

# Log into history
if "history" in st.session_state:
    st.session_state["history"].append("Viewed Data Overview page")
