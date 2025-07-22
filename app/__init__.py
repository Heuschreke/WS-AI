from flask import Flask
from config import DevelopmentConfig
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    register_routes(app)

    return app
