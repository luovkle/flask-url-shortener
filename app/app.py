import os
from secrets import token_urlsafe

from flask import Flask

from app.db import init_app
from app.public import bp as public_bp


def register_blueprints(app):
    app.register_blueprint(public_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=token_urlsafe(64),
        POSTGRES_USER=os.getenv("POSTGRES_USER"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
        POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
        POSTGRES_DB=os.getenv("POSTGRES_DB"),
        CURRENT_HOST=os.getenv("CURRENT_HOST"),
    )
    init_app(app)
    register_blueprints(app)
    return app
