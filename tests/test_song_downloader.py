from gyguesssong.song.song_downloader import download_song


def test_download_song(app):
    env = {
        'USERNAME': app.config["SONG_EXT_USERNAME"],
        'PASSWORD': app.config["SONG_EXT_PASSWORD"]
    }
    track_uri = "spotify:track:5BbCTsFpRotDXwfdvnw6DI"
    download_song(track_uri, "./sample_song.ogg", env=env)
