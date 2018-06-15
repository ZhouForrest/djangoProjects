import os

import redis
from flask import Flask

from App.user_views import user_blue
from App.views import blue
from utils.exits_init import exits_init

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def create_app():
    template_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    app.register_blueprint(blueprint=blue, url_prefix='/app')
    app.register_blueprint(blueprint=user_blue, url_prefix='/user')

    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask'

    exits_init(app)

    return app




