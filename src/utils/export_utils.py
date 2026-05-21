import io
import pandas as pd
from datetime import datetime
import streamlit as st

import src.utils.loaders as loaders
from src.utils.branding import (
    get_theme_assets,
    export_pdf_with_logo,
    export_excel_with_branding,
    export_csv_with_branding,
    cli_confirm
)

# -------------------------------
# Core Export Helper
# -------------------------------
def export_with_summary(df, filename_base, dataset_sheet="Data", title="StreamIQ Report", ts=None, mode=None):
    """
    Create branded exports (Excel, PDF, CSV) with a summary sheet/section and dataset sheet.
    """
    if ts is None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if mode is None:
        mode = "Dummy Data Mode" if loaders.USE_DUMMY else "Backend Mode"

    # ✅ Expanded summary with footer
    summary = {
        "Row Count": len(df),
        "Last Refresh": ts,
        "Mode": mode,
        "Footer": f"✅ Completed at {ts} | Mode: {mode}"
    }
    summary_df = pd.DataFrame({
        "Metric": list(summary.keys()),
        "Value": list(summary.values())
    })

    # --- Excel Export ---
    excel_file = f"{filename_base}.xlsx"
    excel_output = io.BytesIO()
    with pd.ExcelWriter(excel_output, engine="xlsxwriter") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        df.to_excel(writer, sheet_name=dataset_sheet, index=False)
        # Insert logo if available
        assets = get_theme_assets()
        worksheet = writer.sheets[dataset_sheet]
        if assets and "logo" in assets:
            try:
                worksheet.insert_image("A1", assets["logo"], {'x_scale': 0.4, 'y_scale': 0.4})
            except Exception:
                pass
    excel_data = excel_output.getvalue()

    # --- PDF Export ---
    pdf_file = f"{filename_base}.pdf"
    export_pdf_with_logo(pdf_file, title=title, df=df, summary=summary)

    # --- CSV Export ---
    csv_file = f"{filename_base}.csv"
    export_csv_with_branding(df, csv_file, summary=summary)

    return {
        "excel": (excel_data, excel_file),
        "pdf": pdf_file,
        "csv": csv_file
    }

# -------------------------------
# Streamlit Summary Panel
# -------------------------------
def render_summary_panel(df, ts=None, mode=None):
    """
    Render a stakeholder-ready summary panel in Streamlit.
    """
    if ts is None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if mode is None:
        mode = "Dummy Data Mode" if loaders.USE_DUMMY else "Backend Mode"

    row_count = len(df)

    st.write("### 📊 Summary Panel")
    st.write(f"- **Row Count:** {row_count}")
    st.write(f"- **Last Refresh:** {ts}")
    st.write(f"- **Mode:** {mode}")
    st.write("---")
    st.write(f"✅ Completed at {ts} | Mode: {mode}")

# -------------------------------
# Dataset-specific exports
# -------------------------------
def export_callcenter(base_filename="callcenter", limit=50):
    df, ts, mode = loaders.load_call_center(limit=limit)
    return export_with_summary(df, base_filename, dataset_sheet="CallCenter", title="StreamIQ Call Center Records", ts=ts, mode=mode)

def export_claims(base_filename="claims", limit=50):
    df, ts, mode = loaders.load_claims(limit=limit)
    return export_with_summary(df, base_filename, dataset_sheet="Claims", title="StreamIQ Claims Records", ts=ts, mode=mode)

def export_bigdata(base_filename="bigdata", limit=50):
    df, ts, mode = loaders.load_bigdata(limit=limit)
    return export_with_summary(df, base_filename, dataset_sheet="BigData", title="StreamIQ Big Data Records", ts=ts, mode=mode)

def export_multilingual(base_filename="multilingual", limit=50):
    df, ts, mode = loaders.load_multilingual(limit=limit)
    return export_with_summary(df, base_filename, dataset_sheet="Multilingual", title="StreamIQ Multilingual Records", ts=ts, mode=mode)

def export_transcriptions(base_filename="transcriptions"):
    df, ts, mode = loaders.load_transcriptions()
    return export_with_summary(df, base_filename, dataset_sheet="Transcriptions", title="StreamIQ Speech-to-Text Records", ts=ts, mode=mode)

def export_auditlogs(base_filename="auditlogs", limit=50):
    df, ts, mode = loaders.load_audit_logs(limit=limit)
    return export_with_summary(df, base_filename, dataset_sheet="AuditLogs", title="StreamIQ Audit Logs", ts=ts, mode=mode)

def export_bank_records(base_filename="bank_records", limit=50):
    df, ts, mode = loaders.load_bank_records(limit=limit)
    return export_with_summary(df, base_filename, dataset_sheet="BankRecords", title="StreamIQ Banking Records", ts=ts, mode=mode)

def export_insurance_records(base_filename="insurance_records", limit=50):
    df, ts, mode = loaders.load_insurance_records(limit=limit)
    return export_with_summary(df, base_filename, dataset_sheet="InsuranceRecords", title="StreamIQ Insurance Records", ts=ts, mode=mode)

def export_callcenter_nlp(base_filename="callcenter_nlp", limit=50):
    df, ts, mode = loaders.load_callcenter_nlp(limit=limit)
    return export_with_summary(df, base_filename, dataset_sheet="CallCenterNLP", title="StreamIQ Call Center NLP Records", ts=ts, mode=mode)

# -------------------------------
# Module Load Confirmation
# -------------------------------
cli_confirm("Export Utils module loaded")
