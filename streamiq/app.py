import os, sys
import streamlit as st
import pandas as pd
import altair as alt
import pytest

# --- Ensure project root is on Python path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.utils.branding import (
    add_chart_watermark,
    export_pdf_with_logo,
    export_excel_with_branding,
    export_csv_with_branding,
)

from src.db.connection import init_db, get_sentiment_counts, insert_transcript, reset_db


def load_pipeline_data():
    """Load sentiment counts from the database or return empty DataFrame on error."""
    try:
        data = get_sentiment_counts()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Pipeline data load failed: {e}")
        return pd.DataFrame({"category": [], "value": []})


def main():
    """Main StreamIQ dashboard entry point."""
    init_db()
    st.set_page_config(
        page_title="StreamIQ",
        page_icon="assets/streamiq_favicon_dark.png",
        layout="wide"
    )
    st.title("📊 StreamIQ")
    st.markdown("Modular NLP pipeline with enterprise-ready branding")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    nav = st.sidebar.radio("Go to:", ["Overview", "Charts", "Data", "Exports", "Settings"])
    st.sidebar.subheader("Mode")
    demo_mode = st.sidebar.checkbox("Demo Mode", value=True)

    # Load data
    if demo_mode:
        df = pd.DataFrame({"category": ["A", "B", "C"], "value": [10, 20, 30]})
    else:
        df = load_pipeline_data()

    # Navigation logic
    if nav == "Overview":
        st.subheader("Overview")
        if demo_mode:
            st.info("Currently running in Demo Mode with sample data.")
        else:
            st.success("Live Mode: Connected to pipeline outputs.")

            # --- Custom transcript insertion ---
            st.markdown("### Add Transcript")
            text_input = st.text_input("Transcript text")
            sentiment_input = st.selectbox("Sentiment", ["positive", "neutral", "negative"])

            if st.button("➕ Insert Transcript"):
                if text_input and sentiment_input:
                    insert_transcript(text_input, sentiment_input)
                    st.success("Transcript inserted successfully!")
                    # Reload data so chart updates
                    df = load_pipeline_data()
                else:
                    st.error("Please enter text and select sentiment.")

    elif nav == "Charts":
        st.subheader("Branded Chart")
        chart = alt.Chart(df).mark_bar().encode(x="category", y="value")
        st.altair_chart(add_chart_watermark(chart), use_container_width=True)

    elif nav == "Data":
        st.subheader("Data Preview")
        st.dataframe(df)

    elif nav == "Exports":
        st.subheader("Export Options")
        col1, col2, col3 = st.columns(3)
        if col1.button("Export PDF"):
            export_pdf_with_logo("report.pdf")
            st.success("PDF exported with branding!")
        if col2.button("Export Excel"):
            export_excel_with_branding(df, "data.xlsx")
            st.success("Excel exported with branding!")
        if col3.button("Export CSV"):
            export_csv_with_branding(df, "data.csv")
            st.success("CSV exported with branding!")

    elif nav == "Settings":
        st.subheader("Settings")
        st.info("Theme-aware branding is automatically applied based on Streamlit theme.")

        # --- Reset database option ---
        if st.button("🗑️ Reset Database"):
            reset_db()
            st.success("Database cleared! All transcripts removed.")


def test_app_launch(monkeypatch):
    """Inline smoke test to ensure app launches without errors."""
    monkeypatch.setattr(st, "set_page_config", lambda **kwargs: None)
    try:
        main()
    except Exception as e:
        pytest.fail(f"App failed to launch: {e}")


if __name__ == "__main__":
    main()
