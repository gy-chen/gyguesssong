from base64 import b64encode
from datetime import datetime, timedelta

import requests

from gyguesssong.song.model import Song


class SpotifyClient:
    SEARCH_DEFAULT_LIMIT = 20

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = None
        self._access_token_type = None
        self._access_token_expire_time = None

    def _refresh_access_token_if_needed(self):
        if self._is_access_token_expire():
            self._refresh_access_token()

    def _refresh_access_token(self):
        auth_payload_raw = f'{self._client_id}:{self._client_secret}'.encode()
        headers = {
            'Authorization': f'Basic {b64encode(auth_payload_raw).decode()}'
        }
        data = {
            "grant_type": "client_credentials"
        }
        r = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
        response_data = r.json()
        self._access_token = response_data['access_token']
        self._access_token_type = response_data['token_type']
        self._access_token_expire_time = datetime.now() + timedelta(seconds=response_data['3600'])

    def _is_access_token_expire(self):
        if self._access_token is None:
            return True
        now = datetime.now()
        return now >= self._access_token_expire_time

    def _make_authorization_header(self):
        return f"{self._access_token_type} {self._access_token}"

    def search(self, term, page):
        self._refresh_access_token_if_needed()
        headers = {
            'Authorization': self._make_authorization_header()
        }
        params = {
            'q': f'track:{term}',
            'type': 'track',
            'market': 'TW',
            'limit': self.SEARCH_DEFAULT_LIMIT,
            'offset': self.SEARCH_DEFAULT_LIMIT * page
        }
        r = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)
        return [self._to_song_model(track) for track in r.json()["tracks"]["items"]]

    def get_song(self, uri):
        self._refresh_access_token_if_needed()
        headers = {
            'Authorization': self._make_authorization_header()
        }
        params = {
            'market': 'TW'
        }
        r = requests.get(f'https://api.spotify.com/v1/tracks/{self._extract_spotify_id(uri)}', params=params,
                         headers=headers)
        response_data = r.json()
        return self._to_song_model(response_data)

    @staticmethod
    def _to_song_model(track_item):
        artist = [artist["name"] for artist in track_item["artist"]].join(", ")
        return Song(track_item["uri"], track_item["name"], artist, track_item["album"]["name"])

    @staticmethod
    def _extract_spotify_id(uri):
        return uri..rsplit(':', 1)[-1]
