from flask import Flask
from flask_cors import CORS

from .routes import register_blueprints


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config["JSON_SORT_KEYS"] = False
    app.config["DEBUG"] = True

    register_blueprints(app)
    return app
