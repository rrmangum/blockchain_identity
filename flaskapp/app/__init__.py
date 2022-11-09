import os
from flask import Flask, send_file
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_mail import Mail
from zksync_sdk import ZkSyncLibrary
from datetime import datetime
from .extensions import db, migrate
from .s3_functions import upload_file, show_image
from .models import User

## initialize ZKsync SDK
lib = ZkSyncLibrary()

### Flask extension objects instantiation ###
mail = Mail()

### Application Factory ###
def create_app():

    app = Flask(__name__)
    
    # Needed to handle uploads of credential image files
    UPLOAD_FOLDER = "uploads"

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)
    
    db.init_app(app)
    with app.app_context():
      db.create_all()
        
    # migrate.init_app(app, db)

    # Register blueprints
    register_blueprints(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.index'

    @login_manager.user_loader
    def load_user(user_id):
      return User.query.get(int(user_id))
    return app



### Helper Functions ###
def register_blueprints(app):

  from app.main import main_blueprint
  from app.user import user_blueprint
  from app.credential import credential_blueprint
  from app.roles import roles_blueprint

  from app.register_wallet import register_wallet_blueprint

  app.register_blueprint(register_wallet_blueprint, url_prefix="/register-wallet")
  app.register_blueprint(main_blueprint)
  app.register_blueprint(roles_blueprint, url_prefix='/roles')
  app.register_blueprint(user.user_blueprint, url_prefix='/users')
  app.register_blueprint(credential.credential_blueprint, url_prefix='/credentials')
    
def initialize_extensions(app):
    mail.init_app(app)

def register_error_handlers(app):
  pass

def configure_logging(app):
  pass