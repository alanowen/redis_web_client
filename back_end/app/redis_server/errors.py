from flask import make_response, logging, current_app, _app_ctx_stack
from redis import AuthenticationError, ResponseError, ConnectionError, RedisError

from . import redis_server_bp


def get_logger():
    return logging.create_logger(current_app)


def make_log(e):
    logger = get_logger()
    if current_app.debug:
        logger.exception(e)
    else:
        logger.error(e)


@redis_server_bp.app_errorhandler(ResponseError)
def handle_redis_response_error(e):
    make_log(e)
    return make_response(str(e)), 500


@redis_server_bp.app_errorhandler(ConnectionError)
def handle_redis_connection_error(e):
    make_log(e)
    return make_response('Failed to connect redis server.'), 500
