from flask import g
from wtforms import StringField, IntegerField
from wtforms.validators import ValidationError

from app.models import RedisServer
from utils.wtf import NullableIntegerField, BindNameMeta, CommonForm


class RedisServerEditForm(CommonForm):
    """
    Redis server connection
    """

    Meta = BindNameMeta

    id = NullableIntegerField()

    connection_name = StringField(custom_name='connectionName')

    host = StringField()

    port = IntegerField()

    password = StringField()

    def validate_connection_name(self, field):
        model = RedisServer.query.filter(RedisServer.connection_name == field.data,
                                         RedisServer.user_id == g.current_user.id,
                                         RedisServer.id != self.id.data).first()

        if model:
            raise ValidationError('Connection name already exists.')

