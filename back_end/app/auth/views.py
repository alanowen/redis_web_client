from flask import jsonify, g

from app import token_auth, multi_auth
from app.models import User
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
            return jsonify(token=token)
        else:
            return jsonify([])
    else:
        return jsonify(formError=form.errors)
