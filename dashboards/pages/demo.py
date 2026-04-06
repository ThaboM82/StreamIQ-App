import streamlit as st

st.title("🎬 StreamIQ Demo")

st.write("Demonstration of pipeline outputs in a polished, stakeholder-friendly format.")

st.success("✔️ Real-time NLP pipeline executed successfully.")
st.write("Outputs include sentiment analysis, topic modeling, and entity extraction.")

# Placeholder visual
st.image("https://via.placeholder.com/600x300.png?text=Demo+Visualization", caption="Demo Visualization")

# Log into history
if "history" in st.session_state:
    st.session_state["history"].append("Viewed Demo page")
