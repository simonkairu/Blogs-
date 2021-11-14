from flask import Flask
from config import config_option
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos', IMAGES )
mail = Mail()


def create_app(config_name):
    
    # Initializing the application
    app = Flask(__name__)
    
    # Creating the app configurations
    app.config.from_object(config_option[config_name])
    
    # Initializing our extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Will add the views and forms
    from app.models import Posts,User,Comments
    
    # Configure uploadset
    configure_uploads(app, photos)
    
    # Registering blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/authenticate')
    
    return app