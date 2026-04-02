"""
StreamIQ Application Entry Point
================================

This module creates and runs the Flask application.
It registers API routes and serves as the main entry point
for the StreamIQ pipeline.
"""

from flask import Flask
from src.api.routes import api_blueprint
from src.utils.logger import logger


def create_app() -> Flask:
    """
    Factory function to create and configure the Flask app.
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")

    # Log startup
    logger.info("StreamIQ Flask app created and API blueprint registered.")

    return app


if __name__ == "__main__":
    app = create_app()
    logger.info("Starting StreamIQ Flask server on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
