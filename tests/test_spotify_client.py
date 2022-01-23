from datetime import datetime, timedelta
from gyguesssong.song.ext import song_search_client
from gyguesssong.song.model import Song


def test_search(app):
    for song in song_search_client.search('安靜', 0):
        assert isinstance(song, Song)
        assert song.uri
        assert song.name
        assert song.artist
        assert song.album


def test_token_expire(app):
    assert song_search_client._access_token_expire_time is None
    song_search_client._refresh_access_token()
    assert song_search_client._access_token_expire_time
    assert not song_search_client._is_access_token_expire()
    song_search_client._access_token_expire_time = datetime.now() - timedelta(seconds=1)
    assert song_search_client._is_access_token_expire()
    song_search_client._refresh_access_token()
    assert not song_search_client._is_access_token_expire()


def test_get_song(app):
    song = song_search_client.get_song('spotify:track:5BbCTsFpRotDXwfdvnw6DI')
    assert song == Song(uri='spotify:track:5BbCTsFpRotDXwfdvnw6DI', name='きみの名前', artist='藤川千愛',
                        album='ライカ (Special Edition)')
