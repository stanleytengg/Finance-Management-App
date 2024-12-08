from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

# Loads extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)

    # Loads config and secret key
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Setup login manager
    login_manager.login_view = 'login'
    
    # Loads users
    from app.models.models import User
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))
    
    # Registers routes
    from app.routes import init_routes
    init_routes(app)

    return app

# Creates the app instance
app = create_app()