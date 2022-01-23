from flask import Flask
from gyguesssong.user.ext import UserExt
from gyguesssong.song.ext import SongExt


def create_app(config='config'):
    app = Flask(__name__)
    app.config.from_object(config)

    user_ext = UserExt()
    user_ext.init_app(app)

    song_ext = SongExt()
    song_ext.init_app(app)

    return app
