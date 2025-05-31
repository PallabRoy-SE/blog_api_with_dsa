from flask import Flask
from config import Config
from app.plugins import db, jwt, cors
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    jwt.init_app(app)

    @app.get("/")
    def available_routes():
        return f"<h1>Available API Routes:</h1><ul><li>route 1</li></ul>"

    return app
