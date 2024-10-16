import json
from flask import Flask
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config.from_file(filename='config.json', load=json.load)
    
    
    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
        
    
    # Blueprints
    
    
    
    # Dependency Injection
    # from app.dependencies.DI import config
    # FlaskInjector(app=app, modules=[config])
    
    
    return app