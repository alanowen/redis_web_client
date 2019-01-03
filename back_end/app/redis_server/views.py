from flask import g
from redis import Redis

from app import multi_auth, db
from app.models import RedisServer
from utils import success_json, alert_json
from . import forms
from . import redis_server_bp


@redis_server_bp.route('/auth', methods=['POST'])
@multi_auth.login_required
def validate_redis_server():
    form = forms.RedisServerEditForm()
    if form.validate_on_submit():
        pass

    return form.errors_to_json()


@redis_server_bp.route('/save', methods=['POST'])
@multi_auth.login_required
def add_redis_server():
    form = forms.RedisServerEditForm()
    if form.validate_on_submit():
        if form.id.data:
            model = RedisServer.query.get(form.id.data)
        else:
            model = RedisServer()
        model.connection_name = form.connection_name.data
        model.host = form.host.data
        model.port = form.port.data
        model.user_id = g.current_user.id
        model.password = form.password.data
        db.session.add(model)
        db.session.commit()

        return alert_json(text='Redis server connection has been saved.')

    return form.errors_to_json()


@redis_server_bp.route('/list', methods=['POST'])
@multi_auth.login_required
def get_redis_server_list():
    q = RedisServer.query.filter(RedisServer.user_id == g.current_user.id)
    data = [
        {
            'value': i.id,
            'label': i.connection_name,
            'host': i.host,
            'port': i.port,
            'password': i.password,
            'children': []
        } for i in q]
    return success_json(data=data)


@redis_server_bp.route('/<int:server_id>/database_list', methods=['GET'])
@multi_auth.login_required
def get_databases_of_server(server_id):
    q = RedisServer.query.get(server_id)
    if q.password:
        redis = Redis(host=q.host, port=q.port, password=q.password)
    else:
        redis = Redis(host=q.host, port=q.port)
    db_count = int(redis.config_get('databases')['databases'])

    data = []
    for i in range(db_count):
        if q.password:
            redis = Redis(host=q.host, port=q.port, password=q.password, db=i)
        else:
            redis = Redis(host=q.host, port=q.port, db=i)
        if redis.dbsize() > 0 or i == 0:
            data.append(
                {
                    'leaf': True,
                    'label': i,
                    'value': i
                }
            )
    return success_json(data=data)

