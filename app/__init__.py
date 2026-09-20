from flask import Flask, send_from_directory
from flask_cors import CORS

def create_app():
    app = Flask(
        __name__,
        static_folder="../frontend",
        static_url_path=""
    )

    CORS(app)

    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def home():
        return send_from_directory(app.static_folder, "index.html")

    return app
