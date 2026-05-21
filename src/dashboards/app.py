# src/dashboards/app.py
import sys
import os
import streamlit as st
import pandas as pd
import requests
import altair as alt
import time
from datetime import datetime  

# Backend API base URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Path setup — make sure Python sees the project root 
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Imports from src
import src.utils.loaders as loaders
from src.utils.session_state_initializer import init_session_state
from src.utils.export_utils import export_with_summary, render_summary_panel
from src.utils.preferences import export_preferences
from src.db.init_db import init_db
from src.utils.logger import add_log, show_history, clear_logs
from src.db.repository import get_multilingual_samples
from src.utils.preferences import (
    get_theme_preference, set_theme_preference,
    get_sidebar_state, set_sidebar_state,
    get_last_page, set_last_page,
    reset_preferences
)
from src.utils.validators import (
    SUPPORTED_THEMES, SUPPORTED_SIDEBAR_STATES, SUPPORTED_PAGES,
    validate_page, validate_theme, validate_sidebar_state
)
from src.utils.branding import (
    get_theme_assets, check_assets_exist,
    load_branding, add_chart_watermark,
    cli_confirm, render_branding_image, render_demo_mode_banner
)
from src.utils.chart_theme import load_chart_theme, set_chart_theme
from src.satisfaction import SatisfactionPredictor

# ✅ Show branding image once at app load
render_branding_image()

# ✅ CLI confirmation for app initialization
cli_confirm("App initialized with branding")

assets = get_theme_assets()
check_assets_exist()
st.set_page_config(
    page_title="StreamIQ Dashboard",
    page_icon=assets["favicon"],
    layout="wide",
    initial_sidebar_state="expanded"
)

load_branding()
load_chart_theme()

# Helper for charts
def show_chart(chart: alt.Chart, title: str = None):
    """Apply theme + watermark and render chart."""
    set_chart_theme(st.session_state.get("theme_base", "light"))
    chart = add_chart_watermark(chart, mode="Dummy" if loaders.USE_DUMMY else "Backend")
    if title:
        chart = chart.properties(title=title)
    st.altair_chart(chart, use_container_width=True)

def render_demo_mode_banner(mode_label: str = None, mode_color: str = None, location: str = "header"):
    """Render a consistent demo mode banner in header or sidebar."""
    if mode_label is None:
        mode_label = "Dummy Data Mode" if loaders.USE_DUMMY else "Backend Mode"
    if mode_color is None:
        mode_color = "#ffcc80" if loaders.USE_DUMMY else "#c8e6c9"
    banner_html = (
        f"<div style='background-color:{mode_color}; padding:10px; border-radius:5px; "
        f"font-weight:bold; text-align:center;'>🔄 Demo Mode: {mode_label}</div>"
    )
    if location == "header":
        st.markdown(banner_html, unsafe_allow_html=True)
    elif location == "sidebar":
        st.sidebar.markdown(banner_html, unsafe_allow_html=True)

def render_timestamp_banner(ts: str, location: str = "header"):
    """Render a consistent timestamp banner in header or sidebar."""
    banner_html = (
        f"<div style='background-color:#eee; color:#333; padding:10px; "
        f"text-align:center; font-size:14px;'>Last refreshed at {ts}</div>"
    )
    if location == "header":
        st.markdown(banner_html, unsafe_allow_html=True)
    elif location == "sidebar":
        st.sidebar.markdown(banner_html, unsafe_allow_html=True)
# ============================
# Header / UI Setup
# ============================
assets = get_theme_assets()
check_assets_exist()
st.set_page_config(
    page_title="StreamIQ Dashboard",
    page_icon=assets["favicon"],
    layout="wide",
    initial_sidebar_state="expanded"
)

load_branding()
load_chart_theme()

# Auto-detect mode label and color
mode_label = "Dummy Data Mode" if loaders.USE_DUMMY else "Backend Mode"
mode_color = "#ffcc80" if loaders.USE_DUMMY else "#c8e6c9"

