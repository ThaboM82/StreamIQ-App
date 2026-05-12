import pandas as pd
import sys
from datetime import datetime

def build_summary(df, mode="live"):
    """Create a stakeholder‑ready summary row with row count, timestamp, and mode indicator."""
    summary = {
        "summary_row": True,
        "row_count": len(df),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": mode
    }
    return pd.DataFrame([summary])

def main():
    if len(sys.argv) < 3:
        print("Usage: python preprocess.py <input_csv> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Load dataset
    df = pd.read_csv(input_file)

    # Simple preprocessing: lowercase text
    if "text" in df.columns:
        df["text"] = df["text"].str.lower()
    else:
        print("❌ Input file must contain a 'text' column")
        sys.exit(1)

    # Build summary row
    summary_df = build_summary(df, mode="live")

    # Append summary row to dataset
    final_df = pd.concat([df, summary_df], ignore_index=True)

    # Save preprocessed file
    final_df.to_csv(output_file, index=False)
    print(f"✅ Preprocessed data saved to {output_file}")
    print(f"📊 Summary row appended with {len(df)} rows, timestamp, and mode indicator.")

if __name__ == "__main__":
    main()
