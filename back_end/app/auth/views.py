from flask import g

from app import token_auth
from app.models import User
from utils import success_json, alert_json
from . import auth_bp
from .forms import LoginForm


@token_auth.verify_token
def verify_token(token):
    """
    Verify login token
    :param token:
    :return:
    """
    user_id = User.get_user_id_from_token(token)
    if not user_id:
        return False

    user = User.query.get(user_id)
    if user:
        g.current_user = user
        return True
    else:
        return False


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    :return:
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            g.current_user = user
            token = user.generate_token()
            return success_json(data=token)
        else:
            return alert_json(status='error', text='Email or password is incorrect.')
    else:
        return form.errors_to_json()
