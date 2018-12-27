from flask import jsonify, g
from redis import Redis

from app import multi_auth, db
from app.models import RedisServer
from . import forms
from . import redis_server_bp


@redis_server_bp.route('/auth', methods=['POST'])
@multi_auth.login_required
def validate_redis_server():
    form = forms.RedisServerConnectionForm()
    if form.validate_on_submit():
        try:
            redis = Redis(host=form.host.data, port=form.port.data)
            redis.ping()
        except Exception as e:
            pass

    return jsonify({})


@redis_server_bp.route('/add', methods=['POST'])
@multi_auth.login_required
def add_redis_server():
    form = forms.RedisServerConnectionForm()
    try:
        if form.validate_on_submit():
            model = RedisServer()
            model.connection_name = form.connection_name.data
            model.host = form.host.data
            model.port = form.port.data
            model.user_id = g.current_user.id
            if form.password.data:
                model.password = form.password.data
            db.session.add(model)
            db.session.commit()
            return jsonify([])
    except Exception as e:
        raise e

    else:
        return jsonify(formError=form.errors)


@redis_server_bp.route('/list', methods=['POST'])
@multi_auth.login_required
def get_redis_server_list():
    q = RedisServer.query.filter(RedisServer.user_id == g.current_user.id)
    data = [
        {
            'value': i.id,
            'label': i.connection_name,
            # 'host': i.host,
            # 'port': i.port,
            'children': []
        } for i in q]
    return jsonify(data)


@redis_server_bp.route('/<int:server_id>/databases', methods=['GET'])
@multi_auth.login_required
def get_databases_of_server(server_id):
    try:
        q = RedisServer.query.get(server_id)
        data = []
        for i in range(16):
            redis = Redis(host=q.host, port=q.port, db=i)
            if redis.dbsize() > 0:
                data.append({
                    'leaf': True,
                    'label': i,
                    'value': i
                })
        return jsonify(data)
    except Exception as e:
        return jsonify([])

