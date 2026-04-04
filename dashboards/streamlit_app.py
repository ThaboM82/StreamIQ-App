import streamlit as st
import pandas as pd

# Import from your src package
from src.satisfaction import SatisfactionPredictor
from src.speech_to_text import Transcriber

# Sidebar navigation
st.sidebar.title("📊 StreamIQ Dashboard")
page = st.sidebar.radio("Navigate", ["Home", "Feedback Analysis", "Speech-to-Text Demo"])

# Home page
if page == "Home":
    st.title("Welcome to StreamIQ")
    st.write("Enterprise-ready NLP pipeline for banks, insurers, and call centers.")
    st.write("Use the sidebar to explore Feedback Analysis and Speech-to-Text demos.")

    # Example chart
    st.subheader("📈 Demo Chart")
    demo_data = pd.DataFrame({
        "Metric": ["Sentiment", "Intent", "Satisfaction"],
        "Score": [75, 82, 78]
    })
    st.bar_chart(demo_data.set_index("Metric"))

# Feedback Analysis page
elif page == "Feedback Analysis":
    st.header("📝 Feedback Analysis")
    text_input = st.text_area("Enter customer feedback:", "")

    # Initialize session state for history
    if "feedback_history" not in st.session_state:
        st.session_state.feedback_history = []

    if st.button("Analyze Feedback"):
        if text_input.strip():
            predictor = SatisfactionPredictor()
            result = predictor.predict(text_input)

            # Save to history
            st.session_state.feedback_history.append({
                "Feedback": text_input,
                "Sentiment Polarity": result["sentiment"].get("polarity", 0.0),
                "Sentiment Subjectivity": result["sentiment"].get("subjectivity", 0.0),
                "Intent": result["intent"].get("label", "N/A"),
                "Intent Confidence": result["intent"].get("confidence", 0.0),
                "Satisfaction Score": result["satisfaction"]["satisfaction_score"]
            })
        else:
            st.warning("Please enter feedback text before analyzing.")

    # Show history table
    if st.session_state.feedback_history:
        st.subheader("📜 Feedback History")
        history_df = pd.DataFrame(st.session_state.feedback_history)
        st.dataframe(history_df)

        # Trend chart
        st.subheader("📈 Satisfaction Trend")
        st.line_chart(history_df["Satisfaction Score"])

        # Download button
        st.download_button(
            label="⬇️ Download Feedback History as CSV",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="feedback_history.csv",
            mime="text/csv"
        )

# Speech-to-Text Demo page
elif page == "Speech-to-Text Demo":
    st.header("🎤 Speech-to-Text Demo")
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

    if audio_file is not None:
        transcriber = Transcriber()
        transcription = transcriber.transcribe(audio_file.read())
        st.subheader("Transcription")
        st.write(transcription)
    else:
        st.info("Upload a .wav or .mp3 file to see the transcription.")