# Render banner in header
render_demo_mode_banner(mode_label=mode_label, mode_color=mode_color, location="header")

# Global Timestamp Banner (Header)
render_timestamp_banner(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), location="header")

# Sidebar Snapshot
st.sidebar.markdown("### 📊 Status Panel")
st.sidebar.write(f"Theme: {get_theme_preference() or 'light'}")
st.sidebar.write(f"Sidebar: {get_sidebar_state() or 'expanded'}")
st.sidebar.write(f"Last Page: {get_last_page() or 'Home'}")
st.sidebar.write(f"Last Refresh: {datetime.now().strftime('%H:%M:%S')}")

# ============================
# Sidebar Controls & Audit Trail
# ============================
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    last_refresh = st.session_state.get("last_refresh", "Never")
    lazy_state = st.session_state.get("lazy_load", False)
    audit_log = st.session_state.get("audit_log", [])

    # Backend demo status
    demo_status = None
    try:
        resp = requests.get(f"{BACKEND_URL}/demo_status", timeout=5)
        if resp.status_code == 200:
            demo_status = resp.json()
    except Exception:
        add_log("Backend unreachable during demo_status fetch", log_type="ERROR")

    if demo_status:
        mode_label = "Backend Mode" if demo_status.get("mode") == "Backend" else "Dummy Data Mode"
        mode_color = "#c8e6c9" if mode_label == "Backend Mode" else "#ffcc80"
        render_demo_mode_banner(mode_label, mode_color, location="sidebar")

        callcenter_count = demo_status.get("callcenter_cached", 0)
        claims_count = demo_status.get("claims_cached", 0)
        bigdata_count = demo_status.get("bigdata_cached", 0)
        last_refresh_backend = demo_status.get("last_refresh", "N/A")

        st.write(f"Backend Last Refresh: {last_refresh_backend}")
        st.write(f"Cached Records → CallCenter: {callcenter_count}, Claims: {claims_count}, BigData: {bigdata_count}")

        if st.button("🔄 Refresh Demo Status"):
            try:
                resp = requests.get(f"{BACKEND_URL}/demo_status", timeout=5)
                if resp.status_code == 200:
                    demo_status = resp.json()
                    st.success("Demo status refreshed!")
                    add_log("Demo status refreshed", log_type="INFO")
                else:
                    st.warning("⚠️ Could not refresh demo status.")
            except Exception:
                st.error("⚠️ Backend unreachable during refresh.")
                add_log("Backend unreachable during demo_status refresh", log_type="ERROR")
    else:
        st.warning("⚠️ Backend unreachable — showing local mode only.")
        st.write(f"Local Mode: {'Dummy Data Mode' if loaders.USE_DUMMY else 'Backend Mode'}")

    # ✅ Sidebar Timestamp Banner
    render_timestamp_banner(last_refresh, location="sidebar")

    if st.button("🔄 Global Refresh"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["last_refresh"] = timestamp
        audit_log.append(f"🔄 Global Refresh at {timestamp}")
        st.session_state["audit_log"] = audit_log
        add_log("Global Refresh triggered", log_type="INFO")
        st.rerun()

    if st.button("⚙️ Run Backend Task"):
        with st.spinner("Processing backend task..."):
            time.sleep(2)
        st.success("Backend task completed successfully!")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["last_refresh"] = timestamp
        audit_log.append(f"⚙️ Backend task at {timestamp}")
        st.session_state["audit_log"] = audit_log
        add_log("Backend task executed", log_type="INFO")
        st.rerun()

    lazy_load = st.checkbox("Enable Lazy Loading", value=lazy_state)
    st.session_state["lazy_load"] = lazy_load

    st.markdown("### 📝 Audit Trail")
    if audit_log:
        df_audit = pd.DataFrame({"Action": audit_log})
        st.dataframe(df_audit.tail(5), use_container_width=True)
    else:
        st.write("No actions logged yet.")

# ============================
# Page Selector
# ============================
page = st.sidebar.selectbox(
    "Select a page",
    [
        "📝 Feedback Analysis",
        "🎤 Speech-to-Text Demo",
        "📞 Call Center Demo",
        "📑 Claims Demo",
        "💾 Big Data Demo",
        "🌐 Multilingual Demo",
        "🗂️ Backend Logs",
        "⬇️ Download Center",
        "📜 Audit Trail",
        "⚙️ Settings",
        "ℹ️ About"
    ]
)
# ============================
# Cached Data Loaders (Unified & Resilient)
# ============================

@st.cache_data
def load_call_center(limit=10):
    """Load Call Center records with backend + demo fallback."""
    with st.spinner("Loading Call Center data..."):
        try:
            resp = requests.get(f"{BACKEND_URL}/callcenter?limit={limit}", timeout=5)
            resp.raise_for_status()
            df = pd.DataFrame(resp.json())
            mode = "Backend Mode"
        except Exception:
            st.warning("⚠️ Backend unreachable — showing demo Call Center data")
            df = pd.DataFrame([
                {"ConversationID": 1, "Agent": "Alice", "Calls": 42},
                {"ConversationID": 2, "Agent": "Bob", "Calls": 37},
                {"ConversationID": 3, "Agent": "Charlie", "Calls": 58},
            ])
            mode = "Dummy Data Mode"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df, ts, mode


@st.cache_data
def load_claims(limit=10):
    """Load Claims records with backend + demo fallback."""
    with st.spinner("Loading Claims data..."):
        try:
            resp = requests.get(f"{BACKEND_URL}/claims?limit={limit}", timeout=5)
            resp.raise_for_status()
            df = pd.DataFrame(resp.json())
            mode = "Backend Mode"
        except Exception:
            st.warning("⚠️ Backend unreachable — showing demo Claims data")
            df = pd.DataFrame([
                {"ClaimID": 101, "ClaimType": "Auto", "Status": "Open", "Amount": 5000},
                {"ClaimID": 102, "ClaimType": "Home", "Status": "Closed", "Amount": 12000},
                {"ClaimID": 103, "ClaimType": "Health", "Status": "Pending", "Amount": 3000},
            ])
            mode = "Dummy Data Mode"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df, ts, mode


@st.cache_data
def load_bigdata(limit=10):
    """Load Big Data records with backend + demo fallback."""
    with st.spinner("Loading Big Data demo..."):
        try:
            resp = requests.get(f"{BACKEND_URL}/bigdata?limit={limit}", timeout=5)
            resp.raise_for_status()
            df = pd.DataFrame(resp.json())
            mode = "Backend Mode"
        except Exception:
            st.warning("⚠️ Backend unreachable — showing demo Big Data records")
            df = pd.DataFrame([
                {"RecordID": 201, "Category": "Finance", "Value": 0.87},
                {"RecordID": 202, "Category": "Retail", "Value": 0.65},
                {"RecordID": 203, "Category": "Insurance", "Value": 0.92},
            ])
            mode = "Dummy Data Mode"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df, ts, mode


@st.cache_data
def load_multilingual(limit=10):
    """Load multilingual demo records directly from DB repository or fallback."""
    try:
        samples = get_multilingual_samples(limit=limit)
        df = pd.DataFrame(samples)
        mode = "Backend Mode"
    except Exception:
        st.warning("⚠️ Backend unreachable — showing demo multilingual samples")
        df = pd.DataFrame([
            {"Language": "English", "Text": "Hello"},
            {"Language": "isiZulu", "Text": "Sawubona"},
            {"Language": "Sepedi", "Text": "Dumela"},
        ])
        mode = "Dummy Data Mode"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df, ts, mode


@st.cache_data
def load_audit_logs(limit=50):
    """Load Audit Logs with backend + demo fallback."""
    with st.spinner("Loading Audit Logs..."):
        try:
            resp = requests.get(f"{BACKEND_URL}/auditlog?limit={limit}", timeout=5)
            resp.raise_for_status()
            df = pd.DataFrame(resp.json())
            mode = "Backend Mode"
        except Exception:
            st.warning("⚠️ Backend unreachable — showing demo Audit Logs")
            df = pd.DataFrame([
                {"LogID": 1, "Action": "Demo Refresh", "Timestamp": "2026-05-12 23:00:00"},
                {"LogID": 2, "Action": "Demo Export", "Timestamp": "2026-05-12 23:01:00"},
            ])
            mode = "Dummy Data Mode"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df, ts, mode


@st.cache_data
def load_backend_logs(limit=100):
    """Load Backend Logs with backend + demo fallback."""
    with st.spinner("Loading Backend Logs..."):
        try:
            resp = requests.get(f"{BACKEND_URL}/backendlogs?limit={limit}", timeout=5)
            resp.raise_for_status()
            df = pd.DataFrame(resp.json())
            mode = "Backend Mode"
        except Exception:
            st.warning("⚠️ Backend unreachable — showing demo Backend Logs")
            df = pd.DataFrame([
                {"LogID": 1, "event": "Demo Start", "log_type": "INFO", "timestamp": "2026-05-13 11:50:00"},
                {"LogID": 2, "event": "Demo Export", "log_type": "SYSTEM", "timestamp": "2026-05-13 11:52:00"},
                {"LogID": 3, "event": "Demo Reset", "log_type": "ERROR", "timestamp": "2026-05-13 11:55:00"},
            ])
            mode = "Dummy Data Mode"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df, ts, mode

# ------------------------------- 
# Feedback Analysis Page
# -------------------------------
if page == "📝 Feedback Analysis":
    st.header("📝 Feedback Analysis")

    user_input = st.text_area("Enter feedback text:")
    if st.button("Analyze Feedback"):
        if user_input.strip():
            predictor = SatisfactionPredictor()
            result = predictor.predict(user_input)

            sentiment = result["sentiment"]
            intent = result["intent"]
            satisfaction = result["satisfaction"]

            st.subheader("Analysis Results")
            st.write(f"**Sentiment:** {sentiment}")
            st.write(f"**Intent:** {intent}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Satisfaction Score", satisfaction["satisfaction_score"])
            with col2:
                st.metric("Sentiment Score", satisfaction["sentiment_score"])
            with col3:
                st.metric("Intent Score", satisfaction["intent_score"])

            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.write("---")
            st.write(f"✅ Metrics generated at {ts} | Mode: DEMO")

            if "feedback_history" not in st.session_state:
                st.session_state.feedback_history = []
            st.session_state.feedback_history.append({
                "timestamp": ts,
                "text": user_input,
                "sentiment": sentiment,
                "intent": intent,
                "satisfaction": satisfaction
            })

            add_log("Ran Feedback Analysis", log_type="INFO")

            df = pd.DataFrame(st.session_state.feedback_history)
            excel_data, csv_data, fname = export_with_summary(
                df, "feedback_analysis.xlsx", dataset_sheet="Feedback", ts=ts, mode="Demo"
            )
            st.download_button("⬇️ Download Feedback (Excel)", data=excel_data, file_name=fname,
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            st.download_button("⬇️ Download Feedback (CSV)", data=csv_data, file_name=fname.replace(".xlsx", ".csv"),
                               mime="text/csv")

            render_summary_panel(df, ts, "Demo")
        else:
            st.warning("Please enter feedback text.")

# -------------------------------
# Speech-to-Text Demo Page
# -------------------------------
elif page == "🎤 Speech-to-Text Demo":
    st.header("🎤 Speech-to-Text Demo")

    audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])
    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")
        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing audio..."):
                try:
                    files = {"file": audio_file}
                    response = requests.post(f"{BACKEND_URL}/transcribe", files=files)
                    if response.status_code == 200:
                        transcription = response.json().get("transcription", "")
                        st.subheader("📝 Transcription Result")
                        st.write(transcription)

                        if "transcriptions" not in st.session_state:
                            st.session_state.transcriptions = []
                        st.session_state.transcriptions.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "file_name": audio_file.name,
                            "transcription": transcription
                        })
                        add_log("Ran Speech-to-Text Demo", log_type="INFO")
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Transcription failed: {e}")

    if "transcriptions" in st.session_state and st.session_state.transcriptions:
        df = pd.DataFrame(st.session_state.transcriptions)
        st.dataframe(df, use_container_width=True)

        excel_data, csv_data, fname = export_with_summary(
            df, "transcriptions.xlsx", dataset_sheet="Transcriptions",
            ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mode="Demo"
        )
        st.download_button("⬇️ Download Transcriptions (Excel)", data=excel_data, file_name=fname,
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.download_button("⬇️ Download Transcriptions (CSV)", data=csv_data, file_name=fname.replace(".xlsx", ".csv"),
                           mime="text/csv")

        render_summary_panel(df, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Demo")
    else:
        st.info("No transcriptions yet.")

# -------------------------------
# Call Center Demo
# -------------------------------
elif page == "📞 Call Center Demo":
    st.header("📞 Call Center Demo")

    df, ts, mode = loaders.load_call_center(limit=50)
    st.caption(f"Data loaded at {ts} | Mode: {mode}")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        render_summary_panel(df, ts, mode)

        exports = export_callcenter(limit=50)
        st.download_button("⬇️ Download Excel", data=exports["excel"][0], file_name=exports["excel"][1])
        st.download_button("⬇️ Download PDF", file_name=exports["pdf"], data=open(exports["pdf"], "rb").read())
        st.download_button("⬇️ Download CSV", file_name=exports["csv"], data=open(exports["csv"], "rb").read())
    else:
        st.warning("No Call Center records available.")

# -------------------------
# Claims Demo
# -------------------------------
elif page == "🧾 Claims Demo":
    st.header("🧾 Claims Demo")

    df, ts, mode = loaders.load_claims(limit=50)
    st.caption(f"Data loaded at {ts} | Mode: {mode}")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        render_summary_panel(df, ts, mode)

        exports = export_claims(limit=50)
        st.download_button("⬇️ Download Excel", data=exports["excel"][0], file_name=exports["excel"][1])
        st.download_button("⬇️ Download PDF", file_name=exports["pdf"], data=open(exports["pdf"], "rb").read())
        st.download_button("⬇️ Download CSV", file_name=exports["csv"], data=open(exports["csv"], "rb").read())
    else:
        st.warning("No Claims records available.")

# -------------------------------
# Big Data Demo
# -------------------------------
# 📊 Big Data Demo
elif page == "📊 Big Data Demo":
    st.header("📊 Big Data Demo")

    df, ts, mode = loaders.load_bigdata(limit=50)
    st.caption(f"Data loaded at {ts} | Mode: {mode}")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        render_summary_panel(df, ts, mode)

        exports = export_bigdata(limit=50)
        st.download_button("⬇️ Download Excel", data=exports["excel"][0], file_name=exports["excel"][1])
        st.download_button("⬇️ Download PDF", file_name=exports["pdf"], data=open(exports["pdf"], "rb").read())
        st.download_button("⬇️ Download CSV", file_name=exports["csv"], data=open(exports["csv"], "rb").read())
    else:
        st.warning("No Big Data records available.")

# -------------------------------
# Multilingual Demo Page
# -------------------------------
# 🌐 Multilingual Demo
elif page == "🌐 Multilingual Demo":
    st.header("🌐 Multilingual Demo")

    df, ts, mode = loaders.load_multilingual(limit=50)
    st.caption(f"Data loaded at {ts} | Mode: {mode}")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        render_summary_panel(df, ts, mode)

        exports = export_multilingual(limit=50)
        st.download_button("⬇️ Download Excel", data=exports["excel"][0], file_name=exports["excel"][1])
        st.download_button("⬇️ Download PDF", file_name=exports["pdf"], data=open(exports["pdf"], "rb").read())
        st.download_button("⬇️ Download CSV", file_name=exports["csv"], data=open(exports["csv"], "rb").read())
    else:
        st.warning("No multilingual records available.")

# -------------------------------
# Download Center Page
# -------------------------------
elif page == "⬇️ Download Center":
    st.header("⬇️ Download Center")

    # ✅ Demo Mode banner for stakeholder clarity
    render_demo_mode_banner()

    st.subheader("📥 Export Options")

    # Export Feedback History
    if "feedback_history" in st.session_state and st.session_state.feedback_history:
        df = pd.DataFrame(st.session_state.feedback_history)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.dataframe(df, use_container_width=True)

        excel_data, csv_data, fname = export_with_summary(
            df, "feedback_history.xlsx", dataset_sheet="Feedback", ts=ts, mode="Demo"
        )
        st.download_button("⬇️ Download Feedback History (Excel)", data=excel_data,
                           file_name=fname, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.download_button("⬇️ Download Feedback History (CSV)", data=csv_data,
                           file_name=fname.replace(".xlsx", ".csv"), mime="text/csv")

        render_summary_panel(df, ts, "Demo")
    else:
        st.info("No feedback history available.")

    # Export Backend Logs
    df, ts, mode = loaders.load_backend_logs(limit=100)
    st.caption(f"Backend logs loaded at {ts} | Mode: {mode}")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        excel_data, csv_data, fname = export_with_summary(
            df, "backend_logs.xlsx", dataset_sheet="BackendLogs", ts=ts, mode=mode
        )
        st.download_button("⬇️ Download Backend Logs (Excel)", data=excel_data,
                           file_name=fname, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.download_button("⬇️ Download Backend Logs (CSV)", data=csv_data,
                           file_name=fname.replace(".xlsx", ".csv"), mime="text/csv")

        render_summary_panel(df, ts, mode)
    else:
        st.info("No backend logs available.")

    # Export Preferences Snapshot
    prefs_snapshot = {
        "Theme": get_theme_preference(),
        "Sidebar State": get_sidebar_state(),
        "Last Page": get_last_page(),
        "Last Refresh": st.session_state.get("last_refresh", "Never")
    }
    df = pd.DataFrame([prefs_snapshot])
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.dataframe(df, use_container_width=True)

    excel_data, csv_data, fname = export_with_summary(
        df, "preferences_snapshot.xlsx", dataset_sheet="Preferences", ts=ts, mode=mode
    )
    st.download_button("⬇️ Download Preferences Snapshot (Excel)", data=excel_data,
                       file_name=fname, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.download_button("⬇️ Download Preferences Snapshot (CSV)", data=csv_data,
                       file_name=fname.replace(".xlsx", ".csv"), mime="text/csv")

    render_summary_panel(df, ts, mode)

    add_log("Viewed Download Center Page", log_type="INFO")

#-------------------------------
# Bank Records Page
#-------------------------------
elif page == "🏦 Bank Records":
    st.header("🏦 Bank Records")

    # ✅ Unified loader return
    df, ts, mode = loaders.load_bank_records(limit=50)
    st.caption(f"Bank records loaded at {ts} | Mode: {mode}")

    if not df.empty:
        # ✅ Polished dataframe view
        st.dataframe(df, use_container_width=True)

        # ✅ Stakeholder-ready summary panel
        render_summary_panel(df, ts, mode)

        # ✅ Branded export with summary
        exports = export_bank_records(limit=50)
        st.download_button("⬇️ Download Excel", data=exports["excel"][0], file_name=exports["excel"][1])
        st.download_button("⬇️ Download PDF", data=open(exports["pdf"], "rb").read(), file_name=exports["pdf"])
        st.download_button("⬇️ Download CSV", data=open(exports["csv"], "rb").read(), file_name=exports["csv"])
    else:
        st.warning("No Bank Records available.")

#-------------------------------
# Insurance Records Page
#-------------------------------
elif page == "🛡️ Insurance Records":
    st.header("🛡️ Insurance Records")

    # ✅ Unified loader return
    df, ts, mode = loaders.load_insurance_records(limit=50)
    st.caption(f"Insurance records loaded at {ts} | Mode: {mode}")

    if not df.empty:
        # ✅ Polished dataframe view
        st.dataframe(df, use_container_width=True)

        # ✅ Stakeholder-ready summary panel
        render_summary_panel(df, ts, mode)

        # ✅ Branded export with summary
        exports = export_insurance_records(limit=50)
        st.download_button("⬇️ Download Excel", data=exports["excel"][0], file_name=exports["excel"][1])
        st.download_button("⬇️ Download PDF", data=open(exports["pdf"], "rb").read(), file_name=exports["pdf"])
        st.download_button("⬇️ Download CSV", data=open(exports["csv"], "rb").read(), file_name=exports["csv"])
    else:
        st.warning("No Insurance Records available.")

# -------------------------------
# Audit Trail Page
# -------------------------------
elif page == "📜 Audit Trail":
    st.header("📜 Audit Trail")

    # ✅ Demo Mode banner for stakeholder clarity
    render_demo_mode_banner()

    # ✅ Unified loader return
    df, ts, mode = loaders.load_audit_logs(limit=100)
    st.caption(f"Audit logs loaded at {ts} | Mode: {mode}")

    if not df.empty:
        # ✅ Polished dataframe view
        st.dataframe(df, use_container_width=True)

        # 📈 Trend chart — actions over time
        df["count"] = 1
        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X("Timestamp:T", title="Time"),
                y=alt.Y("count:Q", aggregate="sum", title="Event Count"),
                color=alt.Color("Action:N", title="Action Type"),
                tooltip=["Timestamp:T", "Action:N", "LogID:N"]
            )
            .properties(width=700, height=400)
        )
        show_chart(chart, title="Audit Log Activity")

        # ✅ Branded export with summary
        excel_data, csv_data, fname = export_with_summary(
            df, "audit_trail.xlsx", dataset_sheet="AuditTrail", ts=ts, mode=mode
        )
        st.download_button("⬇️ Download Audit Trail (Excel)", data=excel_data,
                           file_name=fname, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.download_button("⬇️ Download Audit Trail (CSV)", data=csv_data,
                           file_name=fname.replace(".xlsx", ".csv"), mime="text/csv")

        # ✅ Unified summary footer
        render_summary_panel(df, ts, mode)

        # 🗑️ Reset audit trail
        st.subheader("🗑️ Reset Audit Trail")
        confirm_reset = st.checkbox("Confirm reset of audit trail")
        if st.button("Reset Audit Trail"):
            if confirm_reset:
                try:
                    clear_logs()
                    reset_preferences()  # ✅ also clear preferences for consistency
                    st.success("Audit trail and preferences reset successfully.")
                    add_log("Reset Audit Trail", log_type="INFO")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to reset audit trail: {e}")
                    add_log("Audit trail reset failed", log_type="ERROR")
            else:
                st.info("Please confirm before resetting audit trail.")

        add_log("Viewed Audit Trail Page", log_type="INFO")
    else:
        st.info("No audit trail data available.")

# -------------------------------
# Settings Page
# -------------------------------
elif page == "⚙️ Settings":
    st.header("⚙️ Settings")

    # --- Theme Preference ---
    st.subheader("🎨 Theme Preference")
    current_theme = get_theme_preference()
    theme_choice = st.radio(
        "Select Theme",
        SUPPORTED_THEMES,
        index=SUPPORTED_THEMES.index(current_theme) if current_theme in SUPPORTED_THEMES else 0
    )
    if st.button("Save Theme Preference"):
        set_theme_preference(theme_choice)
        st.success(f"Theme preference saved: {theme_choice}")
        add_log(f"Theme set to {theme_choice}", log_type="INFO")

    # --- Sidebar State Preference ---
    st.subheader("📐 Sidebar State")
    current_sidebar = get_sidebar_state()
    sidebar_choice = st.radio(
        "Select Sidebar State",
        SUPPORTED_SIDEBAR_STATES,
        index=SUPPORTED_SIDEBAR_STATES.index(current_sidebar) if current_sidebar in SUPPORTED_SIDEBAR_STATES else 0
    )
    if st.button("Save Sidebar Preference"):
        set_sidebar_state(sidebar_choice)
        st.success(f"Sidebar preference saved: {sidebar_choice}")
        add_log(f"Sidebar set to {sidebar_choice}", log_type="INFO")

    # --- Last Page Preference ---
    st.subheader("📄 Last Page Preference")
    current_page = get_last_page()
    page_choice = st.selectbox(
        "Select Last Page",
        SUPPORTED_PAGES,
        index=SUPPORTED_PAGES.index(current_page) if current_page in SUPPORTED_PAGES else 0
    )
    if st.button("Save Last Page Preference"):
        set_last_page(page_choice)
        st.success(f"Last page preference saved: {page_choice}")
        add_log(f"Last page set to {page_choice}", log_type="INFO")

    # --- Reset Preferences ---
    st.subheader("🗑️ Reset Preferences")
    confirm_reset = st.checkbox("Confirm reset of preferences")
    if st.button("Reset Preferences"):
        if confirm_reset:
            reset_preferences()
            st.success("Preferences reset successfully.")
            add_log("Preferences reset", log_type="INFO")
            st.rerun()
        else:
            st.info("Please confirm before resetting preferences.")

    # --- Export Preferences Snapshot ---
    st.subheader("📤 Export Preferences Snapshot")
    exports = export_preferences(base_filename="preferences_snapshot")

    st.download_button("⬇️ Download Preferences Snapshot (Excel)", data=exports["excel"][0],
                       file_name=exports["excel"][1], mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.download_button("⬇️ Download Preferences Snapshot (CSV)", data=open(exports["csv"], "rb").read(),
                       file_name=exports["csv"], mime="text/csv")
    st.download_button("⬇️ Download Preferences Snapshot (PDF)", data=open(exports["pdf"], "rb").read(),
                       file_name=exports["pdf"], mime="application/pdf")

    # ✅ Unified summary footer
    df = pd.DataFrame([{
        "Theme": get_theme_preference(),
        "Sidebar State": get_sidebar_state(),
        "Last Page": get_last_page(),
        "Last Refresh": st.session_state.get("last_refresh", "Never")
    }])
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    render_summary_panel(df, ts, "Demo")

    add_log("Viewed Settings Page", log_type="INFO")

# -------------------------------
# About Page
# -------------------------------
elif page == "ℹ️ About":
    st.header("ℹ️ About")

    st.markdown("""
    ### StreamIQ Dashboard
    Modular NLP pipeline for banks, insurers, and call centers.
    Features:
    - Persistent user preferences
    - Branded exports with compliance audit trail
    - Demo polish checklist for presentations
    - Multilingual text processing
    """)

    # --- Export About Snapshot ---
    st.subheader("📤 Export About Snapshot")
    exports = export_about(base_filename="about_snapshot")

    st.download_button("⬇️ Download About Snapshot (Excel)", data=exports["excel"][0],
                       file_name=exports["excel"][1], mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.download_button("⬇️ Download About Snapshot (CSV)", data=open(exports["csv"], "rb").read(),
                       file_name=exports["csv"], mime="text/csv")
    st.download_button("⬇️ Download About Snapshot (PDF)", data=open(exports["pdf"], "rb").read(),
                       file_name=exports["pdf"], mime="application/pdf")

    # ✅ Unified summary footer
    df = pd.DataFrame([{
        "Project": "StreamIQ Dashboard",
        "Version": "1.0.0",
        "Lead Developer": "Percy Thabo Mathabela",
        "Location": "Pretoria, South Africa",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    render_summary_panel(df, ts, "Demo")

    add_log("Viewed About Page", log_type="INFO")
