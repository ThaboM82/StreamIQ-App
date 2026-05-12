import sys
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import src.utils.loaders as loaders
from src.utils.logger import log_event
from src.utils.branding import (
    export_csv_with_branding,
    export_excel_with_branding,
    export_pdf_with_logo
)
from src.utils.plot_utils import save_professional_plot   

EXPORT_DIR = Path("src/exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def save_professional_plot(fig, filename: Path, dpi: int = 120):
    """Save a matplotlib figure with StreamIQ's professional sizing standards."""
    sns.set(font_scale=0.9)
    fig.set_size_inches(5, 4)
    fig.tight_layout()
    fig.savefig(filename, dpi=dpi)
    print(f"📊 Professional plot saved to {filename}")

def main():
    if loaders.USE_DUMMY:
        # Seeded demo metrics
        acc = 0.91
        cm = [[50, 5], [7, 38]]
        report = "Demo classification report"
        df = pd.DataFrame({"transcript": ["demo1", "demo2"], "label": ["positive", "negative"]})
    else:
        if len(sys.argv) != 3:
            print("Usage: python evaluate.py <model_path> <test_csv>")
            sys.exit(1)

        model_path = sys.argv[1]
        test_file = sys.argv[2]

        # Load model
        model = joblib.load(model_path)

        # Load test dataset
        df = pd.read_csv(test_file)
        if "transcript" not in df.columns or "label" not in df.columns:
            raise ValueError("Test dataset must contain 'transcript' and 'label' columns")

        X = df["transcript"]
        y = df["label"]

        # Predict
        y_pred = model.predict(X)

        # Compute metrics
        acc = accuracy_score(y, y_pred)
        cm = confusion_matrix(y, y_pred, labels=sorted(set(y)))
        report = classification_report(y, y_pred)

        # Professional confusion matrix plot
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=sorted(set(y)),
                    yticklabels=sorted(set(y)), ax=ax)
        ax.set_xlabel("Predicted Label")
        ax.set_ylabel("True Label")
        ax.set_title("Confusion Matrix Heatmap")
        save_professional_plot(fig, EXPORT_DIR / "confusion_matrix.png")

    # Save metrics text
    metrics_path = EXPORT_DIR / "metrics.txt"
    with open(metrics_path, "w") as f:
        f.write(f"Accuracy: {acc:.4f}\n\n")
        f.write("Confusion Matrix:\n")
        f.write(str(cm))
        f.write("\n\nClassification Report:\n")
        f.write(report)

    # Log event
    log_event(f"Evaluation complete with accuracy {acc:.4f}", log_type="EVALUATE")

    # Export branded metrics with expanded summary
    summary = {
        "Accuracy": acc,
        "Total Rows": len(df),
        "Last Refresh": datetime.now().isoformat(timespec="seconds"),
        "Mode": "Dummy" if loaders.USE_DUMMY else "Backend"
    }
    df_metrics = pd.DataFrame({"Metric": ["Accuracy"], "Value": [acc]})
    export_csv_with_branding(df_metrics, EXPORT_DIR / "metrics.csv", summary=summary)
    export_excel_with_branding(df_metrics, EXPORT_DIR / "metrics.xlsx", summary=summary, dataset_sheet="Evaluation")
    export_pdf_with_logo(EXPORT_DIR / "metrics.pdf", title="StreamIQ Evaluation Metrics", df=df_metrics, summary=summary)

    print(f"✅ Evaluation complete. Metrics saved to {metrics_path}")
    print(f"📊 Confusion matrix heatmap saved to {EXPORT_DIR / 'confusion_matrix.png'}")
    print("📊 Branded evaluation metrics saved to src/exports/")

if __name__ == "__main__":
    main()
