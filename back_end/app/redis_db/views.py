from flask import g, request

from utils import success_json, alert_json
from . import forms
from . import redis_db_bp
from .decorators import use_redis


@redis_db_bp.route('/key_list/<int:page>', methods=['GET'])
@use_redis
def get_keys_of_database(page):
    page_size = 20

    total = g.redis.dbsize()
    rows, data = [], []
    start = (page - 1) * page_size
    end = start + page_size

    for index, item in enumerate(g.redis.scan_iter('*', count=1000)):

        if start <= index < end:
            data.append(item)
        elif index >= end:
            break

    for index, item in enumerate(data):
        rows.append(
            {
                'index': start + index + 1,
                'key': item.decode('utf-8'),
                'type': g.redis.type(item).decode('utf-8').upper()
            }
        )

    return success_json(
        data={
            'total': total,
            'rows': rows
        }
    )


@redis_db_bp.route('/save_key_value', methods=['POST'])
@use_redis
def add_key_value():
    form = forms.KeyValueEditForm()

    if form.validate_on_submit():
        data_type = form.data_type.data
        key = form.key.data
        if data_type == 'STRING':
            g.redis.set(key, form.value.data)
        elif data_type == 'LIST':
            g.redis.lpush(key, *form.list_values.data)
        elif data_type == 'SET':
            g.redis.sadd(key, *form.set_values.data)
        elif data_type == 'ZSET':
            pass
        elif data_type == 'HASH':
            g.redis.hmset(key, form.hash_values.data)

        return alert_json(text='Key value has been saved.')

    return form.errors_to_json()


@redis_db_bp.route('/delete_key', methods=['POST'])
@use_redis
def delete_key():
    pass


@redis_db_bp.route('/update_key_value', methods=['POST'])
@use_redis
def update_key_value():
    pass


@redis_db_bp.route('/rename_key', methods=['POST'])
@use_redis
def rename_key():
    pass
