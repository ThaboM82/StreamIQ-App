# src/utils/branding.py
import os
import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
from fpdf import FPDF
import click

# -------------------------------
# Theme-Aware Assets
# -------------------------------
ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets"))

def ensure_placeholder_images():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    files = {
        "streamiq_favicon.png": ("IQ", (64, 64)),
        "streamiq_banner.png": ("StreamIQ Banner", (800, 200)),
        "streamiq_logo.png": ("StreamIQ", (200, 200)),
        "streamiq_logo_tagline.png": ("StreamIQ Tagline", (240, 240))
    }
    for filename, (text, size) in files.items():
        path = os.path.join(ASSETS_DIR, filename)
        if not os.path.exists(path):
            img = Image.new("RGB", size, color=(220, 220, 220))
            draw = ImageDraw.Draw(img)
            draw.text((10, size[1]//2 - 10), text, fill=(50, 50, 50))
            img.save(path)

def get_theme_assets():
    ensure_placeholder_images()
    theme_base = st.session_state.get("theme_base", "light")
    logo_file   = "streamiq_logo.png" if theme_base == "dark" else "streamiq_logo_tagline.png"
    banner_file = "streamiq_banner.png"
    favicon_file = "streamiq_favicon.png"
    return {
        "logo": os.path.join(ASSETS_DIR, logo_file),
        "banner": os.path.join(ASSETS_DIR, banner_file),
        "favicon": os.path.join(ASSETS_DIR, favicon_file),
        "watermark": os.path.join(ASSETS_DIR, "streamiq_watermark.png")
    }

# -------------------------------
# Branding Image Renderer (fallback only)
# -------------------------------
def render_branding_image():
    assets = get_theme_assets()
    if not os.path.exists(assets["banner"]):
        st.write("StreamIQ Dashboard")

# -------------------------------
# Demo Mode Banner Renderer
# -------------------------------
def render_demo_mode_banner():
    theme_base = st.session_state.get("theme_base", "light").capitalize()
    st.markdown(
        f"<div style='background-color:#f0f0f0; padding:10px; text-align:center;'>"
        f"<strong>🚀 StreamIQ Demo Mode — {theme_base} Mode</strong>"
        "</div>",
        unsafe_allow_html=True
    )

# -------------------------------
# Audit Trail Helpers
# -------------------------------
def log_theme_change():
    theme_base = st.session_state.get("theme_base", "light").capitalize()
    assets = get_theme_assets()
    entry = f"🌓 Theme set to {theme_base} Mode — Banner={os.path.basename(assets['banner'])}"
    if "audit_log" not in st.session_state:
        st.session_state["audit_log"] = []
    if "last_theme_entry" not in st.session_state or st.session_state["last_theme_entry"] != entry:
        timestamped_entry = f"{entry} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        st.session_state["audit_log"].append(timestamped_entry)
        st.session_state["last_theme_entry"] = entry
    st.session_state["audit_log"] = st.session_state["audit_log"][-10:]

def render_audit_sidebar():
    if "audit_log" in st.session_state and st.session_state["audit_log"]:
        st.sidebar.markdown("### 📜 Audit Trail")
        for entry in reversed(st.session_state["audit_log"]):
            if "Theme set" in entry:
                st.sidebar.markdown(f"- 🌓 {entry}")
            elif "export complete" in entry.lower():
                st.sidebar.markdown(f"- ✅ {entry}")
            else:
                st.sidebar.markdown(f"- {entry}")

def check_assets_exist():
    assets = get_theme_assets()
    for key, path in assets.items():
        if not os.path.exists(path):
            st.warning(f"⚠️ {key.capitalize()} file missing: {path}")

# -------------------------------
# Branding Loader
# -------------------------------
def apply_branding():
    st.sidebar.markdown("## 🎨 Theme Settings")
    # ✅ Added unique key to avoid duplicate element ID
    theme_choice = st.sidebar.radio("Choose theme:", ["light", "dark"], key="branding_theme_radio")
    st.session_state["theme_base"] = theme_choice

    assets = get_theme_assets()
    st.set_page_config(
        page_title="StreamIQ Dashboard",
        page_icon=assets["favicon"],
        layout="wide"
    )
    if os.path.exists(assets["banner"]):
        st.image(assets["banner"], use_container_width=True)
    if os.path.exists(assets["logo"]):
        st.sidebar.image(assets["logo"], width=160)

    load_chart_theme()
    log_theme_change()
    render_audit_sidebar()
    check_assets_exist()

def load_branding():
    return apply_branding()

# -------------------------------
# Chart Theme Loader
# -------------------------------
def load_chart_theme():
    theme_base = st.session_state.get("theme_base", "light")
    alt.themes.enable("dark" if theme_base == "dark" else "default")

def set_chart_theme(theme_base: str = None):
    if theme_base is None:
        theme_base = st.session_state.get("theme_base", "light")
    alt.themes.enable("dark" if theme_base == "dark" else "default")

# -------------------------------
# Chart Watermarking
# -------------------------------
def add_chart_watermark(chart, mode: str = None):
    assets = get_theme_assets()
    logo_df = pd.DataFrame({'url': [assets["watermark"]], 'x': [1], 'y': [0]})
    logo = alt.Chart(logo_df).mark_image(width=60, height=60).encode(
        x=alt.X('x', scale=alt.Scale(domain=[0, 1]), axis=None),
        y=alt.Y('y', scale=alt.Scale(domain=[0, 1]), axis=None),
        url='url'
    )
    if mode:
        theme_base = st.session_state.get("theme_base", "light")
        text_color = "lightgray" if theme_base == "dark" else "dimgray"
        text_df = pd.DataFrame({'x': [0.95], 'y': [0.05], 'label': [f"Mode: {mode}"]})
        text = alt.Chart(text_df).mark_text(
            align="right", baseline="top", fontSize=12, color=text_color
        ).encode(x='x', y='y', text='label')
        return chart + logo + text
    return chart + logo

# -------------------------------
# Summary Row Helper
# -------------------------------
def add_summary_row(df: pd.DataFrame, ts: str = None, mode: str = None):
    if ts is None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if mode is None:
        mode = "Dummy" if st.session_state.get("theme_base", "light") == "light" else "Backend"
    summary = {
        "Row Count": len(df),
        "Timestamp": ts,
        "Mode": mode,
        "Data Source": "Demo dataset (backend unreachable)" if mode == "Dummy" else "Live backend records"
    }
    summary_df = pd.DataFrame([summary])
    return pd.concat([df, summary_df], ignore_index=True)

# -------------------------------
# Summary Panel Renderer
# -------------------------------
def render_summary_panel(df: pd.DataFrame, ts: str, mode: str = None):
    """Render a consistent summary footer panel for demo pages."""
    st.markdown("---")
    st.markdown("### 📑 Summary Panel")

    if mode is None:
        mode = "Dummy" if st.session_state.get("theme_base", "light") == "light" else "Backend"

    st.metric("Row Count", len(df))
    st.metric("Last Refresh", ts)
    st.metric("Mode", mode)

    if mode == "Dummy":
        st.info("⚠️ Data source: Demo dataset (backend unreachable)")
    else:
        st.success("✅ Data source: Live backend records")

# -------------------------------
# CLI Confirmation Helper
# -------------------------------
def cli_confirm(message: str):
    click.secho(f"✅ {message}", fg="green", bold=True)

# -------------------------------
# Unified Export Helper
# -------------------------------
def export_with_branding(df: pd.DataFrame, filename: str, export_type: str = "excel", dataset_sheet: str = "Data"):
    assets = get_theme_assets()
    theme_base = st.session_state.get("theme_base", "light")
    df = add_summary_row(df, mode=theme_base.capitalize())

    if export_type == "pdf":
        pdf = FPDF()
        pdf.add_page()
        if os.path.exists(assets["logo"]):
            pdf.image(assets["logo"], x=10, y=8, w=60)
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="StreamIQ Report", ln=True, align="C")
        pdf.set_font("Arial", size=10)
        pdf.ln(10)
        col_width = pdf.w / (len(df.columns) + 1)
        row_height = pdf.font_size * 1.5
        for col in df.columns:
            pdf.cell(col_width, row_height, col, border=1)
        pdf.ln(row_height)
        for _, row in df.iterrows():
            for item in row:
                pdf.cell(col_width, row_height, str(item), border=1)
            pdf.ln(row_height)
        if os.path.exists(assets["watermark"]):
            pdf.image(assets["watermark"], x=10, y=260, w=20)
        pdf.set_font("Arial", size=8)
        pdf.cell(0, 10, f"Mode: {theme_base.capitalize()}", ln=True, align="R")
        pdf.output(filename)

    elif export_type == "excel":
        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name=dataset_sheet, index=False)
            worksheet = writer.sheets[dataset_sheet]

            if os.path.exists(assets["logo"]):
                worksheet.insert_image("A1", assets["logo"], {'x_scale': 0.4, 'y_scale': 0.4})
            if os.path.exists(assets["banner"]):
                worksheet.insert_image("B1", assets["banner"], {'x_scale': 0.4, 'y_scale': 0.4})

            worksheet.write(len(df) + 2, 0, f"Mode: {theme_base.capitalize()}")

    elif export_type == "csv":
        df.to_csv(filename, index=False)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"\n# Logo: {os.path.basename(assets['logo'])}\n")
            f.write(f"# Banner: {os.path.basename(assets['banner'])}\n")
            f.write(f"# Mode: {theme_base.capitalize()}\n# Generated by StreamIQ\n")

    else:
        raise ValueError("Unsupported export_type. Use 'pdf', 'excel', or 'csv'.")


