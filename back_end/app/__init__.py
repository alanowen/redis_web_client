from flask import Flask, logging, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, HTTPDigestAuth, MultiAuth

from config import config


db = SQLAlchemy()
token_auth = HTTPTokenAuth()
multi_auth = MultiAuth(token_auth)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name) or config['default'])

    db.init_app(app)

    from app.main import main_bp
    from app.auth import auth_bp
    from app.user import user_bp
    from app.redis_db import redis_db_bp
    from app.redis_server import redis_server_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(redis_db_bp, url_prefix='/redis_db/<int:redis_server_id>/<int:redis_db_num>')
    app.register_blueprint(redis_server_bp, url_prefix='/redis_server')

    @app.errorhandler(404)
    def handle_page_not_found_error(e):
        raise e

    @app.errorhandler(Exception)
    def handle_internal_error(e):
        logger = logging.create_logger(app)
        if app.debug:
            logger.exception(e)
        else:
            logger.error(e)
        return make_response('Error occurred, please try again later.'), 500

    @app.after_request
    def after_request(response):
        if app.debug:
            response.headers['Access-Control-Allow-Origin'] = '%s' % request.environ['HTTP_ORIGIN']
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,OPTIONS,PUT'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response

    return app
