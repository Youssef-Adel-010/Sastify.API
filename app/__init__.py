import json
from pathlib import Path
from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Error handlers
    from app.errors.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Helpers
    from app.helpers.jwt_helpers import register_jwt_helper
    register_jwt_helper(jwt)

    # Configurations
    config = f'{Path(__file__).resolve().parent}\config.json'
    app.config.from_file(config, load=json.load)
    
    # Models
    from app.models.role import Role
    from app.models.user import User
    from app.models.user_role import UserRole
    from app.models.user_token import UserToken
    from app.models.blocklist import Blocklist
    
    # Blueprints
    from app.routes.user_routes import user_bp
    app.register_blueprint(blueprint=user_bp, url_prefix='/api/users')
    
    # Dependency Injection
    from app.dependencies.DI import config
    FlaskInjector(app=app, modules=[config])
    
    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    return app
