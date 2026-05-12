import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import src.utils.loaders as loaders
from src.utils.logger import log_event
from src.utils.branding import (
    export_csv_with_branding,
    export_excel_with_branding,
    export_pdf_with_logo
)
from src.utils.plot_utils import save_professional_plot   


def clean_text(text: str) -> str:
    """Normalize text: lowercase, strip whitespace, remove newlines."""
    if not isinstance(text, str):
        return ""
    return text.lower().strip().replace("\n", " ").replace("\r", " ")

def main():
    if loaders.USE_DUMMY:
        # Seeded demo dataset
        df = pd.DataFrame({"text": ["Hello World", "Demo Transcript"]})
    else:
        if len(sys.argv) < 3:
            print("Usage: python preprocess.py <input_csv> <output_csv>")
            sys.exit(1)

        input_file = Path(sys.argv[1])
        output_file = Path(sys.argv[2])

        try:
            df = pd.read_csv(input_file)
        except Exception as e:
            print(f"❌ Error reading {input_file}: {e}")
            sys.exit(1)

        if "text" not in df.columns:
            print("❌ Input file must contain a 'text' column")
            sys.exit(1)

        df["text"] = df["text"].apply(clean_text)

        df.to_csv(output_file, index=False)
        print(f"✅ Preprocessed data saved to {output_file}")

    # Log event
    log_event(f"Preprocessed dataset with {len(df)} rows", log_type="PREPROCESS")

    # Branded exports with expanded summary
    summary = {
        "Total Rows": len(df),
        "Last Refresh": datetime.now().isoformat(timespec="seconds"),
        "Mode": "Dummy" if loaders.USE_DUMMY else "Backend"
    }
    export_csv_with_branding(df, "src/exports/preprocessed.csv", summary=summary)
    export_excel_with_branding(df, "src/exports/preprocessed.xlsx", summary=summary, dataset_sheet="Preprocessed")
    export_pdf_with_logo("src/exports/preprocessed.pdf", title="StreamIQ Preprocessed Dataset", df=df, summary=summary)

    print("📊 Branded exports saved to src/exports/")

if __name__ == "__main__":
    main()
