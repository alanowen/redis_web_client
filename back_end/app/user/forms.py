from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError

from app.models import User
from utils.wtf import CommonForm


class SignupForm(CommonForm):
    """
    Signup form
    """
    email = StringField()

    username = StringField()

    password = PasswordField()

    def validate_email(self, field):
        q = User.query.filter_by(email=field.data)
        if q.count() > 0:
            raise ValidationError('The email has been registered.')
