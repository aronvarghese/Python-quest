# -*- coding: utf-8 -*-
"""
Python Quest Backend - Application Entry Point
Flask Application Factory with Database Lifecycle, CORS, and CLI Seeding.
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name
from database import db
from routes import register_blueprints
from services.seed_service import seed_database

def create_app(config_name=None):
    """Factory function to configure and initialize the Flask application."""
    if not config_name:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    # Setup Cross-Origin Resource Sharing (CORS)
    CORS(app, supports_credentials=True)

    # Initialize SQLAlchemy database
    db.init_app(app)

    # Register API blueprints
    register_blueprints(app)

    # Health check route
    @app.route("/", methods=["GET"])
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "online",
            "platform": "Python Quest Backend",
            "version": "1.0.0",
            "modes_available": ["beginner", "intermediate", "difficult"],
            "total_curriculum_levels": 300,
            "architecture": "Flask + SQLite"
        })

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": "The requested endpoint was not found on this Python Quest server."
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": "Internal server error occurred. Please contact the Python Quest mentor."
        }), 500

    # CLI Command to seed database
    @app.cli.command("seed-db")
    def seed_db_command():
        """CLI Command: flask seed-db - Seeds all 300 levels and sample questions."""
        with app.app_context():
            db.create_all()
            seed_database()
            print("Python Quest 300-level database successfully seeded!")

    # Auto-create tables & seed in development if database is empty
    with app.app_context():
        db.create_all()
        # Seed automatically if no levels exist
        from models import Level
        if Level.query.count() == 0:
            seed_database()

    return app

# WSGI Application object
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
.