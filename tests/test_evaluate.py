import pytest
from src.evaluation.evaluate import evaluate_model

def test_binary_classification_metrics():
    y_true = ["Satisfied", "Dissatisfied", "Satisfied", "Dissatisfied"]
    y_pred = ["Satisfied", "Satisfied", "Satisfied", "Dissatisfied"]

    metrics = evaluate_model(y_true, y_pred, labels=["Satisfied", "Dissatisfied"])

    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "confusion_matrix" in metrics
    assert "labels" in metrics

    assert len(metrics["confusion_matrix"]) == 2
    assert all(len(row) == 2 for row in metrics["confusion_matrix"])
    assert 0 <= metrics["accuracy"] <= 1

def test_multiclass_classification_metrics():
    y_true = ["Satisfied", "Neutral", "Dissatisfied", "Satisfied", "Neutral"]
    y_pred = ["Satisfied", "Neutral", "Satisfied", "Satisfied", "Dissatisfied"]

    metrics = evaluate_model(y_true, y_pred, labels=["Satisfied", "Neutral", "Dissatisfied"])

    assert metrics["accuracy"] >= 0
    assert metrics["precision"] >= 0
    assert metrics["recall"] >= 0
    assert metrics["f1_score"] >= 0

    assert len(metrics["confusion_matrix"]) == 3
    assert all(len(row) == 3 for row in metrics["confusion_matrix"])

def test_labels_auto_detection():
    y_true = ["Satisfied", "Neutral", "Dissatisfied"]
    y_pred = ["Satisfied", "Neutral", "Neutral"]

    metrics = evaluate_model(y_true, y_pred)

    assert set(metrics["labels"]) == {"Satisfied", "Neutral", "Dissatisfied"}
