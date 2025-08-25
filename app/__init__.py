from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialise SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Base directory (root folder)
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Configure SQLite database
    db_path = os.path.join(base_dir, "data", "steam.sqlite")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Import and register routes
    from .routes import api_bp
    from .auth import auth_bp
    from .main import main_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app


