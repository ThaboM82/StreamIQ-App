"""
Intent Detection Module
=======================

Provides a basic intent classifier for StreamIQ.
This can be extended with machine learning models
or rule-based approaches for production use.
"""

from typing import Dict

def classify_intent(text: str) -> Dict[str, str]:
    """
    Classify the intent of a given text.

    Parameters
    ----------
    text : str
        Input text from customer interaction.

    Returns
    -------
    dict
        Dictionary containing intent label and confidence score.
    """
    text_lower = text.lower()

    if "help" in text_lower or "support" in text_lower:
        return {"intent": "support_request", "confidence": "0.85"}
    elif "buy" in text_lower or "purchase" in text_lower:
        return {"intent": "purchase_intent", "confidence": "0.80"}
    elif "complain" in text_lower or "not happy" in text_lower:
        return {"intent": "complaint", "confidence": "0.90"}
    else:
        return {"intent": "general", "confidence": "0.60"}
