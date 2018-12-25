try:
    from flask_wtf import FlaskForm
    DefaultMeta = FlaskForm.Meta
except ImportError:
    from wtforms.meta import DefaultMeta
from flask_wtf import FlaskForm

from wtforms.fields import IntegerField
from wtforms.validators import Optional


class BindNameMeta(DefaultMeta):

    def bind_field(self, form, unbound_field, options):
        if 'custom_name' in unbound_field.kwargs:
            options['name'] = unbound_field.kwargs.pop('custom_name')
        return unbound_field.bind(form=form, **options)
