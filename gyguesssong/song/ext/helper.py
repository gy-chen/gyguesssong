def make_song_json_view(song):
    return {
        'uri': song.uri,
        'name': song.name,
        'artist': song.artist,
        'album': song.album
    }
