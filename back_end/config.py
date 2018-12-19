import os


base_dir = os.path.dirname(__file__)


class Config:

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'hard to guess'


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_ECHO = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'data-dev.db')


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}