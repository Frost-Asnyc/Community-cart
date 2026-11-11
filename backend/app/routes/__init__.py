from flask import Flask

from .listings import listings_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(listings_bp)
