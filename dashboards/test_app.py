import streamlit as st
import pandas as pd

st.title("Hello StreamIQ 👋")

demo_data = pd.DataFrame({
    "Category": ["Positive", "Neutral", "Negative"],
    "Count": [10, 5, 3]
})

st.subheader("Demo Data Table")
st.dataframe(demo_data)

st.subheader("Demo Bar Chart")
st.bar_chart(demo_data.set_index("Category"))
