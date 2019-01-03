from wtforms import StringField

from utils.wtf import CommonForm


class LoginForm(CommonForm):
    """
    Login form
    """
    email = StringField()

    password = StringField()