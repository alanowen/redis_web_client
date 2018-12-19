from flask_migrate import Migrate, upgrade, current_app

from app import create_app
from app.models import db, User


app = create_app('development')

migrate = Migrate(app, db)


@app.shell_context_processor
def make_context():
    return dict(db=db, User=User)


if __name__ == '__main__':
    app.run()
