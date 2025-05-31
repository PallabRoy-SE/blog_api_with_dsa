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

    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    @app.get("/")
    def available_routes():
        return f"<h1>Available API Routes:</h1><ul><li>/api/auth/register [POST]</li><li>/api/auth/login [POST]</li><li>/api/auth/refresh [POST]</li><li>/api/auth/current-user [GET]</li></ul>"

    return app
