import functools

from flask import g
from redis import Redis

from app import multi_auth


def use_redis(view_func):

    func = _wrap_login(_wrap_redis(view_func))

    @functools.wraps(view_func)
    def decorator(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return decorator


def _wrap_login(f):
    func = multi_auth.login_required(f)

    @functools.wraps(f)
    def _decorator(*args, **kwargs):
        return func(*args, **kwargs)

    return _decorator


def _wrap_redis(f):
    @functools.wraps(f)
    def _decorator(*args, **kwargs):
        if 'redis' not in g:
            model = g.current_user.get_redis_server(g.redis_server_id)
            if model.password:
                redis = Redis(host=model.host,
                              port=model.port,
                              password=model.password,
                              db=g.redis_db_num)
            else:
                redis = Redis(host=model.host,
                              port=model.port,
                              db=g.redis_db_num)
            g.redis = redis
        result = f(*args, **kwargs)
        return result

    return _decorator
