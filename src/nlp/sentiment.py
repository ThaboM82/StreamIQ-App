"""
Sentiment Analysis Module
=========================

Provides a basic sentiment analysis function for StreamIQ.
This can be extended with advanced NLP models for production use.
"""

from textblob import TextBlob
from typing import Dict

def analyze_sentiment(text: str) -> Dict[str, str]:
    """
    Analyze sentiment of the given text.

    Parameters
    ----------
    text : str
        Input text from customer interaction.

    Returns
    -------
    dict
        Dictionary containing sentiment label and polarity score.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1.0 (negative) to +1.0 (positive)

    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "polarity": f"{polarity:.2f}"
    }
