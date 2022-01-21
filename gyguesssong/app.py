from flask import Flask
from gyguesssong.user.ext import UserExt


def create_app(config='config'):
    app = Flask(__name__)
    app.config.from_object(config)

    user_ext = UserExt()
    user_ext.init_app(app)

    return app
