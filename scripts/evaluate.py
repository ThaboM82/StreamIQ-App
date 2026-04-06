import sys
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def main():
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

    # Predict on transcripts only
    y_pred = model.predict(X)

    # Compute metrics
    acc = accuracy_score(y, y_pred)
    cm = confusion_matrix(y, y_pred, labels=sorted(set(y)))
    report = classification_report(y, y_pred)

    # Save metrics
    metrics_path = "C:/StreamIQ App/data/metrics.txt"
    with open(metrics_path, "w") as f:
        f.write(f"Accuracy: {acc:.4f}\n\n")
        f.write("Confusion Matrix:\n")
        f.write(str(cm))
        f.write("\n\nClassification Report:\n")
        f.write(report)

    # Plot and save confusion matrix heatmap
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=sorted(set(y)),
                yticklabels=sorted(set(y)))
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix Heatmap")
    plt.tight_layout()
    plt.savefig("C:/StreamIQ App/data/confusion_matrix.png")

    print(f"Evaluation complete. Metrics saved to {metrics_path}")
    print("Confusion matrix heatmap saved to C:/StreamIQ App/data/confusion_matrix.png")

if __name__ == "__main__":
    main()
