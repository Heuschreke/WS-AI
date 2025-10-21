from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'routes.login'
    
    from app.routes import register_routes
    register_routes(app)

    return app
