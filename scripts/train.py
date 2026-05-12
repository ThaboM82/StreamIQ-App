import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path
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
    # Resolve paths relative to project root
    base_dir = Path(__file__).resolve().parent.parent
    call_center_path = base_dir / "data" / "call_center_prepared.csv"
    claims_path = base_dir / "data" / "claims_prepared.csv"
    model_path = base_dir / "models" / "sentiment_model.pkl"

    # Load prepared datasets
    call_center = pd.read_csv(call_center_path)
    claims = pd.read_csv(claims_path)

    # Combine datasets (assuming both have 'transcript' and 'label' columns)
    df = pd.concat([call_center, claims], ignore_index=True)

    if "transcript" not in df.columns or "label" not in df.columns:
        raise ValueError("Datasets must contain 'transcript' and 'label' columns")

    X = df["transcript"]
    y = df["label"]

    # Build pipeline: TF-IDF + Logistic Regression
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000)),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    # Train model
    pipeline.fit(X, y)

    # Ensure models folder exists
    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Save model
    joblib.dump(pipeline, model_path)
    print(f"✅ Model trained and saved to {model_path}")

    # Build and append summary row
    summary_df = build_summary(df, mode="live")
    final_df = pd.concat([df, summary_df], ignore_index=True)

    # Save training dataset with summary row
    output_file = base_dir / "data" / "training_with_summary.csv"
    final_df.to_csv(output_file, index=False)
    print(f"📊 Training dataset with summary row saved to {output_file}")

if __name__ == "__main__":
    main()
