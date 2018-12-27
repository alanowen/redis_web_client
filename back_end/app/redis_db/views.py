from flask import g, jsonify

from . import redis_db_bp
from .decorators import user_redis


@redis_db_bp.route('/key_list', methods=['GET'])
@user_redis
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
