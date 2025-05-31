import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "can't_guess_flask_secret_key"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "can't_guess_jwt_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI") or "sqlite:///" + os.path.join(
        basedir, "instance", "data.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
