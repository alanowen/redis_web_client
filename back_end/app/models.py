from datetime import datetime

from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db


class User(db.Model):
    """
    User
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(30))

    email = db.Column(db.String(50), unique=True)

    password_hash = db.Column(db.String(128), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    redis_servers = db.relationship('RedisServer', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, value):
        return check_password_hash(self.password_hash, value)

    def generate_token(self, expiration=60 * 60):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    def verify_token(self, token):
        try:
            s = Serializer(current_app.config['SECRET_KEY'])
            data = s.loads(token).encode('utf-8')
        except Exception as e:
            return False

        if data.get('id') != self.id:
            return False
        db.session.add(self)
        return True

    @classmethod
    def get_user_id_from_token(cls, token):
        try:
            s = Serializer(current_app.config['SECRET_KEY'])
            data = s.loads(token)
        except Exception as e:
            return None
        return data.get('id')

    def get_redis_server(self, redis_server_id):
        return self.redis_servers.filter_by(id=redis_server_id).first()


class RedisServer(db.Model):
    """
    Redis server
    """

    __tablename__ = 'redis_servers'

    id = db.Column(db.Integer, primary_key=True)

    connection_name = db.Column(db.String(50), nullable=False)

    host = db.Column(db.String(128), nullable=False)

    port = db.Column(db.Integer, nullable=False)

    password = db.Column(db.String(128))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

