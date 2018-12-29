from flask_wtf import FlaskForm
from wtforms import StringField

from utils.wtf import DynamicValueField, DynamicKeyValueField, BindNameMeta


class KeyValueEditForm(FlaskForm):

    Meta = BindNameMeta

    data_type = StringField(custom_name='dataType')

    key = StringField()

    value = StringField()

    list_values = DynamicValueField(custom_name='listValues')

    set_values = DynamicValueField(custom_name='setValues')

    zset_values = DynamicValueField(custom_name='zsetValue')

    hash_values = DynamicKeyValueField(custom_name='hashValues')
