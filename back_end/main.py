from time import ctime
from uuid import uuid4

import click
from redis import Redis
from flask_migrate import Migrate, upgrade, current_app

from app import create_app
from app.models import db, User


app = create_app('development')

migrate = Migrate(app, db)


@app.shell_context_processor
def make_context():
    return dict(db=db, User=User)


@app.cli.command()
@click.option('--num', default=1000)
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=6379)
@click.option('--db', default=0)
@click.option('--password', default='')
def insert_redis_keys(num, host, port, db, password):
    redis = Redis(host=host, port=port, password=password, db=db)

    try:
        start = ctime()
        with redis.pipeline() as p:
            for i in range(num):
                p.set(str(uuid4()), i)
            p.execute()
        end = ctime()
        print()
    except Exception as e:
        print('Error occurs when inserting redis keys.')
    else:
        print('Finished! Spent %d seconds in total.' % (end - start))


if __name__ == '__main__':
    app.run()