# -------------------------------
# Backward-Compatible Aliases
# -------------------------------
def export_csv_with_branding(df: pd.DataFrame, filename: str):
    """Alias for CSV export to maintain compatibility with preferences.py"""
    return export_with_branding(df, filename, export_type="csv")

def export_excel_with_branding(df: pd.DataFrame, filename: str, dataset_sheet: str = "Data"):
    """Alias for Excel export to maintain compatibility with preferences.py"""
    return export_with_branding(df, filename, export_type="excel", dataset_sheet=dataset_sheet)

def export_pdf_with_logo(df: pd.DataFrame, filename: str):
    """Alias for PDF export to maintain compatibility with preferences.py"""
    return export_with_branding(df, filename, export_type="pdf")


# -------------------------------
# About Snapshot Export Helper
# -------------------------------
def render_about_snapshot(ts: str):
    """Compact export + summary for the About page."""
    about_info = {
        "Project": "StreamIQ Dashboard",
        "Version": "1.0.0",
        "Lead Developer": "Percy Thabo Mathabela",
        "Location": "Pretoria, South Africa",
        "Timestamp": ts,
    }
    df = pd.DataFrame([about_info])

    excel_data = None
    csv_data = None
    fname = "about_snapshot.xlsx"

    try:
        excel_data = export_excel_with_branding(df, fname, dataset_sheet="About")
        csv_data = export_csv_with_branding(df, fname.replace(".xlsx", ".csv"))
    except Exception as e:
        st.error(f"❌ Failed to export About snapshot: {e}")

    if excel_data is not None:
        st.download_button("⬇️ Download About Snapshot (Excel)", data=excel_data,
                           file_name=fname, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    if csv_data is not None:
        st.download_button("⬇️ Download About Snapshot (CSV)", data=csv_data,
                           file_name=fname.replace(".xlsx", ".csv"), mime="text/csv")

    # ✅ Unified summary footer
    render_summary_panel(df, ts)


# -------------------------------
# Module Load Confirmation
# -------------------------------
cli_confirm("Branding module loaded")
