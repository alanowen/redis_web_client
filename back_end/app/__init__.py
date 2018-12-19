from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, HTTPDigestAuth, MultiAuth

from config import config


db = SQLAlchemy()
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
multi_auth = MultiAuth(basic_auth, token_auth)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name) or config['default'])

    db.init_app(app)

    from app.main import main_bp
    from app.auth import auth_bp
    from app.user import user_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')

    @app.errorhandler(404)
    def handle_page_not_found_error(e):
        raise e

    @app.errorhandler(500)
    def handle_internal_error(e):
        raise e

    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,OPTIONS,PUT'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    return app
