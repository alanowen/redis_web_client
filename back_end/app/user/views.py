from flask import jsonify

from app import db
from app.models import User
from . import user_bp
from .forms import SignupForm


@user_bp.route('/signup', methods=['POST'])
def signup():
    """
    User signup
    :return:
    """
    form = SignupForm()

    if form.validate():
        model = User(email=form.email.data,
                     password=form.email.data)
        db.session.add(model)
        db.session.commit()
    else:
        return jsonify(formError=form.errors)