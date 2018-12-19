from flask import jsonify

from . import auth_bp
from .forms import LoginForm


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    :return:
    """
    form = LoginForm()

    if form.validate_on_submit():
        pass
    else:
        return jsonify(formError=form.errors)