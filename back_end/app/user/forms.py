from flask import request
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm

from app.models import User


class SignupForm(FlaskForm):
    """
    Signup form
    """
    email = StringField()

    password = PasswordField()

    def validate_email(self, field):
        q = User.query.filter_by(email=field.data)
        if q.count() > 0:
            raise ValidationError('The email has been registered.')
