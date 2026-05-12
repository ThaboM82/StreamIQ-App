import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import src.utils.loaders as loaders
from src.utils.logger import log_event
from src.utils.branding import (
    export_csv_with_branding,
    export_excel_with_branding,
    export_pdf_with_logo
)
from src.utils.plot_utils import save_professional_plot   

def save_professional_plot(fig, filename: Path, dpi: int = 120):
    """Save a matplotlib figure with StreamIQ's professional sizing standards."""
    sns.set(font_scale=0.9)
    fig.set_size_inches(5, 4)
    fig.tight_layout()
    fig.savefig(filename, dpi=dpi)
    print(f"📊 Professional plot saved to {filename}")

def main():
    # Resolve paths relative to project root
    base_dir = Path(__file__).resolve().parent.parent
    call_center_path = base_dir / "data" / "call_center_prepared.csv"
    claims_path = base_dir / "data" / "claims_prepared.csv"
    model_path = base_dir / "models" / "sentiment_model.pkl"

    if loaders.USE_DUMMY:
        # Seeded demo dataset
        df = pd.DataFrame({
            "transcript": ["hello world", "demo transcript", "customer complaint"],
            "label": ["positive", "neutral", "negative"]
        })
    else:
        # Load prepared datasets
        call_center = pd.read_csv(call_center_path)
        claims = pd.read_csv(claims_path)
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

    # Log event
    log_event(f"Trained sentiment model on {len(df)} rows", log_type="TRAIN")

    # Export branded metrics with expanded summary
    summary = {
        "Total Rows": len(df),
        "Classes": df['label'].nunique(),
        "Last Refresh": datetime.now().isoformat(timespec="seconds"),
        "Mode": "Dummy" if loaders.USE_DUMMY else "Backend"
    }
    df_metrics = pd.DataFrame({
        "Metric": ["Rows", "Classes"],
        "Value": [len(df), df['label'].nunique()]
    })
    export_csv_with_branding(df_metrics, base_dir / "exports" / "training_metrics.csv", summary=summary)
    export_excel_with_branding(df_metrics, base_dir / "exports" / "training_metrics.xlsx", summary=summary, dataset_sheet="Training")
    export_pdf_with_logo(base_dir / "exports" / "training_metrics.pdf", title="StreamIQ Training Metrics", df=df_metrics, summary=summary)

    # Example: professional training curve (if added later)
    fig, ax = plt.subplots()
    ax.plot([0.7, 0.8, 0.85, 0.9], marker="o")  # dummy accuracy progression
    ax.set_title("Training Accuracy Progression")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")
    save_professional_plot(fig, base_dir / "exports" / "training_curve.png")

    print("📊 Branded training metrics saved to src/exports/")

if __name__ == "__main__":
    main()
