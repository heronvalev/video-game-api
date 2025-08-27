from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_login import LoginManager

# Initialise SQLAlchemy
db = SQLAlchemy()

# Initialise LoginManager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Load environment variables from .env
    load_dotenv()

    # Secret key for CSRF
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Base directory (root folder)
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Configure SQLite database
    db_path = os.path.join(base_dir, "data", "steam.sqlite")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Set up login manager
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register routes
    from .routes import api_bp
    from .auth import auth_bp
    from .main import main_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app


