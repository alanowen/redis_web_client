from flask import g
from wtforms.validators import ValidationError
from wtforms import StringField

from utils.wtf import DynamicValueField, DynamicKeyValueField, BindNameMeta, CommonForm


class KeyValueEditForm(CommonForm):

    Meta = BindNameMeta

    data_type = StringField(custom_name='dataType')

    key = StringField()

    value = StringField()

    list_values = DynamicValueField(custom_name='listValues')

    set_values = DynamicValueField(custom_name='setValues')

    zset_values = DynamicValueField(custom_name='zsetValue')

    hash_values = DynamicKeyValueField(custom_name='hashValues')

    def validate_key(self, field):
        keys = g.redis.keys(field.data)
        if len(keys) > 0:
            raise ValidationError('The key is used.')
