from app import db


class User(db.Model):

    __table__ = 'user'

    pass


class RedisDatabaseConnection(db.Model):

    __table__ = 'redis_database_connection'

    host = ''
    port = ''
