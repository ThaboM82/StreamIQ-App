"""
Satisfaction Predictor Module
=============================

Provides a unified predictor that combines sentiment analysis,
intent classification, and satisfaction scoring.
"""

from typing import Dict
from src.nlp.sentiment import analyze_sentiment
from src.nlp.intent import classify_intent

def predict_customer_satisfaction(text: str) -> Dict[str, Dict]:
    """
    Predict customer satisfaction from raw text.

    Parameters
    ----------
    text : str
        Input text from customer interaction.

    Returns
    -------
    dict
        Dictionary containing sentiment, intent, and satisfaction results.
    """
    sentiment_result = analyze_sentiment(text)
    intent_result = classify_intent(text)

    # Inline satisfaction scoring logic
    polarity = float(sentiment_result.get("polarity", 0.0))
    confidence = float(intent_result.get("confidence", 0.0))

    sentiment_score = (polarity + 1) * 50   # scale -1..+1 to 0..100
    intent_score = confidence * 100         # scale 0..1 to 0..100
    satisfaction_score = round((0.7 * sentiment_score + 0.3 * intent_score), 2)

    satisfaction_result = {
        "satisfaction_score": satisfaction_score,
        "sentiment_score": round(sentiment_score, 2),
        "intent_score": round(intent_score, 2)
    }

    return {
        "sentiment": sentiment_result,
        "intent": intent_result,
        "satisfaction": satisfaction_result
    }
