"""
StreamIQ API Routes
===================

Defines REST API endpoints for StreamIQ:
- Health check
- Sentiment + satisfaction analysis
"""

from flask import Blueprint, request, jsonify
from src.nlp.sentiment import analyze_sentiment
from src.satisfaction.predictor import predict_satisfaction

# Create blueprint
api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/health", methods=["GET"])
def health_check():
    """
    Simple health check endpoint.
    """
    return jsonify({"status": "ok", "message": "StreamIQ API is running"}), 200


@api_blueprint.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze customer feedback text.
    Expects JSON: {"text": "..."}
    Returns sentiment + satisfaction score.
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    sentiment = analyze_sentiment(text)
    satisfaction = predict_satisfaction(text)

    return jsonify({
        "text": text,
        "sentiment": sentiment,
        "satisfaction_score": satisfaction
    }), 200
