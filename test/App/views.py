from flask import Blueprint

blue = Blueprint('hello', __name__)


@blue.route('/')
def hello():
    return 'hello'