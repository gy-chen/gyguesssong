from flask import current_app
from werkzeug.local import LocalProxy
from gyguesssong.song.spotify_client import SpotifyClient


def _get_song_search_client():
    return current_app.extensions['song_ext'].spotify_search_client


class SongExt:
    def __init__(self, app=None):
        self._spotify_search_client = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        client_id = app.config.get('SONG_EXT_CLIENT_ID')
        client_secret = app.config.get('SONG_EXT_CLIENT_SECRET')

        self._spotify_search_client = SpotifyClient(client_id, client_secret)

        self._register_blueprint(app)

        app.extensions['song_ext'] = self

    @staticmethod
    def _register_blueprint(app):
        from gyguesssong.song.ext.view import bp

        app.register_blueprint(bp)

    @property
    def spotify_search_client(self):
        return self._spotify_search_client


song_search_client = LocalProxy(_get_song_search_client)
