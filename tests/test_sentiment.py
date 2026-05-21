import pytest
from src.nlp.sentiment import analyze_sentiment

def test_sentiment_positive():
    text = "I love this product!"
    score = analyze_sentiment(text)
    assert score > 0

def test_sentiment_negative():
    text = "I hate waiting in line."
    score = analyze_sentiment(text)
    assert score < 0

def test_sentiment_neutral():
    text = "The product is okay."
    score = analyze_sentiment(text)
    assert -0.1 <= score <= 0.1
