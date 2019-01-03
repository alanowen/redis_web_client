from app import db
from app.models import User
from utils import alert_json
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
                     username=form.username.data,
                     password=form.password.data)
        db.session.add(model)
        db.session.commit()
        return alert_json(text='Your account has been created.')
    else:
        return form.errors_to_json()
