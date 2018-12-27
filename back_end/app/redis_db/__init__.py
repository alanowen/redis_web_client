from flask import Blueprint, g, request
from redis import Redis


redis_db_bp = Blueprint('redis_db_bp', __name__)


@redis_db_bp.url_value_preprocessor
def url_value_preprocessor(endpoint, values):
    g.redis_server_id = values.pop('redis_server_id')
    g.redis_db_num = values.pop('redis_db_num')


@redis_db_bp.url_defaults
def url_defaults(endpoint, values):
    values.setdefault('redis_server_id', g.redis_server_id)
    values.setdefault('redis_db_num', g.redis_db_num)


@redis_db_bp.before_request
def before_request():
    pass


@redis_db_bp.after_request
def teardown_request(response):
    return response


from . import views
