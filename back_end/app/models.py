from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    """
    用户
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(50), unique=True)

    password_hash = db.Column(db.String(128), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    redis_connections = posts = db.relationship('RedisDatabaseConnection', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, value):
        return check_password_hash(self.password_hash, value)


class RedisDatabaseConnection(db.Model):
    """
    redis数据库连接信息
    """

    __tablename__ = 'redis_database_connections'

    id = db.Column(db.Integer, primary_key=True)

    host = db.Column(db.String(128), nullable=False)

    port = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
