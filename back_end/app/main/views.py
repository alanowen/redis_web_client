from . import main_bp
from app import multi_auth


@main_bp.route('/')
@multi_auth.login_required
def index():
    pass