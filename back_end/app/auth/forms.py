from flask_wtf import FlaskForm
from wtforms import StringField


class LoginForm(FlaskForm):
    """
    Login form
    """
    email = StringField()

    password = StringField()