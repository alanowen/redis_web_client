from flask import g, jsonify, request

from . import forms
from . import redis_db_bp
from .decorators import use_redis


@redis_db_bp.route('/key_list', methods=['GET'])
@use_redis
def get_keys_of_database():
    # def query_key(size):
    #     ele = yield
    #     while True:
    #         ele = yield g.redis.scan(ele, '*', size)
    #
    # def assemble_data(start=0, size=2):
    #     p = query_key(size)
    #     p.send(None)
    #     cursor = p.send(start)
    #     for i in cursor[1]:
    #         key = i.decode('utf-8')
    #         yield {
    #             'index': '',
    #             'key': key,
    #             'type': g.redis.type(i).decode('utf-8').upper()
    #         }
    #     while cursor[0] != 0:
    #         cursor = p.send(cursor[0])
    #         for i in cursor[1]:
    #             key = i.decode('utf-8')
    #             yield {
    #                 'index': '',
    #                 'key': key,
    #                 'type': g.redis.type(i).decode('utf-8').upper()
    #             }

    def query_key(size):
        ele = yield
        while True:
            ele = yield g.redis.scan(ele, '*', size)

    def assemble_data(start=0, size=2):
        p = query_key(size)
        p.send(None)
        cursor = p.send(start)
        for i in cursor[1]:
            key = i.decode('utf-8')
            yield {
                'index': '',
                'key': key,
                'type': g.redis.type(i).decode('utf-8').upper()
            }
        while cursor[0] != 0:
            cursor = p.send(cursor[0])
            for i in cursor[1]:
                key = i.decode('utf-8')
                yield {
                    'index': '',
                    'key': key,
                    'type': g.redis.type(i).decode('utf-8').upper()
                }

    return jsonify(list(assemble_data(0, 20)))


@redis_db_bp.route('/save_key_value', methods=['POST'])
@use_redis
def add_key_value_to_database():
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

        return jsonify([])

    return jsonify(formError=form.errors)
