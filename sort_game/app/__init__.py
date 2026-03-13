import os
from flask import Flask
from flasgger import Swagger
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .routes.api_routes import api_bp
from .routes.page_routes import page_bp


def create_app():
    app = Flask(__name__)

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1
    )

    # Config読み込み
    app.config.from_object(Config)

    # Flask3 JSON設定（重要）
    app.json.ensure_ascii = False
    app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"

    # Swagger(OpenAPI)
    app.config["SWAGGER"] = {
        "openapi": "3.0.2",
        "title": "Sort Portfolio API",
        "uiversion": 3
    }

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    swagger_path = os.path.join(BASE_DIR, "openapi", "openapi.yaml")

    if not os.path.exists(swagger_path):
        raise FileNotFoundError(f"Swagger file not found: {swagger_path}")

    Swagger(app, template_file=swagger_path)

    app.register_blueprint(page_bp)
    app.register_blueprint(api_bp)

    return app