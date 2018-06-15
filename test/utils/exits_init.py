from flask_debugtoolbar import DebugToolbarExtension
from flask_restful import Api
from flask_session import Session

from App.model import db

toolbar = DebugToolbarExtension()
se = Session()
api = Api()


def exits_init(app):
    api.init_app(app=app)
    se.init_app(app=app)
    toolbar.init_app(app=app)
    db.init_app(app=app)

