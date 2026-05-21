import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import src.utils.loaders as loaders
from src.utils.logger import log_event
from src.utils.branding import (
    export_csv_with_branding,
    export_excel_with_branding,
    export_pdf_with_logo
)
from src.utils.plot_utils import save_professional_plot   # ✅ central helper import

def clean_text(text: str) -> str:
    """Normalize call center transcripts: lowercase, strip whitespace, remove newlines."""
    if not isinstance(text, str):
        return ""
    return text.lower().strip().replace("\n", " ").replace("\r", " ")

def normalize_category(cat: str) -> str:
    """Standardize claim categories or labels."""
    if not isinstance(cat, str):
        return "unknown"
    return cat.strip().lower()

def main():
    if loaders.USE_DUMMY:
        # Seeded demo dataset
        df = pd.DataFrame({
            "transcript": ["hello world", "demo transcript"],
            "claim_type": ["auto", "health"]
        })
        before_rows = len(df)
        after_rows = len(df)
    else:
        if len(sys.argv) < 2:
            print("Usage: python prepare.py <input_csv>")
            sys.exit(1)

        input_file = Path(sys.argv[1])
        df = pd.read_csv(input_file)

        # Apply cleaning rules
        if "transcript" in df.columns:
            df["transcript"] = df["transcript"].apply(clean_text)
        if "claim_type" in df.columns:
            df["claim_type"] = df["claim_type"].apply(normalize_category)

        # Drop duplicates and empty rows
        before_rows = len(df)
        df = df.dropna().drop_duplicates()
        after_rows = len(df)

        print(f"Rows before cleaning: {before_rows}, after cleaning: {after_rows}")
        log_event(f"Prepared dataset: {before_rows} → {after_rows} rows", log_type="PREPARE")

        # Save prepared file
        output_file = input_file.with_name(input_file.stem + "_prepared.csv")
        df.to_csv(output_file, index=False)
        print(f"Prepared file saved to {output_file}")

    # Branded exports with expanded summary
    summary = {
        "Rows Before": before_rows,
        "Rows After": after_rows,
        "Last Refresh": datetime.now().isoformat(timespec="seconds"),
        "Mode": "Dummy" if loaders.USE_DUMMY else "Backend"
    }
    export_csv_with_branding(df, "src/exports/prepared.csv", summary=summary)
    export_excel_with_branding(df, "src/exports/prepared.xlsx", summary=summary, dataset_sheet="Prepared")
    export_pdf_with_logo("src/exports/prepared.pdf", title="StreamIQ Prepared Dataset", df=df, summary=summary)

    # Example: professional plot (if added later)
    fig, ax = plt.subplots()
    df["claim_type"].value_counts().plot(kind="bar", ax=ax)  # demo distribution
    ax.set_title("Claim Type Distribution")
    ax.set_xlabel("Claim Type")
    ax.set_ylabel("Count")
    save_professional_plot(fig, Path("src/exports/claim_type_distribution.png"))

    print("📊 Branded exports saved to src/exports/")

if __name__ == "__main__":
    main()


