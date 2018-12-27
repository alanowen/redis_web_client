from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import ValidationError

from app.models import RedisServer
from utils.wtf import BindNameMeta


class RedisServerConnectionForm(FlaskForm):
    """
    Redis server connection
    """

    Meta = BindNameMeta

    id = StringField()

    connection_name = StringField(custom_name='connectionName')

    host = StringField()

    port = IntegerField()

    password = StringField()

    def validate_connection_name(self, field):
        model = RedisServer.query.filter(RedisServer.connection_name == field.data,
                                         RedisServer.user_id == g.current_user.id).first()

        if model:
            raise ValidationError('Connection name already exists.')
