from flask_wtf import FlaskForm
from wtforms import Field, StringField, IntegerField
from wtforms.meta import DefaultMeta


class BindNameMeta(FlaskForm.Meta):

    def __init__(self):
        super(BindNameMeta, self).__init__()
        self.custom_names = {}

    def bind_field(self, form, unbound_field, options):
        if unbound_field in self.custom_names:
            options['name'] = self.custom_names[unbound_field]
        else:
            if 'custom_name' in unbound_field.kwargs:
                options['name'] = unbound_field.kwargs.pop('custom_name')
                self.custom_names[unbound_field] = options['name']
        return unbound_field.bind(form=form, **options)


class DynamicValueField(Field):

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [i['value'] for i in valuelist if i and i.get('value')]


class NullableIntegerField(IntegerField):

    def __init__(self, label=None, validators=None, **kwargs):
        super(NullableIntegerField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                value = valuelist[0]
                if value == '':
                    return None
                else:
                    self.data = int(valuelist[0])
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid integer value'))


class DynamicKeyValueField(Field):

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = {
                i['field']: i['value']
                for i in valuelist if i and i.get('field')
            }
