import pytest
from src.satisfaction.predictor import SatisfactionPredictor

def test_predictor_score_range():
    predictor = SatisfactionPredictor()
    score = predictor.predict("The service was excellent")
    assert 0.0 <= score <= 1.0

def test_predictor_consistency():
    predictor = SatisfactionPredictor()
    text = "Average experience"
    score1 = predictor.predict(text)
    score2 = predictor.predict(text)
    assert score1 == pytest.approx(score2)
