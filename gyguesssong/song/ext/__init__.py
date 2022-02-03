from pathlib import Path

from flask import current_app, send_from_directory
from werkzeug.local import LocalProxy
from werkzeug.security import safe_join

from gyguesssong.song.song_downloader import download_song
from gyguesssong.song.spotify_client import SpotifyClient


def _get_song_ext():
    return current_app.extensions['song_ext']


def _get_song_search_client():
    return song_ext.spotify_search_client


class SongExt:
    SONG_SUFFIX = ".ogg"

    def __init__(self, app=None):
        self._spotify_search_client = None
        self._downloaded_songs_directory = None
        self._spotify_username = None
        self._spotify_password = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        client_id = app.config.get('SONG_EXT_CLIENT_ID')
        client_secret = app.config.get('SONG_EXT_CLIENT_SECRET')

        self._spotify_search_client = SpotifyClient(client_id, client_secret)
        self._downloaded_songs_directory = Path(app.config.get("SONG_EXT_DOWNLOADED_SONGS_DIRECTORY")).absolute()
        self._spotify_username = app.config.get("SONG_EXT_USERNAME")
        self._spotify_password = app.config.get("SONG_EXT_PASSWORD")

        self._register_blueprint(app)

        app.extensions['song_ext'] = self

    @staticmethod
    def _register_blueprint(app):
        from gyguesssong.song.ext.view import bp

        app.register_blueprint(bp)

    @property
    def spotify_search_client(self):
        return self._spotify_search_client

    def serve_downloaded_song(self, uri):
        return send_from_directory(self._downloaded_songs_directory, f'{uri}{self.SONG_SUFFIX}')

    def download_song(self, uri):
        env = {
            "USERNAME": self._spotify_username,
            "PASSWORD": self._spotify_password
        }
        download_song(uri, safe_join(self._downloaded_songs_directory, f"{uri}{self.SONG_SUFFIX}"), env=env)


song_ext = LocalProxy(_get_song_ext)
song_search_client = LocalProxy(_get_song_search_client)
