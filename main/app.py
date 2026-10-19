import os
from flask import Flask, jsonify
from config import Config
from models import db
from services.seed_service import seed_database

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.mode_routes import mode_bp
from routes.level_routes import level_bp
from routes.challenge_routes import challenge_bp
from routes.mentor_routes import mentor_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(mode_bp)
    app.register_blueprint(level_bp)
    app.register_blueprint(challenge_bp)
    app.register_blueprint(mentor_bp)

    @app.route('/')
    def root():
        return jsonify({
            'platform': 'Python Quest API',
            'version': '1.0.0',
            'modes': ['beginner', 'intermediate', 'difficult'],
            'total_levels': 300,
            'status': 'Online'
        })

    @app.route('/api/health')
    def health():
        return jsonify({'status': 'healthy', 'database': 'connected'})

    # Initialize tables and seed questions
    with app.app_context():
        db.create_all()
        seed_database()

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    print(f"🎮 Python Quest Backend running at http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
