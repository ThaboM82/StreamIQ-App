import sys
import pandas as pd
from pathlib import Path

def clean_text(text: str) -> str:
    """Normalize call center transcripts: lowercase, strip whitespace, remove newlines."""
    if not isinstance(text, str):
        return ""
    return (
        text.lower()
        .strip()
        .replace("\n", " ")
        .replace("\r", " ")
    )

def normalize_category(cat: str) -> str:
    """Standardize claim categories or labels."""
    if not isinstance(cat, str):
        return "unknown"
    return cat.strip().lower()

def main():
    if len(sys.argv) < 2:
        print("Usage: python prepare.py <input_csv>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    df = pd.read_csv(input_file)

    # Apply cleaning rules depending on dataset
    if "transcript" in df.columns:
        df["transcript"] = df["transcript"].apply(clean_text)

    if "claim_type" in df.columns:
        df["claim_type"] = df["claim_type"].apply(normalize_category)

    # Drop duplicates and empty rows
    before_rows = len(df)
    df = df.dropna().drop_duplicates()
    after_rows = len(df)

    print(f"Rows before cleaning: {before_rows}, after cleaning: {after_rows}")

    # Save prepared file
    output_file = input_file.with_name(input_file.stem + "_prepared.csv")
    df.to_csv(output_file, index=False)
    print(f"Prepared file saved to {output_file}")

if __name__ == "__main__":
    main()
