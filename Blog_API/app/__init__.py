from flask import Flask
from config import Config
from app.plugins import db, jwt, cors
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)  # create flask app
    app.config.from_object(Config)  # set config

    # make sure instance directory is present
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize plugins with the app
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    jwt.init_app(app)

    # attach routes
    from app.routes.auth import auth_bp
    from app.routes.blog import blog_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    # default path for a basic view
    @app.get("/")
    def available_routes():
        return f"<h1>Available API Routes:</h1><ul><li>/api/auth/register [POST]</li><li>/api/auth/login [POST]</li><li>/api/auth/refresh [POST]</li><li>/api/auth/current-user [GET]</li><li>/api/posts [GET, POST]</li><li>/posts/:post_id [GET, PUT, DELETE]</li><li>/posts/:post_id/comments [GET, POST]</li></ul>"

    return app
