from flask import Flask
from config import Config
from app.routes import register_routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
from app.models import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    register_routes(app)

    return app
